from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any, AsyncGenerator
import asyncio
import json
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
import httpx

class TaskRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict
    id: str

class TaskResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[dict] = None
    error: Optional[dict] = None
    id: str

class StreamEvent(BaseModel):
    event: str  # task_started, progress, insight, artifact_ready, task_completed
    data: dict

class TaskStatus(BaseModel):
    task_id: str
    status: str  # created, working, completed, failed
    progress: int = 0
    message: str = ""
    result: Optional[dict] = None
    artifacts: List[dict] = []
    created_at: str
    updated_at: str

class BaseAgent(ABC):
    def __init__(self, agent_config: dict):
        self.config = agent_config
        self.app = FastAPI(
            title=agent_config["name"],
            version=agent_config["version"]
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Task storage (use database in production)
        self.tasks: Dict[str, TaskStatus] = {}
        self.task_streams: Dict[str, asyncio.Queue] = {}
        
        # Setup routes
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup standard A2A protocol routes"""
        
        @self.app.get("/.well-known/agent.json")
        async def get_agent_card():
            """Return agent capabilities card"""
            return self.config
            
        @self.app.post("/tasks")
        async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
            """Create and execute a new task"""
            
            task_id = request.params.get("task_id", str(uuid.uuid4()))
            # Use JSON-RPC method field as the skill name, fallback to params for compatibility
            skill_required = request.method or request.params.get("skill_required")
            
            # Validate skill availability
            available_skills = [skill["name"] for skill in self.config["skills"]]
            if skill_required not in available_skills:
                return TaskResponse(
                    id=request.id,
                    error={
                        "code": -32601,
                        "message": f"Skill '{skill_required}' not available",
                        "data": {"available_skills": available_skills}
                    }
                )
            
            # Create task
            task = TaskStatus(
                task_id=task_id,
                status="created",
                message="Task created successfully",
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
            
            self.tasks[task_id] = task
            self.task_streams[task_id] = asyncio.Queue()
            
            # Start task execution in background
            # Add skill_required to params for execute_task
            execution_params = request.params.copy()
            execution_params["skill_required"] = skill_required
            background_tasks.add_task(self._execute_task, task_id, execution_params)
            
            return TaskResponse(
                id=request.id,
                result={
                    "task_id": task_id,
                    "status": "created",
                    "message": "Task created and queued for execution"
                }
            )
            
        @self.app.get("/tasks/{task_id}")
        async def get_task_status(task_id: str):
            """Get current task status"""
            
            if task_id not in self.tasks:
                raise HTTPException(status_code=404, detail="Task not found")
                
            return self.tasks[task_id]
            
        @self.app.get("/stream/{task_id}")
        async def stream_task_updates(task_id: str):
            """Stream real-time task updates via Server-Sent Events"""
            
            if task_id not in self.tasks:
                raise HTTPException(status_code=404, detail="Task not found")
                
            async def event_generator() -> AsyncGenerator[str, None]:
                try:
                    while True:
                        try:
                            # Wait for new events with timeout
                            event = await asyncio.wait_for(
                                self.task_streams[task_id].get(), 
                                timeout=30.0
                            )
                            
                            yield f"event: {event.event}\n"
                            yield f"data: {json.dumps(event.data)}\n\n"
                            
                            # Stop streaming when task completes
                            if event.event in ["task_completed", "task_failed"]:
                                break
                                
                        except asyncio.TimeoutError:
                            # Send keepalive
                            yield f"event: keepalive\n"
                            yield f"data: {json.dumps({'timestamp': datetime.utcnow().isoformat()})}\n\n"
                            
                except Exception as e:
                    yield f"event: error\n"
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
                    
            return StreamingResponse(
                event_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*",
                }
            )
            
        @self.app.get("/health")
        async def health_check():
            """Agent health check endpoint"""
            return {
                "status": "healthy",
                "agent_id": self.config["agent_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "active_tasks": len([t for t in self.tasks.values() if t.status == "working"])
            }
    
    async def _execute_task(self, task_id: str, params: dict):
        """Execute task with progress streaming"""
        
        try:
            # Update task status
            await self._update_task_status(task_id, "working", "Task execution started")
            
            # Send start event
            await self._send_stream_event(task_id, "task_started", {
                "task_id": task_id,
                "status": "working",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Task execution started"
            })
            
            # Execute the actual work (implemented by subclasses)
            result = await self.execute_skill(
                skill_name=params["skill_required"],
                context=params.get("context", {}),
                task_id=task_id
            )
            
            # Complete task
            await self._update_task_status(task_id, "completed", "Task completed successfully", result)
            
            await self._send_stream_event(task_id, "task_completed", {
                "task_id": task_id,
                "status": "completed",
                "progress": 100,
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Task completed successfully",
                "result": result
            })
            
        except Exception as e:
            # Handle task failure
            await self._update_task_status(task_id, "failed", f"Task failed: {str(e)}")
            
            await self._send_stream_event(task_id, "task_failed", {
                "task_id": task_id,
                "status": "failed",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Task failed: {str(e)}",
                "error": str(e)
            })
    
    async def _update_task_status(self, task_id: str, status: str, message: str, result: dict = None):
        """Update task status"""
        
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.tasks[task_id].message = message
            self.tasks[task_id].updated_at = datetime.utcnow().isoformat()
            
            if result:
                self.tasks[task_id].result = result
                
            if status == "completed":
                self.tasks[task_id].progress = 100
    
    async def _send_stream_event(self, task_id: str, event_type: str, data: dict):
        """Send streaming event to clients"""
        
        if task_id in self.task_streams:
            event = StreamEvent(event=event_type, data=data)
            await self.task_streams[task_id].put(event)
    
    async def send_progress_update(self, task_id: str, progress: int, message: str, extra_data: dict = None):
        """Send progress update during task execution"""
        
        if task_id in self.tasks:
            self.tasks[task_id].progress = progress
            self.tasks[task_id].message = message
            self.tasks[task_id].updated_at = datetime.utcnow().isoformat()
        
        event_data = {
            "task_id": task_id,
            "status": "working",
            "progress": progress,
            "timestamp": datetime.utcnow().isoformat(),
            "message": message
        }
        
        if extra_data:
            event_data.update(extra_data)
            
        await self._send_stream_event(task_id, "progress", event_data)
    
    async def send_insight(self, task_id: str, insight: dict, message: str = ""):
        """Send insight event during task execution"""
        
        event_data = {
            "task_id": task_id,
            "status": "working",
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "insight": insight
        }
        
        await self._send_stream_event(task_id, "insight", event_data)
    
    async def send_artifact_ready(self, task_id: str, artifact: dict, message: str = ""):
        """Send artifact ready event"""
        
        if task_id in self.tasks:
            self.tasks[task_id].artifacts.append(artifact)
        
        event_data = {
            "task_id": task_id,
            "status": "working",
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "artifact": artifact
        }
        
        await self._send_stream_event(task_id, "artifact_ready", event_data)
    
    @abstractmethod
    async def execute_skill(self, skill_name: str, context: dict, task_id: str) -> dict:
        """Execute a specific skill - must be implemented by subclasses"""
        pass
    
    async def register_with_registry(self, registry_url: str):
        """Register this agent with the A2A registry"""
        
        registration_data = {
            "agent_card": self.config,
            "health_check_url": f"{self.config['endpoints']['base_url']}/health"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{registry_url}/register",
                    json=registration_data,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    print(f"Agent {self.config['agent_id']} registered successfully")
                else:
                    print(f"Registration failed: {response.text}")
                    
        except Exception as e:
            print(f"Failed to register with registry: {str(e)}")
    
    def run(self, host: str = "0.0.0.0", port: int = 8001):
        """Run the agent service"""
        import uvicorn
        import threading
        import time
        
        # Register with registry in a separate thread after service starts
        def register_after_startup():
            time.sleep(3)  # Wait for service to be ready
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.register_with_registry("http://localhost:8000"))
            loop.close()
        
        # Start registration in background
        registration_thread = threading.Thread(target=register_after_startup, daemon=True)
        registration_thread.start()
        
        uvicorn.run(self.app, host=host, port=port) 