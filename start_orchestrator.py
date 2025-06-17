#!/usr/bin/env python3

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import uvicorn
from orchestrator.app import app

if __name__ == "__main__":
    print("Starting A2A Customer Service Orchestrator on port 8001...")
    print("Orchestrator URL: http://localhost:8001")
    print("Traffic Stream: http://localhost:8001/traffic/stream")
    print("Create Incident: POST http://localhost:8001/incidents")
    
    uvicorn.run(app, host="0.0.0.0", port=8001) 