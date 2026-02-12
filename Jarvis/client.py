import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def ask_ai(prompt):
    payload = {
        "model": MODEL,
        "prompt": f"You are Jarvis, a smart AI assistant.\nUser: {prompt}\nJarvis:",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        return "Error connecting to Ollama."
