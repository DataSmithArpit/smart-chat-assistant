import streamlit as st
from styles.themes import get_theme_css

class ThemeManager:
    """Manages application themes and styling"""
    
    def __init__(self):
        self.current_theme = "dark" if st.session_state.get('dark_mode', False) else "light"
    
    def apply_theme(self):
        """Apply the current theme CSS"""
        css = get_theme_css(self.current_theme)
        st.markdown(css, unsafe_allow_html=True)
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        st.session_state.dark_mode = not st.session_state.get('dark_mode', False)
        self.current_theme = "dark" if st.session_state.dark_mode else "light"
        st.rerun()
    
    def render_header(self):
        """Render the application header with theme toggle"""
        header_col1, header_col2 = st.columns([10, 1])
        
        with header_col1:
            st.markdown(f"""
            <div class="app-header">
                <h1 class="app-title">💬 Smart Chat Assistant</h1>
                <p class="app-subtitle">Your AI-powered conversation companion</p>
            </div>
            """, unsafe_allow_html=True)
        
        with header_col2:
            theme_icon = "🌙" if not st.session_state.get('dark_mode', False) else "☀️"
            if st.button(theme_icon, key="theme_toggle"):
                self.toggle_theme()
    
    def get_theme_colors(self):
        """Get current theme color palette"""
        if self.current_theme == "dark":
            return {
                'bg_color': "#1a1a1a",
                'card_bg': "#2d2d2d",
                'text_color': "#ffffff",
                'secondary_text': "#b0b0b0",
                'input_bg': "#3a3a3a",
                'gradient_start': "#667eea",
                'gradient_end': "#764ba2",
                'chat_bubble_user': "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                'chat_bubble_other': "#3a3a3a",
                'shadow': "0 8px 32px rgba(0, 0, 0, 0.3)"
            }
        else:
            return {
                'bg_color': "#f8fafc",
                'card_bg': "#ffffff",
                'text_color': "#1a202c",
                'secondary_text': "#4a5568",
                'input_bg': "#ffffff",
                'gradient_start': "#667eea",
                'gradient_end': "#764ba2",
                'chat_bubble_user': "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                'chat_bubble_other': "#f7fafc",
                'shadow': "0 8px 32px rgba(31, 38, 135, 0.15)"
            }