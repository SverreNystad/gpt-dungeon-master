import numpy as np
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from knowledge_base.models.models import OpenAIModels

class RAG:
    def __init__(self, model: OpenAIModels):
        self.llm = ChatOpenAI(model=model)
        self.embeddings = OpenAIEmbeddings()
        self.doc_embeddings: list[list[float]] = None
        self.docs: list[str] = None

    def load_documents(self, documents: list[str]):
        """Load documents and compute their embeddings."""
        self.docs = documents
        self.doc_embeddings = self.embeddings.embed_documents(documents)

    def get_most_relevant_docs(self, query: str, k: int = 5, threshold: float = 0.8):
        """Find the most relevant document for a given query."""
        if not self.docs or not self.doc_embeddings:
            raise ValueError("Documents and their embeddings are not loaded.")

        query_embedding = self.embeddings.embed_query(query)

        # Using cosine similarity
        similarities = [
            np.dot(query_embedding, doc_emb)
            / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
            for doc_emb in self.doc_embeddings
        ]

        # TODO: Allow for top k elements to be choosen
        most_relevant_doc_index = np.argmax(similarities)

        return [self.docs[most_relevant_doc_index]]

    def generate_answer(self, query: str, relevant_doc: list[str]):
        """Generate an answer for a given query based on the most relevant document."""
        prompt = f"question: {query}\n\nDocuments: {relevant_doc}"
        messages = [
            ("system", "You are a helpful assistant that answers questions based on given documents only."),
            ("human", prompt),
        ]
        ai_msg = self.llm.invoke(messages)
        return ai_msg.content