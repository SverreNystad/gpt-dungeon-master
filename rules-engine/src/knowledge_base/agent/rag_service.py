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
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document
from langchain_core.stores import BaseStore
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness


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
    def __init__(self):
        embedding_model = "text-embedding-3-small"
        self.rag = RAG(OpenAIModels.gpt_4o_mini, embeddings_model=embedding_model)

        self.rag_setup()

    def get_md_seperators(self):
        return [
            # First, try to split along Markdown headings (starting with level 2)
            "\n#{1,2} ",
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

    def rag_setup(self):
        filepath = "knowledge_base/rulesystems/cc-srd5.md"

        rules_document: str = ""
        with open(filepath, encoding="utf-8") as f:
            rules_document = f.read()

        docs = [Document(rules_document)]

        markdown_splitter = MarkdownTextSplitter()
        markdown_splitter._separators = self.get_md_seperators()
        splits = markdown_splitter.split_documents(docs)
        print(len(splits))
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400,chunk_overlap = 200)

        store = fetch_store(splits)
        vectorstore = Chroma(embedding_function=self.rag.embeddings, collection_name="rules_doc", persist_directory="knowledge_base/db_data")
        
        self.parent_doc_retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=text_splitter,
            parent_splitter=markdown_splitter
        )
        if self.parent_doc_retriever.docstore.mget(["0"]) == None:
            batch_size = 5
            splits_length = len(splits)
            print(f"Docs length: {splits_length}")
            for i in range(0, splits_length, batch_size):
                print(f"Batch: {i}")
                ids = []
                if (i + batch_size < splits_length):
                    batch = splits[i:i+batch_size]
                    for k in range(i, i + batch_size):
                        ids.append(k)
                else:
                    batch = splits[i:splits_length]
                    for k in range(i, splits_length):
                        ids.append(k)

                self.parent_doc_retriever.add_documents(batch, ids=ids)

                #TODO Save to file 

        print(f"Number of parent chunks  is: {len(list(store.yield_keys()))}")

        print(f"Number of child chunks is: {len(self.parent_doc_retriever.vectorstore.get()['ids'])}")

        print("Finished adding docs")


    def rag_evaluator(self):
        dataset = []

        df = ps.read_csv("knowledge_base/validation_data/sample_questions_class.csv")
        querys = df["question"].tolist()
        responses = df["answer"].tolist()

        for query, reference in zip(querys, responses):

            relevant_docs = self.rag.relevant_docs_parent_retriever(query, self.parent_doc_retriever)
            response = self.rag.generate_answer_parent_retriever(query, relevant_docs)
            dataset.append(
                {
                    "user_input":query,
                    "retrieved_contexts":relevant_docs,
                    "response":response,
                    "reference":reference
                }
            )

        print(dataset)
        evaluation_dataset = EvaluationDataset.from_list(dataset)

        evaluator_llm = LangchainLLMWrapper(Agent.model)
        
        result = evaluate(
            dataset=evaluation_dataset,
            metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness()],
            llm=evaluator_llm
        )
        return result


