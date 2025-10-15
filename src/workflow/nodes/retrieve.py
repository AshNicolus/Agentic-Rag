from typing import Any, Dict
from src.workflow.state import GraphState
from data.ingestion import retriver

def retrieve(state: GraphState) -> Dict[str, Any]:
    """ Retrieve documents from vector store"""
    print("--- RETRIEVE DOCUMENTS ---")
    question = state["question"]
    documents = retriver.invoke(question)
    return {"documents":documents,"question":question}
