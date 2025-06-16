#!/usr/bin/env python3
"""
Local A2A System Runner
Starts all agents and orchestrator locally for development and testing
"""

import asyncio
import multiprocessing
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import signal
import os

def run_component(component_info):
    """Run a single component (agent, orchestrator, or frontend server)"""
    name, cmd, cwd = component_info
    try:
        print(f"Starting {name}...")
        if cwd:
            subprocess.run(cmd, cwd=cwd, check=True)
        else:
            subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print(f"\n{name} stopped")
    except Exception as e:
        print(f"Error running {name}: {e}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        sys.exit(1)

def install_requirements():
    """Install required Python packages"""
    print("Installing Python requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
        print("Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("Failed to install requirements. Please run: pip install -r backend/requirements.txt")
        sys.exit(1)

def start_simple_frontend_server():
    """Start a simple HTTP server for the frontend"""
    try:
        import http.server
        import socketserver
        import threading
        
        PORT = 3000
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory="frontend", **kwargs)
            
            def end_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                super().end_headers()
            
            def do_OPTIONS(self):
                self.send_response(200)
                self.end_headers()
        
        def run_server():
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print(f"Frontend server running at http://localhost:{PORT}")
                httpd.serve_forever()
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        return PORT
    except Exception as e:
        print(f"Could not start frontend server: {e}")
        return None

def main():
    """Main function to start the A2A system locally"""
    print("🤖 Starting LatentGenius A2A System Locally")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    if not Path("backend/requirements.txt").exists():
        print("Creating requirements.txt...")
        with open("backend/requirements.txt", "w") as f:
            f.write("""fastapi>=0.104.0
uvicorn>=0.24.0
httpx>=0.25.0
pydantic>=2.4.0
python-multipart>=0.0.6
""")
    
    # Install requirements
    install_requirements()
    
    # Start simple frontend server
    frontend_port = start_simple_frontend_server()
    
    # Start agents and orchestrator
    processes = []
    
    try:
        print("\nStarting A2A components...")
        
        # Registry Service (simplified in-memory version)
        print("📋 Starting Agent Registry...")
        registry_proc = subprocess.Popen([
            sys.executable, "-c", """
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="A2A Agent Registry")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

agents = {}

@app.get("/.well-known/agents")
async def list_agents():
    return {"agents": list(agents.keys())}

@app.post("/register")
async def register_agent(agent_data: dict):
    agents[agent_data["agent_id"]] = agent_data
    return {"status": "registered"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        ])
        processes.append(("Registry", registry_proc))
        time.sleep(2)
        
        # Payment Agent
        print("💳 Starting Payment Agent...")
        payment_proc = subprocess.Popen([
            sys.executable, "-m", "backend.agents.payment_agent"
        ])
        processes.append(("Payment Agent", payment_proc))
        time.sleep(1)
        
        # Fraud Agent
        print("🛡️  Starting Fraud Agent...")
        fraud_proc = subprocess.Popen([
            sys.executable, "-m", "backend.agents.fraud_agent"
        ])
        processes.append(("Fraud Agent", fraud_proc))
        time.sleep(1)
        
        # Order Agent
        print("📦 Starting Order Agent...")
        order_proc = subprocess.Popen([
            sys.executable, "-m", "backend.agents.order_agent"
        ])
        processes.append(("Order Agent", order_proc))
        time.sleep(1)
        
        # Tech Agent
        print("🔧 Starting Tech Agent...")
        tech_proc = subprocess.Popen([
            sys.executable, "-m", "backend.agents.tech_agent"
        ])
        processes.append(("Tech Agent", tech_proc))
        time.sleep(1)
        
        # Orchestrator
        print("🎯 Starting Orchestrator...")
        orchestrator_proc = subprocess.Popen([
            sys.executable, "-m", "backend.orchestrator.app"
        ])
        processes.append(("Orchestrator", orchestrator_proc))
        time.sleep(2)
        
        print("\n" + "=" * 50)
        print("🚀 A2A System Started Successfully!")
        print("=" * 50)
        print("📊 Frontend Dashboard: http://localhost:3000")
        print("📋 Agent Registry: http://localhost:8000")
        print("🎯 Orchestrator: http://localhost:8001")
        print("💳 Payment Agent: http://localhost:8002")
        print("🛡️  Fraud Agent: http://localhost:8003")
        print("📦 Order Agent: http://localhost:8004")
        print("🔧 Tech Agent: http://localhost:8005")
        print("=" * 50)
        print("\n💡 Open http://localhost:3000 to see the live A2A demo!")
        print("🎮 Click 'Start A2A Demo' to see agents coordinate in real-time")
        print("\n⏹️  Press Ctrl+C to stop all services")
        
        # Open browser
        if frontend_port:
            time.sleep(1)
            webbrowser.open(f"http://localhost:{frontend_port}")
        
        # Wait for user interrupt
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping A2A system...")
            
    except Exception as e:
        print(f"❌ Error starting system: {e}")
    finally:
        # Stop all processes
        for name, proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print(f"✅ Stopped {name}")
            except:
                proc.kill()
                print(f"🔥 Force killed {name}")

if __name__ == "__main__":
    main() 