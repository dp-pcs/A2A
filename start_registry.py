#!/usr/bin/env python3

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import uvicorn
from agent_registry.app import app

if __name__ == "__main__":
    print("Starting A2A Agent Registry on port 8000...")
    print("Registry URL: http://localhost:8000")
    print("Well-known endpoint: http://localhost:8000/.well-known/agents")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 