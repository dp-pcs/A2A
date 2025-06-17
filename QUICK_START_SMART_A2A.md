# Quick Start - Smart A2A Demo
## AI-Powered Customer Service Agents with LLM Integration

### Prerequisites
1. **API Keys** - You have three LLM API keys configured in `.env`
2. **Python Environment** - Virtual environment activated
3. **Dependencies** - All packages installed

### ✅ Current Status
Your system now has:
- ✅ LLM-powered smart agents with dynamic reasoning
- ✅ 3 comprehensive demo scenarios with expected AI behaviors
- ✅ Smart frontend with AI response visualization  
- ✅ Fallback handling if API keys unavailable
- ✅ Support for Anthropic, OpenAI, and Gemini APIs

### 🚀 Quick Start (5 minutes)

#### Step 1: Test Your Smart Agents
```bash
python test_smart_agents.py
```
This validates your API keys and tests AI agent reasoning.

#### Step 2: Start Core Services
```bash
# Terminal 1 - Agent Registry
python start_registry.py

# Terminal 2 - Smart Payment Agent  
python start_smart_payment_agent.py

# Terminal 3 - Smart Fraud Agent
python start_smart_fraud_agent.py

# Terminal 4 - Orchestrator
python start_orchestrator.py
```

#### Step 3: Open Smart Demo UI
Open `frontend/smart-demo.html` in your browser

### 🎯 Demo Scenarios

#### Scenario 1: "Enterprise Payment Timeout with 3DS Challenge"
- **Customer**: GlobalCorp ($50,000 GPU cluster)
- **Issue**: 3DS authentication timeout
- **Expected AI**: Smart bypass recommendation with risk assessment
- **Key Feature**: Enterprise customer recognition

#### Scenario 2: "Suspicious High-Value Transaction from New Customer"  
- **Customer**: StartupAI ($75,000 infrastructure)
- **Issue**: New customer triggering fraud alerts
- **Expected AI**: Enhanced verification workflow
- **Key Feature**: Balanced security vs. customer experience

#### Scenario 3: "Complex Payment Failure Chain"
- **Customer**: TechStartup ($25,000 expansion)
- **Issue**: Cascading failures with velocity triggers
- **Expected AI**: Root cause analysis and intelligent retry
- **Key Feature**: Complex pattern recognition

### 🧠 What to Watch For

#### AI-Powered Responses
- **Confidence Scores**: Agents provide confidence levels (0.8-0.95)
- **Dynamic Reasoning**: Responses adapt to customer context
- **Rich Artifacts**: Detailed analysis reports generated
- **Cross-Agent Coordination**: Agents collaborate and reach consensus

#### Smart Features
- **Customer Tier Recognition**: Different handling for Enterprise vs Growth customers
- **Risk Assessment**: Sophisticated fraud scoring with behavioral analysis
- **Contextual Strategies**: Recommendations based on customer history and business impact
- **Fallback Handling**: Graceful degradation if LLM APIs unavailable

### 📊 Expected Results

#### Payment Agent AI Output Example:
```json
{
  "root_cause": "3DS authentication timeout due to gateway latency",
  "confidence": 0.87,
  "retry_recommended": true,
  "strategy": "3ds_bypass_with_enhanced_monitoring",
  "success_probability": 0.94
}
```

#### Fraud Agent AI Output Example:
```json
{
  "risk_level": "LOW",
  "confidence": 0.92,
  "recommendation": "APPROVE",
  "customer_analysis": {
    "legitimacy_score": 0.96,
    "verification_status": "verified"
  }
}
```

### 🔧 Troubleshooting

#### No AI Responses?
1. Check `.env` file formatting
2. Verify API keys are valid
3. Check terminal for error messages
4. Agents will fallback to rule-based responses

#### Frontend Not Loading Scenarios?
1. Ensure `demo_scenarios.json` is in root directory
2. Check browser console for errors
3. Verify all services are running

#### Agents Not Registering?
1. Start registry first
2. Wait 2-3 seconds between starting agents
3. Check port conflicts (8000-8005)

### 💡 Demo Tips

1. **Start with Scenario 1** - Clearest demonstration of AI reasoning
2. **Watch Network Traffic** - Real-time A2A communication with AI responses
3. **Compare Confidence Scores** - Notice how agents express uncertainty
4. **Try Without API Keys** - See graceful fallback behavior
5. **Check Agent Logs** - See detailed AI reasoning in terminal output

### 🎉 Success Indicators

- ✅ Smart agents show "Found API key" on startup
- ✅ Scenarios load in frontend with AI expectations
- ✅ Incident creation triggers multiple agents  
- ✅ Agents return structured JSON with confidence scores
- ✅ Frontend displays AI reasoning and recommendations
- ✅ Cross-agent responses show intelligent coordination

**Your Smart A2A system is now ready for demonstration! 🚀** 