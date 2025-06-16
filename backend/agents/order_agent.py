import asyncio
import random
import json
from datetime import datetime, timedelta
from backend.shared.base_agent import BaseAgent

class SimulatedOrderAgent(BaseAgent):
    def __init__(self):
        config = {
            "agent_card_version": "1.0",
            "name": "Order Management Agent",
            "agent_id": "order-mgmt-001",
            "description": "Inventory management, order processing, and fulfillment coordination",
            "version": "2.8.3",
            "homepage": "https://latentgenius.ai/agents/order-management",
            "skills": [
                {
                    "name": "inventory-hold",
                    "description": "Reserve inventory for specified duration",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string"},
                            "items": {"type": "array"},
                            "hold_duration_minutes": {"type": "integer"}
                        }
                    }
                },
                {
                    "name": "expedited-processing",
                    "description": "Enable expedited order processing and shipping",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string"},
                            "expedite_level": {"type": "string"}
                        }
                    }
                }
            ],
            "authentication": {
                "type": "bearer",
                "bearer_format": "JWT"
            },
            "endpoints": {
                "base_url": "https://agents.latentgenius.ai/order-management",
                "tasks": "/tasks",
                "streaming": "/stream"
            },
            "capabilities": {
                "streaming": True,
                "push_notifications": True,
                "modalities": ["text", "structured_data"]
            }
        }
        
        super().__init__(config)
        
        # Inventory simulation data
        self.inventory_database = {
            "AI-COMPUTE-CLUSTER": {
                "sku": "AI-COMPUTE-CLUSTER",
                "name": "High-Performance AI Compute Cluster",
                "available": 12,
                "unit_price": 49999.99,
                "expedited_shipping": True
            }
        }
        
    async def execute_skill(self, skill_name: str, context: dict, task_id: str) -> dict:
        """Execute order management skill"""
        
        if skill_name == "inventory-hold":
            return await self._simulate_inventory_hold(context, task_id)
        elif skill_name == "expedited-processing":
            return await self._simulate_expedited_processing(context, task_id)
        else:
            raise ValueError(f"Unknown skill: {skill_name}")
    
    async def _simulate_inventory_hold(self, context: dict, task_id: str) -> dict:
        """Simulate inventory hold process"""
        
        order_id = context.get("order_id", "ORD-789123")
        items = context.get("items", [{"sku": "AI-COMPUTE-CLUSTER", "quantity": 1}])
        hold_duration_minutes = context.get("hold_duration_minutes", 45)
        
        await self.send_progress_update(task_id, 40, "Checking inventory availability...")
        await asyncio.sleep(2)
        
        await self.send_progress_update(task_id, 80, "Inventory reserved for 45 minutes")
        await asyncio.sleep(2)
        
        hold_id = f"HOLD-{random.randint(100000, 999999)}"
        expires_at = datetime.utcnow() + timedelta(minutes=hold_duration_minutes)
        
        return {
            "hold_id": hold_id,
            "expires_at": expires_at.isoformat(),
            "expedited_shipping": True
        }
    
    async def _simulate_expedited_processing(self, context: dict, task_id: str) -> dict:
        """Simulate expedited processing"""
        
        order_id = context.get("order_id", "ORD-789123")
        expedite_level = context.get("expedite_level", "express")
        
        await self.send_progress_update(task_id, 60, f"Enabling {expedite_level} processing...")
        await asyncio.sleep(2)
        
        delivery_date = datetime.utcnow() + timedelta(days=2)
        
        return {
            "expedite_level": expedite_level,
            "estimated_delivery": delivery_date.isoformat(),
            "additional_cost": 299
        }

if __name__ == "__main__":
    agent = SimulatedOrderAgent()
    agent.run(port=8004) 