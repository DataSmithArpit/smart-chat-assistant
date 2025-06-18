import streamlit as st
import httpx
from groq import Groq
import time

class AuthHandler:
    """Handles API key authentication and setup"""
    
    def __init__(self):
        self.session_manager = self._get_session_manager()
    
    def _get_session_manager(self):
        """Get session manager instance"""
        from utils.session_manager import SessionManager
        return SessionManager()
    
    def is_authenticated(self) -> bool:
        """Check if user has valid API configuration"""
        return self.session_manager.get('api_configured', False)
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate the provided API key"""
        try:
            http_client = httpx.Client(verify=False)
            client = Groq(api_key=api_key.strip(), http_client=http_client)
            
            # Test the API key with a simple request
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model="llama-3.1-8b-instant",
                max_tokens=5
            )
            return True
        except Exception:
            return False
    
    def save_api_key(self, api_key: str) -> bool:
        """Save and configure the API key"""
        if self.validate_api_key(api_key):
            self.session_manager.update({
                'api_key': api_key,
                'api_configured': True
            })
            return True
        return False
    
    def render_setup_screen(self):
        """Render the API key setup interface"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">🔑 Quick Setup</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            api_key = st.text_input(
                "",
                placeholder="Paste your free Groq API key here...",
                type="password",
                help="Get free key from console.groq.com",
                key="api_key_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Save", key="save_api"):
                if api_key:
                    with st.spinner("Validating API key..."):
                        if self.save_api_key(api_key):
                            st.success("🚀 Ready to chat!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid API key")
                else:
                    st.error("Please enter an API key")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # API Key Information
        self._render_api_info()
    
    def _render_api_info(self):
        """Render API key information section"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">🆓 Get FREE API Key</h3>', unsafe_allow_html=True)
        st.markdown("""
        **Quick Steps:**
        1. 🌐 Visit [console.groq.com](https://console.groq.com)
        2. 📝 Sign up (free account)
        3. 🔑 Create API key
        4. 📋 Paste above
        
        **🎁 Completely FREE:** 14,400 requests/day!
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    def logout(self):
        """Clear authentication and reset session"""
        self.session_manager.update({
            'api_key': "",
            'api_configured': False
        })
        st.rerun()
    
    def get_client(self):
        """Get authenticated Groq client"""
        if not self.is_authenticated():
            raise Exception("Not authenticated")
        
        api_key = self.session_manager.get('api_key')
        http_client = httpx.Client(verify=False)
        return Groq(api_key=api_key, http_client=http_client)