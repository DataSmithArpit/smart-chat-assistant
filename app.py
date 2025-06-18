import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import httpx
import time

# Load environment variables
load_dotenv()

# Set page configuration for mobile
st.set_page_config(
    page_title="Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-first design
st.markdown("""
<style>
/* Mobile-first responsive design */
.main > div {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Chat interface styling */
.chat-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.chat-message {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.user-message {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    margin-left: 20%;
    color: white;
}

.other-message {
    background: rgba(255, 255, 255, 0.9);
    margin-right: 20%;
    color: #333;
}

.typing-area {
    background: white;
    border-radius: 25px;
    padding: 15px;
    margin: 15px 0;
    border: 2px solid #e0e0e0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.quick-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 10px 0;
}

.action-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 14px;
    cursor: pointer;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .main > div {
        padding: 0.5rem;
    }
    
    .user-message {
        margin-left: 10%;
    }
    
    .other-message {
        margin-right: 10%;
    }
}

/* Hide Streamlit elements for cleaner mobile experience */
#MainMenu {visibility: hidden;}
.stDeployButton {display: none;}
footer {visibility: hidden;}
.stApp > header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_draft' not in st.session_state:
    st.session_state.current_draft = ""
if 'autocorrect_enabled' not in st.session_state:
    st.session_state.autocorrect_enabled = True
if 'api_configured' not in st.session_state:
    st.session_state.api_configured = False

# Header
st.markdown("""
<div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0; font-size: 24px;'>💬 Smart Chat Assistant</h1>
    <p style='color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 14px;'>Your AI-powered conversation helper</p>
</div>
""", unsafe_allow_html=True)

# Quick Setup Section (Collapsible)
with st.expander("⚙️ Quick Setup", expanded=not st.session_state.api_configured):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        api_key = st.text_input(
            "🔑 Groq API Key:",
            type="password",
            placeholder="Paste your free API key here...",
            help="Get free key from console.groq.com"
        )
    
    with col2:
        if st.button("✅ Save", use_container_width=True):
            if api_key:
                try:
                    http_client = httpx.Client(verify=False)
                    client = Groq(api_key=api_key.strip(), http_client=http_client)
                    st.session_state.api_key = api_key
                    st.session_state.api_configured = True
                    st.success("Ready to chat!")
                    st.rerun()
                except:
                    st.error("Invalid API key")

# Settings Row
if st.session_state.api_configured:
    st.markdown("### 🎛️ Chat Settings")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        chat_style = st.selectbox(
            "Style:",
            ["💬 Casual", "💼 Professional", "😍 Flirty", "😄 Funny", "🤗 Supportive"],
            key="style"
        )
    
    with col2:
        reply_length = st.selectbox(
            "Length:",
            ["📝 Short", "📄 Medium", "📚 Long"],
            key="length"
        )
    
    with col3:
        model = st.selectbox(
            "AI:",
            ["⚡ Fast", "🧠 Smart", "🎯 Balanced"],
            key="model"
        )
    
    with col4:
        autocorrect = st.checkbox(
            "✨ Auto-fix",
            value=st.session_state.autocorrect_enabled,
            help="Automatically fix grammar as you type"
        )
        st.session_state.autocorrect_enabled = autocorrect

    # Map user-friendly names to actual values
    style_map = {
        "💬 Casual": "casual & friendly",
        "💼 Professional": "professional", 
        "😍 Flirty": "flirty",
        "😄 Funny": "humorous",
        "🤗 Supportive": "supportive"
    }
    
    length_map = {
        "📝 Short": "short",
        "📄 Medium": "medium", 
        "📚 Long": "long"
    }
    
    model_map = {
        "⚡ Fast": "llama-3.1-8b-instant",
        "🧠 Smart": "llama-3.1-70b-versatile",
        "🎯 Balanced": "mixtral-8x7b-32768"
    }
    
    # Chat Interface
    st.markdown("---")
    st.markdown("### 💬 Chat Simulation")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for i, message in enumerate(st.session_state.chat_history):
                if message['type'] == 'received':
                    st.markdown(f"""
                    <div class="chat-message other-message">
                        <strong>Friend:</strong> {message['text']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong> {message['text']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="chat-message other-message">
                <strong>Friend:</strong> Hey! How's your day going? 😊
            </div>
            """, unsafe_allow_html=True)
    
    # Typing Area
    st.markdown("### ✏️ Compose Your Reply")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your message:",
            value=st.session_state.current_draft,
            height=100,
            placeholder="Type your reply here...",
            key="user_message"
        )
        st.session_state.current_draft = user_input
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        
        if st.button("🤖 Get Help", use_container_width=True, type="primary"):
            if user_input.strip():
                with st.spinner("Getting suggestions..."):
                    try:
                        http_client = httpx.Client(verify=False)
                        client = Groq(api_key=st.session_state.api_key, http_client=http_client)
                        
                        # Create context from chat history
                        context = ""
                        if st.session_state.chat_history:
                            for msg in st.session_state.chat_history[-6:]:  # Last 6 messages for context
                                sender = "Friend" if msg['type'] == 'received' else "You"
                                context += f"{sender}: {msg['text']}\n"
                        else:
                            context = "Friend: Hey! How's your day going? 😊\n"
                        
                        context += f"You: [typing] {user_input}"
                        
                        prompt = f"""
                        Conversation context:
                        {context}
                        
                        The user is drafting: "{user_input}"
                        
                        Please provide:
                        1. An improved version of their draft (if grammar/style needs fixing)
                        2. 2 alternative reply suggestions
                        
                        Style: {style_map[chat_style]}
                        Length: {length_map[reply_length]}
                        
                        Format as:
                        **✨ Improved:** [improved version]
                        **💡 Option 1:** [alternative 1]
                        **💡 Option 2:** [alternative 2]
                        """
                        
                        response = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are a helpful chat assistant. Provide natural, engaging suggestions that fit the conversation context."},
                                {"role": "user", "content": prompt}
                            ],
                            model=model_map[model],
                            max_tokens=400,
                            temperature=0.7
                        )
                        
                        st.session_state.suggestions = response.choices[0].message.content.strip()
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        if st.button("✨ Auto-Fix", use_container_width=True):
            if user_input.strip():
                with st.spinner("Fixing..."):
                    try:
                        http_client = httpx.Client(verify=False)
                        client = Groq(api_key=st.session_state.api_key, http_client=http_client)
                        
                        response = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": f"Fix grammar and spelling. Make it sound {style_map[chat_style]}. Keep the same meaning. Return only the corrected text."},
                                {"role": "user", "content": user_input}
                            ],
                            model=model_map[model],
                            max_tokens=200,
                            temperature=0.3
                        )
                        
                        fixed_text = response.choices[0].message.content.strip()
                        st.session_state.current_draft = fixed_text
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        if st.button("📤 Send", use_container_width=True):
            if user_input.strip():
                # Add to chat history
                st.session_state.chat_history.append({
                    'type': 'sent',
                    'text': user_input,
                    'timestamp': time.time()
                })
                st.session_state.current_draft = ""
                st.rerun()
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👍 That sounds great!", use_container_width=True):
            st.session_state.current_draft = "That sounds great!"
            st.rerun()
    
    with col2:
        if st.button("🤔 Let me think about it", use_container_width=True):
            st.session_state.current_draft = "Let me think about it and get back to you"
            st.rerun()
    
    with col3:
        if st.button("😊 Can't wait!", use_container_width=True):
            st.session_state.current_draft = "Can't wait! 😊"
            st.rerun()
    
    # Display suggestions if available
    if 'suggestions' in st.session_state:
        st.markdown("### 💡 AI Suggestions")
        
        # Parse and display suggestions nicely
        suggestions_text = st.session_state.suggestions
        st.markdown(f"""
        <div style='background: rgba(102, 126, 234, 0.1); border-radius: 15px; padding: 15px; margin: 10px 0;'>
            {suggestions_text.replace('**', '<strong>').replace('**', '</strong>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Quick copy buttons for each suggestion
        lines = suggestions_text.split('\n')
        for line in lines:
            if line.startswith('**') and ('Improved:' in line or 'Option' in line):
                suggestion_text = line.split(':', 1)[1].strip() if ':' in line else line
                suggestion_text = suggestion_text.replace('*', '')
                
                if st.button(f"📋 Use: {suggestion_text[:50]}...", key=f"copy_{hash(line)}"):
                    st.session_state.current_draft = suggestion_text
                    st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.current_draft = ""
            if 'suggestions' in st.session_state:
                del st.session_state.suggestions
            st.rerun()

else:
    # API Key setup screen
    st.markdown("""
    <div style='text-align: center; padding: 30px;'>
        <h3>🔑 Get Started</h3>
        <p>Get your FREE Groq API key to start using the chat assistant!</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📱 How to get FREE API Key", expanded=True):
        st.markdown("""
        1. 🌐 Go to [console.groq.com](https://console.groq.com)
        2. 📝 Sign up (it's free!)
        3. 🔑 Go to API Keys section
        4. ➕ Create new key
        5. 📋 Copy and paste above
        
        **🆓 100% Free:** 14,400 requests/day!
        """)

# Footer tips
st.markdown("---")
with st.expander("💡 Pro Tips"):
    st.markdown("""
    **🎯 Best Practices:**
    - Use **🤖 Get Help** for reply suggestions
    - Enable **✨ Auto-fix** for automatic grammar correction
    - Try different **styles** for different people you chat with
    - Use **Quick Actions** for common responses
    - Set **Professional** style for work chats
    - Set **Flirty** style for dating apps
    - **Fast AI** = Quick responses
    - **Smart AI** = Better quality responses
    """)