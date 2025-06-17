#!/usr/bin/env python3

import asyncio
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.smart_payment_agent import SmartPaymentAgent
from agents.smart_fraud_agent import SmartFraudAgent

async def test_smart_agents():
    """Test smart agents with sample data"""
    
    print("🧠 Testing Smart A2A Agents with LLM Integration")
    print("=" * 50)
    
    # Check API keys
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if anthropic_key:
        print("✅ Anthropic API key found")
    if openai_key:
        print("✅ OpenAI API key found")
    if not anthropic_key and not openai_key:
        print("⚠️  No API keys found - agents will use fallback responses")
    
    print()
    
    # Test Smart Payment Agent
    print("🔹 Testing Smart Payment Agent")
    payment_agent = SmartPaymentAgent()
    
    payment_context = {
        "transaction_id": "TXN-TEST-001",
        "customer_id": "globalcorp",
        "amount": 50000,
        "error_code": "3DS_AUTH_TIMEOUT",
        "gateway_response": "3D Secure authentication timed out after 45 seconds",
        "payment_method": "corporate_card",
        "customer_tier": "Enterprise"
    }
    
    try:
        result = await payment_agent.execute_skill(
            "transaction-analysis", 
            payment_context, 
            "test-task-001"
        )
        print(f"✅ Payment analysis completed")
        print(f"   Root cause: {result.get('root_cause', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 'N/A')}")
        print(f"   Retry recommended: {result.get('retry_recommended', 'N/A')}")
    except Exception as e:
        print(f"❌ Payment agent test failed: {e}")
    
    print()
    
    # Test Smart Fraud Agent  
    print("🔹 Testing Smart Fraud Agent")
    fraud_agent = SmartFraudAgent()
    
    fraud_context = {
        "customer_id": "startupai_inc",
        "transaction_amount": 75000,
        "customer_history": {
            "account_age": "3 months",
            "total_spent": 0,
            "payment_success_rate": None
        },
        "security_indicators": {
            "device_fingerprint": "new_device",
            "ip_location": "san_francisco",
            "business_registration": "verified"
        }
    }
    
    try:
        result = await fraud_agent.execute_skill(
            "risk-assessment",
            fraud_context,
            "test-task-002"
        )
        print(f"✅ Fraud assessment completed")
        print(f"   Risk level: {result.get('risk_level', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 'N/A')}")
        print(f"   Recommendation: {result.get('recommendation', 'N/A')}")
    except Exception as e:
        print(f"❌ Fraud agent test failed: {e}")
    
    print()
    print("🎯 Test complete! Your smart agents are ready for the demo.")
    print("\nNext steps:")
    print("1. Start the agent registry: python start_registry.py")
    print("2. Start smart agents: python start_smart_payment_agent.py &")
    print("3. Start orchestrator: python start_orchestrator.py") 
    print("4. Open frontend/smart-demo.html and test scenarios")

if __name__ == "__main__":
    asyncio.run(test_smart_agents()) 