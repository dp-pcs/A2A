# A2A Protocol Demo System 🔄

**The Ultimate Interactive Demonstration of Agent-to-Agent Communication Protocols**

A comprehensive, interactive demonstration platform showcasing Google's Agent-to-Agent (A2A) protocol in action, now featuring the groundbreaking **Hybrid A2A + MCP Demo** that shows how horizontal agent coordination and vertical tool access work together.

## 🌟 Featured Demos

### 🎼 **NEW: Hybrid A2A + MCP Demo**
Experience the architectural symphony of two complementary protocols:
- **A2A (Horizontal)**: Agents coordinating with each other using JSON-RPC 2.0
- **MCP (Vertical)**: Agents accessing external knowledge sources and tools
- **Real-time visualization** of both protocols working together
- **Interactive tutorial mode** with step-by-step explanations
- **Live integration** with Trilogy AI knowledge base

### 🔄 **Technical A2A Demo**
Complete A2A protocol implementation with:
- Real-time HTTP traffic visualization
- JSON-RPC 2.0 message exchange
- Task Objects and Agent Cards
- SSE streaming infrastructure
- Multiple scenario support

### 🧠 **Smart Agent Demo**
Advanced LLM-powered agents with:
- Dynamic workflow generation
- Context-aware reasoning
- Multi-step problem solving
- Enhanced orchestration patterns

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/A2A.git
   cd A2A
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-a2a.txt
   ```

4. **Start the complete demo system**
   ```bash
   python start_complete_demo.py
   ```

5. **Open your browser**
   ```
   http://localhost:3000/
   ```

## 🌐 Public Deployment

Want to host this demo suite publicly? We've got you covered!

### 🚀 One-Click Deployments
- **Netlify** (Recommended): [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/your-username/A2A)
- **Vercel**: Deploy directly from your GitHub repo
- **AWS Amplify**: Connect your repository for automatic deployments

### 📖 Complete Deployment Guide
See **[DEPLOYMENT.md](DEPLOYMENT.md)** for comprehensive hosting instructions including:
- Step-by-step deployment for all major platforms
- Custom domain configuration
- Production optimization
- SEO and analytics setup
- Mobile optimization
- Integration with existing websites

### 🎯 Demo Modes
The demos work in two modes:
- **Local Mode**: Full backend services with real A2A traffic
- **Demo Mode**: Frontend-only with simulated responses (perfect for public hosting)

## 🎯 Demo Scenarios

### AI Integration Crisis Resolution
Watch as specialized AI diagnostic agents coordinate to resolve a critical MCP integration failure:
- **Integration Agent**: MCP protocol specialist
- **Protocol Agent**: Connection diagnostics expert  
- **System Agent**: Infrastructure health monitor
- **AI Agent**: Model performance analyst

The agents discover they need external knowledge, query the live Trilogy AI knowledge base via MCP, and apply expert guidance to resolve the crisis.

### Payment Processing Incident
See how agents handle complex payment failures requiring multi-system coordination:
- Real-time fraud analysis
- Payment gateway orchestration
- Customer communication management
- System health monitoring

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent A       │◄──►│   Orchestrator  │◄──►│   Agent B       │
│   (Port 8002)   │    │   (Port 8001)   │    │   (Port 8003)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Registry       │    │   Frontend      │    │  MCP Sources    │
│  (Port 8000)    │    │   (Port 3000)   │    │  (External)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 What You'll Learn

- **A2A Protocol Fundamentals**: Agent Cards, Task Objects, JSON-RPC 2.0
- **Multi-Agent Orchestration**: How agents coordinate complex workflows
- **Protocol Integration**: Combining A2A with MCP for enhanced capabilities
- **Real-time Communication**: SSE streaming and event-driven architecture
- **Production Patterns**: Scalable agent-to-agent communication designs

## 🛠️ Available Commands

### Quick Start Commands
```bash
python start_complete_demo.py      # Start everything (recommended)
python start_local.py             # Start basic A2A demo
python start_a2a_demo.py          # Start enhanced demo system
```

### Individual Services
```bash
python start_registry.py          # Agent registry (port 8000)
python start_orchestrator.py      # Central orchestrator (port 8001)
python start_payment_agent.py     # Payment processing agent (port 8002)
python start_fraud_agent.py       # Fraud detection agent (port 8003)
python start_order_agent.py       # Order management agent (port 8004)
python start_tech_agent.py        # Technical support agent (port 8005)
```

## 🎨 Features

### Interactive Demonstrations
- **Multiple demo modes**: Tutorial, slow, normal, fast
- **Real-time traffic visualization**: See every HTTP request and SSE event
- **Protocol explanations**: Learn what each message means
- **Graceful error handling**: Robust fallbacks for educational purposes

### Educational Content
- **Step-by-step tutorials**: Perfect for learning protocol fundamentals
- **Rich narratives**: Understand the "why" behind each protocol interaction
- **Multiple scenarios**: From simple coordination to complex crisis resolution
- **Live data integration**: Real knowledge sources enhance authenticity

### Production-Ready Components
- **Modular architecture**: Clean separation of concerns
- **Comprehensive logging**: Full audit trail of agent interactions
- **Error recovery**: Graceful handling of failures
- **Scalable design**: Ready for production deployment

## 📚 Documentation

- **[Quick Start Guide](QUICK_START_SMART_A2A.md)**: Get up and running in minutes
- **[System Design](SMART_A2A_SYSTEM_DESIGN.md)**: Deep dive into architecture
- **[Setup Instructions](SMART_A2A_SETUP.md)**: Detailed configuration guide
- **[Demo Guide](README_A2A_DEMO.md)**: Complete demo walkthrough

## 🤝 Contributing

We welcome contributions! This project demonstrates cutting-edge agent communication patterns and serves as a reference implementation for:

- Agent-to-Agent protocol research
- Multi-agent system education
- Production deployment patterns
- Protocol integration examples

## 📜 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Google** for the A2A Protocol specification
- **Anthropic** for Model Context Protocol (MCP)
- **Trilogy AI Center of Excellence** for knowledge integration examples

---

**Ready to explore the future of agent communication? Start the demo and see protocols in action!** 🚀

```bash
git clone https://github.com/your-username/A2A.git
cd A2A
python -m venv venv && source venv/bin/activate
pip install -r requirements-a2a.txt
python start_complete_demo.py
```

*Open `http://localhost:3000/` and begin your journey into agent-to-agent communication!* 