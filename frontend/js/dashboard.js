class A2ADashboard {
    constructor() {
        this.currentIncident = null;
        this.agents = {};
        this.messages = [];
        this.networkVisualization = null;
        this.a2aTrafficStream = null;
        this.isConnected = false;
        
        // Real orchestrator URL
        this.orchestratorUrl = 'http://localhost:8001';
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeNetworkVisualization();
        this.connectToA2ATrafficStream();
        this.loadRecentTraffic();
    }
    
    setupEventListeners() {
        // Demo controls
        document.getElementById('startDemo').addEventListener('click', () => this.startRealDemo());
        document.getElementById('resetDemo').addEventListener('click', () => this.resetDemo());
        
        // Traffic controls
        document.getElementById('clearTraffic').addEventListener('click', () => this.clearTraffic());
        document.getElementById('exportTraffic').addEventListener('click', () => this.exportTraffic());
    }
    
    connectToA2ATrafficStream() {
        console.log('Connecting to real A2A traffic stream...');
        
        this.a2aTrafficStream = new EventSource(`${this.orchestratorUrl}/traffic/stream`);
        
        this.a2aTrafficStream.onopen = () => {
            console.log('Connected to A2A traffic stream');
            this.isConnected = true;
            this.updateConnectionStatus('connected');
        };
        
        this.a2aTrafficStream.addEventListener('a2a_traffic', (event) => {
            const message = JSON.parse(event.data);
            this.handleRealA2AMessage(message);
        });
        
        this.a2aTrafficStream.addEventListener('keepalive', (event) => {
            // Handle keepalive messages
            console.log('A2A stream keepalive received');
        });
        
        this.a2aTrafficStream.onerror = (error) => {
            console.error('A2A traffic stream error:', error);
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
            
            // Attempt to reconnect after 5 seconds
            setTimeout(() => {
                if (!this.isConnected) {
                    this.connectToA2ATrafficStream();
                }
            }, 5000);
        };
        
        this.a2aTrafficStream.onclose = () => {
            console.log('A2A traffic stream closed');
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
        };
    }
    
    async loadRecentTraffic() {
        try {
            const response = await fetch(`${this.orchestratorUrl}/traffic/recent`);
            if (response.ok) {
                const data = await response.json();
                const recentMessages = data.traffic || [];
                
                // Process recent messages
                recentMessages.forEach(message => {
                    this.handleRealA2AMessage(message);
                });
                
                console.log(`Loaded ${recentMessages.length} recent A2A messages`);
            }
        } catch (error) {
            console.error('Failed to load recent traffic:', error);
        }
    }
    
    handleRealA2AMessage(message) {
        console.log('Real A2A message received:', message);
        
        // Add to messages list
        this.messages.push({
            ...message,
            id: `msg-${Date.now()}-${Math.random()}`,
            displayTime: new Date(message.timestamp).toLocaleTimeString()
        });
        
        // Keep only last 100 messages
        if (this.messages.length > 100) {
            this.messages = this.messages.slice(-100);
        }
        
        // Update visualizations
        this.updateNetworkVisualization(message);
        this.updateMessagesDisplay();
        this.updateAgentStatus(message);
        
        // Play notification sound for important messages
        if (message.message_type === 'request' || message.message_type === 'response') {
            this.playNotificationSound();
        }
    }
    
    updateNetworkVisualization(message) {
        const networkContainer = document.getElementById('network-visualization');
        
        // Create agent nodes if they don't exist
        this.ensureAgentNode(message.source_agent);
        this.ensureAgentNode(message.target_agent);
        
        // Animate communication between agents
        this.animateA2ACommunication(message.source_agent, message.target_agent, message);
        
        // Update network stats
        this.updateNetworkStats();
    }
    
    ensureAgentNode(agentId) {
        if (!this.agents[agentId]) {
            this.agents[agentId] = {
                id: agentId,
                name: this.getAgentDisplayName(agentId),
                status: 'active',
                messageCount: 0,
                lastActivity: new Date().toISOString(),
                skills: this.getAgentSkills(agentId)
            };
            
            this.renderAgentNode(agentId);
        }
    }
    
    getAgentDisplayName(agentId) {
        const displayNames = {
            'payment-sys-001': 'Payment Systems',
            'fraud-detect-001': 'Fraud Detection',
            'order-mgmt-001': 'Order Management',
            'tech-support-001': 'Tech Support',
            'orchestrator-001': 'Orchestrator'
        };
        return displayNames[agentId] || agentId;
    }
    
    getAgentSkills(agentId) {
        const skillMap = {
            'payment-sys-001': ['transaction-analysis', 'payment-retry', 'gateway-diagnostics'],
            'fraud-detect-001': ['risk-assessment', 'fraud-detection', 'customer-verification'],
            'order-mgmt-001': ['inventory-hold', 'order-processing', 'shipping-coordination'],
            'tech-support-001': ['system-diagnostics', 'performance-analysis', 'incident-resolution'],
            'orchestrator-001': ['task-orchestration', 'incident-management']
        };
        return skillMap[agentId] || [];
    }
    
    renderAgentNode(agentId) {
        const agent = this.agents[agentId];
        const networkContainer = document.getElementById('network-visualization');
        
        // Create agent element
        const agentElement = document.createElement('div');
        agentElement.className = 'agent-node';
        agentElement.id = `agent-${agentId}`;
        agentElement.innerHTML = `
            <div class="agent-icon">🤖</div>
            <div class="agent-name">${agent.name}</div>
            <div class="agent-status ${agent.status}"></div>
            <div class="agent-stats">
                <small>Messages: <span class="message-count">0</span></small>
            </div>
        `;
        
        // Position agents in a circle
        const agents = Object.keys(this.agents);
        const index = agents.indexOf(agentId);
        const total = agents.length;
        const angle = (index / total) * 2 * Math.PI;
        const radius = 120;
        const centerX = 150;
        const centerY = 150;
        
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        
        agentElement.style.left = `${x}px`;
        agentElement.style.top = `${y}px`;
        
        networkContainer.appendChild(agentElement);
    }
    
    animateA2ACommunication(sourceId, targetId, message) {
        const sourceElement = document.getElementById(`agent-${sourceId}`);
        const targetElement = document.getElementById(`agent-${targetId}`);
        
        if (!sourceElement || !targetElement) return;
        
        // Create message animation
        const messageElement = document.createElement('div');
        messageElement.className = `message-animation ${message.message_type}`;
        messageElement.innerHTML = `
            <div class="message-bubble">
                <small>${message.method || message.message_type}</small>
                ${message.latency_ms ? `<br><small>${message.latency_ms.toFixed(1)}ms</small>` : ''}
            </div>
        `;
        
        // Position at source
        const sourceRect = sourceElement.getBoundingClientRect();
        const targetRect = targetElement.getBoundingClientRect();
        const containerRect = document.getElementById('network-visualization').getBoundingClientRect();
        
        const startX = sourceRect.left - containerRect.left + sourceRect.width / 2;
        const startY = sourceRect.top - containerRect.top + sourceRect.height / 2;
        const endX = targetRect.left - containerRect.left + targetRect.width / 2;
        const endY = targetRect.top - containerRect.top + targetRect.height / 2;
        
        messageElement.style.left = `${startX}px`;
        messageElement.style.top = `${startY}px`;
        
        document.getElementById('network-visualization').appendChild(messageElement);
        
        // Animate to target
        setTimeout(() => {
            messageElement.style.transform = `translate(${endX - startX}px, ${endY - startY}px)`;
            messageElement.style.opacity = '0';
        }, 100);
        
        // Remove after animation
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 2000);
        
        // Update agent activity
        this.updateAgentActivity(sourceId);
        this.updateAgentActivity(targetId);
    }
    
    updateAgentActivity(agentId) {
        if (this.agents[agentId]) {
            this.agents[agentId].messageCount++;
            this.agents[agentId].lastActivity = new Date().toISOString();
            
            // Update UI
            const agentElement = document.getElementById(`agent-${agentId}`);
            if (agentElement) {
                const countElement = agentElement.querySelector('.message-count');
                if (countElement) {
                    countElement.textContent = this.agents[agentId].messageCount;
                }
                
                // Add pulse animation
                agentElement.classList.add('pulse');
                setTimeout(() => agentElement.classList.remove('pulse'), 1000);
            }
        }
    }
    
    updateMessagesDisplay() {
        const messagesContainer = document.getElementById('messages-container');
        
        // Show last 20 messages
        const recentMessages = this.messages.slice(-20);
        
        messagesContainer.innerHTML = recentMessages.map(msg => `
            <div class="message-item ${msg.message_type}">
                <div class="message-header">
                    <span class="message-time">${msg.displayTime}</span>
                    <span class="message-type">${msg.message_type.toUpperCase()}</span>
                    ${msg.latency_ms ? `<span class="message-latency">${msg.latency_ms.toFixed(1)}ms</span>` : ''}
                </div>
                <div class="message-route">
                    <strong>${this.getAgentDisplayName(msg.source_agent)}</strong> 
                    → 
                    <strong>${this.getAgentDisplayName(msg.target_agent)}</strong>
                </div>
                <div class="message-method">${msg.method || 'system'}</div>
                <div class="message-content">
                    <pre>${JSON.stringify(msg.content, null, 2)}</pre>
                </div>
            </div>
        `).join('');
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    updateNetworkStats() {
        document.getElementById('totalMessages').textContent = this.messages.length;
        document.getElementById('activeAgents').textContent = Object.keys(this.agents).length;
        
        // Calculate average latency
        const latencies = this.messages
            .filter(msg => msg.latency_ms)
            .map(msg => msg.latency_ms);
            
        if (latencies.length > 0) {
            const avgLatency = latencies.reduce((sum, lat) => sum + lat, 0) / latencies.length;
            document.getElementById('avgLatency').textContent = `${avgLatency.toFixed(1)}ms`;
        }
        
        // Recent activity
        const recentMessages = this.messages.filter(msg => 
            new Date() - new Date(msg.timestamp) < 60000 // Last minute
        );
        document.getElementById('recentActivity').textContent = recentMessages.length;
    }
    
    updateConnectionStatus(status) {
        const statusElement = document.getElementById('connectionStatus');
        statusElement.textContent = status === 'connected' ? 'Connected to A2A Stream' : 'Disconnected';
        statusElement.className = `connection-status ${status}`;
    }
    
    async startRealDemo() {
        console.log('Starting real A2A demo...');
        
        // Create a real incident
        const incident = {
            incident_type: "payment_failure",
            customer: {
                id: "globalcorp",
                name: "GlobalCorp Enterprise",
                tier: "enterprise",
                contact: "procurement@globalcorp.com"
            },
            order: {
                id: "ORD-20241201-001",
                amount: 50000,
                currency: "USD",
                items: [
                    {
                        id: "ai-cluster-v100",
                        name: "AI Computing Cluster - V100 GPUs",
                        quantity: 8,
                        unit_price: 6250
                    }
                ]
            },
            failure_details: {
                transaction_id: "TXN-20241201-001",
                error_code: "GATEWAY_TIMEOUT",
                timestamp: new Date().toISOString(),
                gateway_response: "3DS authentication timeout after 30 seconds"
            },
            deadline: new Date(Date.now() + 3600000).toISOString() // 1 hour from now
        };
        
        try {
            const response = await fetch(`${this.orchestratorUrl}/incidents`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(incident)
            });
            
            if (response.ok) {
                const result = await response.json();
                this.currentIncident = result.incident_id;
                
                console.log('Real incident created:', result);
                
                // Update UI
                document.getElementById('currentIncident').textContent = this.currentIncident;
                document.getElementById('incidentStatus').textContent = 'EXECUTING (Real A2A)';
                
                // Monitor incident progress
                this.monitorIncidentProgress();
                
            } else {
                console.error('Failed to create incident:', await response.text());
                alert('Failed to start demo. Make sure all A2A services are running.');
            }
            
        } catch (error) {
            console.error('Error starting demo:', error);
            alert('Failed to connect to orchestrator. Make sure services are running on localhost:8001');
        }
    }
    
    async monitorIncidentProgress() {
        if (!this.currentIncident) return;
        
        const checkProgress = async () => {
            try {
                const response = await fetch(`${this.orchestratorUrl}/incidents/${this.currentIncident}`);
                if (response.ok) {
                    const incident = await response.json();
                    
                    // Update incident status
                    document.getElementById('incidentStatus').textContent = 
                        `${incident.status.toUpperCase()} (Real A2A)`;
                    
                    // Update progress details if available
                    if (incident.tasks) {
                        this.updateTaskProgress(incident.tasks);
                    }
                    
                    // Continue monitoring if not completed
                    if (!['resolved', 'failed'].includes(incident.status)) {
                        setTimeout(checkProgress, 2000);
                    } else {
                        console.log('Incident resolved:', incident);
                        if (incident.resolution) {
                            this.displayResolution(incident.resolution);
                        }
                    }
                }
            } catch (error) {
                console.error('Error monitoring incident:', error);
            }
        };
        
        checkProgress();
    }
    
    updateTaskProgress(tasks) {
        const taskContainer = document.getElementById('taskProgress');
        if (!taskContainer) return;
        
        const taskHtml = Object.entries(tasks).map(([taskName, task]) => `
            <div class="task-item ${task.status}">
                <div class="task-name">${taskName.replace('_', ' ').toUpperCase()}</div>
                <div class="task-agent">${this.getAgentDisplayName(task.agent_id)}</div>
                <div class="task-status">${task.status.toUpperCase()}</div>
            </div>
        `).join('');
        
        taskContainer.innerHTML = taskHtml;
    }
    
    displayResolution(resolution) {
        const resolutionContainer = document.getElementById('resolutionDetails');
        if (!resolutionContainer) return;
        
        resolutionContainer.innerHTML = `
            <h3>Resolution: ${resolution.status.toUpperCase()}</h3>
            <p><strong>Strategy:</strong> ${resolution.resolution_strategy}</p>
            <p><strong>Summary:</strong> ${resolution.summary}</p>
            <div class="actions-taken">
                <h4>Actions Taken:</h4>
                ${resolution.actions_taken.map(action => `
                    <div class="action-item">
                        <strong>${action.action}:</strong> ${action.details || action.diagnosis || 'Completed'}
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    resetDemo() {
        this.currentIncident = null;
        document.getElementById('currentIncident').textContent = 'None';
        document.getElementById('incidentStatus').textContent = 'READY';
        
        // Clear task progress
        const taskContainer = document.getElementById('taskProgress');
        if (taskContainer) taskContainer.innerHTML = '';
        
        // Clear resolution
        const resolutionContainer = document.getElementById('resolutionDetails');
        if (resolutionContainer) resolutionContainer.innerHTML = '';
        
        console.log('Demo reset');
    }
    
    clearTraffic() {
        this.messages = [];
        this.updateMessagesDisplay();
        this.updateNetworkStats();
        console.log('Traffic cleared');
    }
    
    exportTraffic() {
        const exportData = {
            export_time: new Date().toISOString(),
            total_messages: this.messages.length,
            agents: this.agents,
            messages: this.messages
        };
        
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `a2a-traffic-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('Traffic exported');
    }
    
    playNotificationSound() {
        // Create a subtle notification sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.1);
    }
    
    initializeNetworkVisualization() {
        const networkContainer = document.getElementById('network-visualization');
        networkContainer.innerHTML = '';
        
        // Add network background grid
        const gridSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        gridSvg.className = 'network-grid';
        gridSvg.style.position = 'absolute';
        gridSvg.style.top = '0';
        gridSvg.style.left = '0';
        gridSvg.style.width = '100%';
        gridSvg.style.height = '100%';
        gridSvg.style.zIndex = '1';
        
        networkContainer.appendChild(gridSvg);
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing A2A Dashboard with real traffic monitoring...');
    window.dashboard = new A2ADashboard();
}); 