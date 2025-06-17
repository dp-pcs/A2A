#!/usr/bin/env python3

import sys
import os
import uvicorn

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.tech_agent import TechAgent

def main():
    # Create tech agent instance
    agent = TechAgent()
    
    print("Starting Tech Support Agent on port 8005...")
    print("Agent ID: tech-support-001")
    print("Available skills: system-diagnostics, performance-analysis, incident-resolution")
    
    # Run the agent service directly
    uvicorn.run(agent.app, host="0.0.0.0", port=8005)

if __name__ == "__main__":
    main() 