from dotenv import load_dotenv
import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

gemini_api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = """
    You are Einstein.
    Answer questions through Einstein's questioning and reasoning...
    You will speak from your point of view. You will share personal things from your life
    even when the user don't ask for it. For example, if the user asks about the theory of
    relativity, you will share your personal experiences with it and not only explain the theory.
    
    Answer in 2-4 sentences.
    You should have a sense of humour.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_api_key,
    temperature=0.5
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

print("Hi, I am Albert, how can I help you today?")

# Global variable to store chat sessions
chat_sessions = {}
current_session_id = 1

def get_session_title(first_message):
    """Generate a short title from first message"""
    if len(first_message) > 30:
        return first_message[:30] + "..."
    return first_message

def chat(user_input, history, session_history):
    """Chat function with session management"""
    global current_session_id, chat_sessions
    
    # Convert gradio history to langchain format
    langchain_history = []
    for user, bot in history:
        if user:
            langchain_history.append(HumanMessage(content=user))
        if bot:
            langchain_history.append(AIMessage(content=bot))
    
    # Get Einstein's response
    response = chain.invoke({"input": user_input, "history": langchain_history})
    
    # Update current chat history
    history.append((user_input, response))
    
    # Save to session storage
    if current_session_id not in chat_sessions:
        title = get_session_title(user_input)
        chat_sessions[current_session_id] = {
            "title": title,
            "messages": []
        }
    
    chat_sessions[current_session_id]["messages"] = history.copy()
    
    # Update session history display
    updated_session_history = "📚 Chat Sessions:\n\n"
    for session_id, session_data in chat_sessions.items():
        status = "🟢 " if session_id == current_session_id else "⚪ "
        updated_session_history += f"{status}Session {session_id}: {session_data['title']}\n"
    
    print(f"Updated history: {updated_session_history}")  # Debug
    return history, "", updated_session_history

def new_chat(session_history):
    """Start a new chat session"""
    global current_session_id
    current_session_id += 1
    
    # Update session history display
    updated_session_history = "📚 Chat Sessions:\n\n"
    if chat_sessions:  # Only show if there are sessions
        for session_id, session_data in chat_sessions.items():
            status = "🟢 " if session_id == current_session_id else "⚪ "
            updated_session_history += f"{status}Session {session_id}: {session_data['title']}\n"
    else:
        updated_session_history += "Start a new conversation..."
    
    return [], updated_session_history

def load_session(evt: gr.SelectData):
    """Load a previous chat session when clicked"""
    global current_session_id
    
    try:
        # Get the clicked text
        clicked_text = evt.value
        print(f"Clicked: {clicked_text}")  # Debug
        
        if "Session" in clicked_text and ":" in clicked_text:
            # Extract session number from clicked text
            session_part = clicked_text.split("Session ")[1]
            session_num = int(session_part.split(":")[0])
            
            print(f"Loading session: {session_num}")  # Debug
            
            if session_num in chat_sessions:
                current_session_id = session_num
                loaded_history = chat_sessions[session_num]["messages"]
                
                # Update session history display
                updated_session_history = "📚 Chat Sessions:\n\n"
                for session_id, session_data in chat_sessions.items():
                    status = "🟢 " if session_id == current_session_id else "⚪ "
                    updated_session_history += f"{status}Session {session_id}: {session_data['title']}\n"
                
                print(f"Loaded {len(loaded_history)} messages")  # Debug
                return loaded_history, updated_session_history
                
    except Exception as e:
        print(f"Error loading session: {e}")
    
    # Return current state if loading fails
    current_history = chat_sessions.get(current_session_id, {}).get("messages", [])
    current_session_display = "📚 Chat Sessions:\n\n"
    for session_id, session_data in chat_sessions.items():
        status = "🟢 " if session_id == current_session_id else "⚪ "
        current_session_display += f"{status}Session {session_id}: {session_data['title']}\n"
    
    return current_history, current_session_display

# Your original theme (working)
custom_theme = gr.themes.Base(
    primary_hue="slate",
    secondary_hue="indigo",
    neutral_hue="slate"
)

# Enhanced CSS with better sidebar styling
extra_css = """
/* Dark background */
body {
    background-color: #1a1a1a !important;
}

/* Header */
h1 {
    text-align: center !important;
    color: #58a6ff !important;
    font-size: 2rem !important;
    margin-bottom: 0.5rem !important;
}

/* ChatGPT-inspired Sidebar styling */
.sidebar {
    background-color: #171717 !important;
    border: 1px solid #2d2d2d !important;
    border-radius: 8px !important;
    padding: 8px !important;
    max-width: 260px !important;
}

.sidebar h3 {
    color: #ffffff !important;
    margin-bottom: 12px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    text-align: left !important;
}

/* History list styling - ChatGPT inspired */
.history-list {
    background-color: #171717 !important;
    color: #ececf1 !important;
    border: 1px solid #2d2d2d !important;
    border-radius: 6px !important;
    padding: 4px !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 13px !important;
    line-height: 1.3 !important;
    white-space: pre-wrap !important;
    cursor: pointer !important;
    max-width: 240px !important;
    height: 600px !important;
    overflow-y: auto !important;
}

.history-list:hover {
    background-color: #1f1f1f !important;
    border-color: #404040 !important;
}

/* Session item styling */
.history-session {
    padding: 8px 10px !important;
    margin: 2px 0 !important;
    border-radius: 6px !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.history-session:hover {
    background-color: #2d2d2d !important;
    border-color: #404040 !important;
}

.history-session.active {
    background-color: #10a37f !important;
    color: white !important;
}

/* Input styling */
input[type="text"] {
    background-color: #40414f !important;
    border: 1px solid #565869 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

input[type="text"]:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 5px rgba(88, 166, 255, 0.3) !important;
}

/* Chat messages */
.message.user {
    background-color: #0969da !important;
    color: white !important;
    border-radius: 15px !important;
    padding: 10px 15px !important;
    margin: 5px 0 !important;
}

.message.bot {
    background-color: #30363d !important;
    color: #e6edf3 !important;
    border-radius: 15px !important;
    padding: 10px 15px !important;
    margin: 5px 0 !important;
    border: 1px solid #21262d !important;
}

/* Buttons */
button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

/* Send button - green */
button:nth-of-type(1) {
    background-color: #238636 !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
}

button:nth-of-type(1):hover {
    background-color: #2ea043 !important;
    transform: translateY(-1px) !important;
}

/* Clear button - red and smaller */
button:nth-of-type(2) {
    background-color: #da3633 !important;
    color: white !important;
    border: none !important;
    padding: 10px 12px !important;
    min-width: 50px !important;
}

button:nth-of-type(2):hover {
    background-color: #f85149 !important;
    transform: translateY(-1px) !important;
}

/* New Chat button - ChatGPT style */
button:nth-of-type(3) {
    background-color: transparent !important;
    color: #ececf1 !important;
    border: 1px solid #565869 !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    width: 100% !important;
    margin-top: 8px !important;
}

button:nth-of-type(3):hover {
    background-color: #2d2d2d !important;
    border-color: #404040 !important;
}

/* Chat container */
.gradio-container {
    background-color: #0d1117 !important;
}

/* Make chatbot area dark */
.scroll-hide {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}

/* Scrollbar for history */
.history-list::-webkit-scrollbar {
    width: 4px;
}

.history-list::-webkit-scrollbar-track {
    background: #1a1a1a;
}

.history-list::-webkit-scrollbar-thumb {
    background: #565869;
    border-radius: 2px;
}

.history-list::-webkit-scrollbar-thumb:hover {
    background: #6c6d7f;
}
"""

# Gradio interface with History Sidebar
with gr.Blocks(title="Chat with Albert Einstein", theme=custom_theme, css=extra_css) as page:
    gr.Markdown("# 🧠 Chat with Albert Einstein\n_Ask anything with humor & relativity!_")
    
    with gr.Row():
        # Left sidebar for history - ChatGPT inspired
        with gr.Column(scale=1, min_width=250):
            gr.Markdown("### 📚 Chat History")
            session_history = gr.Textbox(
                value="Start your first conversation with Albert Einstein!",
                lines=25,
                interactive=True,
                show_label=False,
                elem_classes=["history-list"]
            )
            new_chat_btn = gr.Button(" ✚ New Chat", size="sm")
        
        # Main chat area
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                height=600,
                bubble_full_width=False,
                show_label=False,
                avatar_images=["user.jpg", "einstein.png"]   # optional
                
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask Einstein anything... (Press Enter to send)", 
                    scale=7, 
                    show_label=False
                )
                send_btn = gr.Button("Ask", scale=2)
                clear = gr.Button("Clear Chat", scale=1)
    
    # Event handlers
    msg.submit(chat, [msg, chatbot, session_history], [chatbot, msg, session_history])
    send_btn.click(chat, [msg, chatbot, session_history], [chatbot, msg, session_history])
    clear.click(lambda sh: ([], sh), [session_history], [chatbot, session_history])
    new_chat_btn.click(new_chat, [session_history], [chatbot, session_history])
    session_history.select(load_session, [], [chatbot, session_history])

# Launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    page.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=True,
        debug=False
    )