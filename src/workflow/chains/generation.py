from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from src.models.model import llm

prompt = hub.pull("rlm/rag-prompt")
geneartion_chain = prompt | llm | StrOutputParser()
