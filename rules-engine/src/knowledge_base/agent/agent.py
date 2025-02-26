from langchain_openai import ChatOpenAI


class OpenAIModels:
    gpt_4o_mini = "gpt-4o-mini"  # $0.075 per mil tokens
    gpt_4o = "gpt-4o"  # $1.25  per mil tokens
    gpt_o3 = "o3-mini"  # $0.55  per mil tokens


class Agent:
    """
    A class that specifies which LLM-model to use and if it has access to tools
    """

    model = ChatOpenAI(
        model=OpenAIModels.gpt_4o_mini,
        temperature=0,
        max_tokens=16384,  # Max tokens for mini. For gpt4o it's 128k
    )
