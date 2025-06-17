#!/usr/bin/env python3

import asyncio
import httpx
import json

async def register_agent(agent_info):
    """Register a single agent with the registry"""
    
    agent_id = agent_info["agent_id"]
    base_url = agent_info["base_url"]
    
    try:
        # First get the agent card
        async with httpx.AsyncClient() as client:
            card_response = await client.get(f"{base_url}/.well-known/agent.json")
            if card_response.status_code != 200:
                print(f"❌ Failed to get agent card for {agent_id}")
                return False
            
            agent_card = card_response.json()
            
            # Register with registry
            registration_data = {
                "agent_card": agent_card,
                "health_check_url": f"{base_url}/health"
            }
            
            registry_response = await client.post(
                "http://localhost:8000/register",
                json=registration_data,
                timeout=10.0
            )
            
            if registry_response.status_code == 200:
                print(f"✅ {agent_id} registered successfully")
                return True
            else:
                print(f"❌ Failed to register {agent_id}: {registry_response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error registering {agent_id}: {e}")
        return False

async def main():
    """Register all agents with the registry"""
    
    print("🔧 Registering A2A Agents with Registry...")
    print()
    
    agents = [
        {"agent_id": "payment-sys-001", "base_url": "http://localhost:8002"},
        {"agent_id": "fraud-detect-001", "base_url": "http://localhost:8003"},
        {"agent_id": "order-mgmt-001", "base_url": "http://localhost:8004"},
        {"agent_id": "tech-support-001", "base_url": "http://localhost:8005"}
    ]
    
    # Check if registry is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code != 200:
                print("❌ Registry is not running on port 8000")
                return
    except:
        print("❌ Cannot connect to registry on port 8000")
        return
    
    print("✅ Registry is running")
    print()
    
    # Register each agent
    success_count = 0
    for agent in agents:
        if await register_agent(agent):
            success_count += 1
        await asyncio.sleep(1)  # Small delay between registrations
    
    print()
    print(f"🎉 Registration complete: {success_count}/{len(agents)} agents registered")
    
    # Verify registration
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/.well-known/agents")
            if response.status_code == 200:
                data = response.json()
                registered_agents = data.get("agents", [])
                print(f"📊 Registry now has {len(registered_agents)} agents:")
                for i, agent_url in enumerate(registered_agents, 1):
                    print(f"   {i}. {agent_url}")
    except Exception as e:
        print(f"❌ Error verifying registration: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 