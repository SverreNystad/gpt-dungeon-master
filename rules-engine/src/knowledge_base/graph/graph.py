from langgraph.graph import StateGraph, END
from graph.nodes import tool_node, prompt_GM, should_continue
from graph.graphstate import GraphState
from IPython.display import Image, display


class Graph:
    def __init__(self):
        # Define a new graph
        self.workflow = StateGraph(GraphState)

        # Defining the nodes
        self.workflow.add_node("agent", prompt_GM)
        self.workflow.add_node("tools", tool_node)

        # Defining the starting point of the graph
        self.workflow.set_entry_point("agent")

        # Defining conditional edges
        self.workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )

        # Defining normal edges
        self.workflow.add_edge("tools", "agent")

        self.graph = self.workflow.compile()


    def save_image(self):
        try:
            with open("ex_agent.png", 'wb') as f:
                f.write(self.graph.get_graph().draw_mermaid_png())
                print("Prints")
        except Exception as e:
            print("Exception in Image display: {e}")
            pass

    async def run_agent(self, userInput):
        inputs = {"messages": [("user", userInput)]}
        print(inputs)

        async for event in self.graph.astream(inputs, stream_mode ="values"):
            message = event["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()

    
    def print_stream(self, stream):
        print("Her er stream:")
        for i in range(stream.size()):
            print(stream[i])
        #print(stream)
        for s in stream:
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()
