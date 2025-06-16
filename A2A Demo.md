# A2A Demo

# A2A Customer Service Orchestration: Complete Mock-up Package

## 1. Business Scenario Setup

**Company**: LatentGenius AI Solutions

**Situation**: Flash sale event causing 300% traffic spike

**Crisis**: Enterprise customer GlobalCorp can't complete $50K AI compute cluster order

**Impact**: Revenue loss, customer escalation, potential contract cancellation

**Timeline**: Must resolve within 30 minutes before inventory expires

---

## 2. Agent Cards (Discovery Phase)

### Master Customer Service Agent Card

```tsx
{
  "agent_card_version": "1.0",
  "name": "Customer Service Orchestrator",
  "agent_id": "cs-orchestrator-001",
  "description": "Primary customer service coordination agent",
  "version": "2.1.0",
  "homepage": "https://latentgenius.ai/agents/cs-orchestrator",
  "skills": [
    {
      "name": "incident-coordination",
      "description": "Coordinate multi-agent incident resolution",
      "input_schema": {
        "type": "object",
        "properties": {
          "incident_id": {"type": "string"},
          "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
          "customer_info": {"type": "object"},
          "issue_description": {"type": "string"}
        }
      }
    }
  ],
  "authentication": {
    "type": "oauth2",
    "authorization_url": "https://auth.latentgenius.ai/oauth/authorize",
    "token_url": "https://auth.latentgenius.ai/oauth/token"
  },
  "endpoints": {
    "base_url": "https://agents.latentgenius.ai/cs-orchestrator",
    "tasks": "/tasks",
    "streaming": "/stream"
  },
  "capabilities": {
    "streaming": true,
    "push_notifications": true,
    "modalities": ["text", "structured_data", "images"]
  }
}

```

### Payment Systems Agent Card

```json
{
  "agent_card_version": "1.0",
  "name": "Payment Systems Agent",
  "agent_id": "payment-sys-001",
  "description": "Handles payment processing, transaction analysis, and gateway issues",
  "version": "3.2.1",
  "homepage": "https://latentgenius.ai/agents/payment-systems",
  "skills": [
    {
      "name": "transaction-analysis",
      "description": "Analyze failed transactions and identify root causes",
      "input_schema": {
        "type": "object",
        "properties": {
          "transaction_id": {"type": "string"},
          "customer_id": {"type": "string"},
          "amount": {"type": "number"},
          "timestamp": {"type": "string", "format": "date-time"}
        }
      },
      "output_schema": {
        "type": "object",
        "properties": {
          "failure_reason": {"type": "string"},
          "gateway_status": {"type": "string"},
          "retry_recommended": {"type": "boolean"},
          "analysis_report": {"type": "string"}
        }
      }
    },
    {
      "name": "payment-retry",
      "description": "Attempt payment retry with optimized parameters",
      "input_schema": {
        "type": "object",
        "properties": {
          "original_transaction_id": {"type": "string"},
          "retry_strategy": {"type": "string"}
        }
      }
    }
  ],
  "authentication": {
    "type": "api_key",
    "location": "header",
    "name": "X-API-Key"
  },
  "endpoints": {
    "base_url": "https://agents.latentgenius.ai/payment-systems",
    "tasks": "/tasks",
    "streaming": "/stream"
  },
  "capabilities": {
    "streaming": true,
    "push_notifications": false,
    "modalities": ["text", "structured_data"]
  }
}

```

### Fraud Detection Agent Card

```json
{
  "agent_card_version": "1.0",
  "name": "Fraud Detection Agent",
  "agent_id": "fraud-detect-001",
  "description": "Real-time fraud analysis and risk assessment",
  "version": "4.1.0",
  "skills": [
    {
      "name": "risk-assessment",
      "description": "Evaluate transaction risk and customer legitimacy",
      "input_schema": {
        "type": "object",
        "properties": {
          "customer_id": {"type": "string"},
          "transaction_amount": {"type": "number"},
          "transaction_context": {"type": "object"}
        }
      }
    }
  ],
  "authentication": {
    "type": "oauth2",
    "scopes": ["fraud.read", "risk.assess"]
  },
  "endpoints": {
    "base_url": "https://agents.latentgenius.ai/fraud-detection",
    "tasks": "/tasks",
    "streaming": "/stream"
  },
  "capabilities": {
    "streaming": true,
    "push_notifications": true,
    "modalities": ["text", "structured_data", "images"]
  }
}

```

### Order Management Agent Card

```json

{
  "agent_card_version": "1.0",
  "name": "Order Management Agent",
  "agent_id": "order-mgmt-001",
  "description": "Inventory management, order processing, and fulfillment coordination",
  "version": "2.8.3",
  "skills": [
    {
      "name": "inventory-hold",
      "description": "Reserve inventory for specified duration",
      "input_schema": {
        "type": "object",
        "properties": {
          "order_id": {"type": "string"},
          "items": {"type": "array"},
          "hold_duration_minutes": {"type": "integer"}
        }
      }
    },
    {
      "name": "expedited-processing",
      "description": "Enable expedited order processing and shipping",
      "input_schema": {
        "type": "object",
        "properties": {
          "order_id": {"type": "string"},
          "expedite_level": {"type": "string", "enum": ["standard", "express", "same_day"]}
        }
      }
    }
  ],
  "authentication": {
    "type": "bearer",
    "bearer_format": "JWT"
  },
  "endpoints": {
    "base_url": "https://agents.latentgenius.ai/order-management",
    "tasks": "/tasks",
    "streaming": "/stream"
  }
}

```

## 3. Complete API Call Sequence

### Phase 1: Agent Discovery

```bash
# Customer Service Agent discovers available agents
GET https://registry.latentgenius.ai/.well-known/agents

# Response: List of available agent endpoints
{
  "agents": [
    "https://agents.latentgenius.ai/payment-systems/.well-known/agent.json",
    "https://agents.latentgenius.ai/fraud-detection/.well-known/agent.json",
    "https://agents.latentgenius.ai/order-management/.well-known/agent.json",
    "https://agents.latentgenius.ai/tech-support/.well-known/agent.json"
  ]
}

# Fetch each agent's capabilities
GET https://agents.latentgenius.ai/payment-systems/.well-known/agent.json
GET https://agents.latentgenius.ai/fraud-detection/.well-known/agent.json
GET https://agents.latentgenius.ai/order-management/.well-known/agent.json

```

### Phase 2: Master Task Creation

```bash
POST https://agents.latentgenius.ai/cs-orchestrator/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "create_task",
  "params": {
    "task_id": "incident-20250616-001",
    "skill_required": "incident-coordination",
    "priority": "critical",
    "context": {
      "incident_type": "payment_failure",
      "customer": {
        "id": "CORP-12345",
        "name": "GlobalCorp Industries",
        "tier": "enterprise",
        "account_value": 2500000
      },
      "order": {
        "id": "ORD-789123",
        "amount": 49999.99,
        "items": [
          {
            "sku": "SRV-DELL-R750",
            "quantity": 5,
            "description": "Dell PowerEdge R750 Server"
          }
        ]
      },
      "failure_details": {
        "error_code": "GATEWAY_TIMEOUT",
        "timestamp": "2025-06-16T14:23:15Z",
        "transaction_id": "TXN-456789"
      }
    },
    "deadline": "2025-06-16T15:00:00Z",
    "callback_url": "https://agents.latentgenius.ai/cs-orchestrator/callbacks"
  },
  "id": "req-001"
}

```

### Phase 3: Sub-task Delegation

### Payment Analysis Task

```tsx
POST https://agents.latentgenius.ai/payment-systems/tasks
Authorization: X-API-Key: pm_sk_live_abcd1234...
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "create_task",
  "params": {
    "task_id": "payment-analysis-001",
    "parent_task_id": "incident-20250616-001",
    "skill_required": "transaction-analysis",
    "priority": "critical",
    "context": {
      "transaction_id": "TXN-456789",
      "customer_id": "CORP-12345",
      "amount": 49999.99,
      "timestamp": "2025-06-16T14:23:15Z",
      "gateway": "stripe_enterprise",
      "merchant_account": "techmart_enterprise"
    }
  },
  "id": "req-002"
}

```

### Fraud Assessment Task

```bash
POST https://agents.latentgenius.ai/fraud-detection/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "create_task",
  "params": {
    "task_id": "fraud-check-001",
    "parent_task_id": "incident-20250616-001",
    "skill_required": "risk-assessment",
    "priority": "critical",
    "context": {
      "customer_id": "CORP-12345",
      "transaction_amount": 49999.99,
      "transaction_context": {
        "ip_address": "203.0.113.45",
        "user_agent": "Mozilla/5.0...",
        "payment_method": "corporate_card_ending_5678",
        "billing_address": "verified",
        "shipping_address": "verified"
      }
    }
  },
  "id": "req-003"
}

```

### Inventory Hold Task

```bash
POST https://agents.latentgenius.ai/order-management/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "create_task",
  "params": {
    "task_id": "inventory-hold-001",
    "parent_task_id": "incident-20250616-001",
    "skill_required": "inventory-hold",
    "priority": "high",
    "context": {
      "order_id": "ORD-789123",
      "items": [
        {
          "sku": "SRV-DELL-R750",
          "quantity": 5
        }
      ],
      "hold_duration_minutes": 45,
      "reason": "payment_processing_issue"
    }
  },
  "id": "req-004"
}

```

## 4. Real-time Streaming Updates (SSE)

### Payment Systems Agent Stream

GET [https://agents.latentgenius.ai/payment-systems/stream/payment-analysis-001](https://agents.latentgenius.ai/payment-systems/stream/payment-analysis-001)
Accept: text/event-stream
Authorization: X-API-Key: pm_sk_live_abcd1234...

Stream Response:

event: task_started
data: {"task_id": "payment-analysis-001", "status": "working", "timestamp": "2025-06-16T14:24:01Z", "message": "Beginning transaction analysis..."}

event: progress
data: {"task_id": "payment-analysis-001", "status": "working", "progress": 25, "timestamp": "2025-06-16T14:24:05Z", "message": "Retrieving transaction logs from Stripe..."}

event: progress

data: {"task_id": "payment-analysis-001", "status": "working", "progress": 50, "timestamp": "2025-06-16T14:24:12Z", "message": "Analyzing gateway timeout patterns..."}

event: insight
data: {"task_id": "payment-analysis-001", "status": "working", "progress": 75, "timestamp": "2025-06-16T14:24:18Z", "message": "Detected: Gateway timeout due to 3DS verification delay", "insight": {"root_cause": "3ds_timeout", "confidence": 0.94}}

event: artifact_ready
data: {"task_id": "payment-analysis-001", "status": "working", "progress": 90, "timestamp": "2025-06-16T14:24:22Z", "artifact": {"type": "analysis_report", "url": "[https://artifacts.latentgenius.ai/payment-analysis-001.json](https://artifacts.latentgenius.ai/payment-analysis-001.json)", "format": "application/json"}}

event: task_completed
data: {"task_id": "payment-analysis-001", "status": "completed", "progress": 100, "timestamp": "2025-06-16T14:24:25Z", "message": "Analysis complete. Root cause identified with 94% confidence.", "result": {"retry_recommended": true, "strategy": "bypass_3ds_for_verified_corporate"}}

### Fraud Detection Agent Stream

```
GET https://agents.latentgenius.ai/fraud-detection/stream/fraud-check-001
Accept: text/event-stream
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

event: task_started
data: {"task_id": "fraud-check-001", "status": "working", "timestamp": "2025-06-16T14:24:02Z", "message": "Initiating risk assessment for CORP-12345..."}

event: progress
data: {"task_id": "fraud-check-001", "status": "working", "progress": 30, "timestamp": "2025-06-16T14:24:07Z", "message": "Verifying customer identity and transaction history..."}

event: progress
data: {"task_id": "fraud-check-001", "status": "working", "progress": 60, "timestamp": "2025-06-16T14:24:14Z", "message": "Analyzing payment patterns and behavioral signals..."}

event: risk_score_update
data: {"task_id": "fraud-check-001", "status": "working", "progress": 85, "timestamp": "2025-06-16T14:24:19Z", "risk_score": 0.15, "message": "Low risk detected. Customer verified as legitimate enterprise account."}

event: task_completed
data: {"task_id": "fraud-check-001", "status": "completed", "progress": 100, "timestamp": "2025-06-16T14:24:23Z", "message": "Risk assessment complete: LOW RISK", "result": {"risk_score": 0.15, "recommendation": "approve", "confidence": 0.97, "verified_signals": ["corporate_card", "established_account", "verified_addresses", "normal_order_pattern"]}}

```

### Order Management Agent Stream

```
GET https://agents.latentgenius.ai/order-management/stream/inventory-hold-001
Accept: text/event-stream
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

event: task_started
data: {"task_id": "inventory-hold-001", "status": "working", "timestamp": "2025-06-16T14:24:03Z", "message": "Checking inventory availability for ORD-789123..."}

event: progress
data: {"task_id": "inventory-hold-001", "status": "working", "progress": 40, "timestamp": "2025-06-16T14:24:08Z", "message": "5 units of SRV-DELL-R750 available in warehouse"}

event: inventory_reserved
data: {"task_id": "inventory-hold-001", "status": "working", "progress": 80, "timestamp": "2025-06-16T14:24:11Z", "message": "Inventory reserved for 45 minutes", "hold_expires": "2025-06-16T15:09:11Z"}

event: task_completed
data: {"task_id": "inventory-hold-001", "status": "completed", "progress": 100, "timestamp": "2025-06-16T14:24:13Z", "message": "Inventory hold confirmed. Expedited shipping pre-approved.", "result": {"hold_id": "HOLD-789123", "expires_at": "2025-06-16T15:09:11Z", "expedited_shipping": true}}
```

## 5. Artifact Schemas

### Payment Analysis Report

```tsx
{
  "artifact_id": "payment-analysis-001",
  "task_id": "payment-analysis-001",
  "type": "analysis_report",
  "format": "application/json",
  "created_at": "2025-06-16T14:24:25Z",
  "data": {
    "transaction_analysis": {
      "transaction_id": "TXN-456789",
      "original_amount": 49999.99,
      "currency": "USD",
      "gateway": "stripe_enterprise",
      "failure_reason": "3DS verification timeout",
      "failure_code": "GATEWAY_TIMEOUT",
      "root_cause": {
        "primary": "3ds_authentication_timeout",
        "contributing_factors": [
          "high_traffic_volume",
          "issuing_bank_response_delay"
        ],
        "confidence": 0.94
      },
      "resolution_strategy": {
        "recommended_action": "retry_with_bypass",
        "bypass_reason": "verified_corporate_account",
        "expected_success_rate": 0.97
      },
      "technical_details": {
        "gateway_response_time": "30.2s",
        "timeout_threshold": "30.0s",
        "3ds_challenge_presented": true,
        "customer_authentication_attempted": true
      }
    }
  }
}
```

### Fraud Risk Assessment

```tsx
{
  "artifact_id": "fraud-assessment-001",
  "task_id": "fraud-check-001", 
  "type": "risk_assessment",
  "format": "application/json",
  "created_at": "2025-06-16T14:24:23Z",
  "data": {
    "risk_assessment": {
      "customer_id": "CORP-12345",
      "overall_risk_score": 0.15,
      "risk_level": "LOW",
      "confidence": 0.97,
      "recommendation": "APPROVE",
      "verified_attributes": [
        {
          "attribute": "customer_identity",
          "status": "verified",
          "method": "corporate_registration_check"
        },
        {
          "attribute": "payment_method",
          "status": "verified", 
          "method": "corporate_card_validation"
        },
        {
          "attribute": "billing_address",
          "status": "verified",
          "method": "address_verification_service"
        },
        {
          "attribute": "order_pattern",
          "status": "normal",
          "method": "behavioral_analysis"
        }
      ],
      "risk_factors": {
        "positive_signals": [
          "established_customer_since_2019",
          "consistent_payment_history",
          "verified_corporate_entity",
          "normal_order_size_for_customer"
        ],
        "negative_signals": [],
        "neutral_signals": [
          "peak_traffic_period",
          "first_time_using_this_payment_method"
        ]
      }
    }
  }
}
```

## 6. UI Mockup Design

Let me create a visual representation of the real-time coordination dashboard:

```tsx
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A2A Customer Service Orchestration Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center">
                    <i class="fas fa-robot text-blue-600 text-2xl mr-3"></i>
                    <h1 class="text-2xl font-bold text-gray-900">A2A Customer Service Orchestration</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-sm text-gray-500">Protocol Version: 1.0</span>
                    <div class="flex items-center">
                        <div class="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                        <span class="text-sm text-green-600">Live</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Incident Overview -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                    <i class="fas fa-exclamation-triangle text-red-600 text-xl mr-3"></i>
                    <h2 class="text-xl font-semibold text-red-800">Critical Incident: Payment Processing Failure</h2>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">CRITICAL</span>
                    <span class="text-sm text-red-600" id="incident-timer">00:05:23</span>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <p class="text-sm text-gray-600">Customer</p>
                    <p class="font-semibold text-gray-900">GlobalCorp Industries</p>
                    <p class="text-sm text-gray-500">Enterprise Tier</p>
                </div>
                <div>
                    <p class="text-sm text-gray-600">Order Value</p>
                    <p class="font-semibold text-gray-900">$49,999.99</p>
                    <p class="text-sm text-gray-500">5x Dell PowerEdge R750</p>
                </div>
                <div>
                    <p class="text-sm text-gray-600">Failure Type</p>
                    <p class="font-semibold text-gray-900">Gateway Timeout</p>
                    <p class="text-sm text-gray-500">3DS Verification Delay</p>
                </div>
                <div>
                    <p class="text-sm text-gray-600">Resolution Deadline</p>
                    <p class="font-semibold text-gray-900" id="deadline-timer">24:37 remaining</p>
                    <p class="text-sm text-gray-500">Before inventory expires</p>
                </div>
            </div>
        </div>

        <!-- Agent Discovery & Coordination -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <!-- Agent Cards -->
            <div class="lg:col-span-2">
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Agent Coordination</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Payment Systems Agent -->
                        <div class="border rounded-lg p-4 agent-card" data-agent="payment">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center">
                                    <i class="fas fa-credit-card text-blue-600 mr-2"></i>
                                    <h4 class="font-semibold text-gray-900">Payment Systems</h4>
                                </div>
                                <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs status-badge">Working</span>
                            </div>
                            <p class="text-sm text-gray-600 mb-2">Transaction analysis & retry logic</p>
                            <div class="flex items-center justify-between">
                                <div class="w-full bg-gray-200 rounded-full h-2 mr-2">
                                    <div class="bg-blue-600 h-2 rounded-full progress-bar" style="width: 0%"></div>
                                </div>
                                <span class="text-sm font-medium text-gray-700 progress-text">0%</span>
                            </div>
                        </div>

                        <!-- Fraud Detection Agent -->
                        <div class="border rounded-lg p-4 agent-card" data-agent="fraud">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center">
                                    <i class="fas fa-shield-alt text-green-600 mr-2"></i>
                                    <h4 class="font-semibold text-gray-900">Fraud Detection</h4>
                                </div>
                                <span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs status-badge">Working</span>
                            </div>
                            <p class="text-sm text-gray-600 mb-2">Risk assessment & verification</p>
                            <div class="flex items-center justify-between">
                                <div class="w-full bg-gray-200 rounded-full h-2 mr-2">
                                    <div class="bg-green-600 h-2 rounded-full progress-bar" style="width: 0%"></div>
                                </div>
                                <span class="text-sm font-medium text-gray-700 progress-text">0%</span>
                            </div>
                        </div>

                        <!-- Order Management Agent -->
                        <div class="border rounded-lg p-4 agent-card" data-agent="order">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center">
                                    <i class="fas fa-box text-purple-600 mr-2"></i>
                                    <h4 class="font-semibold text-gray-900">Order Management</h4>
                                </div>
                                <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs status-badge">Working</span>
                            </div>
                            <p class="text-sm text-gray-600 mb-2">Inventory hold & expedited shipping</p>
                            <div class="flex items-center justify-between">
                                <div class="w-full bg-gray-200 rounded-full h-2 mr-2">
                                    <div class="bg-purple-600 h-2 rounded-full progress-bar" style="width: 0%"></div>
                                </div>
                                <span class="text-sm font-medium text-gray-700 progress-text">0%</span>
                            </div>
                        </div>

                        <!-- Tech Support Agent -->
                        <div class="border rounded-lg p-4 agent-card" data-agent="tech">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center">
                                    <i class="fas fa-tools text-orange-600 mr-2"></i>
                                    <h4 class="font-semibold text-gray-900">Tech Support</h4>
                                </div>
                                <span class="bg-orange-100 text-orange-800 px-2 py-1 rounded text-xs status-badge">Working</span>
                            </div>
                            <p class="text-sm text-gray-600 mb-2">System diagnostics & optimization</p>
                            <div class="flex items-center justify-between">
                                <div class="w-full bg-gray-200 rounded-full h-2 mr-2">
                                    <div class="bg-orange-600 h-2 rounded-full progress-bar" style="width: 0%"></div>
                                </div>
                                <span class="text-sm font-medium text-gray-700 progress-text">0%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Resolution Progress -->
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Resolution Progress</h3>
                <div class="mb-4">
                    <canvas id="progressChart" style="height: 200px;"></canvas>
                </div>
                <div class="space-y-2">
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-600">Time Elapsed</span>
                        <span class="font-medium text-gray-900" id="elapsed-time">5:23</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-600">Agents Active</span>
                        <span class="font-medium text-gray-900" id="active-agents">4</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-600">Tasks Created</span>
                        <span class="font-medium text-gray-900" id="tasks-created">4</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-600">Artifacts Generated</span>
                        <span class="font-medium text-gray-900" id="artifacts-count">0</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Real-time Activity Feed -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Activity Stream -->
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Real-time Activity Stream</h3>
                <div class="space-y-3 max-h-96 overflow-y-auto" id="activity-feed">
                    <div class="flex items-start space-x-3">
                        <div class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                        <div>
                            <p class="text-sm text-gray-900">A2A Protocol initialized</p>
                            <p class="text-xs text-gray-500">14:23:45</p>
                        </div>
                    </div>
                    <div class="flex items-start space-x-3">
                        <div class="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                        <div>
                            <p class="text-sm text-gray-900">Agent discovery completed - 4 agents found</p>
                            <p class="text-xs text-gray-500">14:23:52</p>
                        </div>
                    </div>
                    <div class="flex items-start space-x-3">
                        <div class="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                        <div>
                            <p class="text-sm text-gray-900">Master task created: incident-20250616-001</p>
                            <p class="text-xs text-gray-500">14:24:01</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Generated Artifacts -->
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Generated Artifacts</h3>
                <div class="space-y-3" id="artifacts-list">
                    <div class="text-center text-gray-500 py-8">
                        <i class="fas fa-file-alt text-4xl mb-2"></i>
                        <p>Artifacts will appear here as agents complete their tasks</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize progress chart
        const ctx = document.getElementById('progressChart').getContext('2d');
        const progressChart = new Chart(ctx, {
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
                    legend: {
                        display: false
                    }
                },
                cutout: '70%'
            }
        });

        // Simulation data
        const simulationSteps = [
            {
                time: 3000,
                agent: 'payment',
                progress: 25,
                status: 'Working',
                activity: 'Payment Systems Agent: Retrieving transaction logs from Stripe...',
                timestamp: '14:24:05'
            },
            {
                time: 4000,
                agent: 'fraud',
                progress: 30,
                status: 'Working',
                activity: 'Fraud Detection Agent: Verifying customer identity and transaction history...',
                timestamp: '14:24:07'
            },
            {
                time: 5000,
                agent: 'order',
                progress: 40,
                status: 'Working',
                activity: 'Order Management Agent: 5 units of SRV-DELL-R750 available in warehouse',
                timestamp: '14:24:08'
            },
            {
                time: 6000,
                agent: 'tech',
                progress: 35,
                status: 'Working',
                activity: 'Tech Support Agent: Analyzing gateway performance metrics...',
                timestamp: '14:24:10'
            },
            {
                time: 8000,
                agent: 'order',
                progress: 80,
                status: 'Working',
                activity: 'Order Management Agent: Inventory reserved for 45 minutes',
                timestamp: '14:24:11'
            },
            {
                time: 10000,
                agent: 'payment',
                progress: 50,
                status: 'Working',
                activity: 'Payment Systems Agent: Analyzing gateway timeout patterns...',
                timestamp: '14:24:12'
            },
            {
                time: 12000,
                agent: 'order',
                progress: 100,
                status: 'Completed',
                activity: 'Order Management Agent: Inventory hold confirmed. Expedited shipping pre-approved.',
                timestamp: '14:24:13',
                artifact: {
                    name: 'Inventory Hold Confirmation',
                    type: 'JSON',
                    description: 'Hold ID: HOLD-789123, expires at 15:09:11'
                }
            },
            {
                time: 14000,
                agent: 'fraud',
                progress: 60,
                status: 'Working',
                activity: 'Fraud Detection Agent: Analyzing payment patterns and behavioral signals...',
                timestamp: '14:24:14'
            },
            {
                time: 16000,
                agent: 'tech',
                progress: 70,
                status: 'Working',
                activity: 'Tech Support Agent: Identified high latency in 3DS verification service',
                timestamp: '14:24:16'
            },
            {
                time: 18000,
                agent: 'payment',
                progress: 75,
                status: 'Working',
                activity: 'Payment Systems Agent: Detected: Gateway timeout due to 3DS verification delay',
                timestamp: '14:24:18'
            },
            {
                time: 19000,
                agent: 'fraud',
                progress: 85,
                status: 'Working',
                activity: 'Fraud Detection Agent: Low risk detected. Customer verified as legitimate enterprise account.',
                timestamp: '14:24:19'
            },
            {
                time: 22000,
                agent: 'payment',
                progress: 90,
                status: 'Working',
                activity: 'Payment Systems Agent: Analysis report generated',
                timestamp: '14:24:22'
            },
            {
                time: 23000,
                agent: 'fraud',
                progress: 100,
                status: 'Completed',
                activity: 'Fraud Detection Agent: Risk assessment complete: LOW RISK',
                timestamp: '14:24:23',
                artifact: {
                    name: 'Risk Assessment Report',
                    type: 'JSON',
                    description: 'Risk Score: 0.15 (Low Risk), Confidence: 97%'
                }
            },
            {
                time: 25000,
                agent: 'payment',
                progress: 100,
                status: 'Completed',
                activity: 'Payment Systems Agent: Analysis complete. Root cause identified with 94% confidence.',
                timestamp: '14:24:25',
                artifact: {
                    name: 'Payment Analysis Report',
                    type: 'JSON',
                    description: 'Root cause: 3DS timeout, Retry recommended with bypass'
                }
            },
            {
                time: 27000,
                agent: 'tech',
                progress: 100,
                status: 'Completed',
                activity: 'Tech Support Agent: Gateway optimization parameters updated',
                timestamp: '14:24:27',
                artifact: {
                    name: 'System Diagnostic Report',
                    type: 'PDF',
                    description: 'Performance optimizations and recommendations'
                }
            },
            {
                time: 30000,
                activity: 'RESOLUTION COMPLETE: Payment retry successful, order confirmed',
                timestamp: '14:24:30',
                resolution: true
            }
        ];

        let currentStep = 0;
        let startTime = Date.now();
        let artifactsGenerated = 0;

        function updateProgress(agent, progress, status) {
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
                }
            }
        }

        function addActivity(activity, timestamp) {
            const feed = document.getElementById('activity-feed');
            const activityItem = document.createElement('div');
            activityItem.className = 'flex items-start space-x-3';
            activityItem.innerHTML = `
                <div class="w-2 h-2 bg-blue-500 rounded-full mt-2 animate-pulse"></div>
                <div>
                    <p class="text-sm text-gray-900">${activity}</p>
                    <p class="text-xs text-gray-500">${timestamp}</p>
                </div>
            `;
            feed.appendChild(activityItem);
            feed.scrollTop = feed.scrollHeight;
        }

        function addArtifact(artifact) {
            const artifactsList = document.getElementById('artifacts-list');
            
            // Remove placeholder if it exists
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
            
            artifactsGenerated++;
            document.getElementById('artifacts-count').textContent = artifactsGenerated;
        }

        function updateOverallProgress() {
            const totalProgress = simulationSteps.filter(step => step.progress === 100).length;
            const progressPercentage = Math.round((currentStep / simulationSteps.length) * 100);
            
            progressChart.data.datasets[0].data = [progressPercentage, 100 - progressPercentage];
            progressChart.update();
        }

        function runSimulation() {
            if (currentStep < simulationSteps.length) {
                const step = simulationSteps[currentStep];
                
                setTimeout(() => {
                    if (step.agent) {
                        updateProgress(step.agent, step.progress, step.status);
                    }
                    
                    addActivity(step.activity, step.timestamp);
                    
                    if (step.artifact) {
                        addArtifact(step.artifact);
                    }
                    
                    if (step.resolution) {
                        // Show success state
                        document.querySelector('.bg-red-50').className = 'bg-green-50 border border-green-200 rounded-lg p-6 mb-6';
                        document.querySelector('.text-red-800').className = 'text-xl font-semibold text-green-800';
                        document.querySelector('.text-red-800').innerHTML = '<i class="fas fa-check-circle text-green-600 text-xl mr-3"></i>Incident Resolved: Payment Processing Restored';
                        document.querySelector('.bg-red-100').className = 'bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium';
                        document.querySelector('.bg-green-100').textContent = 'RESOLVED';
                    }
                    
                    updateOverallProgress();
                    currentStep++;
                    runSimulation();
                }, step.time);
            }
        }

        // Start simulation
        runSimulation();

        // Update timers
        setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            document.getElementById('elapsed-time').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            document.getElementById('incident-timer').textContent = `${Math.floor(elapsed / 60).toString().padStart(2, '0')}:${(elapsed % 60).toString().padStart(2, '0')}:${Math.floor((elapsed % 1) * 100).toString().padStart(2, '0')}`;
        }, 100);
    </script>
</body>
</html>

```

## 7. Complete Timeline Visualization

Let me create a visual timeline showing the complete A2A workflow:

## 8. Presentation Materials

### Executive Summary Slide Content

**Title: "A2A Protocol: Orchestrating AI Agents for Enterprise Excellence"**

**The Challenge:**

- Enterprise customer unable to complete $50K order
- Payment gateway timeout during flash sale traffic spike
- 30-minute window before inventory expires
- Traditional single-agent approach would fail

**The A2A Solution:**

- **Discovery**: Automatic identification of specialized agents
- **Orchestration**: Parallel task delegation and coordination
- **Real-time**: Live streaming updates from all agents
- **Resolution**: Coordinated solution in under 2 minutes

**Business Impact:**

- ✅ $50K order saved
- ✅ Customer satisfaction maintained
- ✅ 94% faster resolution vs manual process
- ✅ Proactive communication to customer
- ✅ Automated incident documentation

### Technical Architecture Slide

**A2A Protocol Stack:**

```
┌─────────────────────────────────────┐
│        Business Application         │
├─────────────────────────────────────┤
│     Customer Service Orchestrator   │
├─────────────────────────────────────┤
│           A2A Protocol Layer        │
│  • Agent Discovery (Agent Cards)    │
│  • Task Management (JSON-RPC 2.0)   │
│  • Real-time Streaming (SSE)        │
│  • Artifact Exchange                │
├─────────────────────────────────────┤
│      Transport Layer (HTTPS)        │
├─────────────────────────────────────┤
│   Specialized Agent Implementations  │
│  Payment│Fraud│Order│Tech Support   │
└─────────────────────────────────────┘

```

### ROI Calculation Slide

**Traditional vs A2A Approach:**

| Metric | Traditional | A2A Protocol | Improvement |
| --- | --- | --- | --- |
| Resolution Time | 45+ minutes | 2 minutes | **95% faster** |
| Agents Involved | 1 (sequential) | 4 (parallel) | **400% efficiency** |
| Customer Communication | Manual | Automated | **100% consistency** |
| Documentation | Manual | Auto-generated | **Zero admin overhead** |
| Success Rate | 60% first attempt | 97% coordinated | **62% improvement** |

**Annual Impact Projection:**

- Similar incidents: ~500 per year
- Average order value: $25K
- Resolution improvement saves: **$4.6M annually**
- Customer satisfaction increase: **23% improvement**

---

## 9. Implementation Code Examples

### Agent Discovery Implementation

```tsx
import requests
import json
from typing import List, Dict

class A2AAgentDiscovery:
    def __init__(self, registry_url: str, auth_token: str):
        self.registry_url = registry_url
        self.auth_token = auth_token
        
    async def discover_agents_by_skill(self, required_skills: List[str]) -> Dict:
        """Discover agents that match required skills"""
        
        # Get agent registry
        agents_response = requests.get(
            f"{self.registry_url}/.well-known/agents",
            headers={"Authorization": f"Bearer {self.auth_token}"}
        )
        
        agent_endpoints = agents_response.json()["agents"]
        matching_agents = {}
        
        # Check each agent's capabilities
        for endpoint in agent_endpoints:
            agent_card = requests.get(endpoint).json()
            
            agent_skills = [skill["name"] for skill in agent_card["skills"]]
            
            # Check if agent has required skills
            if any(skill in agent_skills for skill in required_skills):
                matching_agents[agent_card["agent_id"]] = {
                    "name": agent_card["name"],
                    "endpoint": agent_card["endpoints"]["base_url"],
                    "skills": agent_skills,
                    "capabilities": agent_card["capabilities"]
                }
                
        return matching_agents

# Usage example
discovery = A2AAgentDiscovery(
    registry_url="https://registry.latentgenius.ai",
    auth_token="your_auth_token"
)

agents = await discovery.discover_agents_by_skill([
    "transaction-analysis", 
    "risk-assessment", 
    "inventory-hold"
])
```

### Task Orchestration Implementation

```python
import asyncio
import json
from typing import Dict, List
import aiohttp

class A2ATaskOrchestrator:
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.active_tasks = {}
        
    async def create_coordinated_incident_response(
        self, 
        incident_data: Dict,
        agents: Dict
    ) -> str:
        """Create and coordinate multi-agent incident response"""
        
        master_task_id = f"incident-{incident_data['timestamp']}"
        
        # Create sub-tasks for each specialized agent
        sub_tasks = []
        
        # Payment analysis task
        if "payment-sys-001" in agents:
            sub_tasks.append({
                "agent_id": "payment-sys-001",
                "endpoint": agents["payment-sys-001"]["endpoint"],
                "task": {
                    "task_id": f"payment-analysis-{master_task_id}",
                    "skill_required": "transaction-analysis",
                    "priority": "critical",
                    "context": {
                        "transaction_id": incident_data["transaction_id"],
                        "customer_id": incident_data["customer_id"],
                        "amount": incident_data["amount"]
                    }
                }
            })
            
        # Fraud detection task  
        if "fraud-detect-001" in agents:
            sub_tasks.append({
                "agent_id": "fraud-detect-001", 
                "endpoint": agents["fraud-detect-001"]["endpoint"],
                "task": {
                    "task_id": f"fraud-check-{master_task_id}",
                    "skill_required": "risk-assessment",
                    "priority": "critical",
                    "context": {
                        "customer_id": incident_data["customer_id"],
                        "transaction_amount": incident_data["amount"]
                    }
                }
            })
            
        # Execute tasks in parallel
        task_results = await asyncio.gather(*[
            self._execute_task(task) for task in sub_tasks
        ])
        
        return master_task_id
        
    async def _execute_task(self, task_config: Dict) -> Dict:
        """Execute individual agent task with streaming"""
        
        async with aiohttp.ClientSession() as session:
            # Create task
            async with session.post(
                f"{task_config['endpoint']}/tasks",
                headers={
                    "Authorization": f"Bearer {self.auth_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "jsonrpc": "2.0",
                    "method": "create_task", 
                    "params": task_config["task"],
                    "id": f"req-{task_config['task']['task_id']}"
                }
            ) as response:
                task_response = await response.json()
                
            # Start streaming updates
            stream_url = f"{task_config['endpoint']}/stream/{task_config['task']['task_id']}"
            await self._stream_task_updates(session, stream_url, task_config['task']['task_id'])
            
        return task_response
        
    async def _stream_task_updates(self, session, stream_url: str, task_id: str):
        """Handle SSE streaming from agent"""
        
        async with session.get(
            stream_url,
            headers={
                "Accept": "text/event-stream",
                "Authorization": f"Bearer {self.auth_token}"
            }
        ) as response:
            async for line in response.content:
                if line.startswith(b'data: '):
                    data = json.loads(line[6:].decode())
                    await self._handle_stream_event(task_id, data)
                    
    async def _handle_stream_event(self, task_id: str, event_data: Dict):
        """Process streaming events from agents"""
        
        print(f"[{task_id}] {event_data.get('message', '')}")
        
        if event_data.get('status') == 'completed':
            self.active_tasks[task_id] = event_data
            
        elif 'artifact' in event_data:
            # Download and process artifact
            artifact_url = event_data['artifact']['url']
            print(f"[{task_id}] Artifact ready: {artifact_url}")

# Usage example
orchestrator = A2ATaskOrchestrator(auth_token="your_token")

incident_data = {
    "timestamp": "20250616-001",
    "customer_id": "CORP-12345", 
    "transaction_id": "TXN-456789",
    "amount": 49999.99
}

master_task = await orchestrator.create_coordinated_incident_response(
    incident_data, 
    discovered_agents
)

```

## 10. Demo Script and Talking Points

### Opening Hook (30 seconds)

*"Imagine your biggest enterprise customer can't complete a $50,000 order during your flash sale. Every minute costs money, customer trust, and potentially the entire relationship. Traditional systems would escalate this through multiple teams over 45+ minutes. Watch how A2A resolves this in under 2 minutes using coordinated AI agents."*

### Act 1: The Crisis (30 seconds)

- **Show**: GlobalCorp attempting to purchase $50K worth of Dell servers
- **Problem**: Payment gateway timeout during traffic spike
- **Stakes**: 30-minute inventory hold expiring, customer escalation risk
- **Traditional approach**: Manual escalation, sequential troubleshooting, high failure rate

### Act 2: A2A Discovery (45 seconds)

- **Show**: Agent Card discovery process
- **Explain**: "The Customer Service Orchestrator instantly discovers specialized agents"
- **Highlight**: Payment Systems, Fraud Detection, Order Management, Tech Support agents
- **Key point**: "This happens automatically - no manual routing or escalation"

### Act 3: Parallel Orchestration (90 seconds)

- **Show**: Real-time dashboard with all 4 agents working simultaneously
- **Stream 1**: Payment Agent analyzing transaction logs
- **Stream 2**: Fraud Agent verifying customer legitimacy
- **Stream 3**: Order Agent securing inventory hold
- **Stream 4**: (Background) Tech Support analyzing system performance
- **Key point**: "All agents work in parallel, sharing insights in real-time"

### Act 4: Resolution (45 seconds)

- **Show**: Artifacts generated by each agent
- **Synthesis**: Orchestrator combines insights into solution
- **Action**: Payment retry with 3DS bypass for verified corporate customer
- **Result**: Successful $50K transaction, expedited shipping approved
- **Customer**: Proactive notification of resolution and upgrade

### Closing Impact (30 seconds)

*"Total resolution time: 1 minute 47 seconds. Customer satisfaction: preserved. Revenue: saved. Documentation: auto-generated. This is the power of A2A - not just connecting agents, but orchestrating them to deliver business outcomes that would be impossible with any single agent or traditional system."*

### Key Technical Points to Emphasize:

1. **Agent Discovery**: Automatic capability matching via Agent Cards
2. **Parallel Processing**: Multiple agents working simultaneously vs sequential
3. **Real-time Streaming**: Live updates via Server-Sent Events
4. **Artifact Integration**: Structured outputs that combine into solutions
5. **Enterprise Security**: OAuth, encryption, audit trails built-in

### ROI Talking Points:

- **Speed**: 95% faster resolution (2 min vs 45+ min)
- **Success Rate**: 97% vs 60% traditional first-attempt success
- **Scalability**: Same approach handles 10x traffic spikes
- **Cost**: Saves $4.6M annually on similar incidents
- **Experience**: Proactive customer communication vs reactive

This complete mock-up package provides everything needed to demonstrate A2A's value proposition in a compelling, technically accurate way that resonates with both business stakeholders and technical implementers.