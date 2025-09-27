# 🤖 Coding Mentor Chatbot

An intelligent coding assistant built with **Streamlit**, **FastAPI**, and **LangGraph** for advanced conversation flow management.

## 🌟 Features

### Smart Conversation Flow (LangGraph)
- **📚 Explanations**: Clear concept clarification with examples
- **💻 Code Generation**: Write clean, commented code snippets  
- **🐛 Debugging**: Systematic error analysis and fixes
- **🔍 Code Review**: Optimization and best practices
- **🎯 Learning Paths**: Structured programming roadmaps
- **💬 General Help**: Friendly programming assistance

### Creative Use Cases
1. **Interactive Learning**: Adaptive responses based on user skill level
2. **Code Mentorship**: Personalized guidance with follow-up suggestions
3. **Project Planning**: Break down complex coding projects into steps
4. **Best Practices**: Context-aware recommendations for different scenarios

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: FastAPI with async endpoints
- **AI Flow**: LangGraph for intelligent conversation routing
- **AI Model**: Google Gemini 2.0 Flash Lite (Free Tier)
- **State Management**: Session-based conversation tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Setup
1. **Clone and navigate to project**
   ```bash
   cd agentic
   ```

2. **Set up environment**
   ```bash
   # Create .env file with your API key
   echo GEMINI_API_KEY=your_api_key_here > .env
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_full.txt
   ```

4. **Run the application**
   ```bash
   # Option 1: Use the batch file (Windows)
   run_chatbot.bat
   
   # Option 2: Manual start
   # Terminal 1: Start backend
   python -m uvicorn backend_api:app --reload --port 8000
   
   # Terminal 2: Start frontend  
   python -m streamlit run streamlit_frontend.py
   ```

5. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🎯 How It Works

### LangGraph Conversation Flow
```
User Input → Router Node → Intent Classification → Specialized Handler → Response
```

1. **Router Node**: Analyzes user input to determine intent
2. **Intent Classification**: Categories include explanation, code generation, debugging, etc.
3. **Specialized Handlers**: Each conversation type has a dedicated node
4. **Context Awareness**: Maintains conversation state and provides relevant suggestions

### API Architecture
- **FastAPI Backend**: RESTful API with automatic documentation
- **Pydantic Models**: Type-safe request/response handling
- **Error Handling**: Graceful degradation with informative messages
- **Session Management**: Tracks conversation context across requests

## 📊 Project Structure

```
agentic/
├── backend_api.py          # FastAPI backend with LangGraph
├── streamlit_frontend.py   # Streamlit UI with modern styling
├── requirements_full.txt   # Python dependencies
├── run_chatbot.bat        # Easy startup script
├── .env                   # Environment variables
└── README.md              # This file
```

## 🎨 UI Features

- **Modern Design**: Custom CSS with gradient headers and styled chat bubbles
- **Conversation Types**: Visual badges showing current conversation mode
- **Smart Suggestions**: Context-aware follow-up questions
- **Session Stats**: Track messages and session information
- **Quick Examples**: Pre-built prompts for common use cases
- **Responsive Layout**: Works on different screen sizes

## 🔧 API Endpoints

- `POST /chat`: Main conversation endpoint
- `GET /`: Health check
- `GET /health`: Service status
- `GET /docs`: Interactive API documentation

## 🚀 Advanced Features

### Creative Use Cases Implemented

1. **Adaptive Learning Assistant**
   - Adjusts complexity based on user questions
   - Provides progressive learning suggestions
   - Tracks conversation patterns

2. **Code Mentorship System**
   - Personalized feedback on coding style
   - Best practices recommendations
   - Project structure guidance

3. **Interactive Debugging Companion**
   - Step-by-step problem analysis
   - Multiple solution approaches
   - Prevention strategies

4. **Learning Path Generator**
   - Custom roadmaps for different technologies
   - Skill assessment integration
   - Resource recommendations

## 🔮 Future Enhancements

- **User Profiles**: Persistent learning progress
- **Code Execution**: Safe sandbox for running code
- **Multi-language Support**: Beyond Python programming
- **Voice Interface**: Speech-to-text integration
- **Collaborative Features**: Share conversations and solutions

## 🤝 Contributing

Feel free to contribute by:
- Adding new conversation types
- Improving the UI/UX
- Enhancing the LangGraph flow
- Adding more creative use cases

## 📝 License

This project is open source and available under the MIT License.

---

**Built with using Streamlit + FastAPI + LangGraph + Gemini AI**