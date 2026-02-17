import os
from langchain_project_learning import ContentState
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY")

def writer_node(state: ContentState) -> ContentState:
    llm = ChatGroq(model="llama-3.1-8b-instant")

    # Using itemgetter to get the values from the state
    input = {
        "brand_voice" : itemgetter("brand_voice"),
        "validation_feedback" : itemgetter("validation_feedback"),
        "synthesize_data" : itemgetter("synthesized_content")
    }
    prompt = ChatPromptTemplate.from_template("""You are a professional Brand and Marketing manager who has an expertise in Research and making brands go viral and as a result the sales are going crazy , Your task is understand the provided pointers and summarise according to this brand voice {brand_voice} and according to the provided {validation_feedback}-
    The below is the data you need to summarise according to the rules.
    {synthesize_data}
    """)

    chain = input |  prompt | llm | StrOutputParser()

    output = chain.invoke(state)
    state["draft_content"] = output
    return state


# if __name__ == "__main__":
#     state = ContentState(
#         synthesize_data="Mobile phones: 1. Instant global connectivity, 2. Professional-grade cameras, 3. Access to the world's information, 4. Secure mobile payments, 5. Endless entertainment options, 6. Essential productivity tools.",
#         brand_voice="Fun but catchy",
#         validation_feedback="",
#     )

#     writer_node(state)
#     print(state)