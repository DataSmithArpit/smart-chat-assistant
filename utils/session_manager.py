import streamlit as st
from typing import Dict, Any, List

class SessionManager:
    """Manages Streamlit session state and initialization"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables with defaults"""
        defaults = {
            'chat_history': [],
            'current_draft': "",
            'autocorrect_enabled': True,
            'api_configured': False,
            'dark_mode': False,
            'suggestions': "",
            'loading': False,
            'api_key': "",
            'chat_style': "💬 Casual",
            'reply_length': "📄 Medium",
            'ai_model': "🎯 Balanced",
            'generate_suggestions': False,
            'auto_fix_request': False,
            'send_message': False
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get session state value with optional default"""
        return st.session_state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set session state value"""
        st.session_state[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple session state values"""
        for key, value in updates.items():
            st.session_state[key] = value
    
    def clear_chat_history(self) -> None:
        """Clear chat history and related state"""
        self.update({
            'chat_history': [],
            'current_draft': "",
            'suggestions': ""
        })
    
    def add_message(self, message_type: str, text: str) -> None:
        """Add a message to chat history"""
        import time
        
        message = {
            'type': message_type,
            'text': text,
            'timestamp': time.time()
        }
        
        chat_history = self.get('chat_history', [])
        chat_history.append(message)
        self.set('chat_history', chat_history)
    
    def get_chat_context(self, max_messages: int = 6) -> str:
        """Get recent chat context for AI processing"""
        chat_history = self.get('chat_history', [])
        
        if not chat_history:
            return "Friend: Hey! How's your day going? 😊\n"
        
        context = ""
        for msg in chat_history[-max_messages:]:
            sender = "Friend" if msg['type'] == 'received' else "You"
            context += f"{sender}: {msg['text']}\n"
        
        return context
    
    def reset_action_flags(self) -> None:
        """Reset action trigger flags"""
        self.update({
            'generate_suggestions': False,
            'auto_fix_request': False,
            'send_message': False
        })