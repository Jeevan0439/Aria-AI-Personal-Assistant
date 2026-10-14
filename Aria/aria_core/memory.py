import json, os
from datetime import datetime

class Memory:
    def __init__(self, mem_dir="F:\\Aria\\memory"):
        self.dir = mem_dir
        os.makedirs(mem_dir, exist_ok=True)
        self.facts_path = os.path.join(mem_dir, "facts.json")
        self.convo_path = os.path.join(mem_dir, "conversations.json")
        self.facts   = self._load(self.facts_path, {})
        self.history = self._load(self.convo_path, [])

    def _load(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return default
        return default

    def _save(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def remember_fact(self, key, value):
        self.facts[key.lower()] = {"value": value, "ts": datetime.now().isoformat()}
        self._save(self.facts_path, self.facts)

    def recall_facts(self):
        return {k: v["value"] for k, v in self.facts.items()}

    def add_turn(self, role, content):
        self.history.append({
            "role": role,
            "content": content,
            "ts": datetime.now().isoformat()
        })
        self.history = self.history[-200:]
        self._save(self.convo_path, self.history)

    def recent_context(self, n=12):
        return [{"role": t["role"], "content": t["content"]}
                for t in self.history[-n:]]