from typing import List, TypedDict

class GraphState(TypedDict):
    """State object for workflow containg query,documents,control flags and answers."""
    question:str  # User original Query
    generation:str # generation of llm answer 
    web_search:bool # Flag to indicate if web search was used 
    documents:List[str] # Retrieved document context 
    



