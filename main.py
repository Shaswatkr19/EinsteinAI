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
    """Convert history dicts → LangChain messages → return chatbot-friendly tuples"""
    langchain_history = []
    for item in history:
        if item[0] == "user":
            langchain_history.append(HumanMessage(content=item[1]))
        elif item[0] == "assistant":
            langchain_history.append(AIMessage(content=item[1]))

    response = chain.invoke({"input": user_input, "history": langchain_history})

    # Gradio.Chatbot expects list of (user, bot) tuples
    history.append(("user", user_input))
    history.append(("assistant", response))
    return history, ""


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

# ⚡ Extra CSS
extra_css = """
.message.user {
    background-color: #1f6feb !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    font-size: 16px !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}
.message.bot {
    background-color: #30363d !important;
    color: #e6edf3 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    font-size: 16px !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}
"""

# 🧠 Gradio Page
with gr.Blocks(title="Chat with Einstein", theme=custom_theme, css=extra_css) as page:
    gr.Markdown("# 🧠 Chat with Einstein\n_Ask anything with humor & relativity!_")

    chatbot = gr.Chatbot(height=500, bubble_full_width=False, show_label=False)

    with gr.Row():
        msg = gr.Textbox(placeholder="Ask Einstein anything...", scale=8, show_label=False)
        clear = gr.Button("🧹 Clear Chat", scale=2)

    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot)

# --------- Render / Local Deployment ---------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    page.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=True,
        debug=False
    )