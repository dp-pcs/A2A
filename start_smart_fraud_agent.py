#!/usr/bin/env python3

import sys
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.smart_fraud_agent import SmartFraudAgent

def main():
    # Check for API keys
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not anthropic_key and not openai_key:
        print("⚠️  WARNING: No LLM API keys found!")
        print("   Set ANTHROPIC_API_KEY or OPENAI_API_KEY for dynamic responses")
        print("   Agent will use fallback responses without API keys")
        print()
    else:
        provider = "anthropic" if anthropic_key else "openai"
        print(f"✅ Found {provider.upper()} API key - enabling smart responses")
    
    # Create smart fraud agent instance
    agent = SmartFraudAgent()
    
    print("🧠 Starting Smart Fraud Agent on port 8003...")
    print("Agent ID: fraud-detect-001")
    print("Available skills: risk-assessment, fraud-detection, customer-verification")
    print("Intelligence: LLM-powered dynamic reasoning")
    
    # Run the agent service directly
    uvicorn.run(agent.app, host="0.0.0.0", port=8003)

if __name__ == "__main__":
    main() 