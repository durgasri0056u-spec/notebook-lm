from langgraph.graph import StateGraph


def build_graph(rag_chain, web_tool, llm):

    def classify(state):
        q = state["query"].lower()
        if "latest" in q or "search" in q:
            return {"intent": "web"}
        return {"intent": "doc"}

    def doc_node(state):
        result = rag_chain(state["query"])
        return {"context": result["result"], "sources": result["source_documents"]}

    def web_node(state):
        result = web_tool.run(state["query"])
        return {"context": result, "sources": []}

    def generate(state):
        prompt = f"Answer using:\n{state['context']}"
        return {"answer": llm.invoke(prompt)}

    graph = StateGraph(dict)

    graph.add_node("classify", classify)
    graph.add_node("doc", doc_node)
    graph.add_node("web", web_node)
    graph.add_node("generate", generate)

    graph.set_entry_point("classify")
    graph.add_conditional_edges(
        "classify",
        lambda x: x["intent"],
        {"doc": "doc", "web": "web"}
    )

    graph.add_edge("doc", "generate")
    graph.add_edge("web", "generate")

    graph.set_finish_point("generate")

    return graph.compile()