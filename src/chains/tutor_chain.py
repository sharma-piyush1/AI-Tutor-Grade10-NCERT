"""
AI Tutor - LangChain Conversational Chain
Combines retrieval + Groq LLM + memory
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Langchain imports
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

import sys
sys.path.append(str(Path(__file__).parent.parent))
from retrieval.query_vectorstore import VectorStoreRetriever

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class AITutor:

    def __init__(self):
        """
        Main AI Tutor class that orchestrates retrieval + LLM + memory
        """

        print("="*80)
        print("INITIATING AI TUTOR CHAIN...")
        print("="*80)

        # Initialize LLM
        llm = ChatGroq(
            api_key=GROQ_API_KEY, 
            model="llama-3.3-70b-versatile", 
            temperature=0.7
        )
        
        # Initialize retriever
        retriever = VectorStoreRetriever()
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True, 
            output_key="answer"
        )
        
        # Create custom prompt template
        prompt_template = """You are an AI Tutor for Grade 10 students studying Maths, Physics, and Chemistry.
You were created by Piyush Sharma, an AI/ML enthusiast.

Your role:
- Explain concepts clearly and step-by-step
- Use simple language appropriate for 10th graders
- Provide examples when helpful
- Encourage students to think critically
- If you don't know something, admit it honestly

Context from textbooks:
{context}

Previous conversation:
{chat_history}

Student's question: {question}

Your response (be encouraging and clear):"""

        qa_prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        # Build the chain with custom prompt
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": qa_prompt}  
        )
        
        print("AI TUTOR CHAIN READY.")
        print("="*80)

    def ask(self, question):
        """
        Ask a question to the AI Tutor chain
        """
        try:
            response = self.chain.invoke({"question": question})
            return response["answer"]
        except Exception as e:
            print(f"Error during chain execution: {e}")
            return None

    def get_conversation_history(self):
        """
        Get the current conversation history from memory
        """
        return self.memory.load_memory_variables({})

    def clear_history(self):
        """
        Clear the conversation history
        """
        self.memory.clear()
        print("Conversation history cleared.")


def test_ai_tutor():
    tutor = AITutor()

    # Test questions
    test_questions = [
        "What is a quadratic equation?",
        "Can you give me an example with numbers?",  # Tests memory
        "Who created you?",  # Tests creator attribution
        "How does image formation by spherical mirrors occur?"  # Tests subject switching
    ]
    
    print("\n" + "="*80)
    print("TESTING AI TUTOR CHAIN")
    print("="*80 + "\n")

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"Question {i}: {question}")
        print(f"{'='*80}\n")

        answer = tutor.ask(question)
        print(f"Answer:\n{answer}\n")

        input("Press Enter to continue to the next question...")

    # Show conversation history 
    print("\n" + "="*80)
    print("CURRENT CONVERSATION HISTORY")
    print("="*80)
    history = tutor.get_conversation_history()
    print(history)


if __name__ == "__main__":
    test_ai_tutor()