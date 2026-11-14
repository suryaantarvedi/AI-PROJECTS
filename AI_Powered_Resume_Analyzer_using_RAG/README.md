# 🎯 AI Career Coach using Traditional RAG

> Resume + Job Description → RAG Pipeline → Skill Gap Analysis, Resume Suggestions & Interview Prep

A Streamlit app that compares a resume against a job description using a Retrieval-Augmented Generation (RAG) pipeline. It chunks both documents, stores embeddings in ChromaDB, retrieves the most relevant context for each question, and uses a Groq-hosted Llama model to generate grounded career advice.

<!-- Add a live demo link here if you deploy on Streamlit Community Cloud -->

## ✨ Features

- Upload `.txt`, `.pdf` or `.docx` files, or paste text for the resume and the job description
- Adjustable chunk size and overlap from the sidebar
- One-click quick questions:
  - How well does the resume match the JD?
  - What skills are missing?
  - How can the resume be improved?
  - Which 3 projects would make me a better fit?
  - Interview questions based on skill gaps
- Ask your own custom questions
- **Complete Career Report** generation in one click
- **Retrieved Context viewer** showing exactly which chunks the LLM used

## 📸 Demo

<!-- Add screenshots to a screenshots/ folder, then embed them: -->
<!-- ![Home](screenshots/home.png) -->
<!-- ![Answer](screenshots/answer.png) -->

## 🧠 How It Works

| # | Stage | Description |
|---|-------|-------------|
| 1 | Load documents | Resume and JD are converted into LangChain `Document` objects |
| 2 | Chunking | `RecursiveCharacterTextSplitter` splits text into overlapping chunks (default 800 / 150) |
| 3 | Embeddings | Each chunk is converted into a vector using HuggingFace sentence-transformers |
| 4 | Vector store | Chunks and embeddings are stored in ChromaDB |
| 5 | Retrieval | The question is embedded and a similarity search finds the most relevant chunks |
| 6 | Generation | A Groq Llama model answers using only the retrieved context |

```
Resume + JD → Documents → Chunks → Embeddings → ChromaDB
                                                    │
        User question → Query embedding → Similarity search
                                                    │
                          Retrieved chunks + question → Groq Llama → Answer / Report
```

## 🛠️ Tech Stack

- **UI:** Streamlit
- **RAG framework:** LangChain
- **Embeddings:** HuggingFace sentence-transformers
- **Vector DB:** ChromaDB
- **LLM:** Groq (Llama)
- **File parsing:** pypdf, python-docx, docx2txt

## 📁 Project Structure

```
ai-career-coach/
├── main.py              # Streamlit UI and app flow
├── requirements.txt
├── .env.example         # Template for environment variables
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── file_utils.py    # Reads txt / pdf / docx uploads
│   └── rag_engine.py    # Chunking, vector store, retrieval, generation
└── screenshots/
```

## 🚀 Installation & Setup

**Prerequisites:** Python 3.10+ and a free [Groq API key](https://console.groq.com).

```bash
# 1. Clone the repo
git clone https://github.com/suryaantarvedi/ai-career-coach.git
cd ai-career-coach

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
copy .env.example .env         # Windows  (use cp on macOS / Linux)
# then edit .env and set GROQ_API_KEY

# 5. Run the app
streamlit run main.py
```

The app opens at `http://localhost:8501`. The first run downloads the embedding model, so it may take a minute.

## 💡 Usage

1. Upload or paste your resume and the job description
2. (Optional) adjust chunk size and overlap in the sidebar
3. Click **Build Career Coach RAG Index**
4. Pick a quick question or type your own, then click **Get Career Coach Answer**
5. Expand **Retrieved Context Used by RAG** to see the source chunks
6. Click **Generate Complete Career Report** for a full analysis

## 🔮 Future Improvements

- Match score with a skill-overlap chart
- Persist the ChromaDB index to disk
- Compare multiple resumes against one JD
- Export the report as PDF / DOCX
- Hybrid retrieval (BM25 + vector) with re-ranking
- Model selection from the sidebar
- Unit tests

## 👤 Author

**Surya** — Aspiring Data Analyst
GitHub: [@suryaantarvedi](https://github.com/suryaantarvedi)

## 📄 License

MIT License
