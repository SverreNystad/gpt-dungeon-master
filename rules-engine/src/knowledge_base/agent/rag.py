import numpy as np
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from knowledge_base.models.models import OpenAIModels
from knowledge_base.agent.agent import Agent
from langchain.retrievers import ParentDocumentRetriever, EnsembleRetriever
from langchain_core.documents import Document

class RAG:
    def __init__(self, agent: Agent, embeddings_model: str):
        self.llm = Agent.model
        self.embeddings = OpenAIEmbeddings(model = embeddings_model)
        self.doc_embeddings: list[list[float]] = None
        self.docs: list[str] = None

    def load_documents(self, documents: list[str]):
        """Load documents and compute their embeddings."""
        self.docs = documents
        self.doc_embeddings = self.embeddings.embed_documents(documents)


    def get_most_relevant_docs(self, query: str, k: int = 5, threshold: float = 0.7):
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
    
    def relevant_docs_parent_retriever(self, query: str, parent_document_retriver: ParentDocumentRetriever, k: int = 5, threshold: float = 0.8) -> str:
        return self.convert_docs_to_strings(parent_document_retriver.invoke(input=query)) 
    
    def relevant_docs_ensemble_retrivers(self, query: str, ensemble_retriver: EnsembleRetriever):
        return self.convert_docs_to_strings(ensemble_retriver.invoke(input=query))
    
    # Convert Document objects to strings
    def convert_docs_to_strings(self, docs: list[Document]) -> list[str]:
        return [doc.page_content for doc in docs]

    def generate_answer(self, query: str, relevant_doc: list[str]) -> tuple[str, int]:
        """Generate an answer for a given query based on the most relevant document."""
        system_prompt = """
        You are a rules chatbot for the Dungeons & Dragons roleplaying game. Your task is to provide precise answers to user questions based solely on the relevant information retrieved from the D&D rulebook.

        1) When a user asks a question, retrieve the relevant text from the rulebook using the RAG (Retrieval-Augmented Generation).

        2) Analyze the retrieved information and formulate a concise answer that directly addresses the user's question.

        3) Do not provide any additional commentary, interpretations, or information that is not present in the retrieved text.

        4) If the retrieved information does not contain a direct answer to the question, respond with 'I cannot provide an answer based on the available information.'

        For example:

        User Question: 'What are the rules for casting a spell?'

        Retrieved Information: [Insert relevant rules about spellcasting]

        Your Response: [Generate a direct response based on that information]


        Now, please answer the user question based on the retrieved information.    

        """

        prompt = f"question: {query}\n\n Relevant documents from the RAG: {relevant_doc}"
        messages = [
            ("system", system_prompt),
            ("human", prompt),
        ]
        ai_msg = self.llm.invoke(messages)

        if hasattr(ai_msg, 'usage_metadata'):
            token_count = ai_msg.usage_metadata['total_tokens']
        else:
            token_count = 0
        
        return ai_msg.content, token_count