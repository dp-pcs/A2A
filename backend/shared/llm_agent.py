import asyncio
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx
from dotenv import load_dotenv
from shared.base_agent import BaseAgent

# Ensure environment variables are loaded
load_dotenv()

class LLMAgent(BaseAgent):
    """Base class for LLM-powered agents that can reason dynamically"""
    
    def __init__(self, agent_config: dict, llm_config: dict = None):
        super().__init__(agent_config)
        
        # Auto-detect best available LLM provider
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        # Default LLM Configuration with auto-selection
        if llm_config:
            self.llm_config = llm_config
        elif anthropic_key:
            self.llm_config = {
                "provider": "anthropic",
                "model": "claude-3-haiku-20240307",
                "api_key": anthropic_key,
                "max_tokens": 1000,
                "temperature": 0.1
            }
        elif openai_key:
            self.llm_config = {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "api_key": openai_key,
                "max_tokens": 1000,
                "temperature": 0.1
            }
        else:
            # Fallback - no API key available
            self.llm_config = {
                "provider": None,
                "model": None,
                "api_key": None,
                "max_tokens": 1000,
                "temperature": 0.1
            }
        
        # Agent personality and context
        self.agent_personality = self._get_agent_personality()
        self.knowledge_base = self._get_knowledge_base()
        
    def _get_agent_personality(self) -> str:
        """Define the agent's personality and role - override in subclasses"""
        return f"""You are {self.config['name']}, an AI agent specializing in {self.config['description']}.
        
You work for LatentGenius AI Solutions, a technology company that provides AI computing clusters and services.
You are part of a multi-agent customer service system and communicate with other agents to resolve incidents.

Your role is professional, analytical, and solution-focused. You provide specific, actionable recommendations
based on data and established procedures."""

    def _get_knowledge_base(self) -> dict:
        """Define agent-specific knowledge - override in subclasses"""
        return {
            "company": "LatentGenius AI Solutions",
            "domain": "AI computing infrastructure and services",
            "procedures": [],
            "tools": [],
            "escalation_paths": []
        }
    
    async def execute_skill(self, skill_name: str, context: dict, task_id: str) -> dict:
        """Execute skill using LLM reasoning or fallback to base implementation"""
        
        # Check if we have LLM capabilities
        if self.llm_config["provider"] is None:
            # Fall back to base agent implementation
            return await super().execute_skill(skill_name, context, task_id)
        
        # Build prompt for the specific skill and context
        prompt = self._build_skill_prompt(skill_name, context)
        
        # Send progress update
        await self.send_progress_update(task_id, 25, f"Analyzing {skill_name} request...")
        
        try:
            # Get LLM response
            llm_response = await self._call_llm(prompt)
            
            await self.send_progress_update(task_id, 75, "Processing analysis results...")
            
            # Parse and structure the response
            result = self._process_llm_response(skill_name, llm_response, context)
            
            # Generate artifacts if needed
            if result.get("generate_artifact"):
                artifact = self._generate_artifact(skill_name, result, task_id)
                await self.send_artifact_ready(task_id, artifact, "Analysis report generated")
            
            await self.send_progress_update(task_id, 100, f"{skill_name} analysis complete")
            
            return result
            
        except Exception as e:
            print(f"LLM call failed: {e}, falling back to base implementation")
            # Fall back to base agent implementation
            return await super().execute_skill(skill_name, context, task_id)
    
    def _build_skill_prompt(self, skill_name: str, context: dict) -> str:
        """Build LLM prompt for specific skill - override in subclasses"""
        return f"""
{self.agent_personality}

TASK: {skill_name}
CONTEXT: {json.dumps(context, indent=2)}

Please analyze this situation and provide a structured response.
"""
    
    async def _call_llm(self, prompt: str) -> str:
        """Call the configured LLM API"""
        
        if self.llm_config["provider"] == "anthropic":
            return await self._call_anthropic(prompt)
        elif self.llm_config["provider"] == "openai":
            return await self._call_openai(prompt)
        elif self.llm_config["provider"] is None:
            raise ValueError("No LLM provider configured - missing API keys")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_config['provider']}")
    
    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        
        headers = {
            "x-api-key": self.llm_config["api_key"],
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.llm_config["model"],
            "max_tokens": self.llm_config["max_tokens"],
            "temperature": self.llm_config["temperature"],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["content"][0]["text"]
            else:
                raise Exception(f"Anthropic API error: {response.status_code} - {response.text}")
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        
        headers = {
            "Authorization": f"Bearer {self.llm_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.llm_config["model"],
            "messages": [
                {
                    "role": "system",
                    "content": self.agent_personality
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": self.llm_config["max_tokens"],
            "temperature": self.llm_config["temperature"]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
    
    def _process_llm_response(self, skill_name: str, llm_response: str, context: dict) -> dict:
        """Process LLM response into structured result - override in subclasses"""
        
        # Try to extract JSON if present
        try:
            # Look for JSON blocks in the response
            import re
            json_match = re.search(r'```json\n(.*?)\n```', llm_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Try to parse the entire response as JSON
            return json.loads(llm_response)
            
        except json.JSONDecodeError:
            # Fallback to text response
            return {
                "analysis": llm_response,
                "confidence": 0.8,
                "recommendations": ["Review analysis for specific actions"],
                "generate_artifact": False
            }
    
    def _generate_artifact(self, skill_name: str, result: dict, task_id: str) -> dict:
        """Generate artifact from analysis result"""
        
        return {
            "type": "analysis_report",
            "url": f"https://artifacts.latentgenius.ai/{skill_name}-{task_id}.json",
            "format": "application/json",
            "summary": f"{skill_name} analysis completed",
            "data": result
        } 