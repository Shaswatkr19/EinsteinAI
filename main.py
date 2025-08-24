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

def chat(user_input, history):
    """Proper user/bot tuple formatting for Gradio Chatbot"""
    langchain_history = []
    for user, bot in history:
        if user:
            langchain_history.append(HumanMessage(content=user))
        if bot:
            langchain_history.append(AIMessage(content=bot))
    
    response = chain.invoke({"input": user_input, "history": langchain_history})
    
    # Append as (user_msg, bot_msg) tuple
    history.append((user_input, response))
    return history, ""

# Your original theme (working)
custom_theme = gr.themes.Base(
    primary_hue="slate",
    secondary_hue="indigo",
    neutral_hue="slate"
)

# Enhanced CSS (simple and working)
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

/* Input styling */
input[type="text"] {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
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
"""

# Simple Gradio interface (based on your original)
with gr.Blocks(title="Chat with Albert Einstein", theme=custom_theme, css=extra_css) as page:
    gr.Markdown("# 🧠 Chat with Albert Einstein\n_Ask anything with humor & relativity!_")
    
    chatbot = gr.Chatbot(
    height=500,
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
    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    send_btn.click(chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot)

# Launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    page.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=True,
        debug=False
    )