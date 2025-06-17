#!/usr/bin/env python3

import sys
import os
import uvicorn

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.payment_agent import PaymentAgent

def main():
    # Create payment agent instance
    agent = PaymentAgent()
    
    print("Starting Payment Agent on port 8002...")
    print("Agent ID: payment-sys-001")
    print("Available skills: transaction-analysis, payment-retry, gateway-diagnostics")
    
    # Run the agent service directly
    uvicorn.run(agent.app, host="0.0.0.0", port=8002)

if __name__ == "__main__":
    main() 