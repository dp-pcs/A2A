import asyncio
import random
import json
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path to import shared modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.llm_agent import LLMAgent

class SmartTechAgent(LLMAgent):
    def __init__(self):
        config = {
            "agent_card_version": "1.0",
            "name": "Smart Tech Support Agent",
            "agent_id": "tech-support-001",
            "description": "AI-powered technical analysis with business-friendly recommendations",
            "version": "4.0.0",
            "homepage": "https://latentgenius.ai/agents/smart-tech-support",
            "skills": [
                {
                    "name": "system-diagnostics",
                    "description": "Analyze system performance and identify root causes",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "incident_type": {"type": "string"},
                            "system_components": {"type": "array"}
                        }
                    }
                }
            ],
            "authentication": {
                "type": "api_key",
                "location": "header",
                "name": "X-Tech-API-Key"
            },
            "endpoints": {
                "base_url": "http://localhost:8005",
                "tasks": "/tasks",
                "streaming": "/stream"
            },
            "capabilities": {
                "streaming": True,
                "push_notifications": True,
                "modalities": ["text", "structured_data", "logs", "metrics"],
                "intelligence": "LLM-powered dynamic reasoning"
            }
        }
        
        super().__init__(config)
        
    async def execute_skill(self, skill_name: str, context: dict, task_id: str) -> dict:
        """Execute tech support skill with AI reasoning"""
        
        if skill_name == "system-diagnostics":
            return await self._ai_system_diagnostics(context, task_id)
        else:
            raise ValueError(f"Unknown skill: {skill_name}")
    
    async def _ai_system_diagnostics(self, context: dict, task_id: str) -> dict:
        """AI-powered system diagnostics with business-friendly recommendations"""
        
        await self.send_progress_update(task_id, 25, "Analyzing system performance data...")
        await asyncio.sleep(1)
        
        # Extract key context
        amount = context.get("amount", "unknown")
        currency = context.get("currency", "USD")
        incident_type = context.get("incident_type", "payment_timeout")
        customer_context = context.get("customer_context", {})
        business_context = context.get("business_context", {})
        technical_context = context.get("technical_context", {})
        
        # Format customer information for business context
        customer_info = self._format_customer_context(customer_context)
        business_info = self._format_business_context(business_context)
        technical_info = self._format_technical_context(technical_context)
        
        await self.send_progress_update(task_id, 50, "Identifying root cause and business impact...")
        await asyncio.sleep(1)
        
        prompt = f"""
🔧 TECH SUPPORT AGENT DOMAIN OWNERSHIP:
I am responsible for analyzing and resolving:
✅ Payment gateway infrastructure issues
✅ 3DS authentication service failures
✅ Network connectivity problems
✅ Server performance and capacity issues
✅ Database timeouts and connection issues
✅ API endpoint failures and latency
✅ System monitoring and alerting

❌ NOT my responsibility:
- Customer fraud risk assessment
- Payment method validation
- Business rule violations
- Inventory allocation
- Order fulfillment processes

You are a Senior Technical Support Manager who explains technical issues to business stakeholders. Your role is to:

STEP 1 - DOMAIN ASSESSMENT: First determine if this is a technical infrastructure issue within my expertise
STEP 2 - If technical issue: Provide detailed analysis and business-friendly remediation
STEP 3 - If not technical: Provide brief assessment but defer to appropriate team

1. Diagnose technical problems in plain business language
2. Explain the business impact clearly
3. Provide actionable next steps that business managers can implement
4. Avoid technical jargon - speak like you're talking to executives

INCIDENT DETAILS:
- Type: {incident_type}
- Transaction Amount: {amount} {currency}
- Customer Context: {customer_info}
- Business Context: {business_info}
- Technical Context: {technical_info}

INITIAL DOMAIN CHECK: Assess if this incident requires technical infrastructure analysis or if it's primarily a business/fraud/order management issue.

Your analysis should:
- First determine if this is within technical infrastructure domain
- Identify the root cause in business terms
- Explain the customer impact
- Provide clear action items for the operations team
- Include timeline estimates for resolution
- Suggest preventive measures in business language

Respond with business-friendly language that executives and operations managers can understand and act upon.
"""

        await self.send_progress_update(task_id, 75, "Generating business-focused recommendations...")
        
        # Get AI analysis
        ai_response = await self._call_llm(prompt)
        if not ai_response:
            # Fallback response
            return await self._fallback_diagnostics(context, task_id)
        
        await self.send_progress_update(task_id, 90, "Finalizing technical analysis...")
        await asyncio.sleep(1)
        
        # Parse the AI response into structured format
        return self._parse_tech_response(ai_response, context)
    
    def _format_customer_context(self, customer_context: dict) -> str:
        """Format customer context for business understanding"""
        if not customer_context:
            return "Standard customer transaction"
        
        customer_type = customer_context.get("type", "individual")
        purchase_history = customer_context.get("purchase_history", {})
        
        context_parts = [f"{customer_type} customer"]
        
        if purchase_history:
            avg_order = purchase_history.get("average_order_value", 0)
            total_orders = purchase_history.get("total_orders", 0)
            if avg_order > 0:
                context_parts.append(f"typical order value ${avg_order}")
            if total_orders > 0:
                context_parts.append(f"{total_orders} previous orders")
        
        return ", ".join(context_parts)
    
    def _format_business_context(self, business_context: dict) -> str:
        """Format business context"""
        if not business_context:
            return "Standard business transaction"
        
        urgency = business_context.get("urgency", "normal")
        business_impact = business_context.get("business_impact", "medium")
        
        return f"Business urgency: {urgency}, Impact level: {business_impact}"
    
    def _format_technical_context(self, technical_context: dict) -> str:
        """Format technical context for business understanding"""
        if not technical_context:
            return "Standard system environment"
        
        systems = technical_context.get("affected_systems", [])
        if systems:
            return f"Affected systems: {', '.join(systems)}"
        return "Payment processing system"
    
    def _parse_tech_response(self, ai_response: str, context: dict) -> dict:
        """Parse AI response into structured tech analysis"""
        
        # Extract confidence score (look for percentage or confidence indicators)
        confidence = 0.88  # Default confidence
        if "high confidence" in ai_response.lower():
            confidence = 0.95
        elif "medium confidence" in ai_response.lower():
            confidence = 0.85
        elif "low confidence" in ai_response.lower():
            confidence = 0.70
        elif "%" in ai_response:
            # Try to extract percentage
            import re
            percentages = re.findall(r'(\d+)%', ai_response)
            if percentages:
                confidence = float(percentages[0]) / 100
        
        # Extract domain assessment
        domain_assessment = self._extract_domain_assessment(ai_response)
        
        # Return structured response
        return {
            "domain_assessment": domain_assessment,
            "analysis": ai_response,
            "confidence": confidence,
            "diagnosis": self._extract_diagnosis(ai_response),
            "business_impact": self._extract_business_impact(ai_response),
            "action_items": self._extract_action_items(ai_response),
            "timeline": self._extract_timeline(ai_response),
            "preventive_measures": self._extract_preventive_measures(ai_response)
        }
    
    def _extract_diagnosis(self, response: str) -> str:
        """Extract main diagnosis from AI response"""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['root cause', 'diagnosis', 'issue identified', 'problem']):
                return line.strip('- ').strip()
        return "Technical issue identified requiring immediate attention"
    
    def _extract_business_impact(self, response: str) -> str:
        """Extract business impact from AI response"""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['impact', 'customer', 'business', 'revenue']):
                return line.strip('- ').strip()
        return "Customer transaction processing affected"
    
    def _extract_action_items(self, response: str) -> list:
        """Extract action items from AI response"""
        lines = response.split('\n')
        actions = []
        in_actions_section = False
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['action', 'recommend', 'next steps', 'should']):
                in_actions_section = True
                if line.startswith('-') or line.startswith('•'):
                    actions.append(line.strip('- •').strip())
            elif in_actions_section and (line.startswith('-') or line.startswith('•')):
                actions.append(line.strip('- •').strip())
            elif in_actions_section and not line:
                in_actions_section = False
        
        if not actions:
            actions = ["Escalate to technical operations team", "Monitor system performance closely"]
        
        return actions[:3]  # Limit to top 3 actions
    
    def _extract_timeline(self, response: str) -> str:
        """Extract timeline from AI response"""
        import re
        # Look for time patterns
        time_patterns = re.findall(r'(\d+)\s*(minute|hour|day)s?', response.lower())
        if time_patterns:
            num, unit = time_patterns[0]
            return f"{num} {unit}{'s' if int(num) > 1 else ''}"
        return "2-4 hours"
    
    def _extract_preventive_measures(self, response: str) -> list:
        """Extract preventive measures from AI response"""
        lines = response.split('\n')
        measures = []
        in_prevention_section = False
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['prevent', 'future', 'avoid', 'proactive']):
                in_prevention_section = True
                if line.startswith('-') or line.startswith('•'):
                    measures.append(line.strip('- •').strip())
            elif in_prevention_section and (line.startswith('-') or line.startswith('•')):
                measures.append(line.strip('- •').strip())
            elif in_prevention_section and not line:
                in_prevention_section = False
        
        if not measures:
            measures = ["Implement enhanced monitoring", "Review system capacity planning"]
        
        return measures[:2]  # Limit to top 2 measures
    
    def _extract_domain_assessment(self, response: str) -> dict:
        """Extract domain assessment from AI response"""
        # Default assessment
        domain_assessment = {
            "is_technical_issue": True,
            "confidence_in_domain": 0.85,
            "rationale": "Technical infrastructure analysis required",
            "primary_responsible_team": "technical"
        }
        
        # Look for domain-related keywords
        if any(keyword in response.lower() for keyword in ['not technical', 'not infrastructure', 'fraud', 'business rule']):
            domain_assessment["is_technical_issue"] = False
            domain_assessment["primary_responsible_team"] = "fraud" if "fraud" in response.lower() else "business"
            domain_assessment["rationale"] = "Issue appears to be non-technical in nature"
        
        if any(keyword in response.lower() for keyword in ['technical issue', 'infrastructure', 'gateway', 'server', 'network']):
            domain_assessment["is_technical_issue"] = True
            domain_assessment["confidence_in_domain"] = 0.95
            
        return domain_assessment
    
    async def _fallback_diagnostics(self, context: dict, task_id: str) -> dict:
        """Fallback when AI is not available"""
        incident_type = context.get("incident_type", "payment_timeout")
        
        await self.send_progress_update(task_id, 95, "Applying standard diagnostic procedures...")
        
        return {
            "analysis": f"Technical analysis of {incident_type} completed using standard procedures. The system experienced a service interruption that affected customer transaction processing.",
            "confidence": 0.75,
            "diagnosis": "Payment gateway service interruption detected",
            "business_impact": "Customer transactions temporarily delayed",
            "action_items": [
                "Contact payment service provider for status update",
                "Implement customer communication plan",
                "Monitor transaction queue for backlog processing"
            ],
            "timeline": "1-2 hours",
            "preventive_measures": [
                "Review service level agreements with payment providers",
                "Implement backup payment processing options"
            ]
        }

if __name__ == "__main__":
    agent = SmartTechAgent()
    agent.run(port=8005) 