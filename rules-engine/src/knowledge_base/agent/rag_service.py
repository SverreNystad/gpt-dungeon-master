from knowledge_base.agent.agent import Agent

from langchain_core.prompts import PromptTemplate
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "no_key")
# LANGCHAIN_TRACING_V2=True
# LANGCHAIN_ENDPOINT="https://eu.api.smith.langchain.com"
# LANGCHAIN_PROJECT="GPT-gm"



def lookup_rules(context, filepath = "knowledge_base/rulesystems/rules.txt") -> list[str]:
    """
    Lookup rules based on the context
    """
    rules_document = ""

    with open(filepath, encoding="utf-8") as f:
        rules_document = f.read()
    
    MAX_LENGTH = 128_000

    if len(rules_document) > MAX_LENGTH:
        rules_document = rules_document[:MAX_LENGTH]
    rules = []
    prompt = PromptTemplate(
        template="""Given the following document providing the rules of the role playing system: '''{rules_document}''' Give a list of relevant rules in json based on the context provided: '''{context}''' Only include the json rules.""", 
        input_variables=["rules_document", "context"]
    )

    
    chain = prompt | Agent.model
    result = chain.invoke({"rules_document":rules_document, "context":context})
    rules = result
    return rules

from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def lookup_rules_v2(context, filepath = "knowledge_base/rulesystems/rules.txt") -> list[str]:
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

