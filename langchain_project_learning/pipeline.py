"""
Content Engine Pipeline
========================
Connects all 4 nodes: Search → Synthesize → Writer → Validator

Why not just use `|` pipe for everything?
-----------------------------------------
The LCEL pipe `|` works great for INDIVIDUAL chains (prompt | llm | parser).
But our nodes are FUNCTIONS that take/return ContentState dicts, not Runnables.

Solution: Wrap each node function with `RunnableLambda` to make them pipeable.
For the validator retry loop, we handle it manually since `|` is strictly linear.
"""

from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_project_learning.nodes.search_node import search_node
from langchain_project_learning.nodes.synthesize_node import synthesize_data
from langchain_project_learning.nodes.writer_node import writer_node
from langchain_project_learning.nodes.validator_node import validate_results
from langchain_project_learning.state import ContentState

# ──────────────────────────────────────────────────
# Step 1: Wrap node functions as RunnableLambdas
# This converts plain functions into LCEL-compatible Runnables
# ──────────────────────────────────────────────────
search_runnable = RunnableLambda(search_node)
synthesize_runnable = RunnableLambda(synthesize_data)
writer_runnable = RunnableLambda(writer_node)
validator_runnable = RunnableLambda(validate_results)

# ──────────────────────────────────────────────────
# Step 2: Build the linear pipeline using `|` pipe
# This chains: Search → Synthesize → Writer
# (Validator is separate because it has a retry loop)
# ──────────────────────────────────────────────────
linear_pipeline = search_runnable | synthesize_runnable | writer_runnable


# ──────────────────────────────────────────────────
# Step 3: Full pipeline with validator retry loop
# ──────────────────────────────────────────────────
MAX_RETRIES = 1

def run_pipeline(topic: str, brand_voice: str = "professional") -> ContentState:
    """
    Runs the full content engine pipeline:
    1. Search → Synthesize → Writer (via LCEL pipe)
    2. Validator (with retry loop)

    If validation fails, it sends feedback back to the writer
    and retries ONCE.
    """
    # Initialize state with defaults
    initial_state: ContentState = {
        "topic": topic,
        "brand_voice": brand_voice,
        "search_result": [],
        "synthesized_content": "",
        "draft_content": "",
        "validation_passed": False,
        "validation_feedback": "",
        "retry_count": 0,
        "final_content": "",
    }

    # Run the linear pipeline: Search → Synthesize → Writer
    state = linear_pipeline.invoke(initial_state)

    # Validation loop (max 1 retry)
    for attempt in range(MAX_RETRIES + 1):
        state = validator_runnable.invoke(state)

        if state.get("validation_passed"):
            print(f"✅ Validation PASSED on attempt {attempt + 1}")
            break
        else:
            print(f"❌ Validation FAILED on attempt {attempt + 1}")
            if attempt < MAX_RETRIES:
                # Feed validation feedback back to the writer
                state["retry_count"] = attempt + 1
                print(f"🔄 Retrying writer with feedback...")
                state = writer_runnable.invoke(state)
            else:
                print(f"⚠️  Max retries reached. Accepting latest draft.")
                state["final_content"] = state["draft_content"]

    return state["final_content"]


if __name__ == "__main__":
    print(run_pipeline("AI"))
