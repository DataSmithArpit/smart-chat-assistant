# 🤖 Grammar AI - Smart Chat Assistant

An AI-powered chat assistant that helps you craft perfect messages with real-time grammar correction, intelligent suggestions, and multiple conversation styles.

## ✨ Current Features (MVP v1.0)

- **🔧 Auto-Fix Grammar**: Instantly correct spelling and grammar errors
- **💡 Smart Suggestions**: Get 3 AI-powered reply options for any message
- **🎨 Multiple Chat Styles**: 
  - 💬 Casual - Relaxed and friendly
  - 👔 Professional - Business and formal
  - 😊 Friendly - Warm and approachable  
  - 😘 Flirty - Playful and charming
- **⚡ AI Model Options**:
  - ⚡ Fast (llama-3.1-8b-instant) - Quick responses
  - 🧠 Smart (llama-3.1-70b-versatile) - High-quality outputs
- **🎛️ Advanced Settings**: Temperature, response length, creativity control
- **📱 Clean Interface**: Modern Streamlit design with real-time updates
- **🛡️ Secure**: API keys stored in session (not saved locally)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key ([Get one free](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/grammer-ai-app.git
   cd grammer-ai-app
   ```

2. **Create virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```powershell
   streamlit run app.py --logger.level error
   ```

5. **Configure API key**
   - Open http://localhost:8501 in your browser
   - Click "⚙️ Chat Settings" 
   - Enter your Groq API key
   - Start improving your messages!

## 📁 Project Architecture

```
grammer-ai-app/
├── components/
│   ├── __init__.py
│   ├── auth_handler.py       # API key management & validation
│   ├── chat_interface.py     # Main chat UI & message composition
│   ├── settings_panel.py     # Configuration panel
│   ├── suggestions_engine.py # AI suggestions & auto-fix logic
│   └── theme_manager.py      # UI themes & styling
├── config/
│   ├── __init__.py
│   └── settings.py           # App configuration & constants
├── styles/
│   ├── __init__.py
│   └── themes.py             # CSS styles & themes
├── utils/
│   ├── __init__.py
│   ├── ai_client.py          # Groq API wrapper & error handling
│   └── session_manager.py    # Streamlit session state management
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
└── README.md                # This documentation
```

## 🎯 How to Use

### Basic Usage
1. **Type your message** in the compose area
2. **Select your style** (Casual, Professional, Friendly, Flirty)
3. **Get AI help**:
   - **🤖 Get Help**: Receive 3 alternative message suggestions
   - **✨ Auto-Fix**: Automatically correct grammar and spelling
   - **📋 Send**: Use your perfected message

### Advanced Features
- **Adjust creativity** with the temperature slider
- **Control response length** with max tokens
- **Switch AI models** based on your needs (speed vs quality)
- **View suggestions** with clean formatting and easy-to-use buttons

## 🛠️ Technical Details

- **Frontend**: Streamlit with custom CSS
- **AI Backend**: Groq API (Llama 3.1 models)
- **Architecture**: Modular component-based design
- **State Management**: Custom session manager
- **Error Handling**: Comprehensive API error handling

## 🧪 Testing

```powershell
# Development mode (with full logging)
streamlit run app.py

# Production mode (clean terminal)
streamlit run app.py --logger.level error
```

## 🔮 Roadmap & Next Steps

### Phase 2 - Enhanced UX
- [ ] 🌙 Dark mode toggle
- [ ] 💾 Save conversation history
- [ ] 📤 Export messages to clipboard
- [ ] ⌨️ Keyboard shortcuts (Ctrl+Enter to send)

### Phase 3 - Advanced Features  
- [ ] 🗂️ Multiple conversation threads
- [ ] 📊 Writing analytics dashboard
- [ ] 🎯 Context-aware suggestions
- [ ] 🔊 Voice input support

### Phase 4 - Deployment
- [ ] 🌐 Web deployment (Streamlit Cloud)
- [ ] 📱 Mobile-responsive design
- [ ] 👥 Multi-user support
- [ ] 🔐 User authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues
- **"Invalid API key"**: Check your Groq API key in settings
- **"Server/Model error"**: Try switching to a different AI model
- **App won't start**: Ensure all dependencies are installed in your venv

### Getting Help
- Open an issue on GitHub
- Check the Groq API status
- Ensure you're using Python 3.8+

## ⭐ Acknowledgments

- [Streamlit](https://streamlit.io/) - Amazing web app framework
- [Groq](https://groq.com/) - Lightning-fast AI inference
- [Llama 3.1](https://llama.meta.com/) - Powerful language models

---

**Made with ❤️ for better communication**

*Current Version: MVP v1.0 | Last Updated: June 2025*