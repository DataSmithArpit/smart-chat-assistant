import httpx
from groq import Groq
from typing import Dict, List, Optional
import time
import streamlit as st
from config.settings import AppConfig

class AIClient:
    """Wrapper for Groq AI API with error handling and rate limiting"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.config = AppConfig()
        self.http_client = httpx.Client(verify=False)
        self.client = Groq(api_key=api_key, http_client=self.http_client)
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_delay = self.config.API_CONFIG['rate_limit_delay']
        
        if time_since_last < min_delay:
            time.sleep(min_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _build_system_prompt(self, style: str, length: str, task_type: str = "chat") -> str:
        """Build system prompt based on settings and task type"""
        style_text = self.config.get_style_prompt(style)
        length_text = self.config.get_length_prompt(length)
        
        if task_type == "suggestions":
            return f"""You are a helpful chat assistant. Provide natural, engaging suggestions that fit the conversation context. 
            Style: {style_text}
            Length: {length_text}
            
            Always format your response as:
            **✨ Improved:** [enhanced version]
            **💡 Option 1:** [alternative 1] 
            **💡 Option 2:** [alternative 2]"""
        
        elif task_type == "grammar":
            return f"Fix grammar and spelling. Make it sound {style_text}. Keep the same meaning. Return only the corrected text."
        
        else:
            return f"You are a helpful chat assistant. Respond in a {style_text} manner with {length_text} responses."
    
    def generate_chat_response(self, message: str, context: str = "", settings: Dict = None) -> str:
        """Generate a chat response"""
        if settings is None:
            settings = self.config.DEFAULTS
        
        try:
            self._rate_limit()
            
            system_prompt = self._build_system_prompt(
                settings.get('style', '💬 Casual'),
                settings.get('length', '📄 Medium'),
                "chat"
            )
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\nUser message: {message}"}
            ]
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.config.get_model_name(settings.get('model', '🎯 Balanced')),
                max_tokens=settings.get('max_tokens', 400),
                temperature=settings.get('temperature', 0.7)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._handle_error(e)
    
    def generate_suggestions(self, user_input: str, context: str = "", settings: Dict = None) -> str:
        """Generate message suggestions"""
        if settings is None:
            settings = self.config.DEFAULTS
        
        try:
            self._rate_limit()
            
            system_prompt = self._build_system_prompt(
                settings.get('style', '💬 Casual'),
                settings.get('length', '📄 Medium'),
                "suggestions"
            )
            
            full_context = f"""
            Conversation context:
            {context}
            
            The user is drafting: "{user_input}"
            
            Please provide:
            1. An improved version of their draft (if grammar/style needs fixing)
            2. 2 alternative reply suggestions
            
            Style: {self.config.get_style_prompt(settings.get('style', '💬 Casual'))}
            Length: {self.config.get_length_prompt(settings.get('length', '📄 Medium'))}
            """
            
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_context}
                ],
                model=self.config.get_model_name(settings.get('model', '🎯 Balanced')),
                max_tokens=settings.get('max_tokens', 400),
                temperature=settings.get('temperature', 0.7)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._handle_error(e)
    
    def fix_grammar(self, text: str, settings: Dict = None) -> str:
        """Fix grammar and style of text"""
        if settings is None:
            settings = self.config.DEFAULTS
        
        try:
            self._rate_limit()
            
            # Simplified grammar fix prompt
            simple_prompt = f"Fix grammar and spelling errors in this text. Keep the same meaning and style. Only return the corrected text: {text}"
            
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": simple_prompt}
                ],
                model="llama-3.1-8b-instant",  # Use fastest model
                max_tokens=200,
                temperature=0.1  # Low temperature for consistency
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Return original text if fixing fails
            return text
    
    def analyze_conversation_mood(self, messages: List[Dict], settings: Dict = None) -> Dict:
        """Analyze the mood/tone of conversation"""
        if not messages or settings is None:
            return {"mood": "neutral", "confidence": 0.5, "suggestions": []}
        
        try:
            self._rate_limit()
            
            # Build conversation context
            context = ""
            for msg in messages[-5:]:  # Last 5 messages
                sender = "Friend" if msg.get('type') == 'received' else "You"
                context += f"{sender}: {msg.get('text', '')}\n"
            
            system_prompt = """Analyze the mood and tone of this conversation. 
            Return a JSON object with:
            - mood: (positive/negative/neutral/excited/confused/romantic/professional)
            - confidence: (0.0-1.0)
            - suggestions: [list of 2-3 response suggestions that match the mood]
            
            Keep suggestions brief and contextually appropriate."""
            
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Conversation:\n{context}"}
                ],
                model="llama-3.1-8b-instant",  # Use faster model for analysis
                max_tokens=200,
                temperature=0.3
            )
            
            import json
            result = json.loads(response.choices[0].message.content.strip())
            return result
            
        except Exception as e:
            return {"mood": "neutral", "confidence": 0.5, "suggestions": [], "error": str(e)}
    
    def validate_api_key(self) -> bool:
        """Validate if the API key is working"""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model="llama-3.1-8b-instant",
                max_tokens=5
            )
            return True
        except Exception:
            return False
    
    def _handle_error(self, error: Exception) -> str:
        """Handle and format API errors"""
        error_str = str(error).lower()
        
        if "api key" in error_str or "unauthorized" in error_str:
            return "❌ Invalid API key. Please check your key."
        elif "rate limit" in error_str or "too many requests" in error_str:
            return "⏱️ Rate limit reached. Please wait a moment."
        elif "network" in error_str or "connection" in error_str:
            return "🌐 Network error. Please check your connection."
        elif "server" in error_str or "500" in error_str or "model" in error_str:
            return "🚫 Server/Model error. Trying backup model..."
        else:
            return f"❌ Error: {str(error)}"
    
    def get_model_info(self) -> Dict:
        """Get information about available models"""
        return {
            "⚡ Fast": {
                "name": "llama-3.1-8b-instant",
                "description": "Fastest responses, good for quick interactions",
                "speed": "⚡⚡⚡",
                "quality": "⭐⭐",
                "context": "8K tokens"
            },
            "🧠 Smart": {
                "name": "llama-3.1-70b-versatile", 
                "description": "Highest quality responses, best for complex tasks",
                "speed": "⚡",
                "quality": "⭐⭐⭐",
                "context": "32K tokens"
            },
            "🎯 Balanced": {
                "name": "mixtral-8x7b-32768",
                "description": "Good balance of speed and quality",
                "speed": "⚡⚡",
                "quality": "⭐⭐⭐",
                "context": "32K tokens"
            }
        }
    
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'http_client'):
            self.http_client.close()