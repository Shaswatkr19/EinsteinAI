from dotenv import load_dotenv
import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

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
    (MessagesPlaceholder(variable_name="history")),
    ("user", "{input}")]
)

chain = prompt | llm | StrOutputParser()

print("Hi, I am Albert, how can i help you today?")


def chat(user_input, hist):
    print(user_input, hist)

    langchain_history = []
    for item in hist:
        if item['role'] == 'user':
            langchain_history.append(HumanMessage(content=item['content']))
        elif item['role'] == 'assistant':
            langchain_history.append(AIMessage(content=item['content']))    

    response = chain.invoke({"input": user_input, "history": langchain_history})

    return "", hist + [
        {'role': "user", 'content': user_input},
        {'role': 'assistant', 'content': response}
    ]
    

# 🎨 Custom Dark Theme (Professional GitHub Dark Style)
custom_theme = gr.themes.Base(
    primary_hue="slate",
    secondary_hue="indigo",
    neutral_hue="slate"
).set(
    body_background_fill="#0d1117",     # Full dark background
    body_text_color="#e6edf3",          # Light text everywhere
    block_background_fill="#161b22",    # Blocks (slightly lighter)
    block_label_text_color="#58a6ff",   # Accent for labels
    block_title_text_color="#58a6ff",   # Headings
    input_background_fill="#0d1117",    # Textbox background
    input_border_color="#30363d",       # Textbox border
    button_primary_background_fill="#238636",   # Green button
    button_primary_text_color="white",
    button_secondary_background_fill="#21262d",
    button_secondary_text_color="#e6edf3"
)

# ⚡ Extra CSS for chat bubbles (professional look)
extra_css = """
/* User bubble */
.message.user {
    background-color: #1f6feb !important;  /* Blue bubble */
    color: #ffffff !important;             /* White text */
    border-radius: 10px !important;
    padding: 8px 12px !important;
    opacity: 1 !important;
    font-size: 16px !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}

/* Assistant bubble */
.message.bot {
    background-color: #30363d !important;  /* Dark grey bubble */
    color: #e6edf3 !important;             /* Light text */
    border-radius: 10px !important;
    padding: 8px 12px !important;
    opacity: 1 !important;
    font-size: 16px !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}

/* Remove weird transparency everywhere */
.message {
    opacity: 1 !important;
}
"""
# 🧠 Gradio Page
with gr.Blocks(
    title="Chat with Einstein",
    theme=custom_theme,
    css=extra_css
) as page:
    gr.Markdown(
        """
        # 🧠 Chat with Einstein  
        _Step into a conversation with the great Albert Einstein himself._  
        **Ask anything about science, life, or even relativity with a touch of humor!**  
        """
    )

    chatbot = gr.Chatbot(type="messages", height=500, bubble_full_width=False,
                         avatar_images=['user.jpg', 'einstein.png'],
                         show_label=False)

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask Einstein anything...",
            scale=8,
            show_label=False
        )
        clear = gr.Button("🧹 Clear Chat", scale=2)

    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot)

page.launch(share=True)