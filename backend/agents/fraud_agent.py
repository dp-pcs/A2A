import asyncio
import random
import json
from datetime import datetime, timedelta
from backend.shared.base_agent import BaseAgent

class SimulatedFraudAgent(BaseAgent):
    def __init__(self):
        config = {
            "agent_card_version": "1.0",
            "name": "Fraud Detection Agent",
            "agent_id": "fraud-detect-001",
            "description": "Real-time fraud analysis and risk assessment",
            "version": "4.1.0",
            "homepage": "https://latentgenius.ai/agents/fraud-detection",
            "skills": [
                {
                    "name": "risk-assessment",
                    "description": "Evaluate transaction risk and customer legitimacy",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "transaction_amount": {"type": "number"},
                            "transaction_context": {"type": "object"}
                        }
                    },
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "risk_score": {"type": "number"},
                            "risk_level": {"type": "string"},
                            "recommendation": {"type": "string"},
                            "confidence": {"type": "number"}
                        }
                    }
                },
                {
                    "name": "customer-verification",
                    "description": "Verify customer identity and payment method",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "verification_type": {"type": "string"}
                        }
                    }
                }
            ],
            "authentication": {
                "type": "oauth2",
                "scopes": ["fraud.read", "risk.assess"]
            },
            "endpoints": {
                "base_url": "https://agents.latentgenius.ai/fraud-detection",
                "tasks": "/tasks",
                "streaming": "/stream"
            },
            "capabilities": {
                "streaming": True,
                "push_notifications": True,
                "modalities": ["text", "structured_data", "images"]
            }
        }
        
        super().__init__(config)
        
        # Customer risk profiles for realistic scenarios
        self.customer_profiles = {
            "CORP-12345": {
                "risk_level": "low",
                "established_since": "2019",
                "account_value": 2500000,
                "payment_history": "excellent",
                "verification_status": "verified",
                "previous_incidents": 0,
                "base_risk_score": 0.15
            },
            "RETAIL-67890": {
                "risk_level": "medium", 
                "established_since": "2023",
                "account_value": 15000,
                "payment_history": "good",
                "verification_status": "pending",
                "previous_incidents": 1,
                "base_risk_score": 0.45
            },
            "NEW-11111": {
                "risk_level": "high",
                "established_since": "2024",
                "account_value": 0,
                "payment_history": "none",
                "verification_status": "unverified",
                "previous_incidents": 0,
                "base_risk_score": 0.75
            }
        }
        
        # Risk factors that can modify the base score
        self.risk_factors = {
            "high_transaction_amount": {"modifier": 0.1, "threshold": 25000},
            "unusual_time": {"modifier": 0.05, "description": "Transaction outside normal hours"},
            "new_payment_method": {"modifier": 0.15, "description": "First time using this payment method"},
            "velocity_check": {"modifier": 0.2, "description": "Multiple transactions in short time"},
            "geographic_anomaly": {"modifier": 0.25, "description": "Transaction from unusual location"},
            "device_fingerprint": {"modifier": -0.1, "description": "Recognized device"},
            "verified_corporate_card": {"modifier": -0.2, "description": "Corporate payment method"}
        }
        
    async def execute_skill(self, skill_name: str, context: dict, task_id: str) -> dict:
        """Execute fraud detection analysis with realistic simulation"""
        
        if skill_name == "risk-assessment":
            return await self._simulate_risk_assessment(context, task_id)
        elif skill_name == "customer-verification":
            return await self._simulate_customer_verification(context, task_id)
        else:
            raise ValueError(f"Unknown skill: {skill_name}")
    
    async def _simulate_risk_assessment(self, context: dict, task_id: str) -> dict:
        """Simulate comprehensive fraud risk assessment"""
        
        customer_id = context.get("customer_id", "CORP-12345")
        transaction_amount = context.get("transaction_amount", 49999.99)
        transaction_context = context.get("transaction_context", {})
        
        # Step 1: Initial customer lookup
        await self.send_progress_update(task_id, 30, "Verifying customer identity and transaction history...")
        await asyncio.sleep(2)
        
        # Get customer profile
        customer_profile = self.customer_profiles.get(customer_id, self.customer_profiles["NEW-11111"])
        base_risk_score = customer_profile["base_risk_score"]
        
        # Step 2: Analyze transaction context
        await self.send_progress_update(task_id, 60, "Analyzing payment patterns and behavioral signals...")
        await asyncio.sleep(3)
        
        # Calculate risk modifiers
        risk_modifiers = []
        final_risk_score = base_risk_score
        
        # High amount check
        if transaction_amount > self.risk_factors["high_transaction_amount"]["threshold"]:
            modifier = self.risk_factors["high_transaction_amount"]["modifier"]
            final_risk_score += modifier
            risk_modifiers.append("high_transaction_amount")
        
        # Simulate other risk factors
        active_factors = self._simulate_risk_factors(customer_profile, transaction_context)
        for factor in active_factors:
            if factor in self.risk_factors:
                final_risk_score += self.risk_factors[factor]["modifier"]
                risk_modifiers.append(factor)
        
        # Ensure score stays within bounds
        final_risk_score = max(0.0, min(1.0, final_risk_score))
        
        # Step 3: Generate risk insights
        risk_level = "LOW" if final_risk_score < 0.3 else "MEDIUM" if final_risk_score < 0.7 else "HIGH"
        recommendation = "approve" if final_risk_score < 0.5 else "review" if final_risk_score < 0.8 else "decline"
        confidence = 0.97 if customer_profile["verification_status"] == "verified" else 0.85
        
        await self.send_progress_update(task_id, 85, f"{risk_level.title()} risk detected. Customer verified as {customer_profile['verification_status']}.")
        await asyncio.sleep(1)
        
        # Step 4: Generate detailed risk assessment artifact
        risk_assessment = {
            "artifact_id": f"fraud-assessment-{task_id}",
            "task_id": task_id,
            "type": "risk_assessment",
            "format": "application/json",
            "created_at": datetime.utcnow().isoformat(),
            "data": {
                "risk_assessment": {
                    "customer_id": customer_id,
                    "overall_risk_score": round(final_risk_score, 2),
                    "risk_level": risk_level,
                    "confidence": confidence,
                    "recommendation": recommendation.upper(),
                    "verified_attributes": self._get_verified_attributes(customer_profile),
                    "risk_factors": {
                        "positive_signals": self._get_positive_signals(customer_profile, active_factors),
                        "negative_signals": self._get_negative_signals(risk_modifiers),
                        "neutral_signals": self._get_neutral_signals()
                    },
                    "customer_profile": {
                        "account_age": customer_profile["established_since"],
                        "account_value": customer_profile["account_value"],
                        "payment_history": customer_profile["payment_history"],
                        "verification_status": customer_profile["verification_status"],
                        "previous_incidents": customer_profile["previous_incidents"]
                    },
                    "transaction_analysis": {
                        "amount": transaction_amount,
                        "amount_percentile": self._calculate_amount_percentile(customer_id, transaction_amount),
                        "time_analysis": "normal_business_hours",
                        "device_analysis": "recognized_corporate_device",
                        "location_analysis": "expected_geographic_region"
                    }
                }
            }
        }
        
        await self.send_artifact_ready(task_id, {
            "type": "risk_assessment",
            "url": f"https://artifacts.latentgenius.ai/fraud-assessment-{task_id}.json",
            "format": "application/json"
        }, "Risk assessment report generated")
        
        # Send insight about the assessment
        await self.send_insight(task_id, {
            "risk_score": final_risk_score,
            "confidence": confidence,
            "key_factors": risk_modifiers[:3]  # Top 3 factors
        }, f"Risk analysis complete: {risk_level} risk with {int(confidence*100)}% confidence")
        
        return {
            "risk_score": final_risk_score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "confidence": confidence,
            "verified_signals": [attr["attribute"] for attr in risk_assessment["data"]["risk_assessment"]["verified_attributes"]],
            "risk_assessment": risk_assessment
        }
    
    async def _simulate_customer_verification(self, context: dict, task_id: str) -> dict:
        """Simulate customer identity verification process"""
        
        customer_id = context.get("customer_id", "CORP-12345")
        verification_type = context.get("verification_type", "identity")
        
        await self.send_progress_update(task_id, 50, f"Performing {verification_type} verification...")
        await asyncio.sleep(2)
        
        customer_profile = self.customer_profiles.get(customer_id, self.customer_profiles["NEW-11111"])
        
        # Simulate verification results based on customer profile
        verification_success = customer_profile["verification_status"] == "verified"
        
        await self.send_progress_update(task_id, 100, f"Verification {'successful' if verification_success else 'failed'}")
        
        return {
            "verification_status": "verified" if verification_success else "failed",
            "verification_type": verification_type,
            "confidence": 0.95 if verification_success else 0.3,
            "details": customer_profile
        }
    
    def _simulate_risk_factors(self, customer_profile: dict, transaction_context: dict) -> list:
        """Simulate realistic risk factors based on customer and transaction"""
        
        active_factors = []
        
        # Corporate customers get positive signals
        if customer_profile["account_value"] > 100000:
            active_factors.append("verified_corporate_card")
            active_factors.append("device_fingerprint")
        
        # New customers get risk factors
        if customer_profile["established_since"] == "2024":
            active_factors.append("new_payment_method")
        
        # Randomly add some factors for realism
        possible_factors = ["unusual_time", "velocity_check"]
        if random.random() < 0.3:  # 30% chance
            active_factors.extend(random.sample(possible_factors, 1))
            
        return active_factors
    
    def _get_verified_attributes(self, customer_profile: dict) -> list:
        """Generate verified attributes based on customer profile"""
        
        base_attributes = [
            {
                "attribute": "customer_identity",
                "status": "verified" if customer_profile["verification_status"] == "verified" else "pending",
                "method": "corporate_registration_check"
            },
            {
                "attribute": "payment_method",
                "status": "verified" if customer_profile["account_value"] > 50000 else "pending",
                "method": "corporate_card_validation"
            },
            {
                "attribute": "billing_address",
                "status": "verified",
                "method": "address_verification_service"
            },
            {
                "attribute": "order_pattern",
                "status": "normal" if customer_profile["previous_incidents"] == 0 else "flagged",
                "method": "behavioral_analysis"
            }
        ]
        
        return base_attributes
    
    def _get_positive_signals(self, customer_profile: dict, active_factors: list) -> list:
        """Generate positive fraud signals"""
        
        signals = []
        
        if customer_profile["established_since"] <= "2020":
            signals.append(f"established_customer_since_{customer_profile['established_since']}")
        
        if customer_profile["payment_history"] == "excellent":
            signals.append("consistent_payment_history")
        
        if customer_profile["verification_status"] == "verified":
            signals.append("verified_corporate_entity")
        
        if "verified_corporate_card" in active_factors:
            signals.append("corporate_payment_method")
        
        signals.append("normal_order_size_for_customer")
        
        return signals
    
    def _get_negative_signals(self, risk_modifiers: list) -> list:
        """Generate negative fraud signals"""
        
        negative_signals = []
        
        for modifier in risk_modifiers:
            if modifier in ["velocity_check", "geographic_anomaly", "unusual_time"]:
                negative_signals.append(modifier.replace("_", " "))
        
        return negative_signals
    
    def _get_neutral_signals(self) -> list:
        """Generate neutral fraud signals"""
        
        return [
            "peak_traffic_period",
            "automated_payment_processing"
        ]
    
    def _calculate_amount_percentile(self, customer_id: str, amount: float) -> int:
        """Calculate what percentile this transaction amount is for the customer"""
        
        customer_profile = self.customer_profiles.get(customer_id, self.customer_profiles["NEW-11111"])
        
        if customer_profile["account_value"] > 1000000:
            return 65  # Normal for enterprise
        elif customer_profile["account_value"] > 50000:
            return 85  # High for mid-market
        else:
            return 95  # Very high for small customers

if __name__ == "__main__":
    agent = SimulatedFraudAgent()
    agent.run(port=8003) 