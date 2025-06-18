import streamlit as st
from utils.session_manager import SessionManager
from config.settings import AppConfig

class SettingsPanel:
    """Handles settings and configuration UI"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.config = AppConfig()
    
    def render(self):
        """Render the complete settings panel"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">🎛️ Chat Settings</h3>', unsafe_allow_html=True)
        
        # Create settings grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self._render_style_selector()
        
        with col2:
            self._render_length_selector()
        
        with col3:
            self._render_model_selector()
        
        with col4:
            self._render_autocorrect_toggle()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Advanced settings (collapsible)
        self._render_advanced_settings()
    
    def _render_style_selector(self):
        """Render chat style selector"""
        current_style = self.session_manager.get('chat_style', '💬 Casual')
        
        style = st.selectbox(
            "Style",
            self.config.CHAT_STYLES,
            index=self.config.CHAT_STYLES.index(current_style),
            key="style_selector"
        )
        
        self.session_manager.set('chat_style', style)
    
    def _render_length_selector(self):
        """Render reply length selector"""
        current_length = self.session_manager.get('reply_length', '📄 Medium')
        
        length = st.selectbox(
            "Length",
            self.config.REPLY_LENGTHS,
            index=self.config.REPLY_LENGTHS.index(current_length),
            key="length_selector"
        )
        
        self.session_manager.set('reply_length', length)
    
    def _render_model_selector(self):
        """Render AI model selector"""
        current_model = self.session_manager.get('ai_model', '🎯 Balanced')
        
        model = st.selectbox(
            "AI Model",
            self.config.AI_MODELS,
            index=self.config.AI_MODELS.index(current_model),
            key="model_selector"
        )
        
        self.session_manager.set('ai_model', model)
    
    def _render_autocorrect_toggle(self):
        """Render autocorrect toggle"""
        autocorrect = st.checkbox(
            "✨ Auto-fix",
            value=self.session_manager.get('autocorrect_enabled', True),
            help="Auto-correct grammar",
            key="autocorrect_toggle"
        )
        
        self.session_manager.set('autocorrect_enabled', autocorrect)
    
    def _render_advanced_settings(self):
        """Render advanced settings in expandable section"""
        with st.expander("⚙️ Advanced Settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Temperature setting
                temperature = st.slider(
                    "🌡️ Creativity",
                    min_value=0.0,
                    max_value=1.0,
                    value=self.session_manager.get('temperature', 0.7),
                    step=0.1,
                    help="Higher = more creative responses"
                )
                self.session_manager.set('temperature', temperature)
                
                # Max tokens
                max_tokens = st.slider(
                    "📝 Max Response Length",
                    min_value=50,
                    max_value=1000,
                    value=self.session_manager.get('max_tokens', 400),
                    step=50,
                    help="Maximum length of AI responses"
                )
                self.session_manager.set('max_tokens', max_tokens)
            
            with col2:
                # Context messages
                context_messages = st.slider(
                    "🧠 Context Memory",
                    min_value=2,
                    max_value=20,
                    value=self.session_manager.get('context_messages', 6),
                    step=2,
                    help="How many previous messages to remember"
                )
                self.session_manager.set('context_messages', context_messages)
                
                # Auto-send delay
                auto_send_delay = st.slider(
                    "⏱️ Auto-send Delay (sec)",
                    min_value=0,
                    max_value=10,
                    value=self.session_manager.get('auto_send_delay', 0),
                    step=1,
                    help="Delay before auto-sending (0 = disabled)"
                )
                self.session_manager.set('auto_send_delay', auto_send_delay)
            
            # Export/Import Settings
            self._render_settings_management()
    
    def _render_settings_management(self):
        """Render settings import/export functionality"""
        st.markdown("---")
        st.markdown("**🔧 Settings Management:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Export Settings", key="export_settings"):
                settings_data = self._export_settings()
                st.download_button(
                    label="💾 Download",
                    data=settings_data,
                    file_name="chat_assistant_settings.json",
                    mime="application/json"
                )
        
        with col2:
            uploaded_file = st.file_uploader(
                "📥 Import Settings",
                type=['json'],
                key="import_settings"
            )
            if uploaded_file:
                self._import_settings(uploaded_file)
        
        with col3:
            if st.button("🔄 Reset to Defaults", key="reset_settings"):
                self._reset_to_defaults()
                st.success("Settings reset to defaults!")
                st.rerun()
    
    def _export_settings(self) -> str:
        """Export current settings to JSON"""
        import json
        
        settings = {
            'chat_style': self.session_manager.get('chat_style'),
            'reply_length': self.session_manager.get('reply_length'),
            'ai_model': self.session_manager.get('ai_model'),
            'autocorrect_enabled': self.session_manager.get('autocorrect_enabled'),
            'temperature': self.session_manager.get('temperature'),
            'max_tokens': self.session_manager.get('max_tokens'),
            'context_messages': self.session_manager.get('context_messages'),
            'auto_send_delay': self.session_manager.get('auto_send_delay'),
            'dark_mode': self.session_manager.get('dark_mode')
        }
        
        return json.dumps(settings, indent=2)
    
    def _import_settings(self, uploaded_file):
        """Import settings from uploaded JSON file"""
        import json
        
        try:
            settings = json.load(uploaded_file)
            
            # Validate and apply settings
            for key, value in settings.items():
                if key in ['chat_style', 'reply_length', 'ai_model', 'autocorrect_enabled',
                          'temperature', 'max_tokens', 'context_messages', 'auto_send_delay', 'dark_mode']:
                    self.session_manager.set(key, value)
            
            st.success("✅ Settings imported successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error importing settings: {str(e)}")
    
    def _reset_to_defaults(self):
        """Reset all settings to default values"""
        defaults = {
            'chat_style': '💬 Casual',
            'reply_length': '📄 Medium',
            'ai_model': '🎯 Balanced',
            'autocorrect_enabled': True,
            'temperature': 0.7,
            'max_tokens': 400,
            'context_messages': 6,
            'auto_send_delay': 0,
            'dark_mode': False
        }
        
        self.session_manager.update(defaults)
    
    def get_current_settings(self) -> dict:
        """Get current settings as a dictionary"""
        return {
            'style': self.session_manager.get('chat_style'),
            'length': self.session_manager.get('reply_length'),
            'model': self.session_manager.get('ai_model'),
            'autocorrect': self.session_manager.get('autocorrect_enabled'),
            'temperature': self.session_manager.get('temperature'),
            'max_tokens': self.session_manager.get('max_tokens'),
            'context_messages': self.session_manager.get('context_messages')
        }
    
    def render_compact(self):
        """Render a compact version of settings for mobile"""
        with st.expander("⚙️ Quick Settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                self._render_style_selector()
                self._render_model_selector()
            
            with col2:
                self._render_length_selector()
                self._render_autocorrect_toggle()