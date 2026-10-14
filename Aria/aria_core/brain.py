import requests
import sys
sys.path.insert(0, "F:\\Aria")
from config import OLLAMA_MODEL, USER_NAME, ASSISTANT_NAME

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, an advanced personal AI assistant for {USER_NAME}, a third-year AI/ML engineering student and founder of Jeedar Agency in Bengaluru, India.
You are sharp, concise, warm and capable — like Jarvis. Address the user as {USER_NAME}.
Answer in 1-3 sentences max. Be direct. Never say "As an AI". Just answer."""

class Brain:
    def __init__(self, memory):
        self.memory = memory

    def think(self, user_input, extra_context=""):
        facts = self.memory.recall_facts()
        fact_str = "\n".join(f"- {k}: {v}" for k, v in facts.items()) or "None yet."

        recent = self.memory.recent_context()
        hist_str = "\n".join(f"{t['role'].capitalize()}: {t['content']}" for t in recent)

        prompt = f"""{SYSTEM_PROMPT}

Known facts about {USER_NAME}:
{fact_str}

{f'Recent conversation:{chr(10)}{hist_str}' if hist_str else ''}
{f'Extra context: {extra_context}' if extra_context else ''}

{USER_NAME}: {user_input}
{ASSISTANT_NAME}:"""

        try:
            res = requests.post(OLLAMA_URL,
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=60)
            answer = res.json().get("response", "").strip()
        except Exception as e:
            answer = f"Ollama error: {e}"

        self.memory.add_turn("user", user_input)
        self.memory.add_turn("assistant", answer)
        return answer