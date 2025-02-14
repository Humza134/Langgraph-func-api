import os
from typing import TypedDict, List, Dict
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

@task
def extract_issues(customer_email: str)-> str:
    """
    First LLM Call: Extract the main issues from the customer's email
    """
    prompt = f"Extract the main issues and concerns from the following customer email:\n\n{customer_email}"
    msg = llm.invoke(prompt)
    return msg.content

@task
def generate_draft_response(issues: str)-> str:
    """
    Second LLM Call: Draft a response addresing the extracted issues.    
    """
    prompt = f"""Draft a response email addresing the following customer issues: {issues}\n
                Ensure the response is clear, professional and empathetic."""
    
    msg = llm.invoke(prompt)
    return msg.content

@task
def check_tone(draft_response: str)-> str:
    """
    Gate function: Chaeck if the drafted response is empathetic language.
    A simple check could look for word like 'sory' or 'appologize'.
    """
    if "sory" in draft_response.lower() or "appologize" in draft_response.lower():
        return "Pass"
    else:
        return "Fail"
    
@task
def improve_response_tone(draft_response: str)-> str:
    """
    Third LLM call: Improve the tone of the response to be more empathetic if necessary.
    """
    prompt = f"The following response needs a warmer, more empathetic tone:\n\n{draft_response}\n\n" \
             f"Rewrite it to better express understanding and concern for the customer's situation."
    msg = llm.invoke(prompt)
    return msg.content

@task
def polish_response(draft_response: str) -> str:
    """
    Fourth LLM call: Polish the response for clarity and professionalism.
    """
    prompt = f"Polish and finalize the following customer support response for clarity and professionalism:\n\n{draft_response}"
    msg = llm.invoke(prompt)
    return msg.content

@task
def write_to_file(response: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    response_file_path = os.path.join(output_dir, "customer_support_email.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(response)
    
    return response_file_path

@entrypoint()
def customer_support_response_workflow(customer_email: str)-> dict:
    #Stpe 1: Extract the main issues from the customer's email
    issues = extract_issues(customer_email).result()

    #Step 2: Draft a response addresing the extracted issues.
    draft_response = generate_draft_response(issues).result()

    #Step 3: Gate function: Chaeck if the drafted response is empathetic language.
    if check_tone(draft_response) == "Pass":
        final_response = polish_response(draft_response).result()
    else:
        improved_response = improve_response_tone(draft_response).result()
        final_response = polish_response(improved_response).result()

    #Step 4: Write the final response to a file
    response_file_path = write_to_file(final_response).result()

    return {
        "final_response": final_response,
        "file_path": response_file_path 
    }