import httpx
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

# Setup logging for A2A traffic
logger = logging.getLogger("a2a_traffic")
logger.setLevel(logging.INFO)

@dataclass
class A2AMessage:
    """Represents an A2A communication message"""
    timestamp: str
    source_agent: str
    target_agent: str
    message_type: str  # request, response, error
    method: Optional[str]
    message_id: str
    content: dict
    latency_ms: Optional[float] = None

class A2ATrafficMonitor:
    """Monitor and capture all A2A traffic for real-time display"""
    
    def __init__(self):
        self.traffic_log: List[A2AMessage] = []
        self.subscribers: List[asyncio.Queue] = []
    
    def log_message(self, message: A2AMessage):
        """Log an A2A message and notify subscribers"""
        self.traffic_log.append(message)
        
        # Keep only last 1000 messages to prevent memory issues
        if len(self.traffic_log) > 1000:
            self.traffic_log = self.traffic_log[-1000:]
        
        # Notify all subscribers
        for queue in self.subscribers:
            try:
                queue.put_nowait(message)
            except asyncio.QueueFull:
                # Skip if queue is full
                pass
    
    def subscribe(self) -> asyncio.Queue:
        """Subscribe to traffic updates"""
        queue = asyncio.Queue(maxsize=100)
        self.subscribers.append(queue)
        return queue
    
    def unsubscribe(self, queue: asyncio.Queue):
        """Unsubscribe from traffic updates"""
        if queue in self.subscribers:
            self.subscribers.remove(queue)
    
    def get_recent_traffic(self, limit: int = 50) -> List[A2AMessage]:
        """Get recent traffic messages"""
        return self.traffic_log[-limit:]

# Global traffic monitor instance
traffic_monitor = A2ATrafficMonitor()

