class SmartA2ADemo {
    constructor() {
        this.currentIncident = null;
        this.agents = {};
        this.messages = [];
        this.a2aTrafficStream = null;
        this.isConnected = false;
        this.orchestratorUrl = 'http://localhost:8001';
        
        // Load comprehensive demo scenarios
        this.demoScenarios = null;
        
        this.init();
    }
    
    async loadDemoScenarios() {
        try {
            const response = await fetch('/demo_scenarios.json');
            this.demoScenarios = await response.json();
            console.log('Loaded demo scenarios:', this.demoScenarios.scenarios.length);
        } catch (error) {
            console.error('Failed to load demo scenarios:', error);
            // Fallback to basic scenarios
            this.demoScenarios = { scenarios: [] };
        }
    }
    
    async init() {
        this.setupEventListeners();
        await this.loadDemoScenarios(); // Wait for scenarios to load
        this.renderScenarioSelector();
        this.initializeNetworkVisualization();
        this.connectToA2ATrafficStream();
    }
    
    setupEventListeners() {
        // Scenario selection
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('scenario-btn')) {
                const scenarioId = e.target.dataset.scenario;
                this.selectScenario(scenarioId);
            }
        });
        
        // Demo controls
        document.getElementById('startSmartDemo')?.addEventListener('click', () => this.startSelectedDemo());
        document.getElementById('resetDemo')?.addEventListener('click', () => this.resetDemo());
        document.getElementById('clearTraffic')?.addEventListener('click', () => this.clearTraffic());
    }
    
    renderScenarioSelector() {
        const container = document.getElementById('scenario-selector');
        if (!container) return;
        
        if (!this.demoScenarios || !this.demoScenarios.scenarios) {
            container.innerHTML = `
                <div class="scenario-header">
                    <h3>🎯 Loading Demo Scenarios...</h3>
                    <p>Please wait while we load the AI-powered demo scenarios.</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = `
            <div class="scenario-header">
                <h3>🎯 Smart A2A Demo Scenarios</h3>
                <p>Choose a scenario to see AI agents dynamically reason about complex business problems:</p>
            </div>
            <div class="scenario-grid">
                ${this.demoScenarios.scenarios.map((scenario) => `
                    <div class="scenario-card" data-scenario="${scenario.id}">
                        <div class="scenario-title">${scenario.name}</div>
                        <div class="scenario-description">${scenario.description}</div>
                        <div class="scenario-meta">
                            <span class="customer-tier tier-${scenario.incident_data.customer.tier}">
                                ${scenario.incident_data.customer.tier} Customer
                            </span>
                            <span class="amount">$${scenario.incident_data.order.amount.toLocaleString()}</span>
                        </div>
                        <div class="ai-features">
                            <small>🧠 AI Features: Dynamic reasoning, risk assessment, contextual responses</small>
                        </div>
                        <button class="scenario-btn" data-scenario="${scenario.id}">
                            Select Scenario
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    selectScenario(scenarioId) {
        this.selectedScenario = scenarioId;
        const scenario = this.demoScenarios.scenarios.find(s => s.id === scenarioId);
        
        if (!scenario) return;
        
        // Update UI to show selected scenario
        document.querySelectorAll('.scenario-card').forEach(card => {
            card.classList.remove('selected');
        });
        document.querySelector(`[data-scenario="${scenarioId}"]`).classList.add('selected');
        
        // Show scenario details
        this.displayScenarioDetails(scenario);
        
        // Enable start button
        const startBtn = document.getElementById('startSmartDemo');
        if (startBtn) {
            startBtn.disabled = false;
            startBtn.textContent = `Start ${scenario.name} Demo`;
        }
    }
    
    displayScenarioDetails(scenario) {
        const container = document.getElementById('scenario-details');
        if (!container) return;
        
        const data = scenario.incident_data;
        const expected = scenario.expected_ai_responses;
        
        container.innerHTML = `
            <div class="selected-scenario">
                <h4>📋 Selected Scenario: ${scenario.name}</h4>
                <div class="scenario-info">
                    <div class="info-section">
                        <strong>Customer:</strong> ${data.customer.name} (${data.customer.tier})
                    </div>
                    <div class="info-section">
                        <strong>Order:</strong> $${data.order.amount.toLocaleString()} - ${data.order.items[0].name}
                    </div>
                    <div class="info-section">
                        <strong>Issue:</strong> ${data.failure_details.error_code} - ${data.failure_details.gateway_response}
                    </div>
                    <div class="info-section">
                        <strong>Customer Tier:</strong> ${data.customer.tier} customer since ${data.customer.established_since}
                        <br><strong>Account Value:</strong> $${data.customer.account_value.toLocaleString()}
                    </div>
                    <div class="info-section">
                        <strong>Expected AI Behavior:</strong>
                        <div class="ai-expectations">
                            ${Object.entries(expected).map(([agent, response]) => `
                                <div class="agent-expectation">
                                    <strong>${this.getAgentDisplayName(agent)}:</strong> 
                                    ${response.recommendation || response.strategy || 'Dynamic analysis'}
                                    ${response.confidence ? ` (${(response.confidence * 100).toFixed(0)}% confidence)` : ''}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    async startSelectedDemo() {
        if (!this.selectedScenario) {
            alert('Please select a scenario first');
            return;
        }
        
        const scenario = this.demoScenarios.scenarios.find(s => s.id === this.selectedScenario);
        if (!scenario) {
            alert('Scenario not found');
            return;
        }
        
        console.log('Starting smart demo with scenario:', scenario.name);
        
        try {
            const response = await fetch(`${this.orchestratorUrl}/incidents`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(scenario.incident_data)
            });
            
            if (response.ok) {
                const result = await response.json();
                this.currentIncident = result.incident_id;
                
                console.log('Smart A2A incident created:', result);
                
                // Update UI
                document.getElementById('currentIncident').textContent = this.currentIncident;
                document.getElementById('incidentStatus').textContent = 'EXECUTING (Smart A2A)';
                document.getElementById('selectedScenarioDisplay').textContent = scenario.name;
                
                // Show analysis notice
                this.showAnalysisNotice(scenario);
                
                // Monitor incident progress
                this.monitorIncidentProgress();
                
            } else {
                console.error('Failed to create incident:', await response.text());
                alert('Failed to start demo. Make sure all A2A services are running.');
            }
            
        } catch (error) {
            console.error('Error starting smart demo:', error);
            alert('Failed to connect to orchestrator. Make sure services are running.');
        }
    }
    
    showAnalysisNotice(scenario) {
        const notice = document.getElementById('analysis-notice');
        if (notice) {
            notice.innerHTML = `
                <div class="analysis-alert">
                    <h4>🧠 AI Agents Analyzing...</h4>
                    <p>Smart agents are now using LLM reasoning to analyze the <strong>${scenario.name}</strong> scenario.</p>
                    <p>Watch the A2A traffic panel to see real agent-to-agent communication with dynamic responses!</p>
                    <div class="analysis-progress">
                        <div class="progress-bar"></div>
                    </div>
                </div>
            `;
            notice.style.display = 'block';
        }
    }
    
    connectToA2ATrafficStream() {
        console.log('Connecting to smart A2A traffic stream...');
        
        this.a2aTrafficStream = new EventSource(`${this.orchestratorUrl}/traffic/stream`);
        
        this.a2aTrafficStream.onopen = () => {
            console.log('Connected to smart A2A traffic stream');
            this.isConnected = true;
            this.updateConnectionStatus('connected');
        };
        
        this.a2aTrafficStream.addEventListener('a2a_traffic', (event) => {
            const message = JSON.parse(event.data);
            this.handleRealA2AMessage(message);
        });
        
        this.a2aTrafficStream.onerror = (error) => {
            console.error('A2A traffic stream error:', error);
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
        };
    }
    
    handleRealA2AMessage(message) {
        console.log('Smart A2A message received:', message);
        
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
        this.updateAgentActivity(message);
        
        // Highlight LLM-powered responses
        if (message.message_type === 'response' && message.content?.result) {
            this.highlightSmartResponse(message);
        }
    }
    
    highlightSmartResponse(message) {
        // Show a notification for AI-generated responses
        const notification = document.createElement('div');
        notification.className = 'smart-response-notification';
        notification.innerHTML = `
            <div class="notification-content">
                🧠 <strong>${this.getAgentDisplayName(message.source_agent)}</strong> 
                generated AI-powered analysis
                <div class="notification-details">
                    Method: ${message.method} | Latency: ${message.latency_ms?.toFixed(1)}ms
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 4 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 4000);
    }
    
    // ... (rest of the methods from the original dashboard)
    
    updateNetworkVisualization(message) {
        // Create agent nodes if they don't exist
        this.ensureAgentNode(message.source_agent);
        this.ensureAgentNode(message.target_agent);
        
        // Animate communication with special styling for LLM responses
        this.animateA2ACommunication(message.source_agent, message.target_agent, message);
    }
    
    getAgentDisplayName(agentId) {
        const displayNames = {
            'payment-sys-001': 'Smart Payment Systems',
            'fraud-detect-001': 'Smart Fraud Detection', 
            'order-mgmt-001': 'Order Management',
            'tech-support-001': 'Tech Support',
            'orchestrator-001': 'Orchestrator',
            'payment_agent': 'Smart Payment Agent',
            'fraud_agent': 'Smart Fraud Agent'
        };
        return displayNames[agentId] || agentId;
    }
    
    updateConnectionStatus(status) {
        const statusElement = document.getElementById('connectionStatus');
        if (statusElement) {
            statusElement.textContent = status === 'connected' ? 'Connected to Smart A2A Stream' : 'Disconnected';
            statusElement.className = `connection-status ${status}`;
        }
    }
    
    resetDemo() {
        this.currentIncident = null;
        this.selectedScenario = null;
        
        // Reset UI
        document.getElementById('currentIncident').textContent = 'None';
        document.getElementById('incidentStatus').textContent = 'READY';
        document.getElementById('selectedScenarioDisplay').textContent = 'None';
        
        // Hide analysis notice
        const notice = document.getElementById('analysis-notice');
        if (notice) notice.style.display = 'none';
        
        // Reset scenario selection
        document.querySelectorAll('.scenario-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Disable start button
        const startBtn = document.getElementById('startSmartDemo');
        if (startBtn) {
            startBtn.disabled = true;
            startBtn.textContent = 'Select Scenario First';
        }
        
        console.log('Smart demo reset');
    }
    
    clearTraffic() {
        this.messages = [];
        this.updateMessagesDisplay();
        this.updateAgentActivity();
        
        // Clear displays
        const containers = ['traffic-messages', 'agent-metrics', 'incident-progress'];
        containers.forEach(id => {
            const container = document.getElementById(id);
            if (container) {
                container.innerHTML = `<div style="text-align: center; color: #a0aec0; margin-top: 50px;">No data yet</div>`;
            }
        });
        
        console.log('Traffic cleared');
    }
    
    // Enhanced visualization methods
    initializeNetworkVisualization() {
        console.log('Initializing network visualization...');
        // Create a simple network display
        const networkContainer = document.getElementById('network-display');
        if (networkContainer) {
            networkContainer.innerHTML = `
                <div class="network-status">
                    <h4>🌐 Agent Network Status</h4>
                    <div class="agent-nodes">
                        <div class="agent-node smart-payment" id="payment-node">Payment Agent (AI)</div>
                        <div class="agent-node smart-fraud" id="fraud-node">Fraud Agent (AI)</div>
                        <div class="agent-node support" id="order-node">Order Agent</div>
                        <div class="agent-node support" id="tech-node">Tech Agent</div>
                        <div class="agent-node orchestrator" id="orchestrator-node">Orchestrator</div>
                    </div>
                </div>
            `;
        }
    }
    
    ensureAgentNode(agentId) {
        const node = document.getElementById(`${agentId.split('-')[0]}-node`);
        if (node) {
            node.classList.add('active');
        }
    }
    
    animateA2ACommunication(source, target, message) {
        console.log(`Communication: ${source} → ${target}`, message);
        this.ensureAgentNode(source);
        this.ensureAgentNode(target);
        
        // Show activity flash
        const sourceNode = document.getElementById(`${source.split('-')[0]}-node`);
        const targetNode = document.getElementById(`${target.split('-')[0]}-node`);
        
        if (sourceNode) {
            sourceNode.classList.add('transmitting');
            setTimeout(() => sourceNode.classList.remove('transmitting'), 1000);
        }
        if (targetNode) {
            targetNode.classList.add('receiving');
            setTimeout(() => targetNode.classList.remove('receiving'), 1000);
        }
    }
    
    updateMessagesDisplay() {
        const container = document.getElementById('traffic-messages');
        if (!container || this.messages.length === 0) return;
        
        container.innerHTML = `
            <h4>📡 Live A2A Traffic (${this.messages.length} messages)</h4>
            <div class="message-list">
                ${this.messages.slice(-10).map(msg => `
                    <div class="traffic-message ${msg.message_type}">
                        <div class="message-header">
                            <span class="agent-name">${this.getAgentDisplayName(msg.source_agent)}</span>
                            →
                            <span class="agent-name">${this.getAgentDisplayName(msg.target_agent)}</span>
                            <span class="message-time">${msg.displayTime}</span>
                        </div>
                        <div class="message-content">
                            <strong>${msg.method}</strong>
                            ${msg.content?.result ? this.formatAIResult(msg.content.result) : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    formatAIResult(result) {
        if (result?.confidence) {
            return `<div class="ai-insight">
                <span class="confidence">🧠 Confidence: ${(result.confidence * 100).toFixed(0)}%</span>
                ${result.root_cause ? `<br><strong>Root Cause:</strong> ${result.root_cause}` : ''}
                ${result.risk_level ? `<br><strong>Risk Level:</strong> ${result.risk_level}` : ''}
                ${result.recommendation ? `<br><strong>Recommendation:</strong> ${result.recommendation}` : ''}
            </div>`;
        }
        return '';
    }
    
    updateAgentActivity(message) {
        const container = document.getElementById('agent-metrics');
        if (!container) return;
        
        // Count activity by agent
        const activity = {};
        this.messages.forEach(msg => {
            activity[msg.source_agent] = (activity[msg.source_agent] || 0) + 1;
        });
        
        container.innerHTML = `
            <h4>📊 Agent Performance Metrics</h4>
            <div class="metrics-list">
                ${Object.entries(activity).map(([agent, count]) => `
                    <div class="metric-item">
                        <span class="agent-name">${this.getAgentDisplayName(agent)}</span>
                        <span class="activity-count">${count} actions</span>
                        <div class="activity-bar" style="width: ${Math.min(count * 20, 100)}%"></div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    async monitorIncidentProgress() {
        if (!this.currentIncident) return;
        
        // Poll incident status
        const checkProgress = async () => {
            try {
                const response = await fetch(`${this.orchestratorUrl}/incidents/${this.currentIncident}`);
                const incident = await response.json();
                
                this.displayIncidentProgress(incident);
                
                if (incident.status === 'resolved') {
                    this.displayResolution(incident);
                } else {
                    setTimeout(checkProgress, 2000); // Check again in 2 seconds
                }
            } catch (error) {
                console.error('Error checking incident progress:', error);
            }
        };
        
        setTimeout(checkProgress, 1000);
    }
    
    displayIncidentProgress(incident) {
        const container = document.getElementById('incident-progress');
        if (!container) return;
        
        const tasks = incident.tasks || {};
        const completedTasks = Object.values(tasks).filter(t => t.status === 'completed').length;
        const totalTasks = Object.keys(tasks).length;
        
        container.innerHTML = `
            <div class="progress-summary">
                <h4>🎯 Incident Progress: ${incident.incident_id}</h4>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: ${(completedTasks/totalTasks)*100}%"></div>
                    <span class="progress-text">${completedTasks}/${totalTasks} agents completed</span>
                </div>
                <div class="task-status">
                    ${Object.entries(tasks).map(([name, task]) => `
                        <div class="task-item ${task.status}">
                            <span class="task-name">${name.replace('_', ' ')}</span>
                            <span class="task-status">${task.status}</span>
                            ${task.result?.confidence ? `<span class="confidence">🧠 ${(task.result.confidence * 100).toFixed(0)}%</span>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    displayResolution(incident) {
        const notice = document.getElementById('analysis-notice');
        if (notice && incident.resolution) {
            const insights = incident.resolution.agent_insights || {};
            
            notice.innerHTML = `
                <div class="resolution-complete">
                    <h4>✅ AI Multi-Agent Analysis Complete!</h4>
                    <p><strong>Overall Confidence:</strong> ${(incident.resolution.confidence * 100).toFixed(0)}%</p>
                    <p><strong>Resolution:</strong> ${incident.resolution.summary}</p>
                    
                    <div class="ai-reasoning-breakdown">
                        <h5>🧠 What Each AI Agent Discovered:</h5>
                        
                        ${insights.payment ? this.formatPaymentInsight(insights.payment) : ''}
                        ${insights.fraud ? this.formatFraudInsight(insights.fraud) : ''}
                        ${insights.inventory ? this.formatInventoryInsight(insights.inventory) : ''}
                        ${insights.technical ? this.formatTechnicalInsight(insights.technical) : ''}
                        
                        <div class="coordinated-response">
                            <h6>🤝 Coordinated AI Response:</h6>
                            <p>All agents worked together to analyze this incident from multiple angles. 
                            ${this.generateCoordinatedSummary(insights)}</p>
                        </div>
                    </div>
                </div>
            `;
        }
    }
    
    formatPaymentInsight(insight) {
        // Handle nested structure: insight.result.result or insight.result or insight
        const result = insight.result?.result || insight.result || insight;
        const domainAssessment = result.domain_assessment || {};
        
        return `
            <div class="agent-reasoning payment-reasoning">
                <div class="agent-header">
                    <span class="agent-icon">💳</span>
                    <strong>Smart Payment Agent</strong>
                    <span class="confidence-badge">${(result.confidence * 100).toFixed(0)}% Confident</span>
                </div>
                <div class="reasoning-content">
                    ${domainAssessment.is_payment_related === false ? 
                        `<p><strong>🚨 Domain Assessment:</strong> Not a payment processing issue - deferred to ${domainAssessment.primary_responsible_team || 'appropriate'} team</p>
                         <p><strong>📝 Rationale:</strong> ${domainAssessment.rationale || 'Outside payment domain'}</p>` :
                        `<p><strong>🔍 What I Found:</strong> ${result.root_cause || 'Payment analysis completed'}</p>
                         <p><strong>💡 My Analysis:</strong> ${result.technical_analysis?.gateway_issue || result.technical_analysis?.authentication_status || 'Payment gateway functioning normally'}</p>
                         <p><strong>⚡ My Recommendation:</strong> ${result.strategy || result.recommendations?.[0]?.action || 'Standard processing'}</p>
                         <p><strong>🎯 Success Probability:</strong> ${result.recommendations?.[0]?.success_probability ? (result.recommendations[0].success_probability * 100).toFixed(0) + '%' : 'High'}</p>`
                    }
                </div>
            </div>
        `;
    }
    
    formatFraudInsight(insight) {
        // Handle nested structure: insight.result.result or insight.result or insight
        const result = insight.result?.result || insight.result || insight;
        const domainAssessment = result.domain_assessment || {};
        
        return `
            <div class="agent-reasoning fraud-reasoning">
                <div class="agent-header">
                    <span class="agent-icon">🛡️</span>
                    <strong>Smart Fraud Agent</strong>
                    <span class="confidence-badge">${(result.confidence * 100).toFixed(0)}% Confident</span>
                </div>
                <div class="reasoning-content">
                    ${domainAssessment.is_fraud_related === false ? 
                        `<p><strong>🚨 Domain Assessment:</strong> Not a fraud/security issue - deferred to ${domainAssessment.primary_responsible_team || 'appropriate'} team</p>
                         <p><strong>📝 Rationale:</strong> ${domainAssessment.rationale || 'Outside fraud/security domain'}</p>` :
                        `<p><strong>🔍 Risk Assessment:</strong> ${result.risk_level || 'UNKNOWN'} risk (score: ${(result.overall_risk_score || 0).toFixed(2)})</p>
                         <p><strong>🚨 Red Flags Found:</strong> ${result.fraud_indicators?.behavioral_anomalies?.join(', ') || result.fraud_indicators?.technical_red_flags?.join(', ') || 'None detected'}</p>
                         <p><strong>✅ Positive Signals:</strong> Customer is ${result.customer_analysis?.verification_status || 'verified'} with ${result.customer_analysis?.relationship_strength || 'standard'} relationship</p>
                         <p><strong>💡 My Recommendation:</strong> ${result.recommendation || 'REVIEW'} - ${result.recommendations?.[0]?.rationale || result.recommendations?.[0]?.action || 'Standard processing approved'}</p>`
                    }
                </div>
            </div>
        `;
    }
    
    formatInventoryInsight(insight) {
        // Handle nested structure: insight.result.result or insight.result or insight
        const result = insight.result?.result || insight.result || insight;
        return `
            <div class="agent-reasoning inventory-reasoning">
                <div class="agent-header">
                    <span class="agent-icon">📦</span>
                    <strong>Order Management Agent</strong>
                </div>
                <div class="reasoning-content">
                    <p><strong>📋 Action Taken:</strong> Secured inventory hold ${result.hold_id || 'HOLD-ACTIVE'}</p>
                    <p><strong>⏰ Hold Duration:</strong> Until ${result.expires_at ? new Date(result.expires_at).toLocaleString() : 'End of business day'}</p>
                    <p><strong>🚀 Shipping:</strong> ${result.expedited_shipping ? 'Expedited shipping enabled' : 'Standard shipping'}</p>
                </div>
            </div>
        `;
    }
    
    formatTechnicalInsight(insight) {
        // Handle nested structure: insight.result.result or insight.result or insight
        const result = insight.result?.result || insight.result || insight;
        const domainAssessment = result.domain_assessment || {};
        
        return `
            <div class="agent-reasoning technical-reasoning">
                <div class="agent-header">
                    <span class="agent-icon">🔧</span>
                    <strong>Smart Tech Support Agent</strong>
                    <span class="confidence-badge">${((result.confidence || 0.88) * 100).toFixed(0)}% Confident</span>
                </div>
                <div class="reasoning-content">
                    ${domainAssessment.is_technical_issue === false ? 
                        `<p><strong>🚨 Domain Assessment:</strong> Not a technical infrastructure issue - deferred to ${domainAssessment.primary_responsible_team || 'appropriate'} team</p>
                         <p><strong>📝 Rationale:</strong> ${domainAssessment.rationale || 'Outside technical infrastructure domain'}</p>` :
                        `<p><strong>🔍 Technical Analysis:</strong> ${result.diagnosis || 'System analysis completed'}</p>
                         <p><strong>📊 Business Impact:</strong> ${result.business_impact || 'Customer transaction processing affected'}</p>
                         <p><strong>⏱️ Resolution Timeline:</strong> ${result.timeline || '2-4 hours'}</p>
                         <p><strong>✅ Action Items:</strong> ${result.action_items ? result.action_items.slice(0,2).join(', ') : 'Monitor system performance closely'}</p>
                         <p><strong>🛡️ Prevention:</strong> ${result.preventive_measures ? result.preventive_measures.slice(0,2).join(', ') : 'Implement enhanced monitoring'}</p>`
                    }
                </div>
            </div>
        `;
    }
    
    generateCoordinatedSummary(insights) {
        // Handle nested structure: insight.result.result or insight.result or insight
        const hasPayment = insights.payment?.result?.result || insights.payment?.result || insights.payment;
        const hasFraud = insights.fraud?.result?.result || insights.fraud?.result || insights.fraud;
        
        if (hasPayment && hasFraud) {
            const paymentConf = hasPayment.confidence || 0.5;
            const fraudConf = hasFraud.confidence || 0.5;
            const riskLevel = hasFraud.risk_level || 'UNKNOWN';
            
            if (riskLevel === 'LOW' && paymentConf > 0.8) {
                return "Both payment and fraud agents agree this is a legitimate transaction with technical issues that can be resolved.";
            } else if (riskLevel === 'MEDIUM') {
                return "Payment agent identified technical issues while fraud agent flagged moderate risk - proceeding with enhanced verification.";
            } else if (riskLevel === 'HIGH') {
                return "Fraud agent detected high risk factors - payment processing halted pending additional verification.";
            }
        }
        
        return "Agents coordinated their analysis to provide comprehensive incident resolution.";
    }
}

// Initialize smart demo when page loads
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Initializing Smart A2A Demo with LLM-powered agents...');
    window.smartDemo = new SmartA2ADemo();
}); 