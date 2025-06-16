class A2ADashboard {
    constructor() {
        this.API_BASE = 'https://api.latentgenius.ai';
        this.demoRunning = false;
        this.startTime = null;
        this.progressChart = null;
        this.currentStep = 0;
        this.artifactsGenerated = 0;
        
        this.simulationSteps = [
            {
                time: 1000,
                activity: 'A2A Protocol initialized',
                type: 'system'
            },
            {
                time: 2000,
                activity: 'Agent discovery completed - 4 agents found',
                type: 'discovery'
            },
            {
                time: 3000,
                activity: 'Master task created: incident-20250616-001',
                type: 'orchestration'
            },
            {
                time: 4000,
                agent: 'payment',
                progress: 25,
                status: 'Working',
                activity: 'Payment Systems Agent: Retrieving transaction logs...',
                messageTarget: 'orchestrator'
            },
            {
                time: 5000,
                agent: 'fraud',
                progress: 30,
                status: 'Working',
                activity: 'Fraud Detection Agent: Verifying customer identity...',
                messageTarget: 'orchestrator'
            },
            {
                time: 13000,
                agent: 'order',
                progress: 100,
                status: 'Completed',
                activity: 'Order Management Agent: Inventory hold confirmed',
                artifact: {
                    name: 'Inventory Hold Confirmation',
                    type: 'JSON',
                    description: 'Hold ID: HOLD-789123'
                }
            },
            {
                time: 26000,
                agent: 'payment',
                progress: 100,
                status: 'Completed',
                activity: 'Payment Systems Agent: Analysis complete',
                artifact: {
                    name: 'Payment Analysis Report',
                    type: 'JSON',
                    description: 'Root cause: 3DS timeout'
                }
            },
            {
                time: 31000,
                activity: 'RESOLUTION COMPLETE: Payment retry successful',
                resolution: true,
                type: 'success'
            }
        ];
        
        this.init();
    }
    
    init() {
        this.initProgressChart();
        this.setupEventListeners();
    }
    
    initProgressChart() {
        const ctx = document.getElementById('progressChart').getContext('2d');
        this.progressChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Remaining'],
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ['#10B981', '#E5E7EB'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                cutout: '70%'
            }
        });
    }
    
    setupEventListeners() {
        document.getElementById('start-demo-btn').addEventListener('click', () => {
            this.startDemo();
        });
        
        document.getElementById('reset-demo-btn').addEventListener('click', () => {
            this.resetDemo();
        });
    }
    
    startDemo() {
        if (this.demoRunning) return;
        
        this.demoRunning = true;
        this.startTime = Date.now();
        this.currentStep = 0;
        this.artifactsGenerated = 0;
        
        document.getElementById('start-demo-btn').style.display = 'none';
        document.getElementById('reset-demo-btn').style.display = 'block';
        
        document.getElementById('active-agents').textContent = '4';
        document.getElementById('tasks-created').textContent = '4';
        
        this.clearFeed();
        this.runSimulation();
        this.startTimers();
    }
    
    runSimulation() {
        if (this.currentStep < this.simulationSteps.length && this.demoRunning) {
            const step = this.simulationSteps[this.currentStep];
            
            setTimeout(() => {
                if (!this.demoRunning) return;
                
                if (step.agent) {
                    this.updateProgress(step.agent, step.progress, step.status);
                }
                
                this.addActivity(step.activity);
                
                if (step.artifact) {
                    this.addArtifact(step.artifact);
                }
                
                if (step.resolution) {
                    this.showResolution();
                }
                
                this.updateOverallProgress();
                this.currentStep++;
                this.runSimulation();
            }, step.time);
        }
    }
    
    updateProgress(agent, progress, status) {
        const agentCard = document.querySelector(`[data-agent="${agent}"]`);
        if (agentCard) {
            const progressBar = agentCard.querySelector('.progress-bar');
            const progressText = agentCard.querySelector('.progress-text');
            const statusBadge = agentCard.querySelector('.status-badge');
            
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `${progress}%`;
            
            if (status === 'Completed') {
                statusBadge.textContent = 'Completed';
                statusBadge.className = 'bg-green-100 text-green-800 px-2 py-1 rounded text-xs status-badge';
            } else if (status === 'Working') {
                statusBadge.textContent = 'Working';
                statusBadge.className = 'bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs status-badge';
            }
        }
    }
    
    addActivity(activity) {
        const feed = document.getElementById('activity-feed');
        const activityItem = document.createElement('div');
        activityItem.className = 'flex items-start space-x-3';
        
        const timestamp = new Date().toTimeString().slice(0, 8);
        const color = this.getActivityColor(activity);
        
        activityItem.innerHTML = `
            <div class="w-2 h-2 ${color} rounded-full mt-2 animate-pulse"></div>
            <div>
                <p class="text-sm text-gray-900">${activity}</p>
                <p class="text-xs text-gray-500">${timestamp}</p>
            </div>
        `;
        
        feed.appendChild(activityItem);
        feed.scrollTop = feed.scrollHeight;
    }
    
    getActivityColor(activity) {
        if (activity.includes('Payment')) return 'bg-blue-500';
        if (activity.includes('Fraud')) return 'bg-green-500';
        if (activity.includes('Order')) return 'bg-purple-500';
        if (activity.includes('Tech')) return 'bg-orange-500';
        if (activity.includes('RESOLUTION')) return 'bg-green-600';
        return 'bg-gray-500';
    }
    
    addArtifact(artifact) {
        const artifactsList = document.getElementById('artifacts-list');
        
        const placeholder = artifactsList.querySelector('.text-center');
        if (placeholder) {
            placeholder.remove();
        }
        
        const artifactItem = document.createElement('div');
        artifactItem.className = 'border rounded-lg p-3 bg-gray-50';
        artifactItem.innerHTML = `
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <i class="fas fa-file-alt text-blue-600 mr-2"></i>
                    <div>
                        <h4 class="font-medium text-gray-900">${artifact.name}</h4>
                        <p class="text-sm text-gray-600">${artifact.description}</p>
                    </div>
                </div>
                <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">${artifact.type}</span>
            </div>
        `;
        
        artifactsList.appendChild(artifactItem);
        
        this.artifactsGenerated++;
        document.getElementById('artifacts-count').textContent = this.artifactsGenerated;
    }
    
    showResolution() {
        const incidentPanel = document.getElementById('incident-panel');
        incidentPanel.className = 'bg-green-50 border border-green-200 rounded-lg p-6 mb-6';
        
        const incidentStatus = document.getElementById('incident-status');
        incidentStatus.textContent = 'RESOLVED';
        incidentStatus.className = 'bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium';
        
        const title = incidentPanel.querySelector('h2');
        title.innerHTML = '<i class="fas fa-check-circle text-green-600 text-xl mr-3"></i>Incident Resolved: Payment Processing Restored';
        title.className = 'text-xl font-semibold text-green-800';
    }
    
    updateOverallProgress() {
        const progressPercentage = Math.round((this.currentStep / this.simulationSteps.length) * 100);
        this.progressChart.data.datasets[0].data = [progressPercentage, 100 - progressPercentage];
        this.progressChart.update();
    }
    
    startTimers() {
        this.timerInterval = setInterval(() => {
            if (!this.demoRunning) return;
            
            const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            
            document.getElementById('elapsed-time').textContent = 
                `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    
    clearFeed() {
        document.getElementById('activity-feed').innerHTML = '';
        document.getElementById('artifacts-list').innerHTML = '';
    }
    
    resetDemo() {
        this.demoRunning = false;
        this.currentStep = 0;
        this.artifactsGenerated = 0;
        
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        
        document.getElementById('start-demo-btn').style.display = 'block';
        document.getElementById('reset-demo-btn').style.display = 'none';
        
        // Reset all UI elements
        this.resetUI();
    }
    
    resetUI() {
        // Reset incident panel
        const incidentPanel = document.getElementById('incident-panel');
        incidentPanel.className = 'bg-red-50 border border-red-200 rounded-lg p-6 mb-6';
        
        // Reset counters and feeds
        document.getElementById('elapsed-time').textContent = '0:00';
        document.getElementById('active-agents').textContent = '0';
        document.getElementById('tasks-created').textContent = '0';
        document.getElementById('artifacts-count').textContent = '0';
        
        // Reset progress chart
        this.progressChart.data.datasets[0].data = [0, 100];
        this.progressChart.update();
        
        // Reset agent cards
        document.querySelectorAll('.agent-card').forEach(card => {
            const progressBar = card.querySelector('.progress-bar');
            const progressText = card.querySelector('.progress-text');
            const statusBadge = card.querySelector('.status-badge');
            
            progressBar.style.width = '0%';
            progressText.textContent = '0%';
            statusBadge.textContent = 'Idle';
            statusBadge.className = 'bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs status-badge';
        });
        
        // Reset feeds
        document.getElementById('activity-feed').innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-play-circle text-4xl mb-2"></i>
                <p>Click "Start A2A Demo" to begin agent orchestration</p>
            </div>
        `;
        
        document.getElementById('artifacts-list').innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-file-alt text-4xl mb-2"></i>
                <p>Artifacts will appear here as agents complete their tasks</p>
            </div>
        `;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new A2ADashboard();
}); 