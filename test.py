import google.generativeai as genai

genai.configure(api_key="AIzaSyB5fFY--i-HVfmAP9lsr3csuzfV5NjZfYo")

# استخدم النموذج الصحيح الموجود عندك
model = genai.GenerativeModel("models/gemini-2.5-flash")

response = model.generate_content("Hello Gemini, who are you?")
print(response.text)
