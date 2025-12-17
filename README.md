# Claire 🧠🎙️

> *"Memoryless AI is just autocomplete with delusions."*

**Claire** is a context-native voice assistant designed to solve the fundamental limitation of modern LLMs: **Amnesia.** Unlike standard chatbots that reset every session, Claire possesses a persistent long-term memory, allowing for continuous, evolving conversations that feel human.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange)
![Deepgram](https://img.shields.io/badge/Audio-Deepgram-red)
![ElevenLabs](https://img.shields.io/badge/Voice-ElevenLabs-white)

---

## 🧐 The Problem

Despite the rapid advancement of Large Language Models (LLMs), the user experience remains fragmented and inefficient.

1.  **Context Amnesia:** Every time you open ChatGPT or Gemini, you are talking to a stranger. You have to re-explain your preferences, history, and constraints.
2.  **Prompt Fatigue:** The user is forced to be the "Manager," constantly engineering prompts to get the desired output.
3.  **High Latency:** Most voice assistants are just "Text-to-Speech" wrappers with 3-5 second delays, breaking the illusion of conversation.

## 💡 The Solution

**Project Claire** is an experiment in **Persistent AI**. It decouples the "Brain" (LLM) from the "Memory" (Context), allowing the assistant to retain information across sessions, reboots, and days.

### Core Capabilities
* **Infinite Recall:** Uses a Vector Database (FAISS/Chroma) to store and retrieve past interactions via RAG (Retrieval-Augmented Generation).
* **Sub-Second Latency:** Optimized pipeline using **Deepgram Nova-2** (STT) and **Gemini 1.5 Flash** for near-instant responses.
* **Human Parity Voice:** Integrated with **ElevenLabs** for emotive, non-robotic speech synthesis.
* **Proactive Context:** Injects relevant past memories into current prompts automatically, mitigating the need for detailed user instruction.

---

## ⚙️ Tech Stack

This project uses a modular "Micro-Brain" architecture:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **The Brain** | **Google Gemini 2.5 Flash** | Reasoning, personality, and response generation. |
| **The Ears** | **Deepgram Nova-2** | Ultra-fast Speech-to-Text (STT) transcription. |
| **The Voice** | **ElevenLabs (Rachel)** | High-fidelity Text-to-Speech (TTS). |
| **The Memory** | **LangChain + FAISS** | Vector storage for long-term context retention. |
| **Backend** | **FastAPI** | Async Python server handling the audio pipeline. |
| **Frontend** | **Streamlit** | React-like interface for audio capture and playback. |

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* API Keys for:
    * [Google AI Studio](https://aistudio.google.com/) (Gemini)
    * [Deepgram](https://deepgram.com/)
    * [ElevenLabs](https://elevenlabs.io/)

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/project-claire.git](https://github.com/yourusername/project-claire.git)
    cd project-claire
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the `backend/` directory:
    ```bash
    # backend/.env
    GEMINI_API_KEY="your_google_key"
    DEEPGRAM_API_KEY="your_deepgram_key"
    ELEVENLABS_API_KEY="your_elevenlabs_key"
    ```

---

## ⚡ Usage

To run the application, you need to launch the Backend (Brain) and Frontend (Interface) in separate terminals.

**Terminal 1: Backend**
```bash
cd backend
uvicorn main:app --reload

```

*You should see: `INFO: Application startup complete.*`

**Terminal 2: Frontend**

```bash
streamlit run frontend/app.py

```

*This will automatically open the UI in your browser at `http://localhost:8501`.*

---

## 📂 Project Structure

```text
project-claire/
├── backend/
│   ├── main.py            # FastAPI entry point & orchestration
│   ├── memory.py          # RAG logic & Vector DB management
│   └── .env               # API Secrets (Not committed)
├── frontend/
│   └── app.py             # Streamlit UI & Audio handling
└── requirements.txt       # Python dependencies

```

## 🔮 Roadmap (v0.2 and beyond)

* [ ] **Local TTS Fallback:** Implement Deepgram Aura / Edge TTS for lower latency and cost.
* [ ] **State Mutation:** Allow memory to be updated/corrected (e.g., "Actually, I don't like spinach anymore").
* [ ] **Action Layer:** Integrate tool calling (Calendar, Email) via LangGraph.

## 🤝 Author

**Kumar Manik**
*AI Engineer*

[LinkedIn](https://linkedin.com/in/kumar2000manik)

---

*Built with 💻 and ☕ by a human trying to make machines remember.*

```

```
