from typing import Any,Dict
from src.workflow.chains.generation import geneartion_chain
from src.workflow.state import GraphState

def generate(state:GraphState) -> Dict[str,Any]:
    """Generate answer using documents and question"""
    print("---Generate Answer---")
    question = state["question"]
    documents = state["documents"]
    generation = geneartion_chain.invoke({"context":documents,"question":question})
    return {"documents":documents,"question":question,"generation":generation}

