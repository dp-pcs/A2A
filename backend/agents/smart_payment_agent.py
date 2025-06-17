import sys
import os

# Add the parent directory to the path to import shared modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.llm_agent import LLMAgent

class SmartPaymentAgent(LLMAgent):
    """LLM-powered payment agent that analyzes payment failures dynamically"""
    
    def __init__(self):
        config = {
            "agent_card_version": "1.0",
            "name": "Smart Payment Systems Agent",
            "agent_id": "payment-sys-001",
            "description": "Advanced payment processing analysis using AI reasoning",
            "version": "4.0.0",
            "homepage": "https://latentgenius.ai/agents/smart-payment-systems",
            "skills": [
                {
                    "name": "transaction-analysis",
                    "description": "Analyze failed transactions and identify root causes using AI reasoning",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "transaction_id": {"type": "string"},
                            "customer_id": {"type": "string"},
                            "amount": {"type": "number"},
                            "error_code": {"type": "string"},
                            "timestamp": {"type": "string", "format": "date-time"},
                            "payment_method": {"type": "string"},
                            "gateway_response": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "payment-retry",
                    "description": "Develop optimal retry strategies based on failure analysis",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "original_failure": {"type": "object"},
                            "customer_profile": {"type": "object"},
                            "transaction_context": {"type": "object"}
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
                "base_url": "http://localhost:8002",
                "tasks": "/tasks",
                "streaming": "/stream"
            },
            "capabilities": {
                "streaming": True,
                "push_notifications": False,
                "modalities": ["text", "structured_data"]
            }
        }
        
        super().__init__(config)
        
    def _format_purchase_history(self, history: dict) -> str:
        if not history:
            return "No purchase history available"
        
        lines = []
        if 'average_order_value' in history:
            lines.append(f"- Average Order Value: ${history['average_order_value']:,.2f}")
        if 'largest_previous_order' in history:
            lines.append(f"- Largest Previous Order: ${history['largest_previous_order']:,.2f}")
        if 'monthly_volume' in history:
            lines.append(f"- Monthly Transaction Volume: {history['monthly_volume']} orders")
        if 'preferred_payment' in history:
            lines.append(f"- Preferred Payment Method: {history['preferred_payment']}")
        if 'last_successful_transaction' in history:
            lines.append(f"- Last Successful Transaction: {history['last_successful_transaction']}")
        
        return '\n'.join(lines) if lines else "No detailed history available"
    
    def _format_business_context(self, context: dict) -> str:
        if not context:
            return "No business context available"
        
        lines = []
        if 'industry' in context:
            lines.append(f"- Industry: {context['industry']}")
        if 'use_case' in context:
            lines.append(f"- Use Case: {context['use_case']}")
        if 'urgency' in context:
            lines.append(f"- Business Urgency: {context['urgency']}")
        
        return '\n'.join(lines) if lines else "Standard business context"
    
    def _format_order_items(self, items: list) -> str:
        if not items:
            return "No items specified"
        
        return ', '.join([f"{item.get('name', 'Unknown Item')} x{item.get('quantity', 1)}" for item in items])
    
    def _format_technical_context(self, tech_context: dict) -> str:
        if not tech_context:
            return "No technical context available"
        
        lines = []
        if '3ds_challenge_initiated' in tech_context:
            lines.append(f"- 3DS Challenge: {'Initiated' if tech_context['3ds_challenge_initiated'] else 'Not initiated'}")
        if 'issuer_response_time' in tech_context:
            lines.append(f"- Issuer Response: {tech_context['issuer_response_time']}")
        if 'gateway_health' in tech_context:
            lines.append(f"- Gateway Health: {tech_context['gateway_health']}")
        if 'customer_browser' in tech_context:
            lines.append(f"- Customer Browser: {tech_context['customer_browser']}")
        if 'previous_3ds_success' in tech_context:
            lines.append(f"- Previous 3DS Success: {tech_context['previous_3ds_success']}")
        
        return '\n'.join(lines) if lines else "Standard technical context"
        
    def _get_agent_personality(self) -> str:
        return """You are the Smart Payment Systems Agent for LatentGenius AI Solutions.

You specialize in analyzing payment failures and developing strategic solutions for enterprise customers.
You have deep knowledge of payment gateways, fraud systems, 3DS authentication, and enterprise payment patterns.

EXPERTISE AREAS:
- Payment gateway timeouts and connectivity issues
- 3DS authentication failures and bypass strategies  
- Corporate card processing and verification
- High-value transaction risk assessment
- Payment system diagnostics and optimization

ANALYSIS APPROACH:
1. Examine technical failure details
2. Consider customer context and history
3. Identify root cause with confidence level
4. Recommend specific remediation strategy
5. Provide implementation timeline

You communicate in a professional, technical manner and always provide actionable recommendations.
When possible, suggest multiple solution paths with risk/benefit analysis."""

    def _get_knowledge_base(self) -> dict:
        return {
            "company": "LatentGenius AI Solutions",
            "domain": "AI computing infrastructure sales and support",
            "payment_gateways": ["Stripe Enterprise", "Adyen", "Chase Paymentech"],
            "common_failure_codes": {
                "GATEWAY_TIMEOUT": "Connection timeout to payment processor",
                "3DS_AUTH_TIMEOUT": "3D Secure authentication timeout", 
                "INSUFFICIENT_FUNDS": "Card declined due to insufficient funds",
                "CARD_DECLINED": "Generic card issuer decline",
                "FRAUD_SUSPECTED": "Transaction flagged by fraud detection",
                "VELOCITY_EXCEEDED": "Too many transactions in short period"
            },
            "enterprise_procedures": [
                "Corporate card validation bypass for verified customers",
                "3DS exemption for trusted merchant transactions",
                "Manual payment verification for high-value orders",
                "Expedited payment retry with enhanced monitoring"
            ]
        }
    
    def _build_skill_prompt(self, skill_name: str, context: dict) -> str:
        if skill_name == "transaction-analysis":
            return self._build_transaction_analysis_prompt(context)
        elif skill_name == "payment-retry":
            return self._build_retry_strategy_prompt(context)
        else:
            return super()._build_skill_prompt(skill_name, context)
    
    def _build_transaction_analysis_prompt(self, context: dict) -> str:
        customer = context.get('customer', {})
        order = context.get('order', {})
        failure_details = context.get('failure_details', {})
        coordination_context = context.get('coordination_context', '')
        incident_type = context.get('incident_type', 'unknown')
        
        return f"""{self.agent_personality}

💳 PAYMENT AGENT DOMAIN OWNERSHIP:
I am responsible for analyzing and resolving:
✅ Payment gateway failures and timeouts
✅ Credit card processing errors 
✅ 3DS authentication issues
✅ Payment method validation problems
✅ Transaction routing and retries
✅ Payment processor communication issues
✅ Corporate card and enterprise payment flows

❌ NOT my responsibility:
- Customer fraud risk scoring
- Infrastructure server performance  
- Network connectivity issues
- Inventory allocation
- Business rule violations

MULTI-AGENT INCIDENT RESPONSE - PAYMENT ANALYSIS

INCIDENT TYPE: {incident_type}
INITIAL DOMAIN CHECK: First assess if this is a payment processing issue vs. fraud/technical/business issue.

{coordination_context}

CUSTOMER PROFILE:
- Name: {customer.get('name', 'N/A')}
- ID: {customer.get('id', 'N/A')} 
- Tier: {customer.get('tier', 'standard').title()}
- Account Value: ${customer.get('account_value', 0):,.2f}
- Member Since: {customer.get('established_since', 'N/A')}

PURCHASE HISTORY (if available):
{self._format_purchase_history(customer.get('purchase_history', {}))}

BUSINESS CONTEXT:
{self._format_business_context(customer.get('business_context', {}))}

CURRENT ORDER:
- Order ID: {order.get('id', 'N/A')}
- Amount: ${order.get('amount', 0):,.2f}
- Items: {self._format_order_items(order.get('items', []))}
- Justification: {order.get('business_justification', 'Standard purchase')}

PAYMENT FAILURE DETAILS:
- Transaction ID: {failure_details.get('transaction_id', 'N/A')}
- Error Code: {failure_details.get('error_code', 'UNKNOWN')}
- Gateway Response: {failure_details.get('gateway_response', 'N/A')}
- Payment Method: {failure_details.get('payment_method', 'N/A')}
- Timestamp: {failure_details.get('timestamp', 'N/A')}

TECHNICAL CONTEXT:
{self._format_technical_context(failure_details.get('technical_context', {}))}

ANALYSIS REQUIRED:
STEP 1 - DOMAIN ASSESSMENT: First determine if this is a payment processing issue within my expertise
STEP 2 - If payment-related: Analyze gateway, card processing, and authentication issues
STEP 3 - If not payment-related: Provide brief assessment but defer to appropriate team

Considering this customer's purchase history and business context, analyze the payment failure focusing on:
1. Technical vs. business process issues
2. Customer impact given their enterprise status and urgency
3. Coordination with fraud analysis (ensure your assessment aligns with security requirements)
4. Specific remediation strategies appropriate for this customer profile

Provide your analysis in JSON format:

```json
{{
  "domain_assessment": {{
    "is_payment_related": true,
    "confidence_in_domain": 0.95,
    "rationale": "why this is/isn't a payment processing issue",
    "primary_responsible_team": "payment|fraud|technical|order"
  }},
  "root_cause": "primary cause of the failure",
  "failure_category": "timeout|decline|fraud|system_error|authentication",
  "confidence": 0.95,
  "technical_analysis": {{
    "gateway_issue": "description of gateway-specific problems",
    "authentication_status": "3DS/verification status",
    "risk_factors": ["factor1", "factor2"],
    "system_health": "assessment of payment infrastructure"
  }},
  "customer_impact": {{
    "severity": "high|medium|low",
    "business_risk": "description of business impact",
    "urgency": "immediate|standard|low"
  }},
  "recommendations": [
    {{
      "action": "specific action to take",
      "priority": "high|medium|low", 
      "timeline": "immediate|hours|days",
      "success_probability": 0.90
    }}
  ],
  "retry_recommended": true,
  "strategy": "specific retry approach",
  "escalation_needed": false,
  "generate_artifact": true
}}
```"""

    def _build_retry_strategy_prompt(self, context: dict) -> str:
        return f"""{self.agent_personality}

PAYMENT RETRY STRATEGY REQUEST

Original Failure Analysis:
{context.get('original_failure', {})}

Customer Profile:
{context.get('customer_profile', {})}

Current Context:
{context.get('transaction_context', {})}

STRATEGY REQUIRED:
Develop an optimal retry strategy based on the failure analysis. Provide response in JSON format:

```json
{{
  "retry_strategy": "name of the strategy",
  "approach": "detailed description of retry approach",
  "modifications": [
    "specific changes to make for retry"
  ],
  "timing": {{
    "immediate": true,
    "delay_seconds": 0,
    "max_attempts": 3
  }},
  "success_probability": 0.95,
  "risk_assessment": {{
    "customer_experience": "impact on customer",
    "fraud_risk": "low|medium|high",
    "business_impact": "financial and operational impact"
  }},
  "fallback_options": [
    "alternative if retry fails"
  ],
  "monitoring_required": ["metric1", "metric2"],
  "generate_artifact": true
}}
```"""

if __name__ == "__main__":
    import uvicorn
    agent = SmartPaymentAgent()
    uvicorn.run(agent.app, host="0.0.0.0", port=8002) 