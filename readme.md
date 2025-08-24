# 🧠 EinsteinAI

**EinsteinAI** is a smart AI chatbot that lets you experience a conversation with **Albert Einstein**! Ask questions, explore ideas, or just chat, and get intelligent, human-like responses powered by advanced AI.

## 🔗 Live Demo

Try it now: **[https://einsteinai-x8l5.onrender.com/](https://einsteinai-x8l5.onrender.com/)**

Deployed publicly on **Render** — accessible anywhere, anytime!

## ✨ What Makes This Special?

🎭 **Einstein's Personality** - Experience Einstein's wit, curiosity, and genius through AI
🧪 **Personal Stories** - Get insights from Einstein's life experiences and scientific journey  
🎯 **Contextual Responses** - Maintains conversation flow with intelligent memory
🎨 **Beautiful UI** - ChatGPT-inspired dark theme with smooth interactions

## 🚀 Features

- 🧠 **Chat like Einstein** – Ask anything and get insightful, personalized answers
- 📚 **Chat History** – Multiple conversation sessions with easy switching
- 💬 **Interactive UI** – Clean, responsive interface built with Gradio
- ⚡ **Fast responses** – Powered by Google's Gemini AI through LangChain
- 🌐 **Public access** – Live on Render, ready for anyone to use
- 🎨 **Dark Theme** – Modern, eye-friendly design
- ⌨️ **Keyboard Support** – Press Enter to send messages

## 🛠 Tech Stack

- **Python 3.8+** – Backend logic
- **Gradio** – Interactive web interface
- **LangChain** – AI orchestration and prompt management
- **Google Gemini AI** – Large language model
- **Render** – Cloud deployment platform
- **dotenv** – Environment variable management


## 💻 Run Locally

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Shaswatkr19/EinsteinAI.git
cd EinsteinAI
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Create .env file
touch .env

# Add your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

5. **Run the application:**
```bash
python main.py
```

6. **Open your browser:**
```
http://localhost:10000
```

## 🌐 Deployment

### Deploy on Render:

1. Fork this repository
2. Connect your GitHub to Render
3. Create a new Web Service
4. Add environment variable: `GEMINI_API_KEY`
5. Deploy automatically!


## 📝 Project Structure

```
EinsteinAI/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── README.md           # Project documentation
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for the language model
- **LangChain** for AI orchestration
- **Gradio** for the amazing web interface
- **Albert Einstein** for the inspiration! 🧠

## 📧 Contact

**Shaswat Kumar** - [@shaswatkr19](https://github.com/Shaswatkr19)

Project Link: [https://github.com/Shaswatkr19/EinsteinAI](https://github.com/Shaswatkr19/EinsteinAI)

---

⭐ **If you found this project helpful, please give it a star!** ⭐