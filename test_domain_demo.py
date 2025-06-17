#!/usr/bin/env python3
"""
Simple Domain Ownership Demo
Directly tests smart agents to show domain assessment and conditional analysis
"""

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent / "backend"))

from agents.smart_fraud_agent import SmartFraudAgent
from agents.smart_payment_agent import SmartPaymentAgent  
from agents.smart_tech_agent import SmartTechAgent

def print_domain_response(agent_name, response):
    """Pretty print an agent's domain assessment response"""
    print(f"\n🤖 {agent_name} Response:")
    print("=" * 50)
    
    if isinstance(response, dict) and 'domain_assessment' in response:
        domain = response['domain_assessment']
        is_my_domain = domain.get('is_my_domain', domain.get('is_fraud_related', False))
        confidence = domain.get('confidence', domain.get('confidence_in_domain', 0.5))
        reasoning = domain.get('reasoning', domain.get('rationale', 'No reasoning provided'))
        defer_to = domain.get('defer_to', domain.get('primary_responsible_team', 'other team'))
        
        print(f"📊 Domain Assessment: {'YES' if is_my_domain else 'NO'}")
        print(f"🎯 Confidence: {confidence:.1%}")
        print(f"💭 Reasoning: {reasoning}")
        
        if is_my_domain:
            print(f"✅ Taking ownership - proceeding with analysis")
            if 'overall_risk_score' in response:
                print(f"🔍 Risk Score: {response.get('overall_risk_score', 0):.1%}")
            if 'recommendation' in response:
                print(f"🎯 Recommendation: {response.get('recommendation', 'N/A')}")
            if 'risk_level' in response:
                print(f"⚠️  Risk Level: {response.get('risk_level', 'N/A')}")
        else:
            print(f"🚨 Not my domain - deferring to: {defer_to}")
    elif isinstance(response, dict):
        # Handle other response formats
        print(f"📝 Analysis: {response.get('analysis', 'No analysis provided')}")
        print(f"🎯 Confidence: {response.get('confidence', 0):.1%}")
        if 'recommendations' in response:
            print(f"💡 Recommendations: {', '.join(response['recommendations'])}")
    else:
        print(f"📝 Response: {response}")

async def test_scenario(scenario_name, incident_data):
    """Test a scenario with all three smart agents"""
    print(f"\n🎯 Testing Scenario: {scenario_name}")
    print("=" * 70)
    print(f"📋 Issue: {incident_data['failure_details']['error_code']}")
    print(f"💰 Amount: ${incident_data['order']['amount']:,}")
    print(f"👤 Customer: {incident_data['customer']['name']} ({incident_data['customer']['tier']})")

    # Initialize agents
    fraud_agent = SmartFraudAgent()
    payment_agent = SmartPaymentAgent()
    tech_agent = SmartTechAgent()

    agents = [
        ("Smart Fraud Agent", fraud_agent, "risk-assessment"),
        ("Smart Payment Agent", payment_agent, "transaction-analysis"), 
        ("Smart Tech Agent", tech_agent, "system-diagnostics")
    ]

    # Test each agent
    for agent_name, agent, skill_name in agents:
        try:
            # Generate a unique task ID
            task_id = str(uuid.uuid4())
            
            # Call the agent's execute_skill method directly
            response = await agent.execute_skill(skill_name, incident_data, task_id)
            
            print_domain_response(agent_name, response)
            
        except Exception as e:
            print(f"\n❌ {agent_name} Error: {e}")

