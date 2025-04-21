# chatbot_general.py

import requests
import json

# ==== Configuration ====
API_KEY = "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"  # Put your real OpenRouter key here
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",  # Use your domain if hosted
    "X-Title": "Local Chatbot Test"
}

def chat_with_deepseek(prompt, history=None):
    if history is None:
        history = []

    # Add the new user message to the conversation history
    history.append({"role": "user", "content": prompt})

    payload = {
        "model": "deepseek/deepseek-r1-zero:free",
        "messages": history,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        # Add the assistant's reply to the history
        history.append({"role": "assistant", "content": reply})

        return reply, history

    except requests.exceptions.RequestException as e:
        return f"🔴 Request error: {e}", history
    except KeyError:
        return "🔴 Unexpected response format.", history

# Test block
if __name__ == "__main__":
    history = []
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply, history = chat_with_deepseek(user_input, history)
        print("🤖 ", reply)
