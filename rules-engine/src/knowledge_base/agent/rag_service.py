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
