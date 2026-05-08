# NOVAERP RAG Chatbots — HR & Customer Support

Two Retrieval-Augmented Generation (RAG) chatbots built for the **NOVAERP** Egyptian enterprise system. Both chatbots use FAISS vector search with local LLMs (via LM Studio) to answer questions based on company documentation, each specialized for a different department.

---

## Architecture Overview

```
NOVAERP RAG Chatbots
├── hr-chatbot/                  # HR Department Chatbot
│   ├── main_app.py              # Flask API (port 5001)
│   ├── config.py                # Pydantic configuration
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.template
│   ├── src/
│   │   ├── quick_test.py
│   │   └── test_api.py
│   └── notebook/
│       └── another_chatbot.ipynb
│
└── customer-support-chatbot/    # Customer Support Chatbot
    ├── main_app.py              # Flask API (port 5000)
    ├── config.py                # Pydantic configuration
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env.template
    ├── src/
    │   ├── quick_test.py
    │   └── test_api.py
    └── notebook/
        └── another_chatbot.ipynb
```

---

## How It Works

Both chatbots follow the same RAG pipeline:

1. **Document Ingestion** — PDF manual is loaded and split into chunks using `RecursiveCharacterTextSplitter`
2. **Embedding & Indexing** — Chunks are embedded with `sentence-transformers/all-MiniLM-L6-v2` and stored in a FAISS vector index
3. **Retrieval** — User questions are matched against the vector index using similarity search (top-k)
4. **Generation** — Retrieved context is passed to a local LLM (Llama 3.2 via LM Studio) which generates a grounded answer

The key difference between the two chatbots is the **system prompt** and **port assignment**:

| Feature | HR Chatbot | Customer Support Chatbot |
|---------|-----------|------------------------|
| Purpose | HR policies, leave, benefits, attendance | Customer inquiries, system access, procedures |
| Port | 5001 | 5000 |
| System Prompt | HR Assistant focused on policies & leave | Customer Support Assistant focused on user help |
| Sample Questions | Sick leave, maternity leave, casual leave | Password reset, system access, account issues |

---

## Quick Start

### Prerequisites

- Python 3.11+
- [LM Studio](https://lmstudio.ai/) with Llama 3.2 model loaded
- Your ERP manual PDF file(s)

### 1. Clone & Setup

```bash
git clone https://github.com/aliisnetalive/hr-and-customer-support-erp-chatbot.git
cd hr-and-customer-support-erp-chatbot
```

### 2. HR Chatbot

```bash
cd hr-chatbot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and set your PDF file path

# Place your HR manual PDF in this folder

# Run the chatbot
python main_app.py
# API available at http://localhost:5001
```

### 3. Customer Support Chatbot

```bash
cd customer-support-chatbot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and set your PDF file path

# Place your Customer Support manual PDF in this folder

# Run the chatbot
python main_app.py
# API available at http://localhost:5000
```

### 4. Run with Docker

Each chatbot can be containerized independently:

```bash
# HR Chatbot
cd hr-chatbot
docker-compose up --build

# Customer Support Chatbot
cd customer-support-chatbot
docker-compose up --build
```

> **Note:** Make sure LM Studio is running on the host machine before starting the Docker container. The container uses `host.docker.internal` to reach the LLM server.

---

## API Endpoints

Both chatbots expose the same REST API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check & chatbot readiness |
| `/config` | GET | View current configuration |
| `/ask` | POST | Ask a question (JSON: `{"question": "..."}`) |
| `/ask/<question>` | GET | Ask a question (URL-encoded) |
| `/api/docs` | GET | API documentation |

### Example Request

```bash
# HR Chatbot
curl -X POST http://localhost:5001/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the sick leave policy?"}'

# Customer Support Chatbot
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'
```

### Example Response

```json
{
  "success": true,
  "answer": "Employees are entitled to **15 days of sick leave** per year...",
  "sources": [12, 34, 35],
  "processing_time_ms": 2345.67,
  "documents_retrieved": 10
}
```

---

## Tech Stack

- **LLM**: Llama 3.2 (3B Instruct) via LM Studio
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Framework**: Flask + Flask-CORS
- **Document Processing**: LangChain + PyPDF
- **Configuration**: Pydantic + python-dotenv
- **Containerization**: Docker + Docker Compose

---

## Project Structure Notes

- Each chatbot is fully self-contained in its own folder with independent configuration, Docker setup, and dependencies
- The `.env.template` file shows all configurable parameters — copy it to `.env` and customize
- PDF documents are excluded from the repository via `.gitignore` (place your own manual in each folder)
- FAISS index files are generated at runtime and also excluded from version control

---

## Part of NOVAERP

These chatbots are AI modules within the **NOVAERP** system — an enterprise Egyptian ERP solution. Other AI modules in the ecosystem include:

- [Employee Attrition Prediction](https://github.com/aliisnetalive/hr-attrition-prediction) — XGBoost-based attrition risk scoring
- [Employee Performance Analytics](https://github.com/aliisnetalive/employee-performance-analytics) — RandomForest performance prediction with dashboards
- [Resume-Job Matching](https://github.com/aliisnetalive/resume-job-matching) — BERT embeddings for candidate-role similarity
- [Fraud Detection](https://github.com/aliisnetalive/fraud-detection-deploy-finance-NOVAERP) — ML fraud detection on financial transactions
