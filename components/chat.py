import streamlit as st
from core.vector_store import get_db
from core.rag_chain import get_rag
from langchain_community.llms import Ollama
from langchain_community.tools.tavily_search import TavilySearchResults


def render_chat():
    st.subheader("💬 Chat Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    if st.button("Clear Chat"):
        st.session_state.chat = []

    # Show chat
    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["text"])

    # Input
    if q := st.chat_input("Ask your question..."):
        st.session_state.chat.append({"role": "user", "text": q})

        db = get_db()
        rag = get_rag(db, st.session_state.get("docs", []))

        llm = Ollama(model="tinyllama")

        with st.spinner("Thinking..."):

            # 🔹 RAG answer
            result = rag(q)
            answer = result["result"]

            # 🔹 If weak answer → use web search
            if len(answer.strip()) < 20:
                tavily = TavilySearchResults()
                web = tavily.invoke({"query": q})
                answer = f"{answer}\n\n🌐 Web Results:\n{web}"

        st.session_state.chat.append({"role": "assistant", "text": answer})
        st.chat_message("assistant").write(answer)