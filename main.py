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

# Mobile responsive CSS
mobile_responsive_css = """
/* Base styles */
* {
    box-sizing: border-box;
}

/* Container */
.gradio-container {
    background-color: #0d1117 !important;
    padding: 10px !important;
}

/* Header - responsive */
h1 {
    text-align: center !important;
    color: #58a6ff !important;
    font-size: clamp(1.5rem, 4vw, 2rem) !important;
    margin-bottom: 1rem !important;
    line-height: 1.2 !important;
}

/* Layout adjustments for mobile */
@media (max-width: 768px) {
    .gradio-container {
        padding: 5px !important;
    }
    
    /* Stack layout on mobile */
    .gr-row {
        flex-direction: column !important;
        gap: 10px !important;
    }
    
    /* History sidebar - mobile adjustments */
    .sidebar-column {
        order: 2 !important;
        min-width: 100% !important;
        max-height: 200px !important;
    }
    
    /* Chat area - mobile first */
    .chat-column {
        order: 1 !important;
        min-width: 100% !important;
    }
    
    /* History list - mobile */
    .history-list {
        height: 150px !important;
        font-size: 12px !important;
        line-height: 1.2 !important;
    }
    
    /* Chatbot - mobile height */
    .chatbot-mobile {
        height: 400px !important;
    }
    
    /* Input row - mobile stack */
    .input-row {
        flex-direction: column !important;
        gap: 8px !important;
    }
    
    /* Message input - full width on mobile */
    .message-input-mobile {
        width: 100% !important;
        min-height: 44px !important;
        font-size: 16px !important; /* Prevents zoom on iOS */
        padding: 12px !important;
    }
    
    /* Buttons - mobile friendly */
    .mobile-buttons {
        display: flex !important;
        gap: 8px !important;
        width: 100% !important;
    }
    
    .mobile-buttons button {
        flex: 1 !important;
        min-height: 44px !important;
        font-size: 14px !important;
    }
}

/* Tablet adjustments */
@media (min-width: 769px) and (max-width: 1024px) {
    .history-list {
        height: 500px !important;
        max-width: 300px !important;
    }
}

/* Desktop - original styling enhanced */
@media (min-width: 1025px) {
    /* History list desktop */
    .history-list {
        height: 600px !important;
        max-width: 260px !important;
    }
}

/* Dark theme - all devices */
body {
    background-color: #0d1117 !important;
}

/* History list styling */
.history-list {
    background-color: #171717 !important;
    color: #ececf1 !important;
    border: 1px solid #2d2d2d !important;
    border-radius: 6px !important;
    padding: 8px !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 13px !important;
    line-height: 1.3 !important;
    white-space: pre-wrap !important;
    cursor: pointer !important;
    overflow-y: auto !important;
}

.history-list:hover {
    background-color: #1f1f1f !important;
    border-color: #404040 !important;
}

/* Input styling - responsive */
input[type="text"], textarea {
    background-color: #40414f !important;
    border: 1px solid #565869 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

input[type="text"]:focus, textarea:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 5px rgba(88, 166, 255, 0.3) !important;
    outline: none !important;
}

/* Buttons - responsive */
button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

/* Send button */
.send-btn {
    background-color: #238636 !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
}

.send-btn:hover {
    background-color: #2ea043 !important;
    transform: translateY(-1px) !important;
}

/* Clear button */
.clear-btn {
    background-color: #da3633 !important;
    color: white !important;
    border: none !important;
    padding: 10px 12px !important;
}

.clear-btn:hover {
    background-color: #f85149 !important;
    transform: translateY(-1px) !important;
}

/* New Chat button */
.new-chat-btn {
    background-color: transparent !important;
    color: #ececf1 !important;
    border: 1px solid #565869 !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    width: 100% !important;
    margin-top: 8px !important;
}

.new-chat-btn:hover {
    background-color: #2d2d2d !important;
    border-color: #404040 !important;
}

/* Chat messages - responsive */
.message.user {
    background-color: #0969da !important;
    color: white !important;
    border-radius: 15px !important;
    padding: 10px 15px !important;
    margin: 5px 0 !important;
    word-wrap: break-word !important;
}

.message.bot {
    background-color: #30363d !important;
    color: #e6edf3 !important;
    border-radius: 15px !important;
    padding: 10px 15px !important;
    margin: 5px 0 !important;
    border: 1px solid #21262d !important;
    word-wrap: break-word !important;
}

/* Chatbot area */
.scroll-hide {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #161b22;
}

::-webkit-scrollbar-thumb {
    background: #565869;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #6c6d7f;
}

/* Touch targets for mobile */
@media (max-width: 768px) {
    button, input, textarea {
        min-height: 44px !important;
    }
}
"""

# 🎨 Custom Dark Theme
custom_theme = gr.themes.Base(
    primary_hue="slate",
    secondary_hue="indigo",
    neutral_hue="slate"
).set(
    body_background_fill="#0d1117",
    body_text_color="#e6edf3",
    block_background_fill="#161b22",
    block_label_text_color="#58a6ff",
    block_title_text_color="#58a6ff",
    input_background_fill="#0d1117",
    input_border_color="#30363d",
    button_primary_background_fill="#238636",
    button_primary_text_color="white",
    button_secondary_background_fill="#21262d",
    button_secondary_text_color="#e6edf3"
)

# Gradio interface with mobile responsiveness
with gr.Blocks(title="Chat with Albert Einstein", theme=custom_theme, css=mobile_responsive_css) as page:
    gr.Markdown("# 🧠 Chat with Albert Einstein\n_Ask anything with humor & relativity!_")
    
    with gr.Row(elem_classes=["main-row"]):
        # Left sidebar for history - responsive
        with gr.Column(scale=1, min_width=250, elem_classes=["sidebar-column"]):
            gr.Markdown("### 📚 Chat History")
            session_history = gr.Textbox(
                value="Start your first conversation with Albert Einstein!",
                lines=25,
                interactive=True,
                show_label=False,
                elem_classes=["history-list"]
            )
            new_chat_btn = gr.Button(" ✚ New Chat", size="sm", elem_classes=["new-chat-btn"])
        
        # Main chat area - responsive
        with gr.Column(scale=4, elem_classes=["chat-column"]):
            chatbot = gr.Chatbot(
                height=600,
                show_label=False,
                elem_classes=["chatbot-mobile"],
                avatar_images=["user.jpg", "einstein.png"]
            )
            
            with gr.Row(elem_classes=["input-row"]):
                with gr.Column(scale=7):
                    msg = gr.Textbox(
                        placeholder="Ask Einstein anything... (Press Enter to send)", 
                        show_label=False,
                        elem_classes=["message-input-mobile"]
                    )
                with gr.Column(scale=3, elem_classes=["mobile-buttons"]):
                    with gr.Row():
                        send_btn = gr.Button("Ask", elem_classes=["send-btn"])
                        clear = gr.Button("Clear", elem_classes=["clear-btn"])
    
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