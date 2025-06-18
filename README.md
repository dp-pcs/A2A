# 🔄 A2A Protocol Demo Suite

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/dp-pcs/A2A)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **The ultimate interactive demonstration of Agent-to-Agent communication protocols**

A comprehensive, educational platform showcasing Google's A2A protocol with real-time visualizations, interactive tutorials, and the groundbreaking **Hybrid A2A + MCP Demo** showing how agent coordination and tool access work together.

## ✨ What Makes This Special

🎼 **First-ever A2A + MCP integration demo** - See horizontal agent coordination meet vertical tool access  
🔍 **Real protocol traffic** - Watch actual JSON-RPC 2.0 messages and SSE streams  
🎓 **Interactive tutorials** - Step-by-step learning with floating controls  
🌐 **Production ready** - Deploy anywhere, works with or without backend  
📱 **Mobile optimized** - Responsive design for all devices  

## 🚀 Quick Start (60 seconds)

```bash
# Clone and start
git clone https://github.com/dp-pcs/A2A.git
cd A2A
python -m venv venv && source venv/bin/activate
pip install -r requirements-a2a.txt
python start_complete_demo.py

# Open browser to http://localhost:3000
```

That's it! 🎉

## 🎯 Demo Suite Overview

### 🧠 Smart A2A Demo
**Perfect for business audiences** - See the value of agent coordination
- AI-powered decision making
- Dynamic workflow orchestration  
- Customer-specific solutions
- Business impact demonstration

### 🔧 A2A Technical Demo  
**Perfect for developers** - Deep dive into protocol mechanics
- Real-time HTTP traffic visualization
- JSON-RPC 2.0 message exchange
- Task Objects and Agent Cards
- SSE streaming infrastructure
- Interactive tutorial mode

### 🌐 A2A + MCP Hybrid Demo ⭐
**Perfect for AI architects** - See the future of AI integration
- Horizontal agent coordination (A2A)
- Vertical tool access (MCP)  
- Live knowledge integration
- Dual protocol visualization
- Crisis resolution + Research orchestration scenarios

## 📖 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[Quick Start Guide](docs/QUICK_START.md)** | Get running in minutes | Everyone |
| **[Deployment Guide](DEPLOYMENT.md)** | Host publicly | DevOps |
| **[System Architecture](docs/ARCHITECTURE.md)** | Technical deep dive | Developers |
| **[API Reference](docs/API.md)** | Integration guide | Integrators |

## 🏗️ Repository Structure

```
A2A/
├── 📁 frontend/              # Demo web applications
│   ├── index.html           # Main demo selector
│   ├── smart-demo.html      # Business value demo
│   ├── technical-demo.html  # Protocol technical demo
│   ├── hybrid-demo.html     # A2A + MCP integration
│   └── js/                  # JavaScript modules
├── 📁 backend/              # A2A protocol implementation
│   ├── agents/              # Individual agent services
│   ├── orchestrator/        # Central coordination
│   ├── agent_registry/      # Service discovery
│   └── shared/              # Common utilities
├── 📁 scripts/              # Start/utility scripts
├── 📁 docs/                 # Comprehensive documentation
├── 📁 examples/             # Integration examples
└── 📁 deploy/               # Deployment configurations
```

## 🎮 Usage Modes

### 🖥️ Local Development (Full Experience)
```bash
python start_complete_demo.py
```
- Real A2A protocol traffic
- Live agent coordination
- Backend services running
- Perfect for learning protocol internals

### 🌐 Demo Mode (Frontend Only)
```bash
cd frontend && python -m http.server 3000
```
- Simulated protocol responses
- All demos fully functional
- No backend required
- Perfect for presentations

### 🚀 Production Deployment
See **[DEPLOYMENT.md](DEPLOYMENT.md)** for hosting options:
- Netlify (recommended)
- Vercel
- AWS Amplify
- GitHub Pages

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# For enhanced AI responses (optional)
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# For MCP integration (optional)
export MCP_SERVER_URL="your-mcp-server"
```

### Customization
- **Scenarios**: Edit `demo_scenarios.json`
- **Agents**: Modify files in `backend/agents/`
- **UI**: Customize `frontend/` files
- **Deployment**: Update `netlify.toml` or create `amplify.yml`

## 🎓 Learning Path

1. **Start with Smart Demo** - Understand business value
2. **Explore Technical Demo** - Learn protocol mechanics
3. **Try Hybrid Demo** - See integration possibilities
4. **Read Documentation** - Deep dive into architecture
5. **Experiment with Code** - Modify and extend

## 🤝 Contributing

We welcome contributions! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for:

- Development setup
- Code standards
- Pull request process
- Feature requests

### Quick Contribution Guide
```bash
# Fork repo, then:
git clone https://github.com/your-username/A2A.git
cd A2A
python -m venv venv && source venv/bin/activate
pip install -r requirements-a2a.txt
# Make changes, test, submit PR
```

## 📋 What You'll Learn

- **A2A Protocol Fundamentals** - Agent Cards, Task Objects, JSON-RPC 2.0
- **Multi-Agent Orchestration** - Coordinated workflows and decision making
- **Protocol Integration** - Combining A2A with MCP for enhanced capabilities  
- **Real-time Communication** - SSE streaming and event-driven patterns
- **Production Patterns** - Scalable agent coordination architectures

## 🔧 Troubleshooting

### Common Issues

**Port already in use?**
```bash
# Kill existing processes
pkill -f "python.*start_"
# Or use different ports in scripts
```

**Demos not loading?**
```bash
# Check if frontend server is running
curl http://localhost:3000
# Restart if needed
cd frontend && python -m http.server 3000
```

**Backend not responding?**
```bash
# Check services
curl http://localhost:8000/.well-known/agents
# Restart complete demo
python start_complete_demo.py
```

Need help? [Open an issue](https://github.com/dp-pcs/A2A/issues) 🆘

## 📊 Features

✅ **Multiple Demo Types** - Business, technical, and integration focused  
✅ **Real Protocol Implementation** - Authentic A2A and MCP protocols  
✅ **Interactive Tutorials** - Step-by-step learning with controls  
✅ **Production Ready** - Deploy anywhere with graceful fallbacks  
✅ **Mobile Optimized** - Works on all devices  
✅ **Comprehensive Docs** - Guides for every use case  
✅ **Open Source** - MIT licensed, fork and customize  

## 🙏 Acknowledgments

- **Google** - A2A Protocol specification
- **Anthropic** - Model Context Protocol (MCP)  
- **Trilogy AI Center of Excellence** - Knowledge integration examples
- **Open Source Community** - Inspiration and best practices

## 📜 License

This project is licensed under the MIT License - see the **[LICENSE](LICENSE)** file for details.

## ⭐ Star This Repo

If this helped you understand agent coordination protocols, please star this repository! It helps others discover this educational resource.

---

**Ready to explore the future of agent communication?** 🚀

```bash
git clone https://github.com/dp-pcs/A2A.git && cd A2A && python start_complete_demo.py
```

*Open http://localhost:3000 and start your journey!* 