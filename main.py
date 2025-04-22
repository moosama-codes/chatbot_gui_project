# main.py
import customtkinter as ctk
import tkinter.filedialog as fd
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Chatbot")
        self.geometry("600x650")

        self.chat_history = []
        self.file_path = None
        self.last_bot_reply = ""

        # ---- Top Menus ----
        self.tools_var = ctk.StringVar(value="🛠 Tools")
        self.tools_menu = ctk.CTkOptionMenu(
            self, values=["🌍 Translate", "🔊 Speak"],
            command=self.handle_tool_selection,
            variable=self.tools_var, width=150)
        self.tools_menu.place(x=10, y=10)

        self.lecture_tools_var = ctk.StringVar(value="📘 Lecture Tools")
        self.lecture_tools_menu = ctk.CTkOptionMenu(
            self, values=["📝 Summarize", "❓ Generate Quiz", "💡 Flashcards", "📄 Notes", "🔍 Explain"],
            command=self.handle_lecture_tool,
            variable=self.lecture_tools_var, width=200)
        self.lecture_tools_menu.place(x=170, y=10)
        self.lecture_tools_menu.configure(state="disabled")

        # Upload Button (Top-right)
        self.upload_button = ctk.CTkButton(
            self, text="📄 Upload File",
            command=self.upload_file,
            width=150)
        self.upload_button.place(x=400, y=10)

        # ---- Welcome Label ----
        label = ctk.CTkLabel(self, text="")
        label.pack(pady=20)

        # ---- Chat Frame ----
        self.chat_frame = ctk.CTkScrollableFrame(self, width=500, height=450)
        self.chat_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.chat_row = 0
        self.append_chat_bubble("🤖", "👋 Hello! Ask me anything or upload a file.")

        # ---- Input Area ----
        input_row = ctk.CTkFrame(self, fg_color="transparent")
        input_row.pack(pady=10)

        self.entry = ctk.CTkEntry(input_row, placeholder_text="Type your message...", width=400, font=("Arial", 14))
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.ask_general_question())

        self.send_button = ctk.CTkButton(input_row, text="📨 Send", command=self.ask_general_question, width=80)
        self.send_button.pack(side="left")

    def ask_general_question(self):
        user_input = self.entry.get().strip()
        if not user_input:
            self.append_chat_bubble("🤖", "⚠️ Please type something before clicking Send!")
            return

        self.append_chat_bubble("👤", user_input)

        try:
            from chatbot_general import chat_with_deepseek
            from file_handler import load_file

            if self.file_path:
                file_content = load_file(self.file_path)
                combined_prompt = f"Based on the following document:\n\n{file_content}\n\nAnswer this question:\n{user_input}"
                response, self.chat_history = chat_with_deepseek(combined_prompt, self.chat_history)
            else:
                response, self.chat_history = chat_with_deepseek(user_input, self.chat_history)

            self.last_bot_reply = response

        except Exception as e:
            response = f"⚠️ Error: {str(e)}"

        self.append_chat_bubble("🤖", response)
        self.entry.delete(0, 'end')

    def upload_file(self):
        from file_handler import load_file

        file_path = fd.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ['.pdf', '.txt']:
            self.append_chat_bubble("🤖", "⚠️ Unsupported file type. Please upload a .pdf or .txt file.")
            return

        try:
            # Try reading the file content to ensure it's readable
            _ = load_file(file_path)
            self.file_path = file_path
            self.append_chat_bubble("🤖", f"📁 File uploaded: {os.path.basename(file_path)}")
            self.lecture_tools_menu.configure(state="normal")
        except Exception as e:
            self.append_chat_bubble("🤖", f"⚠️ Failed to read file: {str(e)}")


    def summarize_file(self):
        if not self.file_path:
            self.append_chat_bubble("🤖", "⚠️ Please upload a file first to summarize.")
            return

        try:
            from file_handler import load_file
            from chatbot_general import chat_with_deepseek

            content = load_file(self.file_path)
            prompt = f"Please summarize the following document:\n\n{content}"
            summary, self.chat_history = chat_with_deepseek(prompt, self.chat_history)

        except Exception as e:
            summary = f"⚠️ Error summarizing file: {str(e)}"

        self.append_chat_bubble("🤖", f"📄 Summary:\n{summary}")



    def generate_quiz_from_file(self):
        if not self.file_path:
            self.append_chat_bubble("🤖", "⚠️ Please upload a file first to generate a quiz.")
            return

        try:
            from file_handler import load_file
            from chatbot_general import chat_with_deepseek

            content = load_file(self.file_path)
            prompt = (
                "Generate 5 multiple-choice questions based on the following document. "
                "Each question should have 4 options, and mark the correct answer clearly.\n\n"
                f"Document:\n{content}"
            )

            quiz, self.chat_history = chat_with_deepseek(prompt, self.chat_history)

        except Exception as e:
            quiz = f"⚠️ Error generating quiz: {str(e)}"

        self.append_chat_bubble("🤖", f"📝 Quiz:\n{quiz}")

    def generate_flashcards_from_file(self):
        if not self.file_path:
            self.append_chat_bubble("🤖", "⚠️ Please upload a file first to create flashcards.")
            return

        try:
            from file_handler import load_file
            from chatbot_general import chat_with_deepseek

            content = load_file(self.file_path)
            prompt = (
                "Create 5 flashcards based on the following document. Each flashcard should be in Q&A format like:\n"
                "Q: What is X?\nA: Explanation\n\n"
                f"Document:\n{content}"
            )

            flashcards, self.chat_history = chat_with_deepseek(prompt, self.chat_history)

        except Exception as e:
            flashcards = f"⚠️ Error generating flashcards: {str(e)}"

        self.append_chat_bubble("🤖", f"💡 Flashcards:\n{flashcards}")


    def generate_notes_from_file(self):
        if not self.file_path:
            self.append_chat_bubble("🤖", "⚠️ Please upload a file first to create notes.")
            return

        try:
            from file_handler import load_file
            from chatbot_general import chat_with_deepseek

            content = load_file(self.file_path)
            prompt = (
                "Extract structured notes from the following document. Present the notes as clear bullet points, "
                "organized by topic if possible.\n\n"
                f"Document:\n{content}"
            )

            notes, self.chat_history = chat_with_deepseek(prompt, self.chat_history)

        except Exception as e:
            notes = f"⚠️ Error generating notes: {str(e)}"

        self.append_chat_bubble("🤖", f"📄 Notes:\n{notes}")


    def explain_file_concepts(self):
        if not self.file_path:
            self.append_chat_bubble("🤖", "⚠️ Please upload a file first to explain its concepts.")
            return

        try:
            from file_handler import load_file
            from chatbot_general import chat_with_deepseek

            content = load_file(self.file_path)
            prompt = (
                "Read the following document and identify any technical terms, complex concepts, or jargon. "
                "For each, provide a simple explanation like you're teaching a beginner.\n\n"
                f"Document:\n{content}"
            )

            explanation, self.chat_history = chat_with_deepseek(prompt, self.chat_history)

        except Exception as e:
            explanation = f"⚠️ Error generating explanations: {str(e)}"

        self.append_chat_bubble("🤖", f"🔍 Explained Concepts:\n{explanation}")
        
    
        































    

    def translate_last_response(self):
        from translator import translate_text
        user_input = self.entry.get().strip()
        if not user_input:
            self.append_chat_bubble("🤖", "⚠️ Please enter text to translate.")
            return
        translated = translate_text(user_input, dest="ar")
        self.append_chat_bubble("🤖", f"🌍 Translated: {translated}")

    def speak_last_response(self):
        from tts import speak
        if not self.last_bot_reply:
            self.append_chat_bubble("🤖", "⚠️ Nothing to speak yet.")
            return
        speak(self.last_bot_reply)

    def handle_tool_selection(self, selection):
        if selection == "🌍 Translate":
            self.translate_last_response()
        elif selection == "🔊 Speak":
            self.speak_last_response()
        self.tools_var.set("🛠 Tools")

    def handle_lecture_tool(self, selection):
        if selection == "📝 Summarize":
            self.summarize_file()
        elif selection == "❓ Generate Quiz":
            self.generate_quiz_from_file()
        elif selection == "💡 Flashcards":
            self.generate_flashcards_from_file()
        elif selection == "📄 Notes":
            self.generate_notes_from_file()
        elif selection == "🔍 Explain":
            self.explain_file_concepts()
        self.lecture_tools_var.set("📘 Lecture Tools")

    def append_chat_bubble(self, sender, message):
        anchor = "e" if sender == "👤" else "w"
        bg_color = "#128C7E" if sender == "👤" else "#E4E6EB"
        text_color = "white" if sender == "👤" else "black"
        bubble_frame = ctk.CTkFrame(self.chat_frame, fg_color=bg_color, corner_radius=12)
        bubble_frame.grid(row=self.chat_row, column=0, padx=10, pady=5, sticky=anchor)
        message_label = ctk.CTkLabel(bubble_frame, text=message, wraplength=400, justify="left", text_color=text_color)
        message_label.pack(padx=10, pady=5)
        self.chat_row += 1
        self.chat_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
