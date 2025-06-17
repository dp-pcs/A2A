#!/usr/bin/env python3
"""
Complete A2A Demo Startup Script
Starts all services in the correct order and ensures they stay running
"""

import subprocess
import time
import signal
import sys
import os
from pathlib import Path

# Track all processes so we can clean them up
processes = []

def signal_handler(sig, frame):
    print("\n🛑 Shutting down all A2A services...")
    for process in processes:
        try:
            process.terminate()
        except:
            pass
    sys.exit(0)

def start_service(name, script_path, port, wait_time=2):
    """Start a service and track the process"""
    print(f"🚀 Starting {name} on port {port}...")
    
    try:
        process = subprocess.Popen([
            sys.executable, script_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        processes.append(process)
        time.sleep(wait_time)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ {name} started successfully")
            return True
        else:
            print(f"❌ {name} failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error starting {name}: {e}")
        return False

def main():
    print("🎯 Starting Complete A2A Smart Demo")
    print("=" * 50)
    
    # Register signal handler for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Kill any existing processes
    print("🧹 Cleaning up existing processes...")
    os.system("pkill -f 'python start_' > /dev/null 2>&1")
    time.sleep(2)
    
    # Start services in order
    services = [
        ("Registry", "start_registry.py", 8000, 3),
        ("Orchestrator", "start_orchestrator.py", 8001, 3),
        ("Smart Payment Agent", "start_smart_payment_agent.py", 8002, 2),
        ("Smart Fraud Agent", "start_smart_fraud_agent.py", 8003, 2),
        ("Smart Tech Agent", "start_smart_tech_agent.py", 8005, 2),
    ]
    
    failed_services = []
    
    for name, script, port, wait in services:
        if not start_service(name, script, port, wait):
            failed_services.append(name)
    
    if failed_services:
        print(f"\n❌ Failed to start: {', '.join(failed_services)}")
        print("Please check the error logs above")
        return
    
    # Start frontend server
    print("🌐 Starting Frontend Server on port 3000...")
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "http.server", "3000"
    ], cwd="frontend", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    processes.append(frontend_process)
    time.sleep(1)
    
    print("\n🎉 All services started successfully!")
    print("=" * 50)
    print("📊 Service Status:")
    print("• Registry:           http://localhost:8000")
    print("• Orchestrator:       http://localhost:8001") 
    print("• Smart Payment:      http://localhost:8002")
    print("• Smart Fraud:        http://localhost:8003")
    print("• Smart Tech:         http://localhost:8005")
    print("• Frontend Demo:      http://localhost:3000/smart-demo.html")
    print("=" * 50)
    print("🚀 Open http://localhost:3000/smart-demo.html to test the demo!")
    print("🛑 Press Ctrl+C to stop all services")
    
    # Open the frontend automatically
    try:
        import webbrowser
        time.sleep(2)
        webbrowser.open("http://localhost:3000/smart-demo.html")
    except:
        pass
    
    # Keep the script running
    try:
        while True:
            # Check if all processes are still running
            running = 0
            for i, process in enumerate(processes):
                if process.poll() is None:
                    running += 1
                else:
                    print(f"⚠️  Service {i} has stopped")
            
            if running == 0:
                print("❌ All services have stopped")
                break
                
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main() 