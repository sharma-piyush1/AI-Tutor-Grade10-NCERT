"""
AI Tutor: Build Vector Stores Module
Process NCER documents to create FAISS index for efficient retrieval.
"""

import os 
from pathlib import Path
from dotenv import load_dotenv

# Langchain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PDF_DIR = PROJECT_ROOT / "data" / "raw_content"
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"

# Create vector store directory if it doesn't exist
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


def load_pdfs(pdf_directory):
    """
    Load all PDF files from the specified directory.
    """

    documents = []

    if not os.path.exists(pdf_directory): # Check if directory exists
        print(f"Directory {pdf_directory} does not exist.")
        return documents

    # Get all pdfs
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    if not pdf_files:
        print(f"No PDF files found in directory {pdf_directory}.")
        return documents
    
    print(f"Found {len(pdf_files)} PDF files in {pdf_directory}.")

    for pdf_file in pdf_files: # Load each PDF file
        try:
            file_path = os.path.join(pdf_directory, pdf_file)
            print(f"Loading {pdf_file}...")

            loader = PyPDFLoader(file_path)
            docs = loader.load()
            documents.extend(docs)

            print(f"Loaded {len(docs)} pages from {pdf_file}.")
        
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}")
            continue

    print(f"Total documents loaded: {len(documents)}")
    return documents

def chunk_documents(documents, chunk_size=700, chunk_overlap=100):
    """
    Chunk documents into smaller pieces for embedding.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks

def create_embeddings():
    """
    Create HuggingFace embeddings.
    """
    model_name = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings

def build_faiss_index(chunks, embeddings, index_path):
    """
    Build FAISS index from document chunks and save to disk.
    """
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(folder_path=index_path)
    print(f"FAISS index saved to {index_path}")
    return vectorstore

def test_retrieval(vectorstore, query="Explain quadratic formula", k=3):
    """
    Test retrieval from the vector store.
    """
    results = vectorstore.similarity_search(query, k=k)
    print(f"\n🔍 Testing with query: '{query}'")
    print("-" * 80)

    for i, result in enumerate(results, 1):  # Start counting from 1
        print(f"\n📄 Result {i}:")
        print(f"Content: {result.page_content[:200]}...")  
        print(f"Source: {result.metadata.get('source', 'Unknown')}")
        print(f"Page: {result.metadata.get('page', 'Unknown')}")
    
    return results

def main():
    """Main execution pipeline."""

    print("="*80)
    print("AI TUTOR = VECTOR STORE BUILDER")
    print("="*80)

    # Load PDFs
    print("Loading PDF documents...")
    documents = load_pdfs(PDF_DIR)

    print("Chunking documents...")
    chunks = chunk_documents(documents, chunk_size=700, chunk_overlap=100)

    print("Creating embeddings...")
    embeddings = create_embeddings()

    print("Building FAISS index...")
    vectorstore = build_faiss_index(chunks, embeddings, str(VECTOR_STORE_DIR))

    print("Testing retrieval...")
    test_retrieval(vectorstore, query="What is the quadratic formula?", k=3)

    print("\n" + "="*80)
    print("VECTOR STORE BUILDING COMPLETED SUCCESSFULLY!")
    print(f"Vector store saved at: {VECTOR_STORE_DIR}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
    
