# Agentic RAG with LangGraph

An agentic Retrieval-Augmented Generation (RAG) assistant built with **LangGraph**. Instead of blindly passing retrieved text to an LLM, the agent **decides** where to look, **grades** the evidence it finds, **falls back to web search** when its knowledge base is not enough, and **rewrites the query** to retry before giving up.

> Full explanation for beginners: [`docs/Project_Documentation.docx`](docs/Project_Documentation.docx)

## How it works

![Workflow graph](docs/workflow_graph.png)

1. **Router** – greetings/small talk go straight to a direct answer; technical questions go to the knowledge base.
2. **KB retrieval** – top-4 chunks are fetched from a Pinecone vector index.
3. **KB grader** – an LLM judges whether the chunks can actually answer the question (`good` / `weak`).
4. **Web fallback** – if the KB evidence is weak, Tavily web search is used.
5. **Web grader** – the web results are graded the same way.
6. **Query rewrite + retry** – if web evidence is also weak, the query is rewritten and retried (max 1 retry, so no infinite loops).
7. **Answer** – generated from the KB, from the web, or a safe "not enough evidence" reply. The source used is tracked in the state.

## Tech stack

| Part | Tool |
|---|---|
| Orchestration | LangGraph |
| LLM | Groq (`openai/gpt-oss-20b`) |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (384 dims) |
| Vector database | Pinecone (serverless, cosine) |
| Web search | Tavily |
| Knowledge base source | LangChain docs page on Agentic RAG |

## Setup

**Requirements:** Python 3.12 (tested), and free API keys for [Groq](https://console.groq.com), [Tavily](https://tavily.com) and [Pinecone](https://www.pinecone.io).

```bash
git clone <your-repo-url>
cd agentic-rag-langgraph

python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
```

Create your keys file:

```bash
cp .env.example .env
# then open .env and paste your real keys
```

## Run

1. Open `main.ipynb` in Jupyter or VS Code.
2. Run the cells from top to bottom.
3. The first time, the Pinecone cell creates the index and uploads the document chunks. After that, the **"Load Existing Index"** cell reuses it, so you do not need to re-upload.
4. Ask questions with `ask_agent("your question")`.

Example questions included in the notebook:

- A KB question about Agentic RAG
- A question that triggers the **web fallback** (Tavily)
- A greeting that takes the **direct** path
- A current/external question about the `langchain-tavily` package

## Project structure

```
agentic-rag-langgraph/
├── main.ipynb                      # full implementation
├── requirements.txt                # pinned dependencies
├── .env.example                    # template for API keys
├── docs/
│   ├── Project_Documentation.docx  # beginner-friendly project guide
│   └── workflow_graph.png          # LangGraph workflow diagram
└── README.md
```

## Known limitations

- The knowledge base is one web page scraped with `WebBaseLoader`, and the scraped text is mostly site navigation. Because of this the KB grader often marks the evidence `weak`, so even in-scope questions can fall through to web search. Using a cleaner source (markdown/PDF) or a better text extractor would improve KB hits.
- The router only recognises a fixed list of topics; off-topic technical questions are still sent to the KB first.
- Evidence grading is done by an LLM, so it can occasionally be wrong.
- `langchain-community` is being sunset; `WebBaseLoader` may need a replacement in future.

## Security

Never commit your real `.env` file. It is listed in `.gitignore`.