async def main():
    """Run the domain ownership demo"""
    print("🎭 Smart Agent Domain Ownership Demo")
    print("=" * 70)
    print("Testing how agents assess domain ownership and make conditional decisions\n")

    # Test scenarios from our demo file
    scenarios = [
        {
            "name": "Enterprise Payment Timeout (3DS Issue)",
            "data": {
                "incident_type": "payment_failure",
                "customer": {
                    "id": "globalcorp",
                    "name": "GlobalCorp Technologies",
                    "tier": "enterprise",
                    "account_value": 2150000,
                    "established_since": "2022",
                    "purchase_history": {
                        "average_order_value": 45000,
                        "largest_previous_order": 85000,
                        "monthly_volume": 6,
                        "preferred_payment": "corporate_amex_ending_5678",
                        "last_successful_transaction": "2024-11-28T10:15:00Z"
                    },
                    "business_context": {
                        "industry": "AI/ML Infrastructure",
                        "use_case": "Training large language models",
                        "urgency": "Critical - production training pipeline blocked"
                    }
                },
                "order": {
                    "id": "ORD-20241201-001",
                    "amount": 50000,
                    "currency": "USD",
                    "items": [{"name": "GPU Cluster - 8x H100 Cards", "quantity": 8}],
                    "business_justification": "Approved Q4 budget expansion for model training capacity"
                },
                "failure_details": {
                    "transaction_id": "TXN-20241201-001",
                    "error_code": "3DS_AUTH_TIMEOUT",
                    "gateway_response": "3D Secure authentication timed out after 45 seconds - issuer authentication service unavailable",
                    "timestamp": "2024-12-01T14:23:45Z",
                    "payment_method": "corporate_amex_ending_5678",
                    "technical_context": {
                        "3ds_challenge_initiated": True,
                        "issuer_response_time": "timeout_after_45s",
                        "gateway_health": "operational",
                        "customer_browser": "Chrome 119 on macOS",
                        "previous_3ds_success": "2024-11-28T10:15:00Z"
                    }
                }
            }
        },
        {
            "name": "Suspicious High-Value Transaction",
            "data": {
                "incident_type": "payment_failure", 
                "customer": {
                    "id": "startupai_inc",
                    "name": "StartupAI Inc",
                    "tier": "growth",
                    "account_value": 0,
                    "established_since": "2024"
                },
                "order": {
                    "id": "ORD-20241201-002",
                    "amount": 75000,
                    "currency": "USD",
                    "items": [{"name": "Complete AI Infrastructure Package", "quantity": 1}]
                },
                "failure_details": {
                    "transaction_id": "TXN-20241201-002",
                    "error_code": "FRAUD_SUSPECTED",
                    "gateway_response": "Transaction flagged for manual review",
                    "timestamp": "2024-12-01T09:15:22Z",
                    "payment_method": "business_credit_card_ending_1234"
                }
            }
        },
        {
            "name": "Infrastructure Performance Issue",
            "data": {
                "incident_type": "payment_failure",
                "customer": {
                    "id": "techcorp",
                    "name": "TechCorp Ltd",
                    "tier": "standard",
                    "account_value": 125000,
                    "established_since": "2023"
                },
                "order": {
                    "id": "ORD-20241201-003",
                    "amount": 25000,
                    "currency": "USD",
                    "items": [{"name": "Cloud Infrastructure Expansion", "quantity": 1}]
                },
                "failure_details": {
                    "transaction_id": "TXN-20241201-003",
                    "error_code": "GATEWAY_TIMEOUT",
                    "gateway_response": "Payment gateway experiencing high latency",
                    "timestamp": "2024-12-01T16:45:30Z",
                    "payment_method": "business_debit_ending_7890"
                }
            }
        }
    ]

    # Test each scenario
    for scenario in scenarios:
        await test_scenario(scenario["name"], scenario["data"])
        print("\n" + "="*70)

    print("\n🎉 Demo Complete!")
    print("Each agent assessed whether the issue was in their domain of expertise.")
    print("Agents either took ownership with detailed analysis or deferred to the appropriate team.")

if __name__ == "__main__":
    # Check if we have the API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  No ANTHROPIC_API_KEY found. Agents will use fallback responses.")
        print("For full AI capabilities, set your API key in the environment.\n")
    
    asyncio.run(main()) 