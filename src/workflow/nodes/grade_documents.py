from typing import Any,Dict
from src.workflow.chains.retrieval_grader import retrieval_grader
from src.workflow.state import GraphState


def grade_documents(state:GraphState) -> Dict[str,Any]:
    """ Determine whether retrieved documents are relevant to the question.
    If any document is not relevant, we will set a flag to run web search
    
    Args:
        state (dict):The current graph state
    Return:
        state(dict):Filtered out irrelevant documents and updated web_search state
    """
    print("--- GRADE DOCUMENTS ---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs=[]
    web_search = False
    for d in documents:
        score = retrieval_grader.invoke(
            {"quesion":question,"document":d.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---DOCUMENT NOT RELEVANT, WILL RUN WEB SEARCH---")
            web_search = True
            continue
    return {"documents":filtered_docs,"question":question,"web_search":web_search}


