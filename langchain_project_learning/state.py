from typing import TypedDict, List, Optional

class SearchResult(TypedDict):
    url: str
    title: str
    content: str

class ContentState(TypedDict):
    # Inputs
    topic: str
    brand_voice: str


    search_result: List[SearchResult]

    synthesized_content: str

    draft_content: str


    validation_passed: bool               # Did the critic approve?
    validation_feedback: str              # Critic's feedback if failed
    retry_count: int         
    
    final_content: str