# ERP RAG Chatbot — HR & Customer Support

A production-ready **RAG (Retrieval-Augmented Generation)** chatbot for the **NOVAERP** Egyptian ERP System, serving both **HR** and **Customer Support** use cases. It ingests a comprehensive PDF manual, builds a FAISS vector index, and uses a local LLM (Llama 3.2 via LM Studio) to generate accurate, context-grounded responses — deployed as a Flask REST API with Docker support.

---

## Dual-Module Design

This chatbot serves two roles within the NOVAERP system:

| Module | Purpose | Queries |
|--------|---------|---------|
| **HR Chatbot** | Answers employee questions about ERP policies, leave, payroll, attendance, and internal procedures | *"How many annual leave days am I entitled to?"*, *"What is the overtime policy?"* |
| **Customer Support** | Answers external customer questions about system features, account management, and troubleshooting | *"How do I reset my password?"*, *"Where can I find my invoice history?"* |

Both modules share the same RAG pipeline, FAISS index, and Flask API — the only difference is the system prompt and context framing, which can be switched via environment configuration.

---

## Highlights

- **RAG Architecture** — The chatbot follows a retrieval-augmented generation pipeline: the PDF manual is split into overlapping chunks, embedded with `sentence-transformers/all-MiniLM-L6-v2`, and indexed with FAISS. At query time, the top-k most similar chunks are retrieved and passed as context to the LLM, ensuring answers are grounded in the actual ERP documentation rather than hallucinated.
- **Local LLM via LM Studio** — Uses LM Studio as a local OpenAI-compatible API server running `llama-3.2-3b-instruct`. This means zero cloud API costs, full data privacy (no documents leave the machine), and offline capability. The model's low temperature (0.3) ensures focused, deterministic responses rather than creative hallucinations.
- **Flask REST API** — Clean, production-grade API with four endpoints: health check, configuration inspection, and two query modes (POST JSON body and GET URL-encoded). CORS-enabled for frontend integration. Proper error handling with 400/404/500/503 status codes.
- **Docker Deployment** — Includes a Dockerfile and docker-compose.yml for containerized deployment. The Docker setup includes a health check, volume mounting for the PDF, and environment variable injection. LM Studio runs on the host and is accessed via `host.docker.internal`.
- **Pydantic Configuration** — All settings are managed through a structured `SystemConfig` class using Pydantic BaseModel with six sub-configs (LMStudio, Document, Embedding, Retrieval, Flask, Logging). Every parameter is overridable via `.env` environment variables, with sensible defaults for the Egyptian ERP manual.
- **Interactive Test Clients** — Two testing tools included: `test_api.py` for interactive terminal-based Q&A sessions, and `quick_test.py` for automated health check and single-query verification.

---

## Project Structure

```
erp-rag-chatbot/
├── README.md                                        # Project documentation
├── requirements.txt                                 # Python dependencies
├── .gitignore                                       # Git ignore rules
├── .env.template                                    # Environment variable template
├── config.py                                        # Pydantic configuration module
├── main_app.py                                      # Flask API server & chatbot logic
├── Dockerfile                                       # Docker image definition
├── docker-compose.yml                               # Docker Compose orchestration
├── start.bat                                        # Windows startup script
├── start.sh                                         # Linux/Mac startup script
├── GETTING_STARTED.md                                # Quick-start guide
├── SETUP_SUMMARY.txt                                # Detailed setup documentation
│
├── notebook/
│   └── another_chatbot.ipynb                        # Alternative chatbot implementation
│
├── src/
│   ├── test_api.py                                  # Interactive API test client
│   └── quick_test.py                                # Automated health & query test
│
└── data/
    └── Egyptian_ERP_System_Comprehensive_Manual.pdf  # Knowledge base (not in repo)
```

---

## How It Works

### 1. Document Ingestion

When the server starts, `EnterpriseCustomerSupportChatbot.__init__()` triggers the ingestion pipeline:

1. **PDF Loading** — `PyPDFLoader` reads the Egyptian ERP manual page by page, creating one LangChain `Document` per page with page-number metadata.
2. **Filtering** — Pages with fewer than 50 characters of content are discarded (blank pages, cover pages with only images).
3. **Chunking** — `RecursiveCharacterTextSplitter` splits each page into overlapping chunks (default: 600 characters with 100-character overlap). The overlap ensures that information spanning chunk boundaries is not lost.
4. **Embedding** — Each chunk is embedded using `sentence-transformers/all-MiniLM-L6-v2`, a lightweight 384-dimensional model optimized for semantic similarity search.
5. **FAISS Indexing** — All embeddings are stored in a FAISS (Facebook AI Similarity Search) index for sub-millisecond retrieval.

### 2. Query Processing

When a question arrives at `/ask`:

1. **Retrieval** — The question is embedded using the same model, and FAISS performs similarity search to find the top-k most relevant chunks (default k=10).
2. **Context Assembly** — Retrieved chunks are assembled into a context string with page numbers: `[Page N] chunk text`.
3. **Prompt Construction** — A structured prompt instructs the LLM to answer based strictly on the context, with formatting guidelines (bold terms, bullet points, concise paragraphs).
4. **Generation** — LM Studio's local LLM generates the answer using the provided context.
5. **Response** — The API returns the answer, source page numbers, processing time, and document count.

### 3. Architecture

```
User Question (HR or Customer Support)
    ↓
Flask API (/ask endpoint)
    ↓
FAISS Similarity Search → Top-K Relevant Chunks
    ↓
Prompt Construction (Context + Question)
    ↓
LM Studio LLM (Local llama-3.2-3b-instruct)
    ↓
Structured JSON Response
```

### 4. Configuration System

All settings are managed through Pydantic models loaded from `.env`:

| Config Class | Key Settings |
|-------------|-------------|
| `LMStudioConfig` | base_url, api_key, model, temperature |
| `DocumentConfig` | file_path, chunk_size, chunk_overlap |
| `EmbeddingConfig` | model name (sentence-transformers) |
| `RetrievalConfig` | similarity_k (top-k chunks) |
| `FlaskConfig` | host, port, debug mode |
| `LoggingConfig` | log level, log file |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with chatbot readiness status |
| `/config` | GET | View current configuration |
| `/ask` | POST | Ask a question (JSON body: `{"question": "..."}`) |
| `/ask/<question>` | GET | Ask a question (URL-encoded) |
| `/api/docs` | GET | API documentation |

### Example Request

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'
```

### Example Response

```json
{
  "success": true,
  "answer": "To reset your password, click the **Forgot Password** link on the login page...",
  "sources": [12, 45, 67],
  "processing_time_ms": 3421.56,
  "documents_retrieved": 10
}
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- LM Studio running with `llama-3.2-3b-instruct` loaded on `http://localhost:1234/v1`
- 4GB+ RAM
- `Egyptian_ERP_System_Comprehensive_Manual.pdf` placed in the project root

### Quick Start

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.template .env
# Edit .env if needed

# 4. Start server
python main_app.py
```

### Docker Deployment

```bash
# Build
docker build -t erp-rag-chatbot .

# Run
docker run -p 5000:5000 \
  -e FILE_PATH=Egyptian_ERP_System_Comprehensive_Manual.pdf \
  -v $(pwd):/app \
  erp-rag-chatbot

# Or with docker-compose
docker-compose up -d
```

### Testing

```bash
# Interactive test client
python src/test_api.py

# Quick automated test
python src/quick_test.py
```

---

## Configuration

All settings can be customized via the `.env` file:

```ini
# LM Studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=llama-3.2-3b-instruct
TEMPERATURE=0.3

# Document
FILE_PATH=Egyptian_ERP_System_Comprehensive_Manual.pdf
CHUNK_SIZE=600
CHUNK_OVERLAP=100

# Embedding
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Retrieval
SIMILARITY_K=10

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Logging
LOG_LEVEL=INFO
```

### Performance Tuning

| Priority | CHUNK_SIZE | SIMILARITY_K | Response Time |
|----------|-----------|-------------|---------------|
| Speed | 400 | 5 | < 5 seconds |
| Balanced | 600 | 10 | 5-10 seconds |
| Accuracy | 1000 | 12 | 5-15 seconds |

---

## Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.11 |
| **Web Framework** | Flask 3.0 + Flask-CORS |
| **RAG Framework** | LangChain (community, core, text-splitters) |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) |
| **Vector Store** | FAISS (CPU) |
| **LLM** | Llama 3.2 3B Instruct via LM Studio |
| **PDF Processing** | pypdf |
| **Configuration** | Pydantic 2.5 + python-dotenv |
| **Containerization** | Docker + Docker Compose |
| **Testing** | requests + custom test client |

---

## Part of NOVAERP

This project is part of the **NOVAERP** system, serving as both the **HR Chatbot** and **Customer Support Chatbot** module. It is designed to answer employee and customer queries about the Egyptian ERP System by retrieving relevant information from the comprehensive manual and generating accurate, context-grounded responses.

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| "PDF not found" | Ensure `Egyptian_ERP_System_Comprehensive_Manual.pdf` is in the project root |
| "LM Studio connection failed" | Verify LM Studio is running on `http://localhost:1234` with model loaded |
| "Port 5000 already in use" | Change `FLASK_PORT` in `.env` to another port (e.g., 8000) |
| "Module not found" | Activate virtual environment and run `pip install -r requirements.txt` |
| Slow responses | Reduce `CHUNK_SIZE` to 400 and `SIMILARITY_K` to 5 in `.env` |

---

## License

This project is open source and available for educational and personal use.
