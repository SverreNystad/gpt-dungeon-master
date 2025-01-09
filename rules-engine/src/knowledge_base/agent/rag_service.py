from knowledge_base.agent.agent import Agent
from knowledge_base.agent.rag import RAG
from ragas import EvaluationDataset
from langchain_openai import OpenAIEmbeddings
from knowledge_base.models.models import OpenAIModels
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.prompts import PromptTemplate
import pandas as ps


class RagService:
    def __init__(self):
        self.rag = RAG(OpenAIModels.gpt_4o_mini)

        filepath = "knowledge_base/rulesystems/cc-srd5.md"

        rules_document: str = ""
        with open(filepath, encoding="utf-8") as f:
            rules_document = f.read()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_text(rules_document)
        
        # Load documents
        self.rag.load_documents(splits)

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
        rag.load_documents(splits)

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

        df = ps.read_csv("knowledge_base/validation_data/sample_questions_cl.csv")
        querys = df["question"].tolist()
        responses = df["answer"].tolist()


        for query, reference in zip(querys, responses):

            relevant_docs = self.rag.get_most_relevant_docs(query, 5, 0.70)
            response = self.rag.generate_answer(query, relevant_docs)
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


