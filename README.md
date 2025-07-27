# mini_rag

# 🔍 Retrieval-Augmented Generation (RAG) Portal

A lightweight system to query natural language questions against large unstructured documents like policies or contracts using Large Language Models (LLMs) and vector databases.

---

## 📁 Project Structure

```
├── app.py             # Main application entry point (Streamlit/Flask/etc.)
├── logic.py           # Core logic for text extraction, chunking, embedding, retrieval
├── requirements.txt   # All necessary Python dependencies
```

---

## ⚙️ How It Works

1. **Document Upload & Text Extraction**: Extracts clean text from PDF using `pdfplumber`.
2. **Chunking & Embeddings**: Splits document into chunks and converts them into vector embeddings using a sentence transformer.
3. **Vector Store**: Stores embeddings in a vector database (ChromaDB).
4. **Query Handling**: Takes a user query, converts it to an embedding, and retrieves similar chunks.
5. **LLM Response Generation**: Uses a language model (e.g., OpenAI or HuggingFace) to answer using the retrieved context.

---

## 🚀 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/rag-portal.git
cd rag-portal
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
python app.py
```

Or, if using Streamlit:

```bash
streamlit run app.py
```

---

## 🛠 Dependencies

Key libraries used (see `requirements.txt`):

- `pdfplumber` – Extract text from PDFs
- `chromadb` – Vector database for similarity search
- `sentence-transformers` – Embedding generation
- `openai` or `transformers` – LLM response generation
- `streamlit` or `flask` – UI (based on your implementation)

---

## ✍️ Example Use Case

> Upload your policy document → Ask questions like:  
> _“What is the claim procedure for 46-year-olds?”_  
> → Get structured answers in JSON format.

---

## 📌 Notes

- Supports **multiple queries** on the same document. - still working on it
- Add OCR fallback if PDF contains scanned text.
- Easily extendable to handle multiple documents or chatbot-style history.

---

