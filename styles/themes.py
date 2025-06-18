def get_theme_css(theme="light"):
    """Generate CSS based on theme selection"""
    
    if theme == "dark":
        colors = {
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
        colors = {
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

    return f"""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {{
        background: {colors['bg_color']};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu, .stDeployButton, footer, .stApp > header {{
        visibility: hidden;
    }}
    
    .main > div {{
        padding: 1rem;
        max-width: 450px;
        margin: 0 auto;
    }}
    
    /* Header styling */
    .app-header {{
        background: linear-gradient(135deg, {colors['gradient_start']} 0%, {colors['gradient_end']} 100%);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: {colors['shadow']};
        position: relative;
        overflow: hidden;
    }}
    
    .app-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        z-index: 1;
    }}
    
    .app-header > * {{
        position: relative;
        z-index: 2;
    }}
    
    .app-title {{
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }}
    
    .app-subtitle {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 14px;
        margin: 5px 0 0 0;
        font-weight: 400;
    }}
    
    /* Cards */
    .card {{
        background: {colors['card_bg']};
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: {colors['shadow']};
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }}
    
    .card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.2);
    }}
    
    .card-title {{
        color: {colors['text_color']};
        font-size: 18px;
        font-weight: 600;
        margin: 0 0 15px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    /* Chat messages */
    .chat-container {{
        max-height: 300px;
        overflow-y: auto;
        padding: 10px 0;
        margin: 15px 0;
    }}
    
    .chat-message {{
        margin: 12px 0;
        animation: slideIn 0.3s ease-out;
    }}
    
    .message-bubble {{
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 85%;
        word-wrap: break-word;
        position: relative;
        font-size: 14px;
        line-height: 1.4;
    }}
    
    .user-message .message-bubble {{
        background: {colors['chat_bubble_user']};
        color: white;
        margin-left: auto;
        margin-right: 0;
        border-bottom-right-radius: 4px;
    }}
    
    .other-message .message-bubble {{
        background: {colors['chat_bubble_other']};
        color: {colors['text_color']};
        margin-left: 0;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .message-sender {{
        font-size: 12px;
        color: {colors['secondary_text']};
        margin-bottom: 4px;
        font-weight: 500;
    }}
    
    /* Input areas */
    .stTextArea textarea {{
        background: {colors['input_bg']} !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: {colors['text_color']} !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
        resize: none !important;
    }}
    
    .stTextArea textarea:focus {{
        border-color: {colors['gradient_start']} !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {colors['gradient_start']} 0%, {colors['gradient_end']} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Select boxes */
    .stSelectbox > div > div {{
        background: {colors['input_bg']};
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        color: {colors['text_color']};
    }}
    
    /* Suggestions */
    .suggestions-container {{
        background: rgba(102, 126, 234, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 16px;
        margin: 15px 0;
    }}
    
    .suggestion-item {{
        background: {colors['card_bg']};
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .suggestion-item:hover {{
        background: rgba(102, 126, 234, 0.1);
        transform: scale(1.02);
    }}
    
    /* Loading animation */
    .loading-dots {{
        display: inline-flex;
        gap: 4px;
        align-items: center;
    }}
    
    .loading-dots::after {{
        content: '●●●';
        animation: dots 1.5s infinite;
        color: {colors['gradient_start']};
    }}
    
    @keyframes dots {{
        0%, 20% {{ color: transparent; text-shadow: 0.25em 0 0 transparent, 0.5em 0 0 transparent; }}
        40% {{ color: {colors['gradient_start']}; text-shadow: 0.25em 0 0 transparent, 0.5em 0 0 transparent; }}
        60% {{ text-shadow: 0.25em 0 0 {colors['gradient_start']}, 0.5em 0 0 transparent; }}
        80%, 100% {{ text-shadow: 0.25em 0 0 {colors['gradient_start']}, 0.5em 0 0 {colors['gradient_start']}; }}
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {{
        .main > div {{
            padding: 0.5rem;
        }}
        
        .message-bubble {{
            max-width: 90%;
        }}
    }}
    </style>
    """