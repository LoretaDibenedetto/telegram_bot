from typing import List

MAX_MEMORY = 5

def add_message(memory: List[str], message: str) -> List[str]:
    memory.append(message)
    if len(memory) > MAX_MEMORY:
        memory = memory[-MAX_MEMORY:]
    return memory

def build_context(memory: List[str]) -> str:
    return "\n".join(memory) + "\nAI:"
