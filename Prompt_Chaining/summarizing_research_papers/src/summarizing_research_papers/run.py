from summarizing_research_papers.workflow import summarize_research_workflow

research_paper = (
    """
    The Role of Intelligent Agents in Modern Systems

    Intelligent agents, autonomous software entities, are revolutionizing industries 
    by performing tasks with minimal human intervention. These agents perceive environments
    via sensors, process data, and act using actuators to achieve goals. Applications span 
    healthcare (diagnosis), finance (fraud detection), and robotics (autonomous navigation). 
    Challenges include ethical concerns (bias, privacy), scalability, and explainability.
    Future research focuses on human-agent collaboration and interoperability in 
    multi-agent systems. As AI advances, intelligent agents will play a pivotal role 
    in shaping technology, provided ethical and technical challenges are addressed. 
    Their potential to transform industries and improve efficiency remains unparalleled.

    Keywords: Intelligent agents, AI, autonomy, ethics, applications.
    """
)

def main_run():
    # Run the workflow
    result = summarize_research_workflow.invoke(research_paper)
    print("\n\n", "Summarizing Research Papers: ", result, "\n\n")

def stream_run():
    for step in summarize_research_workflow.stream(research_paper, stream_mode="updates"):
        print(step)
        print("\n")