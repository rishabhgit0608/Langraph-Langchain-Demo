from langchain_project_learning.state import ContentState
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def synthesize_data(state: ContentState):
    """
    Cleans and synthesizes search results into a bullet-point summary.
    Takes the search_result list from state and returns a clean string
    stored in state["synthesized_content"].
    """
    llm = ChatGroq(temperature=0, model="llama-3.3-70b-versatile")
    synthesize_prompt = ChatPromptTemplate.from_template("""
        You are a helpful data cleaner, your main task is to remove unwanted characters and fields coming from the LLM Model
        and return the clean data in the form of Regular String bullet point wise for the provided array which means if array is of size 4, then there should be 4 bullet points for the clean data.
        This is the input I only expect a string output
        {input}
    """)

    chain = synthesize_prompt | llm | StrOutputParser()

    result = chain.invoke({"input": state["search_result"]})
    state["synthesized_content"] = result
    return state

