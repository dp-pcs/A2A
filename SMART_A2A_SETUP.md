# 🧠 Smart A2A Demo Setup Guide

This guide shows how to run the **intelligent A2A demo** with LLM-powered agents that can dynamically reason through real business problems.

## 🎯 What Makes This "Smart"

### Dynamic AI Reasoning
- **Payment Agent**: Uses Claude/GPT to analyze transaction failures and develop retry strategies
- **Fraud Agent**: Applies behavioral analysis and threat intelligence to assess security risks  
- **Incident Selection**: Users choose from 3 realistic business scenarios
- **Real-time Adaptation**: Agents respond dynamically based on actual incident context

### Scenario Options
1. **Payment Gateway Timeout** - Corporate transaction failing during peak load
2. **Suspected Account Compromise** - Unusual behavioral patterns triggering security alerts
3. **Supply Chain Disruption** - Critical inventory shortage affecting enterprise deployment

## 🚀 Quick Start

### 1. Set up LLM API Keys (Required for Smart Responses)

**Option A: Anthropic Claude (Recommended)**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

**Option B: OpenAI GPT**
```bash
export OPENAI_API_KEY="sk-..."
```

### 2. Install Dependencies
```bash
pip install -r requirements-a2a.txt
```

### 3. Start All Services
```bash
# Terminal 1: Agent Registry
python start_registry.py

# Terminal 2: Smart Payment Agent  
python start_smart_payment_agent.py

# Terminal 3: Smart Fraud Agent
python start_smart_fraud_agent.py

# Terminal 4: Order Agent
python start_order_agent.py

# Terminal 5: Tech Agent
python start_tech_agent.py

# Terminal 6: Orchestrator
python start_orchestrator.py
```

### 4. Register Agents
```bash
python register_agents.py
```

### 5. Open Smart Demo
```bash
open frontend/smart-demo.html
```

## 🎮 How to Use the Smart Demo

### Scenario Selection
1. **Choose Your Challenge**: Select from 3 realistic business scenarios
2. **Review Details**: See customer profile, order value, and specific issues
3. **Start Demo**: Click to trigger intelligent agent collaboration

### Watch AI in Action
- **Real-time Reasoning**: See agents analyze problems with LLM intelligence
- **Dynamic Responses**: Each run produces different analysis based on context
- **A2A Traffic**: Monitor actual JSON-RPC calls between smart agents
- **Live Results**: Watch agents coordinate solutions in real-time

## 🧠 Smart Agent Capabilities

### Smart Payment Agent
- **Root Cause Analysis**: Identifies specific payment failure causes
- **Strategy Development**: Creates tailored retry approaches
- **Risk Assessment**: Evaluates success probability and business impact
- **Technical Diagnosis**: Analyzes gateway timeouts, 3DS issues, etc.

### Smart Fraud Agent  
- **Behavioral Analysis**: Detects deviations from normal patterns
- **Threat Assessment**: Evaluates security risks with confidence scoring
- **Investigation Planning**: Develops investigation strategies
- **Security Recommendations**: Provides specific protective measures

## 📊 Example Scenarios in Detail

### Scenario 1: Payment Gateway Timeout
**Customer**: GlobalCorp Enterprise ($2.5M account value)
**Order**: $75,000 AI computing cluster
**Challenge**: 3DS verification timeout during peak traffic

**Smart Agent Analysis**:
- Payment Agent analyzes gateway logs and timeout patterns
- Identifies corporate card bypass opportunities
- Recommends optimized retry strategy with 97% success probability
- Suggests infrastructure improvements

### Scenario 2: Suspected Account Compromise  
**Customer**: TechStart AI Inc ($150K account value)
**Order**: $95,000 unexpected large purchase
**Challenge**: Multiple security flags triggered

**Smart Agent Analysis**:
- Fraud Agent correlates behavioral anomalies
- Assesses account takeover probability
- Evaluates legitimacy vs. threat indicators
- Recommends verification workflow

### Scenario 3: Supply Chain Disruption
**Customer**: MegaCorp Research Labs ($5M account value)  
**Order**: $250,000 enterprise AI cluster
**Challenge**: Critical shortage with mission-critical deadline

**Smart Agent Analysis**:
- Order Agent evaluates alternative solutions
- Assesses supplier networks and availability
- Develops expedited fulfillment strategies
- Coordinates cross-functional resolution

## 🔧 Configuration Options

### LLM Model Selection
Edit `backend/shared/llm_agent.py`:
```python
llm_config = {
    "provider": "anthropic",  # or "openai"
    "model": "claude-3-haiku-20240307",  # or "gpt-3.5-turbo"
    "temperature": 0.1,  # Low for consistent business decisions
    "max_tokens": 1000
}
```

### Custom Scenarios
Add new scenarios to `frontend/js/smart-demo.js`:
```javascript
custom_scenario: {
    title: "Your Custom Challenge",
    description: "Description of the business problem",
    complexity: "High",
    data: {
        incident_type: "custom_type",
        customer: { /* customer details */ },
        order: { /* order details */ },
        failure_details: { /* specific issues */ }
    }
}
```

## 🎯 Key Differences from Basic Demo

| Aspect | Basic A2A | Smart A2A |
|--------|-----------|-----------|
| **Agent Intelligence** | Hardcoded responses | LLM-powered reasoning |
| **Scenario Variety** | Single payment failure | 3 diverse business challenges |
| **Response Quality** | Static simulation | Dynamic context-aware analysis |
| **User Experience** | Fixed demo path | Interactive scenario selection |
| **Business Realism** | Generic responses | Specific actionable recommendations |

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Orchestrator   │    │ Agent Registry  │
│ Smart Demo UI   │◄──►│  Coordinates    │◄──►│ Service         │
│ Scenario Select │    │  Multi-Agent    │    │ Discovery       │
└─────────────────┘    │  Tasks          │    └─────────────────┘
                       └─────────────────┘
                               │
                   ┌───────────┼───────────┐
                   │           │           │
           ┌───────▼──────┐ ┌──▼──────┐ ┌──▼──────┐
           │Smart Payment │ │Smart    │ │Order    │
           │Agent         │ │Fraud    │ │Agent    │
           │+ Claude/GPT  │ │Agent    │ │         │
           └──────────────┘ │+ LLM    │ └─────────┘
                           │Analysis │
                           └─────────┘
```

## 🚨 Troubleshooting

### No Dynamic Responses
- Check API keys: `echo $ANTHROPIC_API_KEY`
- Verify network connectivity to LLM APIs
- Check agent logs for API errors

### Agents Not Registering
```bash
# Check registry health
curl http://localhost:8000/health

# Re-register manually
python register_agents.py
```

### Demo Not Loading
- Ensure all 6 services are running
- Check browser console for connection errors
- Verify ports 8000-8005 are available

## 💡 Demo Tips

1. **Try Different Scenarios**: Each scenario showcases different agent capabilities
2. **Watch Traffic Panel**: See real LLM-generated responses in A2A messages
3. **Compare Runs**: Run the same scenario multiple times to see dynamic variations
4. **Monitor Latency**: LLM calls add realistic processing time
5. **Export Traffic**: Download real A2A communication logs for analysis

## 🔮 Next Steps

This smart A2A demo showcases:
- ✅ Real multi-agent orchestration with AI reasoning
- ✅ Dynamic problem-solving capabilities  
- ✅ Realistic business scenario handling
- ✅ Professional-grade A2A protocol compliance

Ready to see AI agents intelligently collaborate? **Start the demo!** 🚀 