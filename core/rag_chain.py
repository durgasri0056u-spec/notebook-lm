from langchain_community.llms import Ollama


def get_rag(db, selected_docs):

    # 🔹 Apply metadata filtering (only selected PDFs)
    if selected_docs:
        retriever = db.as_retriever(
            search_kwargs={
                "k": 4,
                "filter": {"source": {"$in": selected_docs}}
            }
        )
    else:
        retriever = db.as_retriever(search_kwargs={"k": 4})

    def rag_fn(query):

        # 🔹 Step 1: Retrieve relevant chunks
        docs = retriever.invoke(query)

        # 🔴 Step 2: If nothing useful → return NOT FOUND
        if not docs:
            return {"result": "I couldn't find this information in the uploaded documents."}

        # 🔹 Combine context
        context = "\n\n".join([doc.page_content for doc in docs])

        # 🔴 Step 3: Simple relevance check (IMPORTANT)
        if len(context.strip()) < 50:
            return {"result": "I couldn't find this information in the uploaded documents."}

        # 🔹 Step 4: Strict prompt
        prompt = f"""
You are a strict assistant.

Answer ONLY using the context below.

If the answer is not clearly present in the context, say:
"I couldn't find this information in the uploaded documents."

Context:
{context}

Question:
{query}

Answer:
"""

        # 🔹 Step 5: LLM call (tiny model)
        llm = Ollama(model="tinyllama")
        response = llm.invoke(prompt)

        return {"result": response}

    return rag_fn