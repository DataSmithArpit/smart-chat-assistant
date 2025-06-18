class AppConfig:
    """Application configuration and constants"""
    
    # Chat style options
    CHAT_STYLES = [
        "💬 Casual",
        "💼 Professional", 
        "😍 Flirty",
        "😄 Funny",
        "🤗 Supportive"
    ]
    
    # Reply length options
    REPLY_LENGTHS = [
        "📝 Short",
        "📄 Medium",
        "📚 Long"
    ]
    
    # AI model options
    AI_MODELS = [
        "⚡ Fast",
        "🧠 Smart",
        "🎯 Balanced"
    ]
    
    # Style mappings for AI prompts
    STYLE_MAPPINGS = {
        "💬 Casual": "casual & friendly",
        "💼 Professional": "professional",
        "😍 Flirty": "flirty",
        "😄 Funny": "humorous",
        "🤗 Supportive": "supportive"
    }
    
    # Length mappings for AI prompts
    LENGTH_MAPPINGS = {
        "📝 Short": "short",
        "📄 Medium": "medium",
        "📚 Long": "long"
    }
    
    # Model mappings to actual Groq model names
    MODEL_MAPPINGS = {
        "⚡ Fast": "llama-3.1-8b-instant",
        "🧠 Smart": "llama-3.1-70b-versatile", 
        "🎯 Balanced": "llama-3.1-8b-instant"
    }
    
    # Default settings
    DEFAULTS = {
        'chat_style': "💬 Casual",
        'reply_length': "📄 Medium",
        'ai_model': "🎯 Balanced",
        'autocorrect_enabled': True,
        'temperature': 0.7,
        'max_tokens': 400,
        'context_messages': 6,
        'auto_send_delay': 0,
        'dark_mode': False
    }
    
    # API Configuration
    API_CONFIG = {
        'base_url': 'https://api.groq.com/openai/v1',
        'timeout': 30,
        'max_retries': 3,
        'rate_limit_delay': 1.0
    }
    
    # UI Configuration
    UI_CONFIG = {
        'max_chat_height': 300,
        'message_fade_delay': 0.3,
        'typing_animation_speed': 50,
        'auto_scroll': True,
        'mobile_breakpoint': 768
    }
    
    # Feature Flags
    FEATURES = {
        'voice_input': False,
        'auto_translate': False,
        'conversation_memory': True,
        'analytics': False,
        'export_chat': True,
        'custom_themes': False
    }
    
    # Error Messages
    ERROR_MESSAGES = {
        'api_key_invalid': "❌ Invalid API key. Please check your key and try again.",
        'api_key_missing': "🔑 Please enter your API key to continue.",
        'network_error': "🌐 Network error. Please check your connection and try again.",
        'rate_limit': "⏱️ Rate limit reached. Please wait a moment and try again.",
        'server_error': "🚫 Server error. Please try again later.",
        'message_empty': "📝 Please type a message first.",
        'generation_failed': "❌ Failed to generate suggestions. Please try again."
    }
    
    # Success Messages
    SUCCESS_MESSAGES = {
        'api_key_saved': "🚀 API key saved successfully!",
        'message_sent': "✅ Message sent!",
        'settings_saved': "💾 Settings saved!",
        'chat_cleared': "🗑️ Chat history cleared!",
        'export_success': "📤 Settings exported successfully!",
        'import_success': "📥 Settings imported successfully!"
    }
    
    # Quick Response Templates
    QUICK_RESPONSES = [
        {
            'label': "👍 Sounds great!",
            'text': "That sounds great!",
            'category': 'positive'
        },
        {
            'label': "🤔 Let me think",
            'text': "Let me think about it and get back to you",
            'category': 'neutral'
        },
        {
            'label': "😊 Can't wait!",
            'text': "Can't wait! 😊",
            'category': 'positive'
        },
        {
            'label': "🙄 Not really",
            'text': "Not really my thing, but thanks for asking",
            'category': 'negative'
        },
        {
            'label': "💯 Absolutely!",
            'text': "Absolutely! Count me in! 💯",
            'category': 'positive'
        },
        {
            'label': "❓ Tell me more",
            'text': "That's interesting! Can you tell me more?",
            'category': 'neutral'
        }
    ]
    
    # Suggestion Categories
    SUGGESTION_CATEGORIES = {
        'improvement': {
            'icon': '✨',
            'label': 'Improved',
            'description': 'Enhanced version of your message'
        },
        'alternative': {
            'icon': '💡',
            'label': 'Alternative',
            'description': 'Different way to say it'
        },
        'formal': {
            'icon': '💼',
            'label': 'Formal',
            'description': 'More professional tone'
        },
        'casual': {
            'icon': '😊',
            'label': 'Casual',
            'description': 'More relaxed tone'
        }
    }
    
    @classmethod
    def get_style_prompt(cls, style_key: str) -> str:
        """Get the prompt text for a style"""
        return cls.STYLE_MAPPINGS.get(style_key, "casual & friendly")
    
    @classmethod
    def get_length_prompt(cls, length_key: str) -> str:
        """Get the prompt text for a length"""
        return cls.LENGTH_MAPPINGS.get(length_key, "medium")
    
    @classmethod
    def get_model_name(cls, model_key: str) -> str:
        """Get the actual model name for API calls"""
        return cls.MODEL_MAPPINGS.get(model_key, "mixtral-8x7b-32768")
    
    @classmethod
    def is_feature_enabled(cls, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        return cls.FEATURES.get(feature_name, False)
    
    @classmethod
    def get_error_message(cls, error_type: str) -> str:
        """Get error message by type"""
        return cls.ERROR_MESSAGES.get(error_type, "An error occurred. Please try again.")
    
    @classmethod
    def get_success_message(cls, success_type: str) -> str:
        """Get success message by type"""
        return cls.SUCCESS_MESSAGES.get(success_type, "Operation completed successfully!")