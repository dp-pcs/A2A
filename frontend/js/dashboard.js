class A2ADashboard {
    constructor() {
        this.agents = new Map();
        this.connections = new Map();
        this.messageId = 0;
        this.isInitialized = false;
        this.progressChart = null;
        this.startTime = null;
        this.timerInterval = null;
        this.artifactsGenerated = 0;
    }

    async initialize() {
        if (this.isInitialized) return;
        
        this.initProgressChart();
        this.initNetworkVisualization();
        this.isInitialized = true;
        
        // Add the orchestrator to the center
        this.addOrchestrator();
    }

    initProgressChart() {
        const ctx = document.getElementById('progressChart');
        if (!ctx) return;
        
        this.progressChart = new Chart(ctx.getContext('2d'), {
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

    initNetworkVisualization() {
        // Clear existing network content and start fresh
        const networkSvg = document.querySelector('#agent-network svg');
        if (networkSvg) {
            // Clear all dynamic content but keep the base structure
            const messageGroup = networkSvg.querySelector('#message-bubbles') || this.createMessageGroup(networkSvg);
            const animationGroup = networkSvg.querySelector('#animation-layer') || this.createAnimationGroup(networkSvg);
            
            messageGroup.innerHTML = '';
            animationGroup.innerHTML = '';
        }
    }

    createMessageGroup(svg) {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.id = 'message-bubbles';
        svg.appendChild(group);
        return group;
    }

    createAnimationGroup(svg) {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.id = 'animation-layer';
        svg.appendChild(group);
        return group;
    }

    addOrchestrator() {
        const orchestrator = {
            id: 'orchestrator',
            name: 'Orchestrator',
            status: 'active',
            position: { x: 400, y: 125 }
        };
        this.agents.set('orchestrator', orchestrator);
    }

    addAgent(agentConfig) {
        this.agents.set(agentConfig.id, {
            ...agentConfig,
            progress: 0,
            status: agentConfig.status || 'idle'
        });

        // Update the corresponding agent card in the UI
        this.updateAgentCard(agentConfig.id, agentConfig.status);
        this.animateAgentActivation(agentConfig.id);
    }

    updateAgentCard(agentId, status) {
        // Map agent IDs to the card data attributes
        const agentCardMapping = {
            'payment-sys-001': 'payment',
            'fraud-detect-001': 'fraud',
            'order-mgmt-001': 'order',
            'tech-support-001': 'tech'
        };

        const cardId = agentCardMapping[agentId];
        if (!cardId) return;

        const agentCard = document.querySelector(`[data-agent="${cardId}"]`);
        if (!agentCard) return;

        const statusBadge = agentCard.querySelector('.status-badge');
        const statusClasses = {
            'idle': 'bg-gray-100 text-gray-800',
            'analyzing': 'bg-blue-100 text-blue-800',
            'working': 'bg-blue-100 text-blue-800',
            'completed': 'bg-green-100 text-green-800'
        };

        if (statusBadge) {
            statusBadge.textContent = status.charAt(0).toUpperCase() + status.slice(1);
            statusBadge.className = `${statusClasses[status] || statusClasses.idle} px-2 py-1 rounded text-xs status-badge`;
        }
    }

    updateAgentProgress(agentId, progress, message) {
        if (this.agents.has(agentId)) {
            this.agents.get(agentId).progress = progress;
        }

        // Update the progress bar in the agent card
        const agentCardMapping = {
            'payment-sys-001': 'payment',
            'fraud-detect-001': 'fraud', 
            'order-mgmt-001': 'order',
            'tech-support-001': 'tech'
        };

        const cardId = agentCardMapping[agentId];
        if (!cardId) return;

        const agentCard = document.querySelector(`[data-agent="${cardId}"]`);
        if (!agentCard) return;

        const progressBar = agentCard.querySelector('.progress-bar');
        const progressText = agentCard.querySelector('.progress-text');

        if (progressBar && progressText) {
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `${progress}%`;
            
            // Add smooth transition
            progressBar.style.transition = 'width 0.5s ease-in-out';
        }
    }

    updateAgentStatus(agentId, status) {
        if (this.agents.has(agentId)) {
            this.agents.get(agentId).status = status;
        }

        this.updateAgentCard(agentId, status);
        
        if (status === 'completed') {
            this.animateAgentCompletion(agentId);
        }
    }

    showCommunication(fromId, toId, message) {
        this.animateMessage(fromId, toId, message);
        this.flashConnection(fromId, toId);
    }

    animateMessage(fromId, toId, message) {
        const svg = document.querySelector('#agent-network svg');
        if (!svg) return;

        let messageGroup = svg.querySelector('#message-bubbles');
        if (!messageGroup) {
            messageGroup = this.createMessageGroup(svg);
        }

        // Get positions for the message path
        const fromPos = this.getAgentPosition(fromId);
        const toPos = this.getAgentPosition(toId);
        
        if (!fromPos || !toPos) return;

        // Create message bubble
        const messageId = `msg-${this.messageId++}`;
        const messageElement = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        messageElement.id = messageId;

        // Create message background
        const messageBg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        messageBg.setAttribute('r', '8');
        messageBg.setAttribute('fill', '#3B82F6');
        messageBg.setAttribute('stroke', '#1E40AF');
        messageBg.setAttribute('stroke-width', '1');

        messageElement.appendChild(messageBg);
        messageGroup.appendChild(messageElement);

        // Animate message travel
        const animateX = document.createElementNS('http://www.w3.org/2000/svg', 'animateTransform');
        animateX.setAttribute('attributeName', 'transform');
        animateX.setAttribute('type', 'translate');
        animateX.setAttribute('values', `${fromPos.x},${fromPos.y}; ${toPos.x},${toPos.y}`);
        animateX.setAttribute('dur', '1.5s');
        animateX.setAttribute('fill', 'freeze');

        messageElement.appendChild(animateX);

        // Remove message after animation
        setTimeout(() => {
            if (messageElement && messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 2000);
    }

    flashConnection(fromId, toId) {
        const lineId = this.getConnectionLineId(fromId, toId);
        const line = document.getElementById(lineId);
        
        if (line) {
            // Store original attributes
            const originalStroke = line.getAttribute('stroke');
            const originalWidth = line.getAttribute('stroke-width');
            
            // Flash effect
            line.setAttribute('stroke', '#3B82F6');
            line.setAttribute('stroke-width', '3');
            line.style.opacity = '1';
            
            setTimeout(() => {
                line.setAttribute('stroke', originalStroke);
                line.setAttribute('stroke-width', originalWidth);
                line.style.opacity = '0.6';
            }, 800);
        }
    }

    animateAgentActivation(agentId) {
        const agentElement = document.getElementById(this.getAgentElementId(agentId));
        if (!agentElement) return;

        const circle = agentElement.querySelector('circle');
        if (circle) {
            // Add pulsing animation
            circle.style.animation = 'pulse 2s infinite';
        }
    }

    animateAgentCompletion(agentId) {
        const agentElement = document.getElementById(this.getAgentElementId(agentId));
        if (!agentElement) return;

        const circle = agentElement.querySelector('circle');
        if (circle) {
            // Change to success color and add checkmark effect
            circle.setAttribute('fill', '#10B981');
            circle.setAttribute('stroke', '#059669');
            circle.style.animation = 'none';
            
            // Brief flash effect
            setTimeout(() => {
                circle.style.filter = 'brightness(1.3)';
                setTimeout(() => {
                    circle.style.filter = 'brightness(1)';
                }, 300);
            }, 100);
        }
    }

    getAgentPosition(agentId) {
        const positions = {
            'orchestrator': { x: 400, y: 125 },
            'payment-sys-001': { x: 200, y: 60 },
            'fraud-detect-001': { x: 600, y: 60 },
            'order-mgmt-001': { x: 200, y: 190 },
            'tech-support-001': { x: 600, y: 190 }
        };
        return positions[agentId];
    }

    getAgentElementId(agentId) {
        const elementIds = {
            'orchestrator': 'orchestrator',
            'payment-sys-001': 'payment-agent',
            'fraud-detect-001': 'fraud-agent',
            'order-mgmt-001': 'order-agent',
            'tech-support-001': 'tech-agent'
        };
        return elementIds[agentId];
    }

    getConnectionLineId(fromId, toId) {
        // Map to the connection line IDs in the SVG
        const connections = {
            'orchestrator-payment-sys-001': 'line-orch-payment',
            'orchestrator-fraud-detect-001': 'line-orch-fraud',
            'orchestrator-order-mgmt-001': 'line-orch-order',
            'orchestrator-tech-support-001': 'line-orch-tech',
            'fraud-detect-001-payment-sys-001': 'line-payment-fraud',
            'tech-support-001-payment-sys-001': 'line-order-tech'
        };
        
        const key1 = `${fromId}-${toId}`;
        const key2 = `${toId}-${fromId}`;
        
        return connections[key1] || connections[key2];
    }

    addActivity(activity) {
        const feed = document.getElementById('activity-feed');
        if (!feed) return;

        // Remove placeholder if it exists
        const placeholder = feed.querySelector('.text-center');
        if (placeholder) {
            placeholder.remove();
        }

        const activityItem = document.createElement('div');
        activityItem.className = 'flex items-start space-x-3 animate-fadeIn';
        
        const timestamp = new Date().toLocaleTimeString();
        const color = this.getActivityColor(activity.type || 'info');
        
        activityItem.innerHTML = `
            <div class="w-2 h-2 ${color} rounded-full mt-2 animate-pulse"></div>
            <div class="flex-1">
                <p class="text-sm text-gray-900">${activity.message}</p>
                <p class="text-xs text-gray-500">${timestamp}</p>
            </div>
        `;
        
        feed.appendChild(activityItem);
        feed.scrollTop = feed.scrollHeight;
    }

    getActivityColor(type) {
        const colors = {
            'communication': 'bg-blue-500',
            'progress': 'bg-indigo-500',
            'completion': 'bg-green-500',
            'resolution': 'bg-green-600',
            'info': 'bg-gray-500'
        };
        return colors[type] || colors.info;
    }

    showResolution(message) {
        // Update incident panel to resolved state
        const incidentPanel = document.getElementById('incident-panel');
        if (incidentPanel) {
            incidentPanel.className = 'bg-green-50 border border-green-200 rounded-lg p-6 mb-6';
            
            const statusBadge = document.getElementById('incident-status');
            if (statusBadge) {
                statusBadge.textContent = 'RESOLVED';
                statusBadge.className = 'bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium';
            }
            
            const title = incidentPanel.querySelector('h2');
            if (title) {
                title.innerHTML = '<i class="fas fa-check-circle text-green-600 text-xl mr-3"></i>Incident Resolved: Payment Processing Restored';
                title.className = 'text-xl font-semibold text-green-800';
            }
        }

        // Show resolution summary
        const resolutionDiv = document.getElementById('resolution-summary');
        if (resolutionDiv) {
            resolutionDiv.innerHTML = `
                <div class="resolution-success">
                    <h3 class="text-lg font-semibold text-green-800 mb-2">✓ Incident Resolved</h3>
                    <p class="text-green-700">${message}</p>
                    <div class="mt-3 text-sm text-green-600">
                        All agents coordinated successfully to resolve the incident.
                    </div>
                </div>
            `;
            resolutionDiv.style.display = 'block';
        }
    }

    reset() {
        // Clear agents
        this.agents.clear();
        this.messageId = 0;
        this.artifactsGenerated = 0;

        // Reset timers
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }

        // Reset network visualization
        this.initNetworkVisualization();
        this.addOrchestrator();

        // Reset agent cards
        document.querySelectorAll('.agent-card').forEach(card => {
            const progressBar = card.querySelector('.progress-bar');
            const progressText = card.querySelector('.progress-text');
            const statusBadge = card.querySelector('.status-badge');
            
            if (progressBar) progressBar.style.width = '0%';
            if (progressText) progressText.textContent = '0%';
            if (statusBadge) {
                statusBadge.textContent = 'Idle';
                statusBadge.className = 'bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs status-badge';
            }
        });

        // Reset SVG agent colors
        document.querySelectorAll('#agent-network circle').forEach(circle => {
            const parentId = circle.parentElement.id;
            const originalColors = {
                'orchestrator': '#3B82F6',
                'payment-agent': '#EF4444',
                'fraud-agent': '#10B981',
                'order-agent': '#8B5CF6',
                'tech-agent': '#F59E0B'
            };
            if (originalColors[parentId]) {
                circle.setAttribute('fill', originalColors[parentId]);
                circle.style.animation = 'none';
                circle.style.filter = 'none';
            }
        });

        // Reset progress chart
        if (this.progressChart) {
            this.progressChart.data.datasets[0].data = [0, 100];
            this.progressChart.update();
        }

        // Reset activity feed
        const feed = document.getElementById('activity-feed');
        if (feed) {
            feed.innerHTML = `
                <div class="text-center text-gray-500 py-8">
                    <i class="fas fa-play-circle text-4xl mb-2"></i>
                    <p>Click "Start A2A Demo" to begin agent orchestration</p>
                </div>
            `;
        }

        // Reset artifacts
        const artifactsList = document.getElementById('artifacts-list');
        if (artifactsList) {
            artifactsList.innerHTML = `
                <div class="text-center text-gray-500 py-8">
                    <i class="fas fa-file-alt text-4xl mb-2"></i>
                    <p>Artifacts will appear here as agents complete their tasks</p>
                </div>
            `;
        }

        // Reset counters
        const counters = ['elapsed-time', 'active-agents', 'tasks-created', 'artifacts-count'];
        counters.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = id === 'elapsed-time' ? '0:00' : '0';
            }
        });

        // Hide resolution
        const resolutionDiv = document.getElementById('resolution-summary');
        if (resolutionDiv) {
            resolutionDiv.style.display = 'none';
        }
    }
}

// Add CSS animations for the effects
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fadeIn {
        animation: fadeIn 0.3s ease-out;
    }
`;
document.head.appendChild(style);

// Make dashboard available globally
window.A2ADashboard = A2ADashboard; 