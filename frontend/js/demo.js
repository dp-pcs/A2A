class A2ADemoController {
    constructor() {
        this.currentIncident = null;
        this.demoScenarios = this.loadDemoScenarios();
        this.isRunning = false;
        this.dashboard = null;
    }

    loadDemoScenarios() {
        return {
            payment_failure: {
                name: "Payment Gateway Timeout",
                description: "Corporate customer payment failure during $50K order processing",
                customer: {
                    id: "CORP-12345",
                    name: "GlobalCorp Engineering",
                    type: "enterprise",
                    account_value: 2500000,
                    payment_history: "excellent"
                },
                order: {
                    id: "ORD-789123",
                    amount: 49999.99,
                    items: [
                        {
                            sku: "AI-COMPUTE-CLUSTER",
                            name: "High-Performance AI Compute Cluster",
                            quantity: 1,
                            unit_price: 49999.99
                        }
                    ],
                    currency: "USD"
                },
                failure_details: {
                    transaction_id: "TXN-20241201-456789",
                    error_code: "GATEWAY_TIMEOUT",
                    timestamp: new Date().toISOString(),
                    error_message: "3DS authentication service timeout",
                    payment_method: "corporate_card_ending_5678",
                    attempt_number: 1
                },
                deadline: new Date(Date.now() + 15 * 60 * 1000).toISOString() // 15 minutes
            },
            fraud_investigation: {
                name: "Suspicious Transaction Pattern",
                description: "Multiple high-value orders from new customer location",
                customer: {
                    id: "NEW-11111",
                    name: "TechStart Innovations",
                    type: "new_customer",
                    account_value: 0,
                    payment_history: "none"
                },
                order: {
                    id: "ORD-888777",
                    amount: 89999.99,
                    items: [
                        {
                            sku: "GPU-NVIDIA-A100",
                            name: "NVIDIA A100 GPU",
                            quantity: 3,
                            unit_price: 12999.99
                        },
                        {
                            sku: "SRV-DELL-R750", 
                            name: "Dell PowerEdge R750 Server",
                            quantity: 6,
                            unit_price: 8999.99
                        }
                    ],
                    currency: "USD"
                },
                failure_details: {
                    transaction_id: "TXN-20241201-555666",
                    error_code: "FRAUD_REVIEW_REQUIRED",
                    timestamp: new Date().toISOString(),
                    error_message: "Transaction requires manual fraud review",
                    risk_flags: ["high_velocity", "new_customer", "high_amount"],
                    ip_address: "203.0.113.99"
                }
            }
        };
    }

    async startDemo(scenarioName = 'payment_failure') {
        if (this.isRunning) {
            console.log('Demo already running');
            return;
        }

        this.isRunning = true;
        const scenario = this.demoScenarios[scenarioName];
        
        if (!scenario) {
            console.error('Unknown scenario:', scenarioName);
            return;
        }

        // Initialize dashboard if not already done
        if (!this.dashboard) {
            this.dashboard = new A2ADashboard();
            await this.dashboard.initialize();
        }

        console.log(`Starting A2A Demo: ${scenario.name}`);
        
        try {
            // Show scenario details
            this.displayScenarioInfo(scenario);
            
            // Create incident
            const incident = await this.createIncident(scenarioName, scenario);
            this.currentIncident = incident;
            
            // Monitor incident progress
            await this.monitorIncidentProgress(incident.incident_id);
            
        } catch (error) {
            console.error('Demo failed:', error);
            this.displayError(error);
        } finally {
            this.isRunning = false;
        }
    }

    displayScenarioInfo(scenario) {
        const scenarioCard = document.getElementById('scenario-info');
        if (scenarioCard) {
            scenarioCard.innerHTML = `
                <div class="scenario-header">
                    <h3>${scenario.name}</h3>
                    <p>${scenario.description}</p>
                </div>
                <div class="scenario-details">
                    <div class="customer-info">
                        <strong>Customer:</strong> ${scenario.customer.name} (${scenario.customer.id})
                    </div>
                    <div class="order-info">
                        <strong>Order:</strong> $${scenario.order.amount.toLocaleString()} - ${scenario.order.items.length} items
                    </div>
                    <div class="issue-info">
                        <strong>Issue:</strong> ${scenario.failure_details.error_message}
                    </div>
                </div>
            `;
        }
    }

    async createIncident(scenarioName, scenario) {
        try {
            // Call the orchestrator directly on port 8001
            const response = await fetch('http://localhost:8001/api/incidents', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    incident_type: scenarioName,
                    customer: scenario.customer,
                    order: scenario.order,
                    failure_details: scenario.failure_details,
                    deadline: scenario.deadline
                })
            });

            if (!response.ok) {
                console.log(`Orchestrator not available (${response.status}), falling back to simulation`);
                return this.createSimulatedIncident(scenarioName, scenario);
            }

            const result = await response.json();
            console.log('✅ Connected to real orchestrator:', result);
            return result;
        } catch (error) {
            console.log('🔄 Orchestrator not available, using simulation:', error.message);
            // Fallback to simulated incident for demo
            return this.createSimulatedIncident(scenarioName, scenario);
        }
    }

    createSimulatedIncident(scenarioName, scenario) {
        const incidentId = `incident-${Date.now()}`;
        
        // Simulate incident creation
        setTimeout(() => {
            if (this.dashboard) {
                this.dashboard.addAgent({
                    id: 'payment-sys-001',
                    name: 'Payment Systems',
                    status: 'analyzing',
                    position: { x: 200, y: 150 }
                });
                
                this.dashboard.addAgent({
                    id: 'fraud-detect-001', 
                    name: 'Fraud Detection',
                    status: 'analyzing',
                    position: { x: 400, y: 100 }
                });
                
                this.dashboard.addAgent({
                    id: 'order-mgmt-001',
                    name: 'Order Management', 
                    status: 'analyzing',
                    position: { x: 400, y: 200 }
                });
                
                this.dashboard.addAgent({
                    id: 'tech-support-001',
                    name: 'Tech Support',
                    status: 'analyzing', 
                    position: { x: 200, y: 250 }
                });

                // Start the coordination simulation
                this.simulateAgentCoordination();
            }
        }, 1000);

        return {
            incident_id: incidentId,
            status: 'created',
            message: 'Incident created and orchestration started'
        };
    }

    async simulateAgentCoordination() {
        const timeline = [
            // Initial Alert
            { time: 500, action: 'activity_alert', level: 'critical', message: '🚨 CRITICAL INCIDENT: $49,999.99 payment failure detected for enterprise customer GlobalCorp', detail: 'Transaction TXN-20241201-456789 failed due to 3DS authentication timeout. Automatic A2A orchestration initiated.' },
            
            // Orchestrator dispatches tasks
            { time: 2000, action: 'activity_alert', level: 'info', message: '🎯 Orchestrator analyzing incident and dispatching specialized agents', detail: 'Multi-agent coordination protocol activated. Identifying required skills: payment analysis, fraud assessment, inventory management, technical diagnostics.' },
            { time: 2200, action: 'show_communication', from: 'orchestrator', to: 'payment-sys-001', message: 'PRIORITY: Analyze failed transaction TXN-20241201-456789 - Corporate customer at risk' },
            { time: 2500, action: 'show_communication', from: 'orchestrator', to: 'fraud-detect-001', message: 'VERIFY: Risk assessment for CORP-12345 - $49K transaction requires validation' },
            { time: 3000, action: 'show_communication', from: 'orchestrator', to: 'order-mgmt-001', message: 'URGENT: Secure inventory hold for ORD-789123 - AI Compute Cluster (1 unit)' },
            { time: 3500, action: 'show_communication', from: 'orchestrator', to: 'tech-support-001', message: 'DIAGNOSE: Payment gateway latency issues affecting 3DS authentication' },
            
            // Agents start working
            { time: 5000, action: 'activity_alert', level: 'working', message: '🔍 Payment Agent: Deep-diving into Stripe gateway logs and transaction metadata', detail: 'Analyzing 35-second timeout against 30s threshold. Checking for patterns in recent 3DS failures for corporate accounts.' },
            { time: 6000, action: 'activity_alert', level: 'working', message: '🛡️  Fraud Agent: Cross-referencing customer profile against risk databases', detail: 'GlobalCorp has excellent payment history (2.5M account value). Validating IP geolocation and device fingerprinting for this $49K transaction.' },
            { time: 7000, action: 'activity_alert', level: 'working', message: '📦 Order Agent: Coordinating with inventory systems for critical hold placement', detail: 'AI Compute Cluster (SKU: AI-COMPUTE-CLUSTER) - Last unit in stock. Extending hold duration to 45 minutes given payment resolution in progress.' },
            { time: 8000, action: 'activity_alert', level: 'working', message: '🔧 Tech Agent: Running diagnostics on payment infrastructure performance', detail: 'Detected elevated latency in 3DS challenge service. Average response time: 32.8s (normal: 18s). Investigating root cause and bypass options.' },
            
            // Progress updates with technical details
            { time: 8000, action: 'agent_progress', agent: 'payment-sys-001', progress: 45, message: 'Identified 3DS timeout as root cause - analyzing retry strategies' },
            { time: 10000, action: 'agent_progress', agent: 'fraud-detect-001', progress: 60, message: 'Customer verification complete - Corporate account in good standing' },
            { time: 12000, action: 'agent_progress', agent: 'order-mgmt-001', progress: 80, message: 'Inventory hold secured - System reserved last available unit' },
            { time: 14000, action: 'agent_progress', agent: 'tech-support-001', progress: 70, message: 'Gateway diagnostics complete - 3DS bypass strategy identified' },
            
            // Agent-to-agent coordination
            { time: 16000, action: 'activity_alert', level: 'coordination', message: '🤝 Inter-agent coordination: Fraud → Payment', detail: 'Fraud Agent sharing risk assessment with Payment Agent. Customer cleared for bypass authentication due to verified corporate status and excellent payment history.' },
            { time: 18000, action: 'show_communication', from: 'fraud-detect-001', to: 'payment-sys-001', message: '✅ CLEARED: Risk score 0.15 (LOW) - Corporate customer verified, bypass approved' },
            { time: 19000, action: 'activity_alert', level: 'coordination', message: '🤝 Inter-agent coordination: Tech → Payment', detail: 'Tech Agent providing gateway optimization parameters to Payment Agent. 3DS bypass enabled for verified corporate accounts to prevent future timeouts.' },
            { time: 20000, action: 'show_communication', from: 'tech-support-001', to: 'payment-sys-001', message: '⚡ OPTIMIZED: 3DS bypass parameters configured - retry authorization granted' },
            
            // Resolution phase
            { time: 22000, action: 'activity_alert', level: 'success', message: '🎯 Payment Agent initiating retry with optimized parameters', detail: 'Using 3DS bypass for verified corporate customer. Expected success rate: 97%. Processing $49,999.99 charge with fraud clearance and gateway optimization.' },
            { time: 25000, action: 'agent_complete', agent: 'fraud-detect-001', result: '✅ Customer verification complete - Corporate account authenticated (Risk: 0.15)' },
            { time: 26000, action: 'activity_alert', level: 'success', message: '✅ Fraud Agent: Customer identity and transaction legitimacy confirmed', detail: 'GlobalCorp validated as enterprise customer with 2.5M account value. Transaction approved for processing with fraud clearance certificate.' },
            { time: 27000, action: 'agent_complete', agent: 'order-mgmt-001', result: '✅ Inventory secured and shipping expedited - Hold active for 45 minutes' },
            { time: 28000, action: 'activity_alert', level: 'success', message: '✅ Order Agent: Critical inventory secured and shipping prioritized', detail: 'Last AI Compute Cluster unit reserved. Expedited shipping arranged. Customer will receive tracking information within 2 hours of payment confirmation.' },
            { time: 29000, action: 'agent_complete', agent: 'tech-support-001', result: '✅ Gateway performance optimized - 3DS bypass enabled for corporate accounts' },
            { time: 30000, action: 'activity_alert', level: 'success', message: '✅ Tech Agent: Payment infrastructure optimized for future transactions', detail: 'Implemented corporate customer 3DS bypass. Average processing time reduced from 35s to 8s. Similar timeouts prevented for verified accounts.' },
            { time: 32000, action: 'agent_complete', agent: 'payment-sys-001', result: '✅ Payment successful - $49,999.99 processed via optimized gateway' },
            { time: 33000, action: 'activity_alert', level: 'resolved', message: '🎉 Payment Agent: Transaction successfully processed!', detail: 'Retry successful using optimized parameters. $49,999.99 charged to corporate card ending in 5678. Transaction ID: TXN-20241201-789456. Customer notification sent.' },
            
            { time: 35000, action: 'show_resolution', message: '🎯 INCIDENT RESOLVED: Multi-agent coordination successfully recovered $49,999.99 transaction. Customer satisfied, inventory secured, system optimized.' }
        ];

        for (const event of timeline) {
            setTimeout(() => {
                this.executeTimelineEvent(event);
            }, event.time);
        }
    }

    executeTimelineEvent(event) {
        if (!this.dashboard) return;

        switch (event.action) {
            case 'activity_alert':
                // New action for detailed, verbose activity alerts
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: 'system',
                    message: event.message,
                    detail: event.detail,
                    level: event.level,
                    type: event.level || 'info'
                });
                break;
                
            case 'show_communication':
                this.dashboard.showCommunication(event.from, event.to, event.message);
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: event.from,
                    message: `→ ${this.getAgentDisplayName(event.to)}: ${event.message}`,
                    type: 'communication'
                });
                break;
                
            case 'agent_progress':
                this.dashboard.updateAgentProgress(event.agent, event.progress, event.message);
                // Add working animation for obvious visual feedback
                this.dashboard.animateAgentWorking(event.agent);
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: event.agent,
                    message: `📊 ${event.message}`,
                    type: 'progress'
                });
                break;
                
            case 'agent_complete':
                this.dashboard.updateAgentStatus(event.agent, 'completed');
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: event.agent,
                    message: `${event.result}`,
                    type: 'completion'
                });
                break;
                
            case 'show_resolution':
                this.dashboard.showResolution(event.message);
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: 'orchestrator',
                    message: event.message,
                    type: 'resolution'
                });
                break;
        }
    }

    getAgentDisplayName(agentId) {
        const displayNames = {
            'payment-sys-001': 'Payment Agent',
            'fraud-detect-001': 'Fraud Agent',
            'order-mgmt-001': 'Order Agent',
            'tech-support-001': 'Tech Agent',
            'orchestrator': 'Orchestrator'
        };
        return displayNames[agentId] || agentId;
    }

    async monitorIncidentProgress(incidentId) {
        // For real backend integration
        const maxAttempts = 30;
        let attempts = 0;
        
        while (attempts < maxAttempts && this.isRunning) {
            try {
                // Call the orchestrator directly on port 8001
                const response = await fetch(`http://localhost:8001/api/incidents/${incidentId}`);
                if (response.ok) {
                    const incident = await response.json();
                    
                    if (incident.status === 'resolved') {
                        this.displayResolution(incident.resolution);
                        break;
                    } else if (incident.status === 'failed') {
                        this.displayError(incident.error);
                        break;
                    }
                    
                    // Update dashboard with real progress
                    this.updateDashboardFromIncident(incident);
                    console.log('📊 Real incident progress:', incident.status);
                }
            } catch (error) {
                console.log('🔄 Backend not available, using simulation');
                break;
            }
            
            attempts++;
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }

    updateDashboardFromIncident(incident) {
        if (!this.dashboard || !incident.tasks) return;
        
        Object.entries(incident.tasks).forEach(([taskName, task]) => {
            const agentId = task.agent_id;
            
            if (task.status === 'completed') {
                this.dashboard.updateAgentStatus(agentId, 'completed');
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: agentId,
                    message: `Task completed: ${task.skill_required}`,
                    type: 'completion'
                });
            } else if (task.status === 'executing') {
                this.dashboard.updateAgentStatus(agentId, 'working');
            }
        });
    }

    displayResolution(resolution) {
        if (this.dashboard) {
            this.dashboard.showResolution(resolution.summary);
        }
        
        const resolutionCard = document.getElementById('resolution-summary');
        if (resolutionCard) {
            resolutionCard.innerHTML = `
                <div class="resolution-success">
                    <h3>✓ Incident Resolved</h3>
                    <p>${resolution.summary}</p>
                    <div class="resolution-time">Total Resolution Time: ${resolution.total_resolution_time}</div>
                </div>
            `;
        }
    }

    displayError(error) {
        console.error('Demo error:', error);
        const errorCard = document.getElementById('error-display');
        if (errorCard) {
            errorCard.innerHTML = `
                <div class="error-message">
                    <h3>⚠ Demo Error</h3>
                    <p>${error}</p>
                </div>
            `;
        }
    }

    stopDemo() {
        this.isRunning = false;
        this.currentIncident = null;
        
        if (this.dashboard) {
            this.dashboard.reset();
        }
        
        console.log('Demo stopped');
    }

    getDemoStatus() {
        return {
            isRunning: this.isRunning,
            currentIncident: this.currentIncident,
            availableScenarios: Object.keys(this.demoScenarios)
        };
    }
}

// Make demo controller available globally
window.A2ADemoController = A2ADemoController; 