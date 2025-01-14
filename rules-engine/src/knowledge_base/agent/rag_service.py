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

from langchain_core.prompts import PromptTemplate
import pandas as ps


class RagService:
    def __init__(self):
        embedding_model = "text-embedding-3-small"
        self.rag = RAG(OpenAIModels.gpt_4o_mini, embeddings_model=embedding_model)

        filepath = "knowledge_base/rulesystems/cc-srd5.md"

        rules_document: str = ""
        with open(filepath, encoding="utf-8") as f:
            rules_document = f.read()


        docs = [Document(rules_document)]

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2")
        ]

        markdown_splitter = MarkdownTextSplitter()
        #markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
        md_splits = markdown_splitter.split_documents(docs)
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400,chunk_overlap = 0)
        splits = text_splitter.split_documents(md_splits)

        # text_splitter = SemanticChunker(
        #     OpenAIEmbeddings(), breakpoint_threshold_type="percentile"
        # )

        #splits: list[str] = []
        # for doc in text_splitter.split_documents(md_splits):
        #     splits.append(doc.page_content)

        store = InMemoryStore()
        vectorstore = Chroma(embedding_function=self.rag.embeddings, collection_name="rules_doc", persist_directory="knowledge_base/db_data")
        
        self.parent_doc_retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=text_splitter,
            parent_splitter =markdown_splitter
        )

        batch_size = 5
        for i in range(0, 90, batch_size):
            print(f"Batch: {i}")
            batch = splits[i:i+batch_size]
            self.parent_doc_retriever.add_documents(batch, ids=None)

        #self.parent_doc_retriever.add_documents(splits, ids=None)

        # Load documents
        #self.rag.load_documents(splits)

    def lookup_rule(self, context, filepath = "knowledge_base/rulesystems/rules.txt") -> list[str]:
        rules_document = ""

        with open(filepath, encoding="utf-8") as f:
            rules_document = f.read()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(rules_document)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever()
        prompt = PromptTemplate(
            template="""Given the following document providing the rules of the role playing system: '''{rules_document}''' Give a list of relevant rules in json based on the context provided: '''{context}''' Only include the json rules.""", 
            input_variables=["rules_document", "context"]
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)


        rag_chain = (
            prompt
            | retriever
            | RunnablePassthrough(format_docs)
            | Agent.model
            | StrOutputParser()
        )
        result = rag_chain.invoke({"context": context})
        rules = result
        return rules


    def rag_setup():

        # filepath = "rules-engine/src/knowledge_base/rulesystems/cc-srd5.md"
        filepath = "knowledge_base/rulesystems/cc-srd5.md"

        rules_document: str = ""
        with open(filepath, encoding="utf-8") as f:
            rules_document = f.read()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_text(rules_document)


        rag = RAG(OpenAIModels.gpt_4o_mini)

        # Load documents
        rag.load_documents(md_splits)

        # Query and retrieve the most relevant document
        query = "How many hitpoints does an Barbarian have at level 1? "
        relevant_doc = rag.get_most_relevant_docs(query)

        # Generate an answer
        answer = rag.generate_answer(query, relevant_doc)

        print(f"Query: {query}")
        print(f"Relevant Document: {relevant_doc}")
        print(f"Answer: {answer}")


    def rag_evaluator(self):
        from ragas import evaluate
        from ragas.llms import LangchainLLMWrapper
        from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness


        dataset = []

        df = ps.read_csv("knowledge_base/validation_data/sample_questions_race.csv")
        querys = df["question"].tolist()
        responses = df["answer"].tolist()


        # for query, reference in zip(querys, responses):

        #     relevant_docs = self.rag.get_most_relevant_docs(query, 5, 0.70)
        #     response = self.rag.generate_answer(query, relevant_docs)
        #     dataset.append(
        #         {
        #             "user_input":query,
        #             "retrieved_contexts":relevant_docs,
        #             "response":response,
        #             "reference":reference
        #         }
        #     )

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


