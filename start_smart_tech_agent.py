#!/usr/bin/env python3
"""
Smart Tech Support Agent Startup Script
Launches the AI-powered technical support agent with business-friendly recommendations
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.smart_tech_agent import SmartTechAgent

if __name__ == "__main__":
    agent = SmartTechAgent()
    agent.run(port=8005) 