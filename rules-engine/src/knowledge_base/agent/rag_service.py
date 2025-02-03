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
from langchain_community.vectorstores import FAISS


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
                vector_k: int = 2,
                breakpoint_threshold: float = 95.0,
                score_threshold: float = 0.7,
                bm25_k: int = 5,
                bm25_weight: float = 0.2,
                md_splits: int = 2
            ):
        embedding_model = "text-embedding-3-small"
        self.rag = RAG(OpenAIModels.gpt_4o_mini, embeddings_model=embedding_model)
        self.splits_length = 0

        self.rag_setup(
            vector_k=vector_k,
            breakpoint_threshold=breakpoint_threshold,
            score_threshold=score_threshold,
            bm25_k = bm25_k,
            bm25_weight = bm25_weight,
            md_splits = md_splits
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
    
    def markdown_setup(self, num_headers: int = 2) -> MarkdownHeaderTextSplitter:
        headers_to_split_on = [
            ("#", "Header 1")
        ]

        if num_headers > 1:
            headers_to_split_on.append(("##", "Header 2"))
        if num_headers > 2:
            headers_to_split_on.append(("###", "Header 3"))
        if num_headers > 3:
            headers_to_split_on.append(("####", "Header 4"))
        if num_headers > 4:
            headers_to_split_on.append(("#####", "Header 5"))
        if num_headers > 5:
            headers_to_split_on.append(("######", "Header 6"))

        return MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False
        )

    def rag_setup(
            self, 
            vector_k: int = 2,
            breakpoint_threshold: float = 95.0,
            score_threshold: float = 0.7,
            bm25_k: int = 5,
            bm25_weight: float = 0.2,
            md_splits: int = 2
            ):
        
        # TODO: Remove after Optima 
        # folder_path = "knowledge_base/db_data"
        # delete_folder_contents(folder_path)

        filepath = "knowledge_base/rulesystems/cc-srd5.md"

        rules_document: str = ""
        with open(filepath, encoding="utf-8") as f:
            rules_document = f.read()

        #docs = [Document(rules_document)]

        markdown_splitter = self.markdown_setup(md_splits)
        #markdown_splitter._separators = self.get_md_seperators(nr_md_splitts)
        splits = markdown_splitter.split_text(rules_document)
        print(f"Markdown splits {len(splits)}")

        text_splitter = SemanticChunker(
            OpenAIEmbeddings(),
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=breakpoint_threshold
        )

        
        child_splits = text_splitter.split_documents(splits)
        print(f"Semantic splits {len(child_splits)}")

        # Vector store backed retriever
        vector_retriever = FAISS.from_documents(child_splits, OpenAIEmbeddings()).as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs = {
                "k": vector_k,
                "score_threshold": score_threshold
                }
        )

        # BM25 retriver
        bm25_retriver = BM25Retriever.from_documents(child_splits)
        bm25_retriver.k = bm25_k

        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriver, vector_retriever], weights=[bm25_weight, 1 - bm25_weight]
        )


        #self.parent_doc_retriever.child_splitter = 
        # print(f"Number of parent chunks  is: {len(list(store.yield_keys()))}")

        # print(f"Number of child chunks is: {len(self.parent_doc_retriever.vectorstore.get()['ids'])}")

        # print("Finished adding docs")


    def rag_evaluator(self) -> tuple[float, float, float]:
        dataset = []

        df = ps.read_csv("knowledge_base/validation_data/sample_questions_class.csv")
        querys = df["question"].tolist()
        responses = df["answer"].tolist()

        token_use = 0

        for query, reference in zip(querys, responses):

            #relevant_docs = self.rag.relevant_docs_parent_retriever(query, self.parent_doc_retriever)
            relevant_docs = self.rag.relevant_docs_ensemble_retrivers(query, self.ensemble_retriever)
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

        #self.close()

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
    
    def ask_model(self, query: str):
        relevant_docs = self.rag.relevant_docs_ensemble_retrivers(query, self.ensemble_retriever)
        return self.rag.generate_answer(query, relevant_docs)

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

