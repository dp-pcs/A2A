import asyncio
import random
import json
from datetime import datetime, timedelta
from backend.shared.base_agent import BaseAgent

class SimulatedPaymentAgent(BaseAgent):
    def __init__(self):
        config = {
            "agent_card_version": "1.0",
            "name": "Payment Systems Agent",
            "agent_id": "payment-sys-001",
            "description": "Handles payment processing, transaction analysis, and gateway issues",
            "version": "3.2.1",
            "homepage": "https://latentgenius.ai/agents/payment-systems",
            "skills": [
                {
                    "name": "transaction-analysis",
                    "description": "Analyze failed transactions and identify root causes",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "transaction_id": {"type": "string"},
                            "customer_id": {"type": "string"},
                            "amount": {"type": "number"},
                            "timestamp": {"type": "string", "format": "date-time"}
                        }
                    },
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "failure_reason": {"type": "string"},
                            "gateway_status": {"type": "string"},
                            "retry_recommended": {"type": "boolean"},
                            "analysis_report": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "payment-retry",
                    "description": "Attempt payment retry with optimized parameters",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "original_transaction_id": {"type": "string"},
                            "retry_strategy": {"type": "string"}
                        }
                    }
                }
            ],
            "authentication": {
                "type": "api_key",
                "location": "header",
                "name": "X-API-Key"
            },
            "endpoints": {
                "base_url": "https://agents.latentgenius.ai/payment-systems",
                "tasks": "/tasks",
                "streaming": "/stream"
            },
            "capabilities": {
                "streaming": True,
                "push_notifications": False,
                "modalities": ["text", "structured_data"]
            }
        }
        
        super().__init__(config)
        
        # Simulation data for realistic scenarios
        self.failure_scenarios = {
            "3ds_timeout": {
                "probability": 0.4,
                "failure_reason": "3DS verification timeout",
                "gateway_status": "timeout",
                "retry_recommended": True,
                "confidence": 0.94,
                "resolution_strategy": "bypass_3ds_for_verified_corporate"
            },
            "insufficient_funds": {
                "probability": 0.2,
                "failure_reason": "Insufficient funds",
                "gateway_status": "declined",
                "retry_recommended": False,
                "confidence": 0.99,
                "resolution_strategy": "request_alternative_payment_method"
            },
            "network_timeout": {
                "probability": 0.3,
                "failure_reason": "Network gateway timeout",
                "gateway_status": "timeout",
                "retry_recommended": True,
                "confidence": 0.87,
                "resolution_strategy": "retry_with_backoff"
            },
            "card_declined": {
                "probability": 0.1,
                "failure_reason": "Card declined by issuer",
                "gateway_status": "declined",
                "retry_recommended": False,
                "confidence": 0.95,
                "resolution_strategy": "contact_card_issuer"
            }
        }
        
    async def execute_skill(self, skill_name: str, context: dict, task_id: str) -> dict:
        """Execute payment analysis with realistic simulation"""
        
        if skill_name == "transaction-analysis":
            return await self._simulate_transaction_analysis(context, task_id)
        elif skill_name == "payment-retry":
            return await self._simulate_payment_retry(context, task_id)
        else:
            raise ValueError(f"Unknown skill: {skill_name}")
    
    async def _simulate_transaction_analysis(self, context: dict, task_id: str) -> dict:
        """Simulate realistic payment transaction analysis"""
        
        transaction_id = context.get("transaction_id", "TXN-456789")
        customer_id = context.get("customer_id", "CORP-12345")
        amount = context.get("amount", 49999.99)
        
        # Step 1: Initial analysis
        await self.send_progress_update(task_id, 25, "Retrieving transaction logs from Stripe...")
        await asyncio.sleep(2)
        
        # Step 2: Pattern analysis  
        await self.send_progress_update(task_id, 50, "Analyzing gateway timeout patterns...")
        await asyncio.sleep(3)
        
        # Select a realistic failure scenario
        selected_scenario = self._select_weighted_scenario()
        scenario_data = self.failure_scenarios[selected_scenario]
        
        # Step 3: Root cause identification
        await self.send_insight(task_id, {
            "root_cause": selected_scenario,
            "confidence": scenario_data["confidence"]
        }, f"Detected: {scenario_data['failure_reason']}")
        
        await self.send_progress_update(task_id, 75, f"Root cause identified: {scenario_data['failure_reason']}")
        await asyncio.sleep(2)
        
        # Step 4: Generate analysis artifact
        analysis_report = {
            "artifact_id": f"payment-analysis-{task_id}",
            "task_id": task_id,
            "type": "analysis_report",
            "format": "application/json",
            "created_at": datetime.utcnow().isoformat(),
            "data": {
                "transaction_analysis": {
                    "transaction_id": transaction_id,
                    "original_amount": amount,
                    "currency": "USD",
                    "gateway": "stripe_enterprise",
                    "failure_reason": scenario_data["failure_reason"],
                    "failure_code": "GATEWAY_TIMEOUT" if "timeout" in selected_scenario else "DECLINED",
                    "root_cause": {
                        "primary": selected_scenario,
                        "contributing_factors": self._get_contributing_factors(selected_scenario),
                        "confidence": scenario_data["confidence"]
                    },
                    "resolution_strategy": {
                        "recommended_action": scenario_data["resolution_strategy"],
                        "bypass_reason": "verified_corporate_account" if scenario_data["retry_recommended"] else None,
                        "expected_success_rate": 0.97 if scenario_data["retry_recommended"] else 0.15
                    },
                    "technical_details": {
                        "gateway_response_time": f"{random.uniform(25.0, 35.0):.1f}s",
                        "timeout_threshold": "30.0s",
                        "3ds_challenge_presented": selected_scenario == "3ds_timeout",
                        "customer_authentication_attempted": True
                    }
                }
            }
        }
        
        await self.send_artifact_ready(task_id, {
            "type": "analysis_report",
            "url": f"https://artifacts.latentgenius.ai/payment-analysis-{task_id}.json",
            "format": "application/json"
        }, "Payment analysis report generated")
        
        await self.send_progress_update(task_id, 90, "Analysis report generated")
        await asyncio.sleep(1)
        
        # Return final result
        return {
            "retry_recommended": scenario_data["retry_recommended"],
            "strategy": scenario_data["resolution_strategy"],
            "confidence": scenario_data["confidence"],
            "root_cause": selected_scenario,
            "analysis_report": analysis_report
        }
    
    async def _simulate_payment_retry(self, context: dict, task_id: str) -> dict:
        """Simulate payment retry attempt"""
        
        original_transaction_id = context.get("original_transaction_id")
        retry_strategy = context.get("retry_strategy", "standard")
        
        await self.send_progress_update(task_id, 30, "Preparing retry with optimized parameters...")
        await asyncio.sleep(2)
        
        await self.send_progress_update(task_id, 60, "Executing payment retry...")
        await asyncio.sleep(3)
        
        # Simulate success/failure based on strategy
        success_rate = 0.95 if retry_strategy == "bypass_3ds_for_verified_corporate" else 0.70
        success = random.random() < success_rate
        
        if success:
            await self.send_progress_update(task_id, 100, "Payment retry successful!")
            return {
                "status": "success",
                "new_transaction_id": f"TXN-{random.randint(100000, 999999)}",
                "amount_charged": 49999.99,
                "retry_strategy_used": retry_strategy
            }
        else:
            await self.send_progress_update(task_id, 100, "Payment retry failed - escalating to manual review")
            return {
                "status": "failed",
                "retry_strategy_used": retry_strategy,
                "escalation_required": True
            }
    
    def _select_weighted_scenario(self) -> str:
        """Select a failure scenario based on weighted probabilities"""
        scenarios = list(self.failure_scenarios.keys())
        weights = [self.failure_scenarios[s]["probability"] for s in scenarios]
        return random.choices(scenarios, weights=weights)[0]
    
    def _get_contributing_factors(self, scenario: str) -> list:
        """Get realistic contributing factors for each scenario"""
        factors_map = {
            "3ds_timeout": ["high_traffic_volume", "issuing_bank_response_delay"],
            "insufficient_funds": ["account_balance_insufficient", "hold_on_account"],
            "network_timeout": ["high_latency", "packet_loss", "gateway_overload"],
            "card_declined": ["fraud_detection_triggered", "card_limit_exceeded"]
        }
        return factors_map.get(scenario, ["unknown_factors"])

if __name__ == "__main__":
    agent = SimulatedPaymentAgent()
    agent.run(port=8002) 