# Multimodal RAG: Chat with Text, Tables, Images & Charts

A beginner-friendly **Multimodal Retrieval-Augmented Generation (RAG)** project.
Ask questions about a PDF and get answers grounded in its **text, tables, images, charts and diagrams**, with page numbers.

Built with **LangChain**, **Pinecone**, **Groq** (text + vision LLMs), **PyMuPDF** and **Hugging Face embeddings**.

![Architecture](docs/architecture.png)

## Why this project?

A normal text-only RAG pipeline extracts the text of a PDF and throws the rest away. But real documents also contain charts, diagrams and tables, and many answers live there:

| Question | Where the answer lives |
|---|---|
| "Which quarter had the highest revenue?" | A line chart |
| "Where is the critical quality-control point?" | A supply-chain diagram |
| "Which region had the highest growth?" | A table |

This project converts every modality into something searchable, and keeps the **original image** so a vision model can look at it when answering.

## How it works (in 30 seconds)

**Phase 1: Ingestion (once per PDF)**
1. PyMuPDF extracts **text**, **tables** (as Markdown) and **images** from every page.
2. A Groq **vision model** writes a short factual summary of each image or chart.
3. Everything is turned into LangChain `Document`s with metadata (`page`, `modality`, `image_path`).
4. A Hugging Face model (`all-MiniLM-L6-v2`) embeds them and they are stored in a **Pinecone** index.

**Phase 2: Question answering (every question)**
1. Your question is embedded and Pinecone returns the most similar documents.
2. If any retrieved document is a **visual**, the original image + context go to the **vision LLM**.
3. Otherwise the context goes to the **text LLM**.
4. The answer cites page numbers.

## Project structure

```
multimodal-rag-project/
├── main.ipynb            # The full pipeline, step by step (start here)
├── requirements.txt      # Python dependencies
├── .env.example          # Template for your API keys (copy to .env)
├── .gitignore            # Keeps secrets and generated files out of Git
├── README.md             # You are here
├── data/
│   └── Multimodal_RAG_LangChain_Pinecone_With_Examples_pptx.pdf   # Sample input PDF
└── docs/
    ├── Project_Documentation.docx   # Detailed beginner guide
    └── architecture.png             # Architecture diagram
```

Folders created automatically when you run the notebook: `novacore_extracted_images/` (extracted images, ignored by Git) and `.env` (your keys, ignored by Git).

## Quick start

**Prerequisites:** Python 3.10+ (developed on 3.12), a free [Groq](https://console.groq.com/keys) API key and a free [Pinecone](https://app.pinecone.io) API key.

```bash
# 1. Clone
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys
copy .env.example .env         # Windows   (macOS/Linux: cp .env.example .env)
# then open .env and paste your GROQ_API_KEY and PINECONE_API_KEY

# 5. Launch the notebook
jupyter notebook main.ipynb
```

Then run the cells from top to bottom. The first run downloads the embedding model (about 90 MB) and creates the Pinecone index automatically.

## Configuration

All settings are in the 4th code cell of `main.ipynb`:

| Variable | Default | Meaning |
|---|---|---|
| `TEXT_MODEL` | `openai/gpt-oss-20b` | Groq model for text-only answers |
| `VISION_MODEL` | `qwen/qwen3.8-27b` | Groq model that reads images |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Turns text into 384-number vectors |
| `PINECONE_INDEX_NAME` | `novacore-multimodal-rag` | Name of the Pinecone index |
| `PINECONE_NAMESPACE` | `fy2026-demo` | Separate "folder" inside the index |

> Model availability on Groq changes over time. If a model name is rejected, pick a current one from the [Groq models page](https://console.groq.com/docs/models).

## Example questions

```python
ask_rag("Which region had the highest year-over-year revenue growth?")
ask_rag("According to the revenue graph, which quarter had the highest revenue?", show_images=True)
ask_rag("According to the supply-chain diagram, what is the critical quality-control point?", show_images=True)
ask_rag("How did average support resolution time change from January to August?", show_images=True)
```

## Security: protect your API keys

- Keys live **only** in your local `.env` file, which `.gitignore` excludes.
- **Never** paste a key into the notebook or commit it. Bots scan public GitHub repos for keys within minutes.
- If a key was ever shared or committed, **revoke it** in the Groq / Pinecone console and create a new one.

## Known limitations

- `ask_rag` keeps only the top 2 retrieved documents, 3,000 characters of context and 1 image to stay inside token limits, so broad multi-part questions can come back with "could not find that information".
- Every embedded image gets a vision summary, including logos, which adds some noise to the index.
- Page numbers are stored as floats by Pinecone (`7.0`).

See `docs/Project_Documentation.docx` for troubleshooting and improvement ideas.

## Credits

The slide deck in `data/` and the fictional *NovaCore* demo scenario come from the DSwithBappy multimodal RAG tutorial material. All NovaCore figures are fictional.
