import streamlit as st
import time
from utils.session_manager import SessionManager

class ChatInterface:
    """Handles chat interface rendering and interactions"""
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    def render(self):
        """Render the complete chat interface"""
        self._render_chat_display()
        self._render_typing_area()
        self._render_quick_actions()
        self._render_chat_controls()
    
    def _render_chat_display(self):
        """Render the chat message display area"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">💬 Chat Simulation</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        chat_history = self.session_manager.get('chat_history', [])
        
        if chat_history:
            for message in chat_history:
                self._render_message(message)
        else:
            # Default first message
            self._render_default_message()
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_message(self, message):
        """Render a single chat message"""
        if message['type'] == 'received':
            st.markdown(f"""
            <div class="chat-message other-message">
                <div class="message-sender">Friend</div>
                <div class="message-bubble">{message['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-sender" style="text-align: right; color: rgba(255,255,255,0.8);">You</div>
                <div class="message-bubble">{message['text']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_default_message(self):
        """Render the default welcome message"""
        st.markdown("""
        <div class="chat-message other-message">
            <div class="message-sender">Friend</div>
            <div class="message-bubble">Hey! How's your day going? 😊</div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_typing_area(self):
        """Render the message typing area"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">✏️ Compose Your Reply</h3>', unsafe_allow_html=True)
        
        # Text area for user input
        current_draft = self.session_manager.get('current_draft', '')
        user_input = st.text_area(
            "",
            value=current_draft,
            height=100,
            placeholder="Type your reply here...",
            key="user_message_input"
        )
        
        # Update session state with current text
        self.session_manager.set('current_draft', user_input)
        
        # Action buttons
        self._render_action_buttons(user_input)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_action_buttons(self, user_input):
        """Render the main action buttons"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🤖 Get Help", type="primary", key="get_help_btn"):
                if user_input.strip():
                    self.session_manager.set('generate_suggestions', True)
                    # Add this debug line temporarily  
                    st.info("🤖 Generating suggestions - please wait...")
                    st.rerun()
                else:
                    st.warning("Please type a message first!")
        
        with col2:
            if st.button("✨ Auto-Fix", key="auto_fix_btn"):
                if user_input.strip():
                    self.session_manager.set('auto_fix_request', True)
                    # Add this debug line temporarily
                    st.info("🔧 Auto-fix requested - processing...")
                    st.rerun()
                else:
                    st.warning("Please type a message first!")
        
        with col3:
            if st.button("📤 Send", key="send_btn"):
                if user_input.strip():
                    self._send_message(user_input)
                else:
                    st.warning("Please type a message first!")
    
    def _render_quick_actions(self):
        """Render quick action buttons"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">⚡ Quick Actions</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        quick_responses = [
            ("👍 Sounds great!", "That sounds great!"),
            ("🤔 Let me think", "Let me think about it and get back to you"),
            ("😊 Can't wait!", "Can't wait! 😊")
        ]
        
        for i, (button_text, response_text) in enumerate(quick_responses):
            with [col1, col2, col3][i]:
                if st.button(button_text, key=f"quick_action_{i}"):
                    self.session_manager.set('current_draft', response_text)
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_chat_controls(self):
        """Render chat control buttons"""
        chat_history = self.session_manager.get('chat_history', [])
        
        if chat_history:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Clear Chat", key="clear_chat_btn"):
                    self.session_manager.clear_chat_history()
                    st.success("Chat cleared!")
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.button("📊 Chat Stats", key="chat_stats_btn"):
                    self._show_chat_stats()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    def _send_message(self, message):
        """Send a message and add it to chat history"""
        self.session_manager.add_message('sent', message)
        self.session_manager.set('current_draft', '')
        st.success("✅ Message sent!")
        time.sleep(1)
        st.rerun()
    
    def _show_chat_stats(self):
        """Display chat statistics"""
        chat_history = self.session_manager.get('chat_history', [])
        
        total_messages = len(chat_history)
        sent_messages = len([msg for msg in chat_history if msg['type'] == 'sent'])
        received_messages = len([msg for msg in chat_history if msg['type'] == 'received'])
        
        st.info(f"""
        **📊 Chat Statistics:**
        - Total Messages: {total_messages}
        - Messages Sent: {sent_messages}
        - Messages Received: {received_messages}
        """)
    
    def handle_message_actions(self):
        """Handle message-related actions triggered by other components"""
        # This method can be called by other components to trigger chat actions
        if self.session_manager.get('send_message', False):
            current_draft = self.session_manager.get('current_draft', '')
            if current_draft.strip():
                self._send_message(current_draft)
            self.session_manager.set('send_message', False)