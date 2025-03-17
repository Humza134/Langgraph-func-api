from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import os

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

#1. Summarizing and Refining Research Papers

#Step 1: Summarize a research paper into bullet points.

@task
def summarize_paper(paper: str) -> str:
    """
    Summarize the research paper into bullet points.
    """
    prompt = f"Summarize the following research paper into bullet points:\n\n{paper}"
    msg = llm.invoke(prompt)
    return msg.content

#Step 2: Extract key insights from the summary.
@task
def extract_insights(summary: str) -> str:
    """
    Extract key insights from the summary.
    """
    prompt = f"Extract the key insights from the following summary:\n\n{summary}"
    msg = llm.invoke(prompt)
    return msg.content

#Step 3: Rephrase insights into layman's terms for a general audience.
@task
def rephrase_insights(insights: str) -> str:
    """
    Rephrase the key insights into layman's terms for a general audience.
    """
    prompt = f"Rephrase the following key insights into layman's terms for a general audience:\n\n{insights}"
    msg = llm.invoke(prompt)
    return msg.content

#Step 4: Polish the layman's terms insights for clarity and readability.
@task
def polish_insights(insights: str) -> str:
    """
    Polish the layman's terms insights for clarity and readability.
    """
    prompt = f"Polish the following layman's terms insights for clarity and readability:\n\n{insights}"
    msg = llm.invoke(prompt)
    return msg.content

#Step 5: Write the refined insights to a file.
@task
def write_to_file(insights: str) -> str:
    """
    Write the refined insights to a file.
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    response_file_path = os.path.join(output_dir, "refined_insights.txt")
    with open(response_file_path, "w", encoding="utf-8") as f:
        f.write(insights)
    return response_file_path

#2. Summarize research Workflow
@entrypoint()
def summarize_research_workflow(paper: str) -> dict:
    #Step 1: Summarize the research paper into bullet points.
    print("STEP1: Summarizing the research paper...")
    summary = summarize_paper(paper).result()

    #Step 2: Extract key insights from the summary.
    print("STEP2: Extracting key insights...")
    insights = extract_insights(summary).result()

    #Step 3: Rephrase insights into layman's terms for a general audience.
    print("STEP3: Rephrasing insights into layman's terms...")
    layman_insights = rephrase_insights(insights).result()

    #Step 4: Polish the layman's terms insights for clarity and readability.
    print("STEP4: Polishing the layman's terms insights")
    polished_insights = polish_insights(layman_insights).result()

    #Step 5: Write the refined insights to a file.
    print("STEP5: Writing the refined insights to a file...")
    file_path = write_to_file(polished_insights).result()

    return {
        "polished_insights": polished_insights,
        "file_path": file_path
    }