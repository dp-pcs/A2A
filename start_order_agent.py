#!/usr/bin/env python3

import sys
import os
import uvicorn

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.order_agent import OrderAgent

def main():
    # Create order agent instance
    agent = OrderAgent()
    
    print("Starting Order Management Agent on port 8004...")
    print("Agent ID: order-mgmt-001")
    print("Available skills: inventory-hold, order-processing, shipping-coordination")
    
    # Run the agent service directly
    uvicorn.run(agent.app, host="0.0.0.0", port=8004)

if __name__ == "__main__":
    main() 