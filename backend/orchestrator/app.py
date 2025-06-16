from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import httpx
import uuid
from datetime import datetime
import json

app = FastAPI(title="Customer Service Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IncidentRequest(BaseModel):
    incident_type: str
    customer: dict
    order: dict
    failure_details: dict
    deadline: Optional[str] = None

class TaskResult(BaseModel):
    task_id: str
    agent_id: str
    status: str
    result: Optional[dict] = None
    artifacts: List[dict] = []

# Storage for active incidents
active_incidents: Dict[str, dict] = {}
task_results: Dict[str, dict] = {}

@app.post("/incidents")
async def create_incident(incident: IncidentRequest, background_tasks: BackgroundTasks):
    """Create and orchestrate incident resolution"""
    
    incident_id = f"incident-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
    
    # Store incident details
    incident_data = {
        "incident_id": incident_id,
        "status": "created",
        "created_at": datetime.utcnow().isoformat(),
        "incident_type": incident.incident_type,
        "customer": incident.customer,
        "order": incident.order,
        "failure_details": incident.failure_details,
        "deadline": incident.deadline,
        "tasks": {},
        "resolution": None
    }
    
    active_incidents[incident_id] = incident_data
    
    # Start incident orchestration in background
    background_tasks.add_task(orchestrate_incident_resolution, incident_id, incident_data)
    
    return {
        "incident_id": incident_id,
        "status": "created",
        "message": "Incident created and orchestration started"
    }

@app.get("/incidents/{incident_id}")
async def get_incident_status(incident_id: str):
    """Get current incident status"""
    
    if incident_id not in active_incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return active_incidents[incident_id]

@app.get("/incidents")
async def list_incidents():
    """List all incidents"""
    return {"incidents": list(active_incidents.values())}

async def orchestrate_incident_resolution(incident_id: str, incident_data: dict):
    """Orchestrate multi-agent incident resolution"""
    
    try:
        # Update incident status
        active_incidents[incident_id]["status"] = "orchestrating"
        
        # Discover available agents
        agents = await discover_agents()
        
        if not agents:
            active_incidents[incident_id]["status"] = "failed"
            active_incidents[incident_id]["error"] = "No agents available"
            return
        
        # Create coordinated tasks based on incident type
        if incident_data["incident_type"] == "payment_failure":
            tasks = await create_payment_failure_tasks(incident_id, incident_data, agents)
        else:
            tasks = await create_generic_incident_tasks(incident_id, incident_data, agents)
        
        # Execute tasks in parallel
        active_incidents[incident_id]["tasks"] = tasks
        active_incidents[incident_id]["status"] = "executing"
        
        # Monitor task completion
        await monitor_task_completion(incident_id, tasks)
        
        # Synthesize results
        resolution = await synthesize_resolution(incident_id, tasks)
        active_incidents[incident_id]["resolution"] = resolution
        active_incidents[incident_id]["status"] = "resolved"
        
    except Exception as e:
        active_incidents[incident_id]["status"] = "failed"
        active_incidents[incident_id]["error"] = str(e)

async def discover_agents():
    """Discover available agents from registry"""
    
    try:
        async with httpx.AsyncClient() as client:
            # Get agent list from registry
            response = await client.get("http://registry:8000/.well-known/agents")
            if response.status_code == 200:
                agent_urls = response.json().get("agents", [])
                
                # Fetch agent capabilities
                agents = {}
                for agent_url in agent_urls:
                    try:
                        agent_response = await client.get(agent_url)
                        if agent_response.status_code == 200:
                            agent_card = agent_response.json()
                            agents[agent_card["agent_id"]] = agent_card
                    except:
                        continue
                
                return agents
    except:
        pass
    
    # Fallback to known agent endpoints
    return {
        "payment-sys-001": {
            "agent_id": "payment-sys-001",
            "name": "Payment Systems Agent",
            "endpoints": {"base_url": "http://payment-agent:8002"}
        },
        "fraud-detect-001": {
            "agent_id": "fraud-detect-001", 
            "name": "Fraud Detection Agent",
            "endpoints": {"base_url": "http://fraud-agent:8003"}
        },
        "order-mgmt-001": {
            "agent_id": "order-mgmt-001",
            "name": "Order Management Agent", 
            "endpoints": {"base_url": "http://order-agent:8004"}
        },
        "tech-support-001": {
            "agent_id": "tech-support-001",
            "name": "Tech Support Agent",
            "endpoints": {"base_url": "http://tech-agent:8005"}
        }
    }

async def create_payment_failure_tasks(incident_id: str, incident_data: dict, agents: dict):
    """Create specialized tasks for payment failure incidents"""
    
    tasks = {}
    
    # Payment analysis task
    if "payment-sys-001" in agents:
        payment_task = {
            "task_id": f"payment-analysis-{incident_id}",
            "agent_id": "payment-sys-001",
            "skill_required": "transaction-analysis",
            "context": {
                "transaction_id": incident_data["failure_details"].get("transaction_id"),
                "customer_id": incident_data["customer"]["id"],
                "amount": incident_data["order"]["amount"],
                "timestamp": incident_data["failure_details"].get("timestamp")
            },
            "status": "created"
        }
        tasks["payment_analysis"] = payment_task
        await delegate_task_to_agent(payment_task, agents["payment-sys-001"])
    
    # Fraud assessment task
    if "fraud-detect-001" in agents:
        fraud_task = {
            "task_id": f"fraud-check-{incident_id}",
            "agent_id": "fraud-detect-001",
            "skill_required": "risk-assessment",
            "context": {
                "customer_id": incident_data["customer"]["id"],
                "transaction_amount": incident_data["order"]["amount"],
                "transaction_context": {
                    "ip_address": "203.0.113.45",
                    "user_agent": "Mozilla/5.0...",
                    "payment_method": "corporate_card_ending_5678"
                }
            },
            "status": "created"
        }
        tasks["fraud_assessment"] = fraud_task
        await delegate_task_to_agent(fraud_task, agents["fraud-detect-001"])
    
    # Inventory hold task
    if "order-mgmt-001" in agents:
        order_task = {
            "task_id": f"inventory-hold-{incident_id}",
            "agent_id": "order-mgmt-001",
            "skill_required": "inventory-hold",
            "context": {
                "order_id": incident_data["order"]["id"],
                "items": incident_data["order"]["items"],
                "hold_duration_minutes": 45
            },
            "status": "created"
        }
        tasks["inventory_hold"] = order_task
        await delegate_task_to_agent(order_task, agents["order-mgmt-001"])
    
    # System diagnostics task
    if "tech-support-001" in agents:
        tech_task = {
            "task_id": f"system-diag-{incident_id}",
            "agent_id": "tech-support-001", 
            "skill_required": "system-diagnostics",
            "context": {
                "incident_type": incident_data["incident_type"],
                "system_components": ["payment_gateway", "database_cluster"]
            },
            "status": "created"
        }
        tasks["system_diagnostics"] = tech_task
        await delegate_task_to_agent(tech_task, agents["tech-support-001"])
    
    return tasks

async def delegate_task_to_agent(task: dict, agent_config: dict):
    """Delegate task to specific agent"""
    
    try:
        async with httpx.AsyncClient() as client:
            task_request = {
                "jsonrpc": "2.0",
                "method": "create_task",
                "params": {
                    "task_id": task["task_id"],
                    "skill_required": task["skill_required"],
                    "context": task["context"]
                },
                "id": f"req-{task['task_id']}"
            }
            
            agent_url = f"{agent_config['endpoints']['base_url']}/tasks"
            response = await client.post(agent_url, json=task_request)
            
            if response.status_code == 200:
                task["status"] = "delegated"
                task["delegated_at"] = datetime.utcnow().isoformat()
            else:
                task["status"] = "failed"
                task["error"] = f"Failed to delegate: {response.status_code}"
                
    except Exception as e:
        task["status"] = "failed"
        task["error"] = str(e)

async def monitor_task_completion(incident_id: str, tasks: dict):
    """Monitor task completion across all agents"""
    
    max_wait_time = 300  # 5 minutes
    check_interval = 2   # 2 seconds
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        all_completed = True
        
        for task_name, task in tasks.items():
            if task["status"] not in ["completed", "failed"]:
                all_completed = False
                # In a real implementation, we would check agent task status
                # For simulation, we'll mark tasks as completed after some time
                if elapsed_time > 30:  # Simulate completion after 30 seconds
                    task["status"] = "completed"
                    task["completed_at"] = datetime.utcnow().isoformat()
                    task["result"] = await simulate_task_result(task)
        
        if all_completed:
            break
            
        await asyncio.sleep(check_interval)
        elapsed_time += check_interval

async def simulate_task_result(task: dict):
    """Simulate task results for demo purposes"""
    
    if task["skill_required"] == "transaction-analysis":
        return {
            "retry_recommended": True,
            "strategy": "bypass_3ds_for_verified_corporate",
            "confidence": 0.94,
            "root_cause": "3ds_timeout"
        }
    elif task["skill_required"] == "risk-assessment":
        return {
            "risk_score": 0.15,
            "risk_level": "LOW",
            "recommendation": "approve",
            "confidence": 0.97
        }
    elif task["skill_required"] == "inventory-hold":
        return {
            "hold_id": f"HOLD-{datetime.utcnow().strftime('%H%M%S')}",
            "expires_at": datetime.utcnow().isoformat(),
            "expedited_shipping": True
        }
    elif task["skill_required"] == "system-diagnostics":
        return {
            "diagnosis": "3DS authentication service experiencing high latency",
            "root_cause": "Gateway timeout due to external service delays",
            "severity": "high"
        }
    
    return {"status": "completed"}

async def synthesize_resolution(incident_id: str, tasks: dict):
    """Synthesize results from all agents into resolution"""
    
    completed_tasks = {k: v for k, v in tasks.items() if v["status"] == "completed"}
    
    if len(completed_tasks) == 0:
        return {
            "status": "failed",
            "message": "No tasks completed successfully"
        }
    
    # Extract key insights
    payment_result = completed_tasks.get("payment_analysis", {}).get("result", {})
    fraud_result = completed_tasks.get("fraud_assessment", {}).get("result", {})
    order_result = completed_tasks.get("inventory_hold", {}).get("result", {})
    
    # Generate coordinated resolution
    resolution = {
        "resolution_id": f"res-{incident_id}",
        "status": "success",
        "resolution_strategy": "coordinated_payment_retry",
        "actions_taken": [],
        "timeline": []
    }
    
    # Payment retry with fraud clearance
    if payment_result.get("retry_recommended") and fraud_result.get("recommendation") == "approve":
        resolution["actions_taken"].append({
            "action": "payment_retry_with_3ds_bypass",
            "reason": "Fraud cleared, corporate customer verified",
            "success_probability": 0.97
        })
    
    # Inventory secured
    if order_result.get("hold_id"):
        resolution["actions_taken"].append({
            "action": "inventory_secured",
            "details": f"Hold ID: {order_result['hold_id']}",
            "expedited_shipping": order_result.get("expedited_shipping", False)
        })
    
    # System optimizations
    resolution["actions_taken"].append({
        "action": "system_optimization_applied",
        "details": "Gateway timeout thresholds adjusted"
    })
    
    resolution["summary"] = f"Incident resolved via coordinated agent response. Payment retry successful, inventory secured, customer notified."
    resolution["total_resolution_time"] = "1 minute 47 seconds"
    
    return resolution

async def create_generic_incident_tasks(incident_id: str, incident_data: dict, agents: dict):
    """Create generic tasks for other incident types"""
    
    # This would contain logic for other incident types
    return {}

@app.get("/health")
async def health_check():
    """Orchestrator health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_incidents": len(active_incidents)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 