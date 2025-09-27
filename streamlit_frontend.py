import streamlit as st
import requests
import json
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Coding Mentor Chatbot",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    .bot-message {
        background-color: #2d2d2d;
        color: white;
        border-left-color: #4a90e2;
    }
    .suggestion-button {
        margin: 0.2rem;
        padding: 0.3rem 0.8rem;
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
    }
    .conversation-type {
        background-color: #667eea;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_" + str(uuid.uuid4())[:8]

# Header
st.markdown("""
<div class="main-header">
    <h1>Coding Mentor Chatbot</h1>
    <p>Your AI-powered programming companion with intelligent conversation flow</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with features and stats
with st.sidebar:
    st.header("Features")
    st.markdown("""
    **Smart Conversation Flow:**
    - **Explanations**: Concept clarification
    - **Code Generation**: Write code snippets
    - **Debugging**: Fix errors and issues
    - **Code Review**: Optimize and improve
    - **Learning Paths**: Structured guidance
    - **General Help**: Programming questions
    """)
    
    st.header("Session Stats")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Session ID", st.session_state.session_id[-8:])
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.header("Quick Examples")
    example_prompts = [
        "Explain Python decorators",
        "Write a binary search function",
        "Debug this sorting algorithm",
        "Review my API code",
        "Create a learning path for web development"
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, key=f"example_{prompt}"):
            st.session_state.example_prompt = prompt

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display conversation type badge
            if "conversation_type" in message:
                type_display = message["conversation_type"].replace("_", " ").title()
                st.markdown(f"""
                <div class="conversation-type">
                    {type_display}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>Coding Mentor:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Display suggestions if available
            if "suggestions" in message and message["suggestions"]:
                st.markdown("**Suggestions:**")
                cols = st.columns(len(message["suggestions"]))
                for j, suggestion in enumerate(message["suggestions"]):
                    with cols[j]:
                        if st.button(suggestion, key=f"suggestion_{i}_{j}"):
                            st.session_state.suggestion_clicked = suggestion

# Handle example prompt from sidebar
if hasattr(st.session_state, 'example_prompt'):
    user_input = st.session_state.example_prompt
    delattr(st.session_state, 'example_prompt')
else:
    user_input = st.text_input("Ask me anything about programming:", key="user_input")

# Handle suggestion clicks
if hasattr(st.session_state, 'suggestion_clicked'):
    user_input = st.session_state.suggestion_clicked
    delattr(st.session_state, 'suggestion_clicked')

# Send button and processing
col_send, col_clear = st.columns([1, 1])

with col_send:
    send_button = st.button("Send", type="primary", use_container_width=True)

with col_clear:
    if st.button("New Topic", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Process user input
if send_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Show loading spinner
    with st.spinner("Thinking..."):
        try:
            # Make API request
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "user_id": st.session_state.user_id,
                    "message": user_input,
                    "session_id": st.session_state.session_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Add bot response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["reply"],
                    "conversation_type": data["conversation_type"],
                    "suggestions": data.get("suggestions", []),
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
                

            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend. Make sure the FastAPI server is running on port 8000.")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The AI might be processing a complex request.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Right column with additional info
with col2:
    st.header("How it Works")
    st.markdown("""
    **LangGraph Flow:**
    1. **Router** classifies your intent
    2. **Specialized nodes** handle different types
    3. **Context-aware** responses
    4. **Smart suggestions** for follow-ups
    """)
    
    st.header("Tech Stack")
    st.markdown("""
    - **Frontend**: Streamlit
    - **Backend**: FastAPI
    - **AI Flow**: LangGraph
    - **AI Model**: Gemini 2.0 Flash Lite
    - **Conversation Management**: State-based routing
    """)
    
    # Show current conversation type if available
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]
        if "conversation_type" in last_message:
            st.header("Current Mode")
            st.info(f"**{last_message['conversation_type'].replace('_', ' ').title()}**")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with Streamlit + FastAPI + LangGraph + Gemini AI<br>
    <small>Intelligent conversation flow for better programming assistance</small>
</div>
""", unsafe_allow_html=True)