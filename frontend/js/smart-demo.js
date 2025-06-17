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
        
        // Clear any existing notifications
        document.querySelectorAll('.smart-response-notification').forEach(el => el.remove());
        
        // Simulate agent responses based on the selected scenario
        await this.simulateSmartAgentDemo(scenario);
    }
    
    async simulateSmartAgentDemo(scenario) {
        // Generate unique incident ID
        this.currentIncident = `smart-incident-${Date.now()}`;
        
        // Update UI
        document.getElementById('currentIncident').textContent = this.currentIncident;
        document.getElementById('incidentStatus').textContent = 'EXECUTING (Smart A2A)';
        document.getElementById('selectedScenarioDisplay').textContent = scenario.name;
        
        // Show analysis notice
        this.showAnalysisNotice(scenario);
        
        // Simulate progressive agent analysis with scenario-specific responses
        await this.simulateAgentCoordination(scenario);
    }
    
    async simulateAgentCoordination(scenario) {
        const expectedResponses = scenario.expected_ai_responses;
        const incidentData = scenario.incident_data;
        
        // Step 1: Initial incident registration
        await this.delay(500);
        this.addAgentMessage('orchestrator', 'system', 'incident_registered', {
            incident_id: this.currentIncident,
            customer: incidentData.customer.name,
            amount: incidentData.order.amount,
            issue: incidentData.failure_details.error_code
        });

        // Step 2: Payment Agent Analysis (scenario-specific)
        await this.delay(1500);
        const paymentAnalysis = this.generatePaymentAnalysis(scenario, expectedResponses.payment_agent);
        this.addAgentMessage('payment_agent', 'orchestrator', 'payment_analysis', paymentAnalysis);

        // Step 3: Fraud Agent Analysis (scenario-specific) 
        await this.delay(1200);
        const fraudAnalysis = this.generateFraudAnalysis(scenario, expectedResponses.fraud_agent);
        this.addAgentMessage('fraud_agent', 'orchestrator', 'fraud_assessment', fraudAnalysis);

        // Step 4: Order Agent Response
        await this.delay(800);
        const orderResponse = this.generateOrderResponse(scenario);
        this.addAgentMessage('order_agent', 'orchestrator', 'inventory_check', orderResponse);

        // Step 5: Final Coordination
        await this.delay(1000);
        const resolution = this.generateCoordinatedResolution(scenario, expectedResponses);
        this.addAgentMessage('orchestrator', 'system', 'incident_resolved', resolution);
        
        // Update status
        document.getElementById('incidentStatus').textContent = 'RESOLVED';
        
        // Hide analysis notice
        const notice = document.getElementById('analysis-notice');
        if (notice) notice.style.display = 'none';
    }
    
    generatePaymentAnalysis(scenario, expectedResponse) {
        const incidentData = scenario.incident_data;
        
        // Scenario-specific analysis
        switch (scenario.id) {
            case 'enterprise_3ds_timeout':
                return {
                    result: {
                        analysis: "3DS timeout indicates issuer service disruption. Enterprise customer with strong payment history.",
                        root_cause: expectedResponse.root_cause,
                        confidence: expectedResponse.confidence,
                        recommendation: "Retry with backup gateway and 3DS bypass for verified enterprise account",
                        success_probability: expectedResponse.success_probability,
                        technical_details: "Issuer authentication service unavailable for 45+ seconds"
                    }
                };
                
            case 'new_customer_high_value':
                return {
                    result: {
                        analysis: "New customer attempting high-value transaction. Legitimate but requires verification.",
                        root_cause: expectedResponse.root_cause,
                        confidence: expectedResponse.confidence,
                        recommendation: expectedResponse.strategy,
                        risk_factors: ["new_customer", "high_value", "startup_profile"]
                    }
                };
                
            case 'cascading_payment_failures':
                return {
                    result: {
                        analysis: "Velocity trigger from legitimate retry attempts. Customer showing urgency but good intent.",
                        root_cause: expectedResponse.root_cause,
                        confidence: expectedResponse.confidence,
                        recommendation: expectedResponse.strategy,
                        wait_time: expectedResponse.wait_time
                    }
                };
                
            default:
                return {
                    result: {
                        analysis: "Payment failure analysis completed",
                        confidence: 0.85,
                        recommendation: "Standard retry procedure"
                    }
                };
        }
    }
    
    generateFraudAnalysis(scenario, expectedResponse) {
        const incidentData = scenario.incident_data;
        
        // Scenario-specific fraud analysis
        switch (scenario.id) {
            case 'enterprise_3ds_timeout':
                return {
                    result: {
                        analysis: "Enterprise customer with established history. Very low fraud risk.",
                        risk_level: expectedResponse.risk_level,
                        confidence: expectedResponse.confidence,
                        recommendation: expectedResponse.recommendation,
                        risk_score: 0.15,
                        factors: ["established_customer", "consistent_patterns", "enterprise_tier", "regular_payments"]
                    }
                };
                
            case 'new_customer_high_value':
                return {
                    result: {
                        analysis: "New customer profile with high-value transaction requires enhanced verification.",
                        risk_level: expectedResponse.risk_level,
                        confidence: expectedResponse.confidence,
                        recommendation: expectedResponse.recommendation,
                        verification_steps: expectedResponse.verification_steps,
                        risk_score: 0.45
                    }
                };
                
            case 'cascading_payment_failures':
                return {
                    result: {
                        analysis: "Multiple retry attempts detected but pattern indicates legitimate customer urgency.",
                        risk_level: expectedResponse.risk_level,
                        confidence: expectedResponse.confidence,
                        recommendation: expectedResponse.recommendation,
                        pattern_analysis: expectedResponse.pattern_analysis,
                        risk_score: 0.25
                    }
                };
                
            default:
                return {
                    result: {
                        analysis: "Fraud assessment completed",
                        risk_level: "MEDIUM",
                        confidence: 0.80,
                        recommendation: "REVIEW"
                    }
                };
        }
    }
    
    generateOrderResponse(scenario) {
        const incidentData = scenario.incident_data;
        
        return {
            result: {
                analysis: `Inventory confirmed for ${incidentData.order.items[0].name}`,
                inventory_status: "AVAILABLE",
                hold_id: `HOLD-${this.currentIncident}`,
                priority_shipping: incidentData.customer.tier === 'enterprise',
                estimated_delivery: this.getEstimatedDelivery(incidentData.customer.tier)
            }
        };
    }
    
    generateCoordinatedResolution(scenario, expectedResponses) {
        const incidentData = scenario.incident_data;
        
        // Create resolution based on all agent inputs
        let resolutionStrategy = "Standard processing";
        let confidence = 0.85;
        
        switch (scenario.id) {
            case 'enterprise_3ds_timeout':
                resolutionStrategy = "Enterprise fast-track: 3DS bypass with enhanced monitoring";
                confidence = 0.94;
                break;
            case 'new_customer_high_value':
                resolutionStrategy = "Enhanced verification workflow with founder video call";
                confidence = 0.78;
                break;
            case 'cascading_payment_failures':
                resolutionStrategy = "Velocity exception granted with 15-minute delay";
                confidence = 0.89;
                break;
        }
        
        return {
            result: {
                resolution: resolutionStrategy,
                incident_id: this.currentIncident,
                status: "RESOLVED",
                confidence: confidence,
                coordinated_agents: 4,
                customer_impact: this.getCustomerImpact(scenario),
                business_value_preserved: incidentData.order.amount
            }
        };
    }
    
    getCustomerImpact(scenario) {
        switch (scenario.id) {
            case 'enterprise_3ds_timeout':
                return "Critical production training pipeline unblocked";
            case 'new_customer_high_value':
                return "New customer onboarded with proper verification";
            case 'cascading_payment_failures':
                return "Legitimate customer served despite velocity triggers";
            default:
                return "Customer issue resolved";
        }
    }
    
    getEstimatedDelivery(tier) {
        const days = tier === 'enterprise' ? 1 : tier === 'growth' ? 3 : 5;
        const deliveryDate = new Date();
        deliveryDate.setDate(deliveryDate.getDate() + days);
        return deliveryDate.toISOString().split('T')[0];
    }
    
    addAgentMessage(source, target, method, content) {
        const message = {
            id: `msg-${Date.now()}-${Math.random()}`,
            source_agent: source,
            target_agent: target,
            method: method,
            content: content,
            message_type: 'response',
            timestamp: new Date().toISOString(),
            displayTime: new Date().toLocaleTimeString(),
            latency_ms: 150 + Math.random() * 200 // Realistic latency
        };
        
        this.handleRealA2AMessage(message);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
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
        // Remove any existing smart response notifications first
        document.querySelectorAll('.smart-response-notification').forEach(el => el.remove());
        
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
        
        // Clear any existing notifications
        document.querySelectorAll('.smart-response-notification').forEach(el => el.remove());
        
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
}

// Initialize smart demo when page loads
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Initializing Smart A2A Demo with LLM-powered agents...');
    window.smartDemo = new SmartA2ADemo();
}); 