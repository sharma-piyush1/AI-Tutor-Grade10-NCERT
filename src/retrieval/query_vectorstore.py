"""
AI Tutor - Vector Store Query Interface
Loads FAISS index and provides retrieval methods
"""

from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS  

# Project paths

PROJECT_ROOT = Path(__file__).parent.parent.parent
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"   

class VectorStoreRetriever:
    """
    Handles loading and querying the FAISS vector store.
    """

    def __init__(self, vector_store_path=None):
        self.vector_store_path = vector_store_path or VECTOR_STORE_DIR

        print(f"Loading FAISS index from {self.vector_store_path}...")

        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        self.vectorstore = FAISS.load_local(
            folder_path=str(self.vector_store_path),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        print("Vector store loaded successfully.")


    def retrieve(self,query,k=3, filter_subject=None):
        """
        Retrive relevant documents from the vector store.
        """

        results = self.vectorstore.similarity_search(
            query,
            k=k,
        )

        if filter_subject:
            filtered_results = []
            for doc in results:
                source = doc.metadata.get('source', '')
                if filter_subject.lower() in source.lower():
                    filtered_results.append(doc)
            results = filtered_results
        return results
    
    def retrieve_with_scores(self, query, k=3):
        # This is a one-liner - FAISS provides this method
        results_with_scores = self.vectorstore.similarity_search_with_score(query, k=k)
        return results_with_scores
    
    def get_context(self, query, k=3):

        docs = self.retrieve(query, k)

        context_parts = []

        for doc in docs:

            source = doc.metadata.get('source', 'Unknown').split('/')[-1]
            page = doc.metadata.get('page', 'Unknown')

            context_block = f"Source: {source}, Page: {page}\nContent: {doc.page_content}\n"
            context_parts.append(context_block)
        final_context = "\n---\n".join(context_parts)
        return final_context



def test_retriever():
    """Test the retriever with sample queries"""
    
    print("="*80)
    print(" TESTING VECTOR STORE RETRIEVER")
    print("="*80)
    
    # Initialize retriever
    retriever = VectorStoreRetriever()
    
    # Test queries for each subject
    test_queries = [
        ("What is a quadratic equation?", "Maths"),
        ("Explain laws of reflection", "Physics"),
        ("What are types of chemical reactions?", "Chemistry")
    ]
    
    for query, expected_subject in test_queries:
        print(f"\n{'='*80}")
        print(f" Query: {query}")
        print(f" Expected Subject: {expected_subject}")
        print(f"{'='*80}\n")
        
        # Test basic retrieval
        results = retriever.retrieve(query, k=2)
        
        for i, doc in enumerate(results, 1):
            print(f"   Result {i}:")
            print(f"   Content: {doc.page_content[:150]}...")
            print(f"   Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"   Page: {doc.metadata.get('page', 'Unknown')}\n")
        
        # Test retrieval with scores
        print("Similarity Scores:")
        scored_results = retriever.retrieve_with_scores(query, k=2)
        for doc, score in scored_results:
            source = doc.metadata.get('source', 'Unknown').split('\\')[-1]
            print(f"   {source} (Page {doc.metadata.get('page', '?')}): Score = {score:.4f}")
        
        print()
    
    # Test context formatting
    print(f"\n{'='*80}")
    print("📝 TESTING CONTEXT FORMATTING")
    print(f"{'='*80}\n")
    
    context = retriever.get_context("Explain quadratic formula", k=2)
    print("Generated Context for LLM:\n")
    print(context)
    
    print(f"\n{'='*80}")
    print("✅ RETRIEVER TESTING COMPLETE")
    print(f"{'='*80}")


if __name__ == "__main__":
    test_retriever()