class A2AClient:
    """Client for making A2A calls to other agents"""
    
    def __init__(self, agent_id: str, registry_url: str = "http://localhost:8000"):
        self.agent_id = agent_id
        self.registry_url = registry_url
        self.agent_cache: Dict[str, dict] = {}
        self.cache_expiry = 300  # 5 minutes
        self.last_cache_update = 0
    
    async def discover_agents(self, required_skills: List[str] = None) -> Dict[str, dict]:
        """Discover available agents, optionally filtered by skills"""
        
        current_time = datetime.utcnow().timestamp()
        
        # Use cache if recent
        if current_time - self.last_cache_update < self.cache_expiry and self.agent_cache:
            return self._filter_agents_by_skills(self.agent_cache, required_skills)
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if required_skills:
                    # Use skill-based discovery
                    response = await client.post(
                        f"{self.registry_url}/discover",
                        json=required_skills
                    )
                    if response.status_code == 200:
                        data = response.json()
                        self.agent_cache = data.get("matching_agents", {})
                else:
                    # Get all agents
                    response = await client.get(f"{self.registry_url}/.well-known/agents")
                    if response.status_code == 200:
                        agent_urls = response.json().get("agents", [])
                        
                        # Fetch agent cards
                        agents = {}
                        for agent_url in agent_urls:
                            try:
                                agent_response = await client.get(agent_url)
                                if agent_response.status_code == 200:
                                    agent_card = agent_response.json()
                                    agents[agent_card["agent_id"]] = {
                                        "name": agent_card["name"],
                                        "endpoint": agent_card["endpoints"]["base_url"],
                                        "skills": [s["name"] for s in agent_card["skills"]],
                                        "capabilities": agent_card["capabilities"]
                                    }
                            except Exception as e:
                                logger.warning(f"Failed to fetch agent card from {agent_url}: {e}")
                        
                        self.agent_cache = agents
                
                self.last_cache_update = current_time
                return self._filter_agents_by_skills(self.agent_cache, required_skills)
                
        except Exception as e:
            logger.error(f"Agent discovery failed: {e}")
            return {}
    
    def _filter_agents_by_skills(self, agents: Dict[str, dict], required_skills: List[str]) -> Dict[str, dict]:
        """Filter agents by required skills"""
        if not required_skills:
            return agents
        
        filtered = {}
        for agent_id, agent_info in agents.items():
            agent_skills = agent_info.get("skills", [])
            if any(skill in agent_skills for skill in required_skills):
                filtered[agent_id] = agent_info
        
        return filtered
    
    async def call_agent(self, 
                        target_agent_id: str, 
                        skill_name: str, 
                        context: dict, 
                        task_id: str = None) -> dict:
        """Make a JSON-RPC call to another agent"""
        
        if task_id is None:
            task_id = str(uuid.uuid4())
        
        # Get agent endpoint
        agents = await self.discover_agents()
        if target_agent_id not in agents:
            raise Exception(f"Agent {target_agent_id} not found")
        
        agent_endpoint = agents[target_agent_id]["endpoint"]
        request_id = str(uuid.uuid4())
        
        # Prepare JSON-RPC request
        request_data = {
            "jsonrpc": "2.0",
            "method": skill_name,
            "params": {
                "task_id": task_id,
                "context": context
            },
            "id": request_id
        }
        
        start_time = datetime.utcnow()
        
        # Log outgoing request
        traffic_monitor.log_message(A2AMessage(
            timestamp=start_time.isoformat(),
            source_agent=self.agent_id,
            target_agent=target_agent_id,
            message_type="request",
            method=skill_name,
            message_id=request_id,
            content=request_data
        ))
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Make the actual HTTP call
                response = await client.post(
                    f"{agent_endpoint}/tasks",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                end_time = datetime.utcnow()
                latency = (end_time - start_time).total_seconds() * 1000
                
                response_data = response.json() if response.status_code == 200 else {
                    "error": {"code": response.status_code, "message": response.text}
                }
                
                # Log response
                traffic_monitor.log_message(A2AMessage(
                    timestamp=end_time.isoformat(),
                    source_agent=target_agent_id,
                    target_agent=self.agent_id,
                    message_type="response" if response.status_code == 200 else "error",
                    method=skill_name,
                    message_id=request_id,
                    content=response_data,
                    latency_ms=latency
                ))
                
                if response.status_code == 200:
                    result = response_data.get("result", {})
                    returned_task_id = result.get("task_id")
                    
                    if returned_task_id:
                        # Monitor task completion
                        final_result = await self._monitor_task_completion(
                            target_agent_id, 
                            returned_task_id,
                            agent_endpoint
                        )
                        return final_result
                    else:
                        return result
                else:
                    raise Exception(f"Agent call failed: {response_data}")
                    
        except Exception as e:
            # Log error
            traffic_monitor.log_message(A2AMessage(
                timestamp=datetime.utcnow().isoformat(),
                source_agent=target_agent_id,
                target_agent=self.agent_id,
                message_type="error",
                method=skill_name,
                message_id=request_id,
                content={"error": str(e)}
            ))
            raise
    
    async def _monitor_task_completion(self, 
                                     agent_id: str, 
                                     task_id: str, 
                                     agent_endpoint: str) -> dict:
        """Monitor task completion and return final result"""
        
        max_wait = 120  # 2 minutes
        check_interval = 2  # 2 seconds
        elapsed = 0
        
        async with httpx.AsyncClient() as client:
            while elapsed < max_wait:
                try:
                    # Check task status
                    response = await client.get(f"{agent_endpoint}/tasks/{task_id}")
                    
                    if response.status_code == 200:
                        task_status = response.json()
                        
                        # Log progress updates
                        traffic_monitor.log_message(A2AMessage(
                            timestamp=datetime.utcnow().isoformat(),
                            source_agent=agent_id,
                            target_agent=self.agent_id,
                            message_type="progress",
                            method="task_status",
                            message_id=f"status-{task_id}",
                            content=task_status
                        ))
                        
                        if task_status["status"] in ["completed", "failed"]:
                            return task_status
                    
                    await asyncio.sleep(check_interval)
                    elapsed += check_interval
                    
                except Exception as e:
                    logger.error(f"Error monitoring task {task_id}: {e}")
                    break
        
        # Timeout
        return {"status": "timeout", "message": "Task monitoring timed out"}
    
    async def subscribe_to_traffic(self) -> asyncio.Queue:
        """Subscribe to real-time A2A traffic updates"""
        return traffic_monitor.subscribe()
    
    def get_recent_traffic(self, limit: int = 50) -> List[dict]:
        """Get recent A2A traffic as serializable dict"""
        messages = traffic_monitor.get_recent_traffic(limit)
        return [
            {
                "timestamp": msg.timestamp,
                "source_agent": msg.source_agent,
                "target_agent": msg.target_agent,
                "message_type": msg.message_type,
                "method": msg.method,
                "message_id": msg.message_id,
                "content": msg.content,
                "latency_ms": msg.latency_ms
            }
            for msg in messages
        ] 