import streamlit as st
import os
import warnings
from components.theme_manager import ThemeManager
from components.auth_handler import AuthHandler
from components.chat_interface import ChatInterface
from components.settings_panel import SettingsPanel
from components.suggestions_engine import SuggestionsEngine
from utils.session_manager import SessionManager

# Suppress warnings for cleaner terminal output
warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'

# Initialize page configuration
st.set_page_config(
    page_title="Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main application entry point"""
    
    # Initialize core managers
    session_manager = SessionManager()
    theme_manager = ThemeManager()
    auth_handler = AuthHandler()
    
    # Apply theme CSS
    theme_manager.apply_theme()
    
    # Render header with theme toggle
    theme_manager.render_header()
    
    # Check authentication status
    if not auth_handler.is_authenticated():
        auth_handler.render_setup_screen()
        return
    
    # Initialize main components
    settings_panel = SettingsPanel()
    chat_interface = ChatInterface()
    suggestions_engine = SuggestionsEngine()
    
    # Render main interface
    settings_panel.render()
    chat_interface.render()
    
    # Handle user interactions and render suggestions
    suggestions_engine.handle_actions()
    suggestions_engine.render_suggestions()
    suggestions_engine.render_writing_assistance()
    
    # Render pro tips
    render_pro_tips()

def render_pro_tips():
    """Render the pro tips section"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 class="card-title">💡 Pro Tips</h3>', unsafe_allow_html=True)
    st.markdown("""
    **🎯 Best Practices:**
    - **🤖 Get Help** for intelligent reply suggestions
    - **✨ Auto-Fix** for instant grammar correction  
    - **⚡ Quick Actions** for common responses
    - **🎭 Different Styles** for different people
    - **⚡ Fast AI** = Quick responses
    - **🧠 Smart AI** = Better quality
    """)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()