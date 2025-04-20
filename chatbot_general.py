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

def chat_with_deepseek(prompt):
    payload = {
        "model": "deepseek/deepseek-r1-zero:free",  # This is the correct model name
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        return reply
    except requests.exceptions.RequestException as e:
        return f"🔴 Request error: {e}"
    except KeyError:
        return "🔴 Unexpected response format."

# Test block
if __name__ == "__main__":
    user_input = input("👤 You: ")
    reply = chat_with_deepseek(user_input)
    print("🤖 DeepSeek:", reply)
