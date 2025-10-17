"""Streamlit web UI for Adaptive RAG.

Allows uploading TXT/MD/PDF documents to the vectorstore, asking questions, and
viewing generated answers and grading information.

Run with: `streamlit run streamlit_app.py` from the project root.
"""

import streamlit as st
from typing import List
from langchain.schema import Document
from src.workflow.chains.generation import geneartion_chain
from src.workflow.chains.retrieval_grader import retrieval_grader
from src.workflow.chains.hallucination_grader import hallucination_grader
from data.ingestion import create_vectorstore, retriever
from src.models.model import embed_model
import os
import tempfile
from langchain.document_loaders import PyPDFLoader

st.set_page_config(page_title="Adaptive RAG", layout="wide")

st.title("Adaptive RAG — Document QA")

# Sidebar: upload or use existing vectorstore
with st.sidebar:
    st.header("Vector store")
    if st.button("(Re)create vectorstore from seeded URLs"):
        with st.spinner("Creating vector store — this may take a while"):
            vs = create_vectorstore()
            st.success("Vector store created")
    st.write("Or upload text files below to add to the vectorstore")

# File uploader
uploaded_files = st.file_uploader(
    "Upload files (txt, md, pdf)", accept_multiple_files=True, type=["txt", "md", "pdf"]
)
if uploaded_files:
    docs: List[Document] = []
    for uploaded in uploaded_files:
        # Handle PDFs separately
        if uploaded.type == "application/pdf" or uploaded.name.lower().endswith(".pdf"):
            # write to temp file and load with PyPDFLoader
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded.getvalue())
                tmp_path = tmp.name
            loader = PyPDFLoader(tmp_path)
            pdf_docs = loader.load()
            for p in pdf_docs:
                docs.append(Document(page_content=p.page_content, metadata={"source": uploaded.name}))
            try:
                os.remove(tmp_path)
            except Exception:
                pass
        else:
            text = uploaded.getvalue().decode("utf-8")
            docs.append(Document(page_content=text, metadata={"source": uploaded.name}))
    st.write(f"Loaded {len(docs)} documents")
    if st.button("Add uploaded docs to vectorstore"):
        # Create a vectorstore and merge with uploaded docs
        vectorstore = create_vectorstore()
        vectorstore.add_documents(docs)
        st.success("Documents added to vectorstore")

st.markdown("---")

# QA UI
question = st.text_input("Question", value="What is retrieval augmented generation?")
if st.button("Ask") and question:
    with st.spinner("Retrieving documents..."):
        # Use the same router logic as the CLI: decide whether to use vectorstore or web search
        from src.workflow.chains.router import question_router
        from src.workflow.nodes.web_search import web_search

        route = question_router.invoke({"question": question})
        # route.datasource is expected to be 'vectorstore' or 'websearch'
        if getattr(route, "datasource", "vectorstore") == "websearch":
            st.info("Router selected web search — fetching web results...")
            state = {"question": question, "documents": []}
            res = web_search(state)
            docs = res.get("documents", [])
        else:
            st.info("Router selected vectorstore — retrieving from vectorstore...")
            docs = retriever.invoke(question)
    st.subheader("Retrieved documents")
    for i, d in enumerate(docs):
        with st.expander(f"Document {i+1}"):
            st.write(d.page_content[:1000])

    with st.spinner("Generating answer..."):
        ans = geneartion_chain.invoke({"context": docs, "question": question})
    st.subheader("Answer")
    st.write(ans)

    # Optional: grade hallucination
    with st.spinner("Grading for hallucinations..."):
        grade = hallucination_grader.invoke({"documents": docs, "generation": ans})
    st.subheader("Hallucination grade")
    st.write(grade)

    # Optional: grade retrievals
    st.subheader("Retrieval relevance per document")
    for i, d in enumerate(docs):
        g = retrieval_grader.invoke({"question": question, "document": d.page_content})
        st.write(f"Document {i+1}: {g.binary_score}")




if __name__ == "__main__":
    st.write()
