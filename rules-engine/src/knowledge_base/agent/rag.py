import numpy as np
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from knowledge_base.models.models import OpenAIModels
from knowledge_base.agent.agent import Agent

class RAG:
    def __init__(self, agent: Agent):
        self.llm = Agent.model
        self.embeddings = OpenAIEmbeddings()
        self.doc_embeddings: list[list[float]] = None
        self.docs: list[str] = None

    def load_documents(self, documents: list[str]):
        """Load documents and compute their embeddings."""
        self.docs = documents
        self.doc_embeddings = self.embeddings.embed_documents(documents)


    def get_most_relevant_docs(self, query: str, k: int = 5, threshold: float = 0.8):
        """Find the top-k most relevant documents for a given query that meet a similarity threshold."""
        if not self.docs or not self.doc_embeddings:
            raise ValueError("Documents and their embeddings are not loaded.")

        # Compute the embedding for the query
        query_embedding = self.embeddings.embed_query(query)

        # Compute cosine similarities between the query and each document
        similarities = [
            np.dot(query_embedding, doc_emb) /
            (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
            for doc_emb in self.doc_embeddings
        ]

        # Sort indices of documents by similarity score in descending order
        sorted_indices = np.argsort(similarities)[::-1]

        # Filter out indices that do not meet the threshold
        relevant_indices = [idx for idx in sorted_indices if similarities[idx] >= threshold]

        # Select the top-k indices from the filtered list
        top_k_indices = relevant_indices[:k]

        # Retrieve and return the corresponding documents
        return [self.docs[i] for i in top_k_indices]


    def generate_answer(self, query: str, relevant_doc: list[str]):
        """Generate an answer for a given query based on the most relevant document."""
        prompt = f"question: {query}\n\nDocuments: {relevant_doc}"
        messages = [
            ("system", "You are a helpful assistant that answers questions based on given documents only."),
            ("human", prompt),
        ]
        ai_msg = self.llm.invoke(messages)
        return ai_msg.content