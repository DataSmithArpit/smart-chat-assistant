import streamlit as st
import time
from utils.session_manager import SessionManager
from utils.ai_client import AIClient
from components.auth_handler import AuthHandler

class SuggestionsEngine:
    """Handles AI-powered suggestions and text processing"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.auth_handler = AuthHandler()
    
    def generate_suggestions(self):
        """Generate AI suggestions for user input"""
        if not self.auth_handler.is_authenticated():
            st.error("Please configure your API key first!")
            return
        
        user_input = self.session_manager.get('current_draft', '').strip()
        if not user_input:
            st.warning("Please type a message first!")
            return
        
        # Show loading state
        self.session_manager.set('loading', True)
        
        with st.spinner("🤖 Generating smart suggestions..."):
            try:
                # Get AI client
                client = self.auth_handler.get_client()
                ai_client = AIClient(self.session_manager.get('api_key'))
                
                # Get conversation context
                context = self.session_manager.get_chat_context()
                
                # Get current settings
                settings = self._get_current_settings()
                
                # Generate suggestions
                suggestions = ai_client.generate_suggestions(
                    user_input=user_input,
                    context=context,
                    settings=settings
                )
                
                # Store suggestions
                self.session_manager.set('suggestions', suggestions)
                self.session_manager.set('loading', False)
                
                # Reset the flag
                self.session_manager.set('generate_suggestions', False)
                
                st.rerun()
                
            except Exception as e:
                self.session_manager.set('loading', False)
                st.error(f"❌ Failed to generate suggestions: {str(e)}")
    
    def auto_fix_grammar(self):
        """Auto-fix grammar and style"""
        if not self.auth_handler.is_authenticated():
            st.error("Please configure your API key first!")
            return
        
        user_input = self.session_manager.get('current_draft', '').strip()
        if not user_input:
            st.warning("Please type a message first!")
            return
        
        with st.spinner("✨ Fixing grammar and style..."):
            try:
                ai_client = AIClient(self.session_manager.get('api_key'))
                settings = self._get_current_settings()
                
                # Simple grammar fix request
                fixed_text = ai_client.fix_grammar(user_input, settings)
                
                if fixed_text and fixed_text != user_input:
                    # Update the draft with fixed text
                    self.session_manager.set('current_draft', fixed_text)
                    st.success(f"✅ Fixed: '{fixed_text}'")
                else:
                    st.info("✨ Your message looks good already!")
                
                # Reset the flag
                self.session_manager.set('auto_fix_request', False)
                
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                self.session_manager.set('auto_fix_request', False)
                st.error(f"❌ Auto-fix failed: {str(e)}")
                # Try a simple fallback
                st.info("💡 Tip: Try using 'Get Help' for suggestions instead!")
    
    def render_suggestions(self):
        """Render the suggestions display area"""
        suggestions = self.session_manager.get('suggestions', '')
        
        if not suggestions:
            return
        
        st.markdown('<div class="suggestions-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin: 0 0 15px 0; color: #667eea;">💡 AI Suggestions</h3>', unsafe_allow_html=True)
        
        # Parse and display suggestions
        self._render_parsed_suggestions(suggestions)
        
        # Clear suggestions button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✨ Clear Suggestions", key="clear_suggestions_btn", type="secondary"):
                self.session_manager.set('suggestions', "")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_parsed_suggestions(self, suggestions_text: str):
        """Parse and render individual suggestions"""
        lines = suggestions_text.split('\n')
        suggestion_count = 0
        
        for line in lines:
            if line.strip() and ('**' in line or 'Improved:' in line or 'Option' in line):
                # Clean up the line and extract content
                clean_line = line.replace('*', '').replace('<strong>', '').replace('</strong>', '').strip()
                
                if ':' in clean_line:
                    parts = clean_line.split(':', 1)
                    if len(parts) == 2:
                        label = parts[0].strip()
                        suggestion_text = parts[1].strip().strip('"').strip("'")
                        
                        if suggestion_text and len(suggestion_text) > 3:
                            suggestion_count += 1
                            self._render_suggestion_item(label, suggestion_text, suggestion_count)
    
    def _render_suggestion_item(self, label: str, suggestion_text: str, count: int):
        """Render a single suggestion item"""
        # Clean up any remaining HTML tags or markdown
        clean_text = suggestion_text.replace('<strong>', '').replace('</strong>', '').replace('**', '').strip()
        clean_label = label.replace('✨', '').replace('💡', '').strip()
        
        # Add appropriate emoji for different suggestion types
        if 'improved' in clean_label.lower():
            display_label = f"✨ {clean_label}"
        elif 'option' in clean_label.lower():
            display_label = f"💡 {clean_label}"
        else:
            display_label = f"🔄 {clean_label}"
        
        st.markdown(f'<div class="suggestion-item">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f'<strong>{display_label}:</strong> {clean_text}', unsafe_allow_html=True)
        
        with col2:
            if st.button("📋 Use", key=f"use_suggestion_{count}"):
                self.session_manager.set('current_draft', clean_text)
                self.session_manager.set('suggestions', "")  # Clear suggestions
                st.success(f"✅ Using: {clean_text[:30]}...")
                time.sleep(1)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _get_current_settings(self) -> dict:
        """Get current user settings for AI generation"""
        return {
            'style': self.session_manager.get('chat_style', '💬 Casual'),
            'length': self.session_manager.get('reply_length', '📄 Medium'),
            'model': self.session_manager.get('ai_model', '🎯 Balanced'),
            'temperature': self.session_manager.get('temperature', 0.7),
            'max_tokens': self.session_manager.get('max_tokens', 400)
        }
    
    def analyze_conversation_mood(self):
        """Analyze and display conversation mood"""
        chat_history = self.session_manager.get('chat_history', [])
        
        if not chat_history or not self.auth_handler.is_authenticated():
            return
        
        try:
            ai_client = AIClient(self.session_manager.get('api_key'))
            mood_analysis = ai_client.analyze_conversation_mood(chat_history)
            
            if mood_analysis and 'mood' in mood_analysis:
                self._render_mood_display(mood_analysis)
                
        except Exception as e:
            # Silently fail for mood analysis - it's not critical
            pass
    
    def _render_mood_display(self, mood_analysis: dict):
        """Render conversation mood analysis"""
        mood = mood_analysis.get('mood', 'neutral')
        confidence = mood_analysis.get('confidence', 0.5)
        
        mood_emojis = {
            'positive': '😊',
            'negative': '😔',
            'neutral': '😐',
            'excited': '🤩',
            'confused': '😕',
            'romantic': '😍',
            'professional': '💼'
        }
        
        emoji = mood_emojis.get(mood, '😐')
        confidence_percent = int(confidence * 100)
        
        if confidence > 0.7:  # Only show if confident
            st.info(f"📊 Conversation mood: {emoji} {mood.title()} ({confidence_percent}% confidence)")
    
    def generate_quick_responses(self, context: str = ""):
        """Generate context-aware quick responses"""
        if not self.auth_handler.is_authenticated():
            return []
        
        try:
            ai_client = AIClient(self.session_manager.get('api_key'))
            
            prompt = f"""Based on this conversation context, suggest 3 brief, natural responses (each under 10 words):
            
            Context: {context or "Casual conversation"}
            
            Format as simple lines without numbering or formatting."""
            
            response = ai_client.generate_chat_response(
                message=prompt,
                settings={'model': '⚡ Fast', 'style': '💬 Casual', 'length': '📝 Short'}
            )
            
            # Parse responses
            quick_responses = []
            for line in response.split('\n'):
                if line.strip() and len(line.strip()) < 50:
                    quick_responses.append(line.strip())
            
            return quick_responses[:3]  # Return max 3
            
        except Exception:
            return []
    
    def handle_actions(self):
        """Handle all suggestion-related actions"""
        # Check for pending actions
        if self.session_manager.get('generate_suggestions', False):
            self.generate_suggestions()
        
        if self.session_manager.get('auto_fix_request', False):
            self.auto_fix_grammar()
            
        # Reset action flags after processing
        self.session_manager.reset_action_flags()
    
    def render_writing_assistance(self):
        """Render writing assistance tools"""
        current_draft = self.session_manager.get('current_draft', '')
        
        if current_draft and len(current_draft) > 10:
            with st.expander("✍️ Writing Assistant"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Word count
                    word_count = len(current_draft.split())
                    char_count = len(current_draft)
                    st.metric("Words", word_count)
                    st.metric("Characters", char_count)
                
                with col2:
                    # Tone analysis
                    if st.button("🎭 Analyze Tone"):
                        self._analyze_text_tone(current_draft)
                
                with col3:
                    # Alternative versions
                    if st.button("🔄 Rephrase"):
                        self._generate_rephrase(current_draft)
    
    def _analyze_text_tone(self, text: str):
        """Analyze the tone of the text"""
        try:
            ai_client = AIClient(self.session_manager.get('api_key'))
            
            analysis = ai_client.generate_chat_response(
                message=f"Analyze the tone of this text in one word: '{text}'",
                settings={'model': '⚡ Fast', 'style': '💬 Casual', 'length': '📝 Short'}
            )
            
            st.info(f"🎭 Detected tone: {analysis}")
            
        except Exception as e:
            st.error("Failed to analyze tone")
    
    def _generate_rephrase(self, text: str):
        """Generate alternative phrasings"""
        try:
            ai_client = AIClient(self.session_manager.get('api_key'))
            settings = self._get_current_settings()
            
            rephrased = ai_client.generate_chat_response(
                message=f"Rephrase this message in a different way while keeping the same meaning: '{text}'",
                settings=settings
            )
            
            if st.button("📋 Use Rephrased Version"):
                self.session_manager.set('current_draft', rephrased)
                st.rerun()
            
            st.write(f"**Alternative:** {rephrased}")
            
        except Exception as e:
            st.error("Failed to generate rephrase")