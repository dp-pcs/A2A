from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
import httpx

app = FastAPI(title="A2A Agent Registry", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (use database in production)
registered_agents: Dict[str, dict] = {}

class AgentCard(BaseModel):
    agent_card_version: str = "1.0"
    name: str
    agent_id: str
    description: str
    version: str
    homepage: Optional[str] = None
    skills: List[dict]
    authentication: dict
    endpoints: dict
    capabilities: dict

class AgentRegistration(BaseModel):
    agent_card: AgentCard
    health_check_url: str
    callback_url: Optional[str] = None

@app.get("/.well-known/agents")
async def get_agent_registry():
    """Return list of all registered agent endpoints"""
    agent_endpoints = []
    
    for agent_id, agent_data in registered_agents.items():
        base_url = agent_data["agent_card"]["endpoints"]["base_url"]
        agent_endpoints.append(f"{base_url}/.well-known/agent.json")
    
    return {"agents": agent_endpoints}

@app.post("/register")
async def register_agent(registration: AgentRegistration):
    """Register a new agent with the registry"""
    
    agent_id = registration.agent_card.agent_id
    
    # Validate agent health
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(registration.health_check_url, timeout=5.0)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Agent health check failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot reach agent: {str(e)}")
    
    # Store agent registration
    registered_agents[agent_id] = {
        "agent_card": registration.agent_card.dict(),
        "health_check_url": registration.health_check_url,
        "callback_url": registration.callback_url,
        "registered_at": datetime.utcnow().isoformat(),
        "last_health_check": datetime.utcnow().isoformat(),
        "status": "active"
    }
    
    return {"message": f"Agent {agent_id} registered successfully"}

@app.get("/agents/{agent_id}")
async def get_agent_info(agent_id: str):
    """Get detailed information about a specific agent"""
    
    if agent_id not in registered_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return registered_agents[agent_id]

@app.post("/discover")
async def discover_agents_by_skills(required_skills: List[str]):
    """Discover agents that match required skills"""
    
    matching_agents = {}
    
    for agent_id, agent_data in registered_agents.items():
        agent_card = agent_data["agent_card"]
        agent_skills = [skill["name"] for skill in agent_card["skills"]]
        
        # Check if agent has any of the required skills
        if any(skill in agent_skills for skill in required_skills):
            matching_agents[agent_id] = {
                "name": agent_card["name"],
                "endpoint": agent_card["endpoints"]["base_url"],
                "skills": agent_skills,
                "capabilities": agent_card["capabilities"],
                "status": agent_data["status"]
            }
    
    return {"matching_agents": matching_agents, "query": required_skills}

@app.delete("/agents/{agent_id}")
async def deregister_agent(agent_id: str):
    """Remove an agent from the registry"""
    
    if agent_id not in registered_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    del registered_agents[agent_id]
    return {"message": f"Agent {agent_id} deregistered successfully"}

@app.get("/health")
async def health_check():
    """Registry service health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "registered_agents": len(registered_agents)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 