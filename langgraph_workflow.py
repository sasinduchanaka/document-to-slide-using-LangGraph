from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load Gemini model
os.environ["GOOGLE_API_KEY"] = "AIzaSyAGcn8qjs5mTj7XeDUm1lcSqDhbQFXwQ9g"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

class DocState(TypedDict):
    text: str
    sections: list
    slides: list

def split_into_sections(state):
    prompt = f"""Split this document into 4–6 logical sections with summaries:\n\n{state['text']}"""
    response = llm.invoke(prompt)
    sections = response.content.strip().split("\n\n")
    return {"text": state["text"], "sections": sections, "slides": []}

def sections_to_slides(state):
    slides = []
    for section in state["sections"]:
        prompt = f"""Convert into slide:\n- Title\n- 3–5 bullet points\n\n{section}"""
        response = llm.invoke(prompt)
        slides.append(response.content.strip())
    return {"text": state["text"], "sections": state["sections"], "slides": slides}

def build_graph():
    graph = StateGraph(DocState)
    graph.add_node("split", RunnableLambda(split_into_sections))
    graph.add_node("slide_gen", RunnableLambda(sections_to_slides))
    graph.set_entry_point("split")
    graph.add_edge("split", "slide_gen")
    graph.add_edge("slide_gen", END)
    return graph.compile()
