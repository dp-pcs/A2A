import sys
import os

# Add the parent directory to the path to import shared modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.llm_agent import LLMAgent

class SmartFraudAgent(LLMAgent):
    """LLM-powered fraud detection agent that analyzes security threats dynamically"""
    
    def __init__(self):
        config = {
            "agent_card_version": "1.0",
            "name": "Smart Fraud Detection Agent",
            "agent_id": "fraud-detect-001",
            "description": "Advanced fraud analysis and security threat assessment using AI reasoning",
            "version": "5.0.0",
            "homepage": "https://latentgenius.ai/agents/smart-fraud-detection",
            "skills": [
                {
                    "name": "risk-assessment",
                    "description": "Comprehensive risk analysis using behavioral patterns and threat intelligence",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "transaction_amount": {"type": "number"},
                            "transaction_context": {"type": "object"},
                            "customer_history": {"type": "object"},
                            "security_indicators": {"type": "object"}
                        }
                    }
                },
                {
                    "name": "fraud-investigation",
                    "description": "Deep dive investigation into suspected fraudulent activities",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "incident_details": {"type": "object"},
                            "evidence": {"type": "object"},
                            "timeline": {"type": "array"}
                        }
                    }
                },
                {
                    "name": "security-assessment",
                    "description": "Evaluate security posture and recommend protective measures",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "security_event": {"type": "object"},
                            "system_context": {"type": "object"},
                            "threat_indicators": {"type": "array"}
                        }
                    }
                }
            ],
            "authentication": {
                "type": "oauth2",
                "scopes": ["fraud.read", "risk.assess", "security.analyze"]
            },
            "endpoints": {
                "base_url": "http://localhost:8003",
                "tasks": "/tasks",
                "streaming": "/stream"
            },
            "capabilities": {
                "streaming": True,
                "push_notifications": True,
                "modalities": ["text", "structured_data", "behavioral_analysis"]
            }
        }
        
        super().__init__(config)
        
    def _format_fraud_purchase_history(self, history: dict) -> str:
        if not history:
            return "- No purchase history available for analysis"
        
        lines = []
        if 'average_order_value' in history:
            lines.append(f"- Average Order Value: ${history['average_order_value']:,.2f}")
        if 'largest_previous_order' in history:
            lines.append(f"- Largest Previous Order: ${history['largest_previous_order']:,.2f}")
        if 'monthly_volume' in history:
            lines.append(f"- Monthly Order Frequency: {history['monthly_volume']} transactions")
        if 'preferred_payment' in history:
            lines.append(f"- Established Payment Method: {history['preferred_payment']}")
        if 'last_successful_transaction' in history:
            lines.append(f"- Last Successful Payment: {history['last_successful_transaction']}")
        
        return '\n'.join(lines) if lines else "- No detailed purchase pattern available"
    
    def _format_fraud_business_context(self, context: dict) -> str:
        if not context:
            return "- No business context available for verification"
        
        lines = []
        if 'industry' in context:
            lines.append(f"- Industry Sector: {context['industry']}")
        if 'use_case' in context:
            lines.append(f"- Business Use Case: {context['use_case']}")
        if 'urgency' in context:
            lines.append(f"- Business Urgency: {context['urgency']}")
        
        return '\n'.join(lines) if lines else "- Standard business context"
    
    def _format_order_items(self, items: list) -> str:
        if not items:
            return "No items specified"
        
        return ', '.join([f"{item.get('name', 'Unknown Item')} x{item.get('quantity', 1)}" for item in items])
        
    def _get_agent_personality(self) -> str:
        return """You are the Smart Fraud Detection Agent for LatentGenius AI Solutions.

You are an expert in cybersecurity, fraud detection, and risk assessment for enterprise technology transactions.
You analyze behavioral patterns, assess security threats, and provide strategic risk mitigation recommendations.

EXPERTISE AREAS:
- Advanced fraud pattern recognition
- Account takeover and identity theft detection  
- Corporate payment fraud and business email compromise
- Insider threat assessment
- Multi-factor authentication and access security
- Threat intelligence and behavioral analytics

ANALYSIS FRAMEWORK:
1. Collect and correlate security indicators
2. Analyze behavioral deviations and anomalies
3. Assess threat probability and impact
4. Evaluate customer legitimacy and history
5. Recommend risk mitigation strategies
6. Provide continuous monitoring guidance

You approach each case with professional skepticism while balancing security with customer experience.
You provide clear risk ratings with detailed justifications and actionable security recommendations."""

    def _get_knowledge_base(self) -> dict:
        return {
            "company": "LatentGenius AI Solutions",
            "domain": "AI computing infrastructure security and fraud prevention",
            "threat_categories": [
                "payment_fraud",
                "account_takeover", 
                "business_email_compromise",
                "insider_threat",
                "synthetic_identity",
                "velocity_abuse"
            ],
            "risk_factors": {
                "high_risk": ["new_customer", "unusual_location", "large_amount", "velocity_spike"],
                "medium_risk": ["payment_method_change", "unusual_hours", "proxy_usage"],
                "low_risk": ["established_customer", "normal_pattern", "verified_device"]
            },
            "security_controls": [
                "Multi-factor authentication verification",
                "Device fingerprinting and recognition", 
                "Behavioral biometrics analysis",
                "Geographic and velocity checks",
                "Corporate verification workflows",
                "Real-time threat intelligence"
            ]
        }
    
    def _build_skill_prompt(self, skill_name: str, context: dict) -> str:
        if skill_name == "risk-assessment":
            return self._build_risk_assessment_prompt(context)
        elif skill_name == "fraud-investigation":
            return self._build_fraud_investigation_prompt(context)
        elif skill_name == "security-assessment":
            return self._build_security_assessment_prompt(context)
        else:
            return super()._build_skill_prompt(skill_name, context)
    
    def _build_risk_assessment_prompt(self, context: dict) -> str:
        customer = context.get('customer', {})
        order = context.get('order', {})
        failure_details = context.get('failure_details', {})
        coordination_context = context.get('coordination_context', '')
        incident_type = context.get('incident_type', 'unknown')
        
        return f"""{self.agent_personality}

🔒 FRAUD AGENT DOMAIN OWNERSHIP:
I am responsible for analyzing:
✅ Customer behavior and transaction patterns
✅ Account security and authentication issues  
✅ Payment fraud and identity verification
✅ Risk scoring and threat assessment
✅ Suspicious activity and velocity monitoring

❌ NOT my responsibility:
- Payment gateway technical failures
- 3DS authentication server issues
- Network connectivity problems
- Database performance issues
- Infrastructure monitoring

MULTI-AGENT INCIDENT RESPONSE - FRAUD RISK ASSESSMENT

INCIDENT TYPE: {incident_type}
INITIAL DOMAIN CHECK: First, I need to assess if this incident requires fraud analysis or if it's purely a technical/infrastructure issue.

{coordination_context}

CUSTOMER PROFILE & LEGITIMACY ANALYSIS:
- Name: {customer.get('name', 'N/A')}
- Customer ID: {customer.get('id', 'N/A')}
- Tier: {customer.get('tier', 'standard').title()} Customer
- Account Value: ${customer.get('account_value', 0):,.2f}
- Established: {customer.get('established_since', 'N/A')}

PURCHASE PATTERN ANALYSIS:
{self._format_fraud_purchase_history(customer.get('purchase_history', {}))}

BUSINESS LEGITIMACY FACTORS:
{self._format_fraud_business_context(customer.get('business_context', {}))}

CURRENT TRANSACTION UNDER REVIEW:
- Order ID: {order.get('id', 'N/A')}
- Amount: ${order.get('amount', 0):,.2f}
- Items: {self._format_order_items(order.get('items', []))}
- Business Justification: {order.get('business_justification', 'None provided')}

PAYMENT FAILURE CONTEXT:
- Transaction ID: {failure_details.get('transaction_id', 'N/A')}
- Error: {failure_details.get('error_code', 'UNKNOWN')}
- Payment Method: {failure_details.get('payment_method', 'N/A')}
- Technical Details: {failure_details.get('gateway_response', 'N/A')}

FRAUD ANALYSIS FOCUS:
STEP 1 - DOMAIN ASSESSMENT: First determine if this incident requires fraud analysis
STEP 2 - If fraud-related: Assess customer behavior, account security, and transaction patterns
STEP 3 - If not fraud-related: Provide brief assessment but defer to appropriate technical team

Given this customer's established history and business profile, assess whether this transaction represents:
1. Legitimate business activity consistent with their profile
2. Account compromise or unauthorized access  
3. Payment processing issues vs. fraud concerns
4. Risk mitigation needs while maintaining customer experience

RISK ANALYSIS REQUIRED:
Analyze the fraud risk for this transaction and provide assessment in JSON format:

```json
{{
  "domain_assessment": {{
    "is_fraud_related": true,
    "confidence_in_domain": 0.95,
    "rationale": "why this is/isn't a fraud concern",
    "primary_responsible_team": "fraud|payment|technical|order"
  }},
  "overall_risk_score": 0.75,
  "risk_level": "HIGH|MEDIUM|LOW",
  "confidence": 0.92,
  "recommendation": "APPROVE|REVIEW|DECLINE|ESCALATE",
  "fraud_indicators": {{
    "behavioral_anomalies": ["specific deviations from normal behavior"],
    "technical_red_flags": ["device, location, or technical concerns"],
    "pattern_matches": ["known fraud patterns detected"],
    "velocity_concerns": ["transaction frequency or amount concerns"]
  }},
  "customer_analysis": {{
    "legitimacy_score": 0.85,
    "verification_status": "verified|pending|unverified",
    "relationship_strength": "strong|moderate|weak|new",
    "historical_behavior": "consistent|mixed|concerning"
  }},
  "security_assessment": {{
    "authentication_strength": "strong|moderate|weak",
    "device_trust": "trusted|unknown|suspicious",
    "location_analysis": "expected|unusual|high_risk",
    "access_pattern": "normal|irregular|suspicious"
  }},
  "recommendations": [
    {{
      "action": "specific security action",
      "priority": "immediate|high|medium|low",
      "rationale": "why this action is needed"
    }}
  ],
  "monitoring_required": ["ongoing monitoring recommendations"],
  "escalation_triggers": ["conditions that require escalation"],
  "generate_artifact": true
}}
```"""

    def _build_fraud_investigation_prompt(self, context: dict) -> str:
        return f"""{self.agent_personality}

FRAUD INVESTIGATION REQUEST

Incident Details:
{context.get('incident_details', {})}

Evidence Collected:
{context.get('evidence', {})}

Timeline of Events:
{context.get('timeline', [])}

INVESTIGATION REQUIRED:
Conduct thorough fraud investigation and provide findings in JSON format:

```json
{{
  "investigation_summary": "overview of findings",
  "fraud_probability": 0.85,
  "fraud_type": "specific type of fraud detected",
  "attack_vector": "how the fraud was attempted",
  "evidence_analysis": {{
    "strong_indicators": ["definitive evidence of fraud"],
    "circumstantial_evidence": ["supporting but not conclusive evidence"],
    "inconsistencies": ["contradictory or suspicious elements"],
    "timeline_analysis": "analysis of event sequence"
  }},
  "threat_assessment": {{
    "sophistication_level": "basic|intermediate|advanced",
    "organized_crime": "likely individual|small group|organized operation",
    "repeat_offender": "first time|repeat|professional",
    "threat_to_others": "isolated|potential for additional victims"
  }},
  "financial_impact": {{
    "direct_loss": 0,
    "potential_loss_prevented": 0,
    "investigation_cost": "estimated resource investment"
  }},
  "recommended_actions": [
    {{
      "action": "specific action to take",
      "urgency": "immediate|urgent|standard",
      "owner": "who should execute this action"
    }}
  ],
  "case_status": "confirmed_fraud|suspected_fraud|false_positive|inconclusive",
  "generate_artifact": true
}}
```"""

    def _build_security_assessment_prompt(self, context: dict) -> str:
        return f"""{self.agent_personality}

SECURITY ASSESSMENT REQUEST

Security Event:
{context.get('security_event', {})}

System Context:
{context.get('system_context', {})}

Threat Indicators:
{context.get('threat_indicators', [])}

SECURITY ANALYSIS REQUIRED:
Evaluate security posture and threats, provide assessment in JSON format:

```json
{{
  "security_status": "secure|at_risk|compromised|unknown",
  "threat_level": "critical|high|medium|low",
  "vulnerability_assessment": {{
    "critical_vulnerabilities": ["immediate security gaps"],
    "potential_weaknesses": ["areas of concern"],
    "security_strengths": ["effective controls in place"],
    "compliance_status": "compliant|non_compliant|partial"
  }},
  "threat_analysis": {{
    "active_threats": ["current threats detected"],
    "potential_threats": ["likely future threats"],
    "attack_likelihood": 0.65,
    "impact_assessment": "description of potential impact"
  }},
  "security_recommendations": [
    {{
      "control": "specific security control",
      "priority": "critical|high|medium|low",
      "implementation_timeline": "immediate|weeks|months",
      "resource_requirement": "effort needed to implement"
    }}
  ],
  "monitoring_enhancements": ["additional monitoring recommendations"],
  "incident_response": "required incident response actions",
  "generate_artifact": true
}}
```"""

if __name__ == "__main__":
    import uvicorn
    agent = SmartFraudAgent()
    uvicorn.run(agent.app, host="0.0.0.0", port=8003) 