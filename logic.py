import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings
from openai import OpenAI
import os
def extract_text(pdf_path):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text.strip())
    cleaned_text = "\n".join(all_text)
    return cleaned_text


def list_files_in_directory(directory_path):
    # Get a list of all entries (files and subdirectories) in the specified directory
    all_entries = os.listdir(directory_path)

    # Filter out directories and keep only file names
    files = [entry for entry in all_entries if os.path.isfile(os.path.join(directory_path, entry))]
    return files

def askbot(collection, query,model1):
    query_embedding = model1.encode([query])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )

    retrieved_chunks = results["documents"][0]  # Top relevant chunks
   # retrieved_chunks = results["documents"][0]  # Top relevant chunks

    context = "\n".join(retrieved_chunks)
    prompt = f"""
    You are an intelligent assistant processing insurance documents.
    Based on the following document content:

    {context}

    Answer the user query:
    "{query}"

    Respond with a JSON of the form:
    {{
    "decision": "...",
    "amount": "...",
    "justification": "...",
    "clauses_used": ["..."]
    }}
    If the documents do not contain the required information, return:
    {{
    "decision": "Insufficient information",
    "justification": "Query could not be answered from provided documents.",
    "clauses_used": []
    }}

    Respond ONLY with the JSON object, without any additional text or explanation.
    """

    from langchain_groq import ChatGroq
    from dotenv import load_dotenv
    import os
    load_dotenv()
    model = ChatGroq(model="llama-3.1-8b-instant",api_key =os.getenv("GROQ_API_KEY"))
    response = model.invoke(prompt)
    response = response.content
    print(response)
    print(type(response))

    return response


def pipeline(query,folder_path="samples"):

    doc_paths = ["samples/policy1.pdf", "samples/policy2.pdf"]  # Remove ... and use actual paths
   # doc_paths = list_files_in_directory(folder_path)
   # doc_paths = [os.path.join(folder_path, file) for file in doc_paths]
    model = SentenceTransformer("all-MiniLM-L6-v2")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # Process each document one by one
    all_chunks = []
    for pdf_path in doc_paths:
        text = extract_text(pdf_path)
        chunks = splitter.split_text(text)
        embeddings = model.encode(chunks)
        all_chunks.extend(zip(chunks, embeddings))


    chroma_client = Client(Settings(persist_directory="./chroma_db"))
    collection = chroma_client.create_collection(name="policy_docs")


    for i, (chunk, emb) in enumerate(all_chunks):
        collection.add(
            documents=[chunk],
            embeddings=[emb],
            ids=[f"chunk_{i}"]
        )
    
    #chroma_client.persist()
    return [collection, query, model]

