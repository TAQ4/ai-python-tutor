# tutor_core.py

import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("❗ OPENROUTER_API_KEY not found in .env")

MODEL = "nousresearch/deephermes-3-mistral-24b-preview:free"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MEMORY_FILE = Path(__file__).parent / "memory.json"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, ensure_ascii=False, indent=2), encoding="utf-8")

def ask_tutor(question: str) -> str:
    memory = load_memory()
    system_prompt = {"role": "system", "content": "You are a helpful AI tutor for Python programming. Keep track of the user's preferences and prior conversation for personalized responses."}
    messages = [system_prompt] + memory + [{"role": "user", "content": question}]
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.3
    }
    response = requests.post(ENDPOINT, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"❗ OpenRouter API error {response.status_code}: {response.text}"
    data = response.json()
    answer = data["choices"][0]["message"]["content"].strip()
    # update memory
    memory.append({"role": "user", "content": question})
    memory.append({"role": "assistant", "content": answer})
    save_memory(memory)
    return answer
