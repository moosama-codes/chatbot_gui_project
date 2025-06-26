import google.generativeai as genai

# ✅ Gemini API Configuration
genai.configure(api_key="AIzaSyB5fFY--i-HVfmAP9lsr3csuzfV5NjZfYo")

# ✅ استخدم نموذج موجود فعليًا في حسابك (سريع وجيد)
MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(model_name=MODEL_NAME)

# ✅ Create a chat session once (to maintain history)
chat_session = model.start_chat(history=[])

# ✅ Chat function with optional history
def chat_with_deepseek(prompt, history=None):
    try:
        # Add user prompt to chat
        response = chat_session.send_message(prompt)
        
        # Return reply and current conversation history
        return response.text, chat_session.history

    except Exception as e:
        return f"⚠️ Gemini API error: {e}", []
