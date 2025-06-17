# 🤖 Real A2A Customer Service Demo

This demonstrates **actual Agent-to-Agent (A2A) communication** using real HTTP services, JSON-RPC 2.0 calls, and live traffic monitoring.

## 🚀 Quick Start

### Option 1: One-Command Demo
```bash
python start_a2a_demo.py
```

This will:
- Start all 6 services (registry + 4 agents + orchestrator)
- Open the dashboard automatically 
- Show real A2A traffic in real-time

### Option 2: Manual Service Startup
```bash
# 1. Start Agent Registry
python start_registry.py

# 2. Start Agents (in separate terminals)
python start_payment_agent.py
python start_fraud_agent.py  
python start_order_agent.py
python start_tech_agent.py

# 3. Start Orchestrator
python start_orchestrator.py

# 4. Open frontend/index.html in browser
```

## 🎯 What Makes This "Real A2A"

### ✅ Actual HTTP Services
- Each agent runs as a separate HTTP server
- Real network communication between services
- No simulated data - everything is live

### ✅ A2A Protocol Compliance
- **Agent Discovery**: Real registry with `/well-known/agents` endpoint
- **Agent Cards**: Each agent publishes capabilities at `/.well-known/agent.json`
- **JSON-RPC 2.0**: Actual task delegation via HTTP POST
- **Streaming**: Server-Sent Events for real-time updates

### ✅ Real Communication Flow
```
Orchestrator → Registry    (Agent Discovery)
Orchestrator → Payment     (JSON-RPC task delegation)
Orchestrator → Fraud       (Parallel risk assessment)
Orchestrator → Order       (Inventory management)
Orchestrator → Tech        (System diagnostics)
Agents → Orchestrator      (Task results)
```

### ✅ Live Traffic Monitoring
- Every HTTP request/response is captured
- Real latency measurements
- Live streaming to dashboard
- Export traffic for analysis

## 🌐 Service Architecture

| Service | Port | Role | Skills |
|---------|------|------|--------|
| Registry | 8000 | Agent discovery | Agent registration, skill matching |
| Payment Agent | 8002 | Payment processing | transaction-analysis, payment-retry |
| Fraud Agent | 8003 | Risk assessment | risk-assessment, fraud-detection |
| Order Agent | 8004 | Inventory management | inventory-hold, order-processing |
| Tech Agent | 8005 | System diagnostics | system-diagnostics, performance-analysis |
| Orchestrator | 8001 | Incident coordination | Multi-agent task orchestration |

## 📱 Dashboard Features

Open `frontend/index.html` to see:

### Real-Time Network Visualization
- Live agent network topology
- Message animations between agents
- Agent status and activity indicators

### A2A Traffic Monitor
- Every JSON-RPC call displayed
- Request/response pairs with latency
- Message content inspection
- Traffic export functionality

### Incident Management
- Real incident creation and tracking
- Live task progress across agents
- Resolution synthesis from agent results

## 🔬 Demo Scenario

When you click **"Start Real A2A Demo"**, here's what happens:

### 1. Incident Creation
```json
{
  "incident_type": "payment_failure",
  "customer": {"id": "globalcorp", "tier": "enterprise"},
  "order": {"id": "ORD-20241201-001", "amount": 50000},
  "failure_details": {"error_code": "GATEWAY_TIMEOUT"}
}
```

### 2. Agent Discovery
- Orchestrator queries registry for agents with required skills
- Registry returns agent endpoints and capabilities

### 3. Parallel Task Execution
- **Payment Agent**: Analyzes transaction failure, recommends retry strategy
- **Fraud Agent**: Assesses customer risk, clears for high-value transaction  
- **Order Agent**: Secures inventory, enables expedited shipping
- **Tech Agent**: Diagnoses system issues, identifies root cause

### 4. Resolution Synthesis
- Orchestrator combines all agent results
- Generates coordinated resolution strategy
- Updates incident status to "resolved"

## 🔍 Monitoring Real Traffic

### Live Stream Endpoint
```bash
curl -N http://localhost:8001/traffic/stream
```

### Recent Traffic API
```bash
curl http://localhost:8001/traffic/recent
```

### Example A2A Message
```json
{
  "timestamp": "2024-12-01T10:30:15.123Z",
  "source_agent": "orchestrator-001",
  "target_agent": "payment-sys-001", 
  "message_type": "request",
  "method": "transaction-analysis",
  "message_id": "req-abc123",
  "latency_ms": 45.7,
  "content": {
    "jsonrpc": "2.0",
    "method": "create_task",
    "params": {
      "task_id": "payment-analysis-incident-20241201-001",
      "skill_required": "transaction-analysis",
      "context": {
        "transaction_id": "TXN-20241201-001",
        "customer_id": "globalcorp",
        "amount": 50000
      }
    }
  }
}
```

## 🛠️ Technical Implementation

### A2A Client Library (`backend/shared/a2a_client.py`)
- Handles agent discovery and communication
- Captures all traffic for monitoring
- Implements JSON-RPC 2.0 protocol
- Provides async task monitoring

### Agent Base Class (`backend/shared/base_agent.py`)
- FastAPI-based HTTP service framework
- A2A protocol compliance (agent cards, task endpoints)
- Server-Sent Events for streaming
- Background task execution

### Traffic Monitoring
- Global traffic monitor captures all messages
- Real-time streaming via WebSocket/SSE
- Message queuing and subscriber management
- Latency measurement and statistics

## 🔧 Troubleshooting

### Services Not Starting
```bash
# Check if ports are free
netstat -an | grep :800[0-5]

# Kill existing processes
pkill -f "start_.*_agent.py"
```

### Agent Registration Issues
```bash
# Check registry health
curl http://localhost:8000/health

# View registered agents
curl http://localhost:8000/.well-known/agents
```

### No Traffic Appearing
1. Ensure all services are running
2. Check browser console for WebSocket errors  
3. Verify orchestrator is connected to registry
4. Try manual incident creation:

```bash
curl -X POST http://localhost:8001/incidents \
  -H "Content-Type: application/json" \
  -d '{"incident_type": "payment_failure", ...}'
```

## 🎓 Key Differences from Simulation

| Aspect | Simulated | Real A2A |
|--------|-----------|----------|
| Communication | Fake delays, hardcoded responses | Actual HTTP calls, real latency |
| Agent Discovery | Static agent list | Dynamic registry lookup |
| Task Execution | Instant fake results | Real async processing |
| Monitoring | Synthetic traffic | Captured network traffic |
| Scalability | Single process | Distributed services |
| Failure Modes | Simulated errors | Real network/service failures |

## 🚀 Next Steps

This real A2A implementation demonstrates:
- ✅ Multi-agent orchestration
- ✅ Real-time communication monitoring  
- ✅ Distributed service architecture
- ✅ A2A protocol compliance
- ✅ Live traffic visualization

You now have actual agent-to-agent communication that can be extended with:
- Authentication and security
- Message persistence and replay
- Load balancing and clustering
- Integration with real business systems
- Advanced monitoring and analytics

**Ready to see real agents talk to each other? Run the demo! 🤖💬** 