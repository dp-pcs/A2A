import asyncio
import random
import json
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path to import shared modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.base_agent import BaseAgent

class TechAgent(BaseAgent):
    def __init__(self):
        config = {
            "agent_card_version": "1.0",
            "name": "Tech Support Agent",
            "agent_id": "tech-support-001",
            "description": "System diagnostics, performance analysis, and infrastructure optimization",
            "version": "3.4.2",
            "homepage": "https://latentgenius.ai/agents/tech-support",
            "skills": [
                {
                    "name": "system-diagnostics",
                    "description": "Analyze system performance and identify bottlenecks",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "incident_type": {"type": "string"},
                            "system_components": {"type": "array"}
                        }
                    }
                },
                {
                    "name": "performance-optimization",
                    "description": "Optimize system performance and recommend improvements",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "optimization_target": {"type": "string"}
                        }
                    }
                }
            ],
            "authentication": {
                "type": "api_key",
                "location": "header",
                "name": "X-Tech-API-Key"
            },
            "endpoints": {
                "base_url": "http://localhost:8005",
                "tasks": "/tasks",
                "streaming": "/stream"
            },
            "capabilities": {
                "streaming": True,
                "push_notifications": True,
                "modalities": ["text", "structured_data", "logs", "metrics"]
            }
        }
        
        super().__init__(config)
        
    async def execute_skill(self, skill_name: str, context: dict, task_id: str) -> dict:
        """Execute tech support skill"""
        
        if skill_name == "system-diagnostics":
            return await self._simulate_system_diagnostics(context, task_id)
        elif skill_name == "performance-optimization":
            return await self._simulate_performance_optimization(context, task_id)
        else:
            raise ValueError(f"Unknown skill: {skill_name}")
    
    async def _simulate_system_diagnostics(self, context: dict, task_id: str) -> dict:
        """Simulate system diagnostics"""
        
        incident_type = context.get("incident_type", "payment_timeout")
        
        await self.send_progress_update(task_id, 35, "Analyzing gateway performance metrics...")
        await asyncio.sleep(2)
        
        await self.send_progress_update(task_id, 70, "Identified high latency in 3DS verification service")
        await asyncio.sleep(2)
        
        return {
            "diagnosis": "3DS authentication service experiencing high latency",
            "root_cause": "Gateway timeout due to external service delays",
            "severity": "high",
            "recommendations": [
                "Implement circuit breaker pattern",
                "Add timeout optimizations",
                "Enable request queuing"
            ]
        }
    
    async def _simulate_performance_optimization(self, context: dict, task_id: str) -> dict:
        """Simulate performance optimization"""
        
        optimization_target = context.get("optimization_target", "response_time")
        
        await self.send_progress_update(task_id, 60, "Generating optimization recommendations...")
        await asyncio.sleep(2)
        
        return {
            "optimization_target": optimization_target,
            "recommendations": [
                "Enable Redis caching layer",
                "Optimize database indexes",
                "Implement connection pooling"
            ],
            "expected_improvement": "30-50% performance gain"
        }

if __name__ == "__main__":
    agent = TechAgent()
    agent.run(port=8005) 