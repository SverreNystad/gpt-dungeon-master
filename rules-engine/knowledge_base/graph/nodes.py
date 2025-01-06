import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from tools.tools import get_tools
from graph.graphstate import GraphState
from agent.agent import Agent


tools_by_name = {tool.name: tool for tool in get_tools()}

#Tool node
def tool_node(state: GraphState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}

# Call method
def prompt_GM(
    state: GraphState,
    config: RunnableConfig,
):
    # # this is similar to customizing the create_react_agent with state_modifier, but is a lot more flexible
    # system_prompt = SystemMessage(
    #     "You are a helpful AI assistant, please respond to the users query to the best of your ability!"
    # )
    prompt = PromptTemplate(
        template= """
        You are a helpful AI assistant, please respond to the users query to the best of your ability!

        Here are previous messages:
        
        Message: {messages}

        """,
    )

    chain = prompt | Agent.model

    response = chain.invoke({"messages": state["messages"]}, config)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Edge conditional wether or not to continue
def should_continue(state: GraphState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"