from langchain_project_learning.state import ContentState, SearchResult
from tavily import TavilyClient
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_node(state: ContentState):
    """
    Searches the web for the given topic and returns the search results.
    """
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    topic = state["topic"]
    response = tavily_client.search(language="English",query=topic+"Language: English", max_results=2, search_depth="fast")
    search_results = [SearchResult(url=result["url"], title=result["title"], content=result["content"]) for result in response["results"]]
    state["search_result"] = search_results
    return state


