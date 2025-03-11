from langgraph.func import task, entrypoint
import time

@task
def multiply_by_two(num: int) -> int:
    """First task that processes independently"""
    print("multiply_by_two: ", num)
    time.sleep(6)
    print("multiply_by_two is done: ")
    return num * 2

@task
def multiply_by_three(num: int) -> int:
    """First task that processes independently"""
    print("multiply_by_two: ", num)
    time.sleep(3)
    print("multiply_by_three is done: ")
    return num * 3

@entrypoint()
def parallel_workflow(num:int)->int:
    #Step 1 get futures
    start_time = time.time()

    futures = [multiply_by_two(num), multiply_by_three(num)]
    #Step 2 get results parallel / concurrently
    results = [future.result() for future in futures]

    end_time = time.time()

    print(f"Time Taken: {end_time - start_time} seconds")

    return {
        "results": results
    }

def call_parallel():
    result = parallel_workflow.invoke(5)
    print("Output: ", result)
