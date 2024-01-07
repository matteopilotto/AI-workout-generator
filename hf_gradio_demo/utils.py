
import random
import time
from langchain.schema.messages import HumanMessage, SystemMessage


def retrieve_knowledge(query, vectorstore, k=10, randomize=True):
    knowledge = [d.page_content.strip() for d in vectorstore.similarity_search(query, k=k)]
    
    if randomize:
        knowledge = random.sample(knowledge, k)

    knowledge = "\n\n\n".join(knowledge)

    return knowledge


def generate_workout(system_prompt, query, knowledge, llm):
    messages = [
        SystemMessage(content=system_prompt.format(workout_context=knowledge)),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages).content.strip()

    return response


def run(gender, muscle_group, equipment, level, duration, vectorstore, system_prompt, llm, k=5, randomize=True):
    query = f"{duration}-minute {muscle_group} workout for {gender} {level} level {equipment}"
    knowledge = retrieve_knowledge(query, vectorstore, k, randomize)
    response = generate_workout(system_prompt, query, knowledge, llm)

    for i in range(len(response)):
        time.sleep(0.01)
        yield response[:i+1]