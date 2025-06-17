#!/usr/bin/env python3

import subprocess
import time
import signal
import sys
import os
from threading import Thread
import webbrowser

# Store process references for cleanup
processes = []

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Shutting down A2A Demo...")
    
    for proc in processes:
        if proc.poll() is None:  # Process is still running
            print(f"   Terminating process {proc.pid}")
            proc.terminate()
    
    # Wait a bit for graceful shutdown
    time.sleep(2)
    
    # Force kill if needed
    for proc in processes:
        if proc.poll() is None:
            print(f"   Force killing process {proc.pid}")
            proc.kill()
    
    print("✅ All A2A services stopped")
    sys.exit(0)

def start_service(name, script, delay=0):
    """Start a service with optional delay"""
    if delay > 0:
        print(f"⏳ Waiting {delay}s before starting {name}...")
        time.sleep(delay)
    
    print(f"🚀 Starting {name}...")
    
    try:
        proc = subprocess.Popen([
            sys.executable, script
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        processes.append(proc)
        
        # Read output in a separate thread to prevent blocking
        def read_output():
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                print(f"[{name}] {line.strip()}")
        
        thread = Thread(target=read_output, daemon=True)
        thread.start()
        
        return proc
        
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def check_service_health(url, service_name, max_retries=10):
    """Check if a service is healthy"""
    import requests
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ {service_name} is healthy")
                return True
        except:
            pass
        
        if i < max_retries - 1:
            print(f"⏳ Waiting for {service_name} to be ready... ({i+1}/{max_retries})")
            time.sleep(2)
    
    print(f"❌ {service_name} failed to start properly")
    return False

def main():
    """Start the complete A2A demo system"""
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🤖 LatentGenius A2A Customer Service Demo")
    print("=" * 50)
    print("Starting all A2A services...")
    print()
    
    # 1. Start Agent Registry first
    start_service("Agent Registry", "start_registry.py")
    time.sleep(3)  # Give registry time to start
    
    # Check registry health
    if not check_service_health("http://localhost:8000", "Agent Registry"):
        print("❌ Registry failed to start. Exiting...")
        return
    
    # 2. Start all agents in parallel (they'll register with the registry)
    agents = [
        ("Smart Payment Agent", "start_smart_payment_agent.py", 1),
        ("Smart Fraud Agent", "start_smart_fraud_agent.py", 2),
        ("Order Agent", "start_order_agent.py", 3),
        ("Smart Tech Agent", "start_smart_tech_agent.py", 4)
    ]
    
    for name, script, delay in agents:
        Thread(target=start_service, args=(name, script, delay), daemon=True).start()
    
    # Wait for agents to start and register
    print("⏳ Waiting for agents to register...")
    time.sleep(8)
    
    # 3. Start Orchestrator
    start_service("Orchestrator", "start_orchestrator.py", 1)
    time.sleep(3)
    
    # Check orchestrator health
    if not check_service_health("http://localhost:8001", "Orchestrator"):
        print("❌ Orchestrator failed to start")
        return
    
    print()
    print("🎉 A2A Demo System is READY!")
    print("=" * 50)
    print()
    print("📊 Service Status:")
    print("   🔧 Agent Registry:     http://localhost:8000")
    print("   💳 Smart Payment Agent: http://localhost:8002")
    print("   🛡️  Smart Fraud Agent:   http://localhost:8003")
    print("   📦 Order Agent:        http://localhost:8004")
    print("   🔧 Smart Tech Agent:   http://localhost:8005")
    print("   🎭 Orchestrator:       http://localhost:8001")
    print()
    print("🌐 Dashboard:")
    print("   📱 Frontend:           Open frontend/index.html in browser")
    print("   📡 A2A Traffic Stream: http://localhost:8001/traffic/stream")
    print()
    print("🚀 Quick Start:")
    print("   1. Open frontend/index.html in your browser")
    print("   2. Click 'Start Real A2A Demo' to see actual agent communication")
    print("   3. Watch real JSON-RPC traffic between agents!")
    print()
    print("💡 Real A2A Features:")
    print("   ✅ Agent discovery via registry")
    print("   ✅ JSON-RPC 2.0 task delegation")
    print("   ✅ Real HTTP calls between agents")
    print("   ✅ Live traffic monitoring")
    print("   ✅ Server-Sent Events streaming")
    print("   ✅ Latency measurement")
    print()
    print("Press Ctrl+C to stop all services")
    print()
    
    # Optionally open browser
    try:
        frontend_path = os.path.abspath("frontend/index.html")
        if os.path.exists(frontend_path):
            print(f"🌐 Opening dashboard: file://{frontend_path}")
            webbrowser.open(f"file://{frontend_path}")
    except:
        pass
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
            
            # Check if any critical processes have died
            if processes[0].poll() is not None:  # Registry died
                print("❌ Agent Registry died. Restarting...")
                processes[0] = start_service("Agent Registry", "start_registry.py")
            
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main() 