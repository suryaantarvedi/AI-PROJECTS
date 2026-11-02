# 🤖 Ollama Local AI Chatbot

An interactive chatbot built with **Python**, **Streamlit**, and **Ollama**, running large language models **fully locally**: no API keys, no cloud costs, and your data never leaves your machine.

## Features

- 💬 Real-time **streaming responses** (token-by-token with a typing cursor)
- 🧠 **Conversation memory** within a session (full chat history sent to the model each turn)
- 🔀 **Model selector**: llama3.2, llama3.1, llama3, mistral, gemma2, qwen2.5, qwen2.5:3b
- 🌡️ **Temperature slider** to control creativity (0.0 focused → 1.0 creative)
- 📝 **Editable system prompt** to change the assistant's behaviour on the fly
- 🧹 **Clear Chat** button to reset the conversation
- 🩺 **Ollama health check**: shows clear instructions if the server isn't running
- ⚠️ Helpful error message when a selected model hasn't been downloaded
- 🎨 Custom dark UI with green accents

## Tech Stack

| Component | Purpose |
|-----------|---------|
| Python 3.9+ | Core language |
| Streamlit | Web UI and chat components |
| Requests | HTTP calls to the Ollama API |
| Ollama | Local LLM runtime |

## How It Works

```
User input → Streamlit UI → build messages (system prompt + history)
          → POST http://localhost:11434/api/chat (stream=True)
          → read response line by line (JSON chunks)
          → render live in the chat window → save reply to session state
```

1. On load, the app pings `http://localhost:11434` to confirm Ollama is running.
2. When the user sends a message, it is added to `st.session_state.messages`.
3. The app builds a payload: the system prompt followed by the full chat history, plus the chosen model and temperature.
4. The request goes to Ollama's `/api/chat` endpoint with `stream: true`.
5. Each JSON chunk is parsed and appended to the on-screen response until `done` is `true`.
6. The final response is stored in session state so the next turn has context.

## Prerequisites

- Python 3.9 or higher
- [Ollama](https://ollama.com/download) installed

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/suryaantarvedi/<your-repo-name>.git
cd <your-repo-name>

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install streamlit requests
```

## Setup Ollama

```bash
# Start the Ollama server (skip if it's already running as a background service)
ollama serve

# Download at least one model
ollama pull llama3.2
```

Pull any other model you want to use from the dropdown, e.g. `ollama pull mistral`.

## Run the App

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

## Usage

1. Pick a model in the sidebar (make sure it's pulled).
2. Adjust the temperature and system prompt if you want.
3. Type a question in the chat box and press Enter.
4. Use **Clear Chat** to start a fresh conversation.

## Configuration

| Setting | Where | Default |
|---------|-------|---------|
| Ollama URL | `OLLAMA_URL` in `app.py` | `http://localhost:11434/api/chat` |
| Model list | `st.selectbox` in sidebar | llama3.2, llama3.1, llama3, mistral, gemma2, qwen2.5, qwen2.5:3b |
| Temperature | Sidebar slider | 0.7 |
| System prompt | Sidebar text area | "You are a helpful AI assistant..." |
| Request timeout | `timeout=120` in `requests.post` | 120 seconds |

To add another model, append its name to the list in the `st.selectbox` call.

## Project Structure

```
.
├── app.py          # Streamlit app (UI, Ollama integration, chat logic)
└── README.md
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Ollama is not running" error | Run `ollama serve` in a terminal, then refresh the page |
| HTTP error / model not found | Run `ollama pull <model-name>` for the model selected in the sidebar |
| Very slow responses | Use a smaller model (e.g. `qwen2.5:3b`, `llama3.2`); larger models need more RAM/GPU |
| Request timed out | Increase `timeout` in `requests.post`, or switch to a lighter model |
| Chat history lost on refresh | Expected: history lives in Streamlit session state, not on disk |

## Limitations

- Chat history is not persisted after the browser tab is refreshed or closed.
- Very long conversations may exceed the model's context window, since the full history is sent every turn.
- Requires Ollama running on the same machine (or an updated `OLLAMA_URL`).

## Future Improvements

- Save and load chat history (JSON / SQLite)
- Auto-detect installed models via Ollama's `/api/tags` endpoint
- Export conversation as text or PDF
- Document Q&A (RAG) with local embeddings
- Docker setup

## Author

**Surya** — [GitHub](https://github.com/suryaantarvedi)

## License

This project is open source and available under the [MIT License](LICENSE).
