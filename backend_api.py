from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

app = FastAPI(title="Coding Mentor Chatbot API")

# Pydantic models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str
    conversation_type: str
    suggestions: list[str] = []

# State definition for LangGraph
class State(TypedDict):
    user_input: str
    conversation_type: str
    context: Dict[str, Any]
    response: str

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# Session memory to track conversations
session_memory = {}

# Helper functions
def classify_intent(message: str) -> str:
    """Classify user intent to determine conversation flow"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["explain", "what is", "how does", "concept"]):
        return "explanation"
    elif any(word in message_lower for word in ["example", "code", "implement", "write"]):
        return "code_generation"
    elif any(word in message_lower for word in ["debug", "error", "fix", "problem", "issue"]):
        return "debugging"
    elif any(word in message_lower for word in ["review", "optimize", "improve", "better"]):
        return "code_review"
    elif any(word in message_lower for word in ["learn", "tutorial", "guide", "roadmap"]):
        return "learning_path"
    else:
        return "general"

def call_gemini(prompt: str) -> str:
    """Call Gemini API with error handling"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"I'm having trouble processing that request. Error: {str(e)}"

# LangGraph nodes
def router_node(state: State) -> State:
    """Route conversation based on intent classification"""
    user_input = state["user_input"]
    conversation_type = classify_intent(user_input)
    
    return {
        **state,
        "conversation_type": conversation_type,
        "context": {"original_query": user_input}
    }

def explanation_node(state: State) -> State:
    """Handle concept explanations"""
    prompt = f"""
    As a coding mentor, explain the following concept clearly and concisely:
    {state['user_input']}
    
    Provide:
    1. A clear definition
    2. Why it's important
    3. A simple code example
    4. Common use cases
    
    Keep it beginner-friendly but comprehensive.
    """
    
    response = call_gemini(prompt)
    return {
        **state,
        "response": response
    }

def code_generation_node(state: State) -> State:
    """Handle code generation requests"""
    prompt = f"""
    As a coding mentor, help with this coding request:
    {state['user_input']}
    
    Provide:
    1. Clean, well-commented code
    2. Explanation of key parts
    3. Best practices used
    4. Potential improvements or variations
    
    Focus on readability and educational value.
    """
    
    response = call_gemini(prompt)
    return {
        **state,
        "response": response
    }

def debugging_node(state: State) -> State:
    """Handle debugging and error resolution"""
    prompt = f"""
    As a coding mentor, help debug this issue:
    {state['user_input']}
    
    Provide:
    1. Analysis of the problem
    2. Step-by-step debugging approach
    3. Fixed code with explanations
    4. Tips to prevent similar issues
    
    Be thorough and educational in your response.
    """
    
    response = call_gemini(prompt)
    return {
        **state,
        "response": response
    }

def code_review_node(state: State) -> State:
    """Handle code review and optimization"""
    prompt = f"""
    As a coding mentor, review and improve this code:
    {state['user_input']}
    
    Provide:
    1. Code quality assessment
    2. Specific improvement suggestions
    3. Optimized version with explanations
    4. Best practices recommendations
    
    Focus on maintainability, performance, and readability.
    """
    
    response = call_gemini(prompt)
    return {
        **state,
        "response": response
    }

def learning_path_node(state: State) -> State:
    """Handle learning roadmap and tutorial requests"""
    prompt = f"""
    As a coding mentor, create a learning path for:
    {state['user_input']}
    
    Provide:
    1. Structured learning roadmap
    2. Key concepts to master
    3. Practical projects to build
    4. Resources and next steps
    
    Make it actionable and progressive.
    """
    
    response = call_gemini(prompt)
    return {
        **state,
        "response": response
    }

def general_node(state: State) -> State:
    """Handle general programming questions"""
    user_input = state['user_input'].lower().strip()
    
    # Handle simple greetings
    if user_input in ['hello', 'hi', 'hey']:
        response = "Hello! I'm your coding mentor. What programming topic would you like to explore today? I can help with explanations, code examples, debugging, or learning paths."
    else:
        prompt = f"""
        As a friendly coding mentor, help with this question:
        {state['user_input']}
        
        Provide a helpful, encouraging response that guides the user toward learning.
        If it's not programming-related, gently redirect to coding topics.
        """
        response = call_gemini(prompt)
    
    return {
        **state,
        "response": response
    }

# Create the conversation flow graph
def create_conversation_graph():
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("explanation", explanation_node)
    workflow.add_node("code_generation", code_generation_node)
    workflow.add_node("debugging", debugging_node)
    workflow.add_node("code_review", code_review_node)
    workflow.add_node("learning_path", learning_path_node)
    workflow.add_node("general", general_node)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add conditional edges based on conversation type
    def route_conversation(state: State) -> str:
        return state["conversation_type"]
    
    workflow.add_conditional_edges(
        "router",
        route_conversation,
        {
            "explanation": "explanation",
            "code_generation": "code_generation",
            "debugging": "debugging",
            "code_review": "code_review",
            "learning_path": "learning_path",
            "general": "general"
        }
    )
    
    # All nodes end the conversation
    for node in ["explanation", "code_generation", "debugging", "code_review", "learning_path", "general"]:
        workflow.add_edge(node, END)
    
    return workflow.compile()

# Initialize the conversation graph
conversation_graph = create_conversation_graph()

# API endpoints
@app.get("/")
async def root():
    return {"message": "Coding Mentor Chatbot API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Check for repeated messages
        session_key = f"{request.user_id}_{request.session_id}"
        if session_key in session_memory:
            last_message = session_memory[session_key].get('last_message', '')
            if last_message == request.message.lower().strip():
                return ChatResponse(
                    reply="I see you're saying the same thing. Try asking a specific programming question!",
                    conversation_type="general",
                    suggestions=["Explain Python basics", "Write a function", "Debug my code"]
                )
        
        # Update session memory
        if session_key not in session_memory:
            session_memory[session_key] = {}
        session_memory[session_key]['last_message'] = request.message.lower().strip()
        
        # Create initial state
        initial_state = {
            "user_input": request.message,
            "conversation_type": "",
            "context": {},
            "response": ""
        }
        
        # Run the conversation graph
        result = conversation_graph.invoke(initial_state)
        
        # Extract response
        response_message = result.get("response", "I'm not sure how to help with that.")
        conversation_type = result["conversation_type"]
        
        # Generate suggestions based on conversation type
        suggestions = []
        if conversation_type == "explanation":
            suggestions = ["Show me an example", "What are the best practices?", "Common mistakes to avoid?"]
        elif conversation_type == "code_generation":
            suggestions = ["Review this code", "How can I optimize it?", "Add error handling"]
        elif conversation_type == "debugging":
            suggestions = ["Explain the fix", "How to prevent this?", "Test this solution"]
        elif conversation_type == "code_review":
            suggestions = ["More optimizations?", "Security considerations?", "Performance tips?"]
        elif conversation_type == "learning_path":
            suggestions = ["Beginner projects", "Advanced topics", "Practice exercises"]
        else:
            suggestions = ["Explain a concept", "Help me code", "Debug an issue"]
        
        return ChatResponse(
            reply=response_message,
            conversation_type=conversation_type,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Coding Mentor Chatbot"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)