from knowledge_base.agent.agent import Agent
from knowledge_base.agent.rag import RAG
from ragas import EvaluationDataset
from langchain_openai import OpenAIEmbeddings
from knowledge_base.models.models import OpenAIModels
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, MarkdownTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.retrievers import ParentDocumentRetriever, EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document
from langchain_core.stores import BaseStore
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, ContextEntityRecall, ContextPrecision
from langchain_community.vectorstores import FAISS
from ragas.utils import safe_nanmean


from langchain_core.prompts import PromptTemplate
import pandas as ps

def fetch_store(splits: list[Document]) -> BaseStore:
    store: BaseStore = InMemoryStore()

    # Check for values are in persistance

    for i, doc in enumerate(splits):
        store.mset([(i, doc)])

    # Retrieve data from file 
    return store

class RagService:
    def __init__(self,
                nr_md_splitts: int = 2,
                chunk_size: int = 400,
                chunk_overlap: int = 200,
                bm25_k: int = 5,
                bm25_weight: float = 0.2
            ):
        embedding_model = "text-embedding-3-small"
        self.rag = RAG(OpenAIModels.gpt_4o_mini, embeddings_model=embedding_model)
        self.splits_length = 0

        self.rag_setup(
            nr_md_splitts = nr_md_splitts,
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            bm25_k = bm25_k,
            bm25_weight = bm25_weight
        )
    
    def get_md_seperators(self, numberOfHeaders: int):
        num_str = ""
        for i in range(1, numberOfHeaders + 1):
            num_str += f"{i},"

        return [
            # First, try to split along Markdown headings (starting with level 2)
            "\n#{" + num_str + "} ",
            # Note the alternative syntax for headings (below) is not handled here
            # Heading level 2
            # ---------------
            # End of code block
            "```\n",
            # Horizontal lines
            "\n\\*\\*\\*+\n",
            "\n---+\n",
            "\n___+\n",
            # Note that this splitter doesn't handle horizontal lines defined
            # by *three or more* of ***, ---, or ___, but this is not handled
            "\n\n",
            "\n",
            " ",
            "",
        ]

    def rag_setup(
            self, 
            nr_md_splitts: int = 2,
            chunk_size: int = 400,
            chunk_overlap: int = 200,
            bm25_k: int = 5,
            bm25_weight: float = 0.2,
            ):
        
        # TODO: Remove after Optima 
        folder_path = "knowledge_base/db_data"
        delete_folder_contents(folder_path)

        filepath = "knowledge_base/rulesystems/cc-srd5.md"

        rules_document: str = ""
        with open(filepath, encoding="utf-8") as f:
            rules_document = f.read()

        docs = [Document(rules_document)]

        markdown_splitter = MarkdownTextSplitter()
        markdown_splitter._separators = self.get_md_seperators(nr_md_splitts)
        splits = markdown_splitter.split_documents(docs)
        #print(len(splits))
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap = chunk_overlap)

        store = fetch_store(splits)
        vectorstore = Chroma(embedding_function=self.rag.embeddings, collection_name="rules_doc", persist_directory="knowledge_base/db_data")
        
        self.parent_doc_retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=text_splitter,
            parent_splitter=markdown_splitter
        )

        #if self.parent_doc_retriever.vectorstore.get(["0"]) == None:
        batch_size = 5
        self.splits_length = len(splits)
        print(f"Docs length: {self.splits_length}")
        for i in range(0, self.splits_length, batch_size):
            #print(f"Batch: {i}")
            ids = []
            if (i + batch_size < self.splits_length):
                batch = splits[i:i+batch_size]
                for k in range(i, i + batch_size):
                    ids.append(k)
            else:
                batch = splits[i:self.splits_length]
                for k in range(i, self.splits_length):
                    ids.append(k)

            self.parent_doc_retriever.add_documents(batch, ids=ids)

        #     #TODO Save to file 

        # BM25 retriver
        child_splits = text_splitter.split_documents(splits)
        bm25_retriver = BM25Retriever.from_documents(child_splits)
        bm25_retriver.k = bm25_k

        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriver, self.parent_doc_retriever], weights=[bm25_weight, 1 - bm25_weight]
        )


        #self.parent_doc_retriever.child_splitter = 
        print(f"Number of parent chunks  is: {len(list(store.yield_keys()))}")

        print(f"Number of child chunks is: {len(self.parent_doc_retriever.vectorstore.get()['ids'])}")

        # print("Finished adding docs")


    def rag_evaluator(self) -> tuple[float, float, float]:
        dataset = []

        df = ps.read_csv("knowledge_base/validation_data/sample_questions_class.csv")
        querys = df["question"].tolist()
        responses = df["answer"].tolist()

        token_use = 0

        for query, reference in zip(querys, responses):

            #relevant_docs = self.rag.relevant_docs_parent_retriever(query, self.parent_doc_retriever)
            relevant_docs = self.rag.relevant_docs_ensemble_retrivers(query, self.parent_doc_retriever)
            response = self.rag.generate_answer(query, relevant_docs)
            dataset.append(
                {
                    "user_input":query,
                    "retrieved_contexts":relevant_docs,
                    "response":response,
                    "reference":reference
                }
            )

        evaluation_dataset = EvaluationDataset.from_list(dataset)

        evaluator_llm = LangchainLLMWrapper(Agent.model)
        
        result = evaluate(
            dataset=evaluation_dataset,
            metrics=[LLMContextRecall(), ContextPrecision(), ContextEntityRecall()],
            llm=evaluator_llm
        )

        print(result)
        
        context_recall = safe_nanmean(result["context_recall"])
        context_precision = safe_nanmean(result["context_precision"])
        context_entity_recall = safe_nanmean(result["context_entity_recall"])

        self.close()

        return context_recall, context_precision, context_entity_recall
    
    def close(self):
        # Close the Chroma connection
        if hasattr(self, 'parent_doc_retriever') and hasattr(self.parent_doc_retriever, 'vectorstore'):
            ids = list(map(str, range(0, self.splits_length))) 
            self.parent_doc_retriever.vectorstore.delete(ids=ids)

    def __exit__(self):
        del self.parent_doc_retriever.vectorstore
        del self.parent_doc_retriever
        folder_path = "knowledge_base/db_data"
        delete_folder_contents(folder_path)

def delete_folder_contents(folder_path: str):
    import os
    import shutil
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

