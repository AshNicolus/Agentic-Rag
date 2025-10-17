"""Model bindings for Adaptive RAG.

This module instantiates the chat LLM and embedding model used across the
project. Environment variables for credentials are loaded via python-dotenv.
Replace the model wiring here if you want to swap providers.
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()
# Chat model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)
# embedding model
embed_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


