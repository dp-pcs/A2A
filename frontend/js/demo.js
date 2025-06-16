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
            const response = await fetch('/api/incidents', {
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
                throw new Error(`Failed to create incident: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error creating incident:', error);
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
            { time: 2000, action: 'show_communication', from: 'orchestrator', to: 'payment-sys-001', message: 'Analyze transaction TXN-20241201-456789' },
            { time: 2500, action: 'show_communication', from: 'orchestrator', to: 'fraud-detect-001', message: 'Perform risk assessment for CORP-12345' },
            { time: 3000, action: 'show_communication', from: 'orchestrator', to: 'order-mgmt-001', message: 'Hold inventory for ORD-789123' },
            { time: 3500, action: 'show_communication', from: 'orchestrator', to: 'tech-support-001', message: 'Diagnose payment gateway issues' },
            
            { time: 8000, action: 'agent_progress', agent: 'payment-sys-001', progress: 45, message: 'Analyzing transaction patterns...' },
            { time: 10000, action: 'agent_progress', agent: 'fraud-detect-001', progress: 60, message: 'Verifying customer identity...' },
            { time: 12000, action: 'agent_progress', agent: 'order-mgmt-001', progress: 80, message: 'Inventory reserved for 45 minutes' },
            { time: 14000, action: 'agent_progress', agent: 'tech-support-001', progress: 70, message: 'Identified high latency in 3DS service' },
            
            { time: 18000, action: 'show_communication', from: 'fraud-detect-001', to: 'payment-sys-001', message: 'Risk assessment: LOW (0.15) - APPROVED' },
            { time: 20000, action: 'show_communication', from: 'tech-support-001', to: 'payment-sys-001', message: '3DS bypass approved for verified corporate customer' },
            
            { time: 25000, action: 'agent_complete', agent: 'fraud-detect-001', result: 'Customer verified - LOW risk (0.15)' },
            { time: 27000, action: 'agent_complete', agent: 'order-mgmt-001', result: 'Inventory secured - Hold expires in 45min' },
            { time: 29000, action: 'agent_complete', agent: 'tech-support-001', result: 'Gateway optimized - 3DS bypass enabled' },
            { time: 32000, action: 'agent_complete', agent: 'payment-sys-001', result: 'Payment retry successful - $49,999.99 processed' },
            
            { time: 35000, action: 'show_resolution', message: 'Incident resolved via coordinated agent response. Payment retry successful, inventory secured, customer notified.' }
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
            case 'show_communication':
                this.dashboard.showCommunication(event.from, event.to, event.message);
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: event.from,
                    message: `→ ${event.to}: ${event.message}`,
                    type: 'communication'
                });
                break;
                
            case 'agent_progress':
                this.dashboard.updateAgentProgress(event.agent, event.progress, event.message);
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: event.agent,
                    message: event.message,
                    type: 'progress'
                });
                break;
                
            case 'agent_complete':
                this.dashboard.updateAgentStatus(event.agent, 'completed');
                this.dashboard.addActivity({
                    timestamp: new Date(),
                    agent: event.agent,
                    message: `✓ ${event.result}`,
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

    async monitorIncidentProgress(incidentId) {
        // For real backend integration
        const maxAttempts = 30;
        let attempts = 0;
        
        while (attempts < maxAttempts && this.isRunning) {
            try {
                const response = await fetch(`/api/incidents/${incidentId}`);
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
                }
            } catch (error) {
                console.log('Backend not available, using simulation');
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