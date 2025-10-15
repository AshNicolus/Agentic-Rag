from typing import Any,Dict
from src.workflow.chains.retrieval_grader import retrieval_grader
from src.workflow.state import GraphState


def grade_documents(state:GraphState) -> Dict[str,Any]: