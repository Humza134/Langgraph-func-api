import random
from typing import Literal, TypedDict
from langgraph.func import entrypoint, task

#Define our types
class RouterInput(TypedDict):
    query: str

class RouterOutput(TypedDict):
    query: str
    category: Literal["math", "writing", "general"]
    response: str

#Define our tasks

@task
def route_query(input: RouterInput) -> Literal["math", "writing", "general"]:
    #This is a simple example of a router that routes queries
    categories = ["math", "writing", "general"]
    return random.choice(categories)

@task
def handle_math(query:str) -> str:
    return f"Math handler processing: {query}"

@task
def handle_writing(query:str) -> str:
    return f"Writing handler processing: {query}"

@task
def handle_general(query:str) -> str:
    return f"General handler processing: {query}"

@entrypoint
def router_workflow(input_data: RouterInput) -> RouterOutput:
    """Main workflow that routes quries appropriate handlres"""

    #Get the routing decision
    #Decision Maker
    category = route_query(input_data).result()

    #Route to appropriate handler based on the query
    if category == "math":
        response = handle_math(input_data["query"]).result()
    elif category == "writing":
        response = handle_writing(input_data["query"]).result()
    else: # general
        response = handle_general(input_data["query"]).result()

    #Return the result with routing information
    return {
        "query": input_data["query"],
        "category": category,
        "response": response
    }

def call_router():
    # test input
    input_data = {"query": "What is the meaning of life??"}

    #Run the workflow
    result = router_workflow.invoke(input_data)

    print("Output: ", result)