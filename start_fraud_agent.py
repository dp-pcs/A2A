#!/usr/bin/env python3

import sys
import os
import uvicorn

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.fraud_agent import FraudAgent

def main():
    # Create fraud agent instance
    agent = FraudAgent()
    
    print("Starting Fraud Detection Agent on port 8003...")
    print("Agent ID: fraud-detect-001")
    print("Available skills: risk-assessment, fraud-detection, customer-verification")
    
    # Run the agent service directly
    uvicorn.run(agent.app, host="0.0.0.0", port=8003)

if __name__ == "__main__":
    main() 