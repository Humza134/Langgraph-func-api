from langgraph.func import entrypoint, task
import time

@task
def task1():
    # print("Task 1")
    time.sleep(3)
    return "Task 1 Executed"

@task
def task2():
    # print("Task 2")
    time.sleep(3)
    return "Task 2 Executed"

# Langchain Runnable === Protocol === Pregel (Google Large Scale Graph Processing Library)
@entrypoint()
def run_flow(input:str):
    print("Running Flow", input)

    task1_output = task1().result()
    task2_output = task2().result()
    time.sleep(3)
    return f"Flow Executed: {task1_output} and {task2_output}"

# Run the workflow
def run_chain():
    # res = run_flow.invoke("Simple Input")
    # print(res)
    for event in run_flow.stream("Simple Input"):
        print(event)