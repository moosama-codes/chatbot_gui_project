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
        self.geometry("620x650")

        self.chat_history = []
        self.file_path = None
        self.last_bot_reply = ""

        # ---- Top Frame for Menus and Buttons ----
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(padx=10, pady=(10, 0), fill="x")

        # Tools Menu
        self.tools_var = ctk.StringVar(value="🛠 Tools")
        self.tools_menu = ctk.CTkOptionMenu(
            self.top_frame, values=["🌍 Translate", "🔊 Speak"],
            command=self.handle_tool_selection,
            variable=self.tools_var, width=150)
        self.tools_menu.pack(side="left", padx=(0, 10))

        # Lecture Tools Menu
        self.lecture_tools_var = ctk.StringVar(value="📘 Lecture Tools")
        self.lecture_tools_menu = ctk.CTkOptionMenu(
            self.top_frame, values=["📝 Summarize", "❓ Generate Quiz", "💡 Flashcards", "📄 Notes", "🔍 Explain"],
            command=self.handle_lecture_tool,
            variable=self.lecture_tools_var, width=200,
            state="disabled")
        self.lecture_tools_menu.pack(side="left", padx=(0, 10))

        # Upload Button
        self.upload_button = ctk.CTkButton(
            self.top_frame, text="📄 Upload File",
            command=self.upload_file,
            width=150)
        self.upload_button.pack(side="right", padx=(10, 0))

        # View File Button
        self.view_file_button = ctk.CTkButton(
            self.top_frame, text="📖 View File",
            command=self.show_file_popup,
            width=150,
            state="disabled"
        )
        self.view_file_button.pack(side="right", padx=(10, 0))

        # ---- Welcome Label ----
        label = ctk.CTkLabel(self, text="")
        label.pack(pady=10)

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

        # Clean the response
        cleaned_response = self.clean_response(response)
        self.animate_bot_response(cleaned_response)


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
            self.view_file_button.configure(state="normal")

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
            prompt = f"Please summarize the following document in a good and short way:\n\n{content}"
            summary, self.chat_history = chat_with_deepseek(prompt, self.chat_history)

        except Exception as e:
            summary = f"⚠️ Error summarizing file: {str(e)}"
        
        cleaned_summary = self.clean_response(summary)
        self.animate_bot_response(f"📄 Summary:\n{cleaned_summary}")



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

        
        cleaned_quiz = self.clean_response(quiz)
        formatted_quiz = self.format_quiz(cleaned_quiz)
        self.animate_bot_response(f"📝 Quiz:\n{formatted_quiz}")

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

        cleaned_flashcards = self.clean_response(flashcards)
        formatted_flashcards = self.format_flashcards(cleaned_flashcards)
        self.animate_bot_response(f"💡 Flashcards:\n{formatted_flashcards}")



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

        cleaned_notes = self.clean_response(notes)
        formatted_notes = self.format_notes(cleaned_notes)
        self.animate_bot_response(f"📄 Notes:\n{formatted_notes}")



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

        cleaned_explanation = self.clean_response(explanation)
        self.animate_bot_response( f"🔍 Explained Concepts:\n{cleaned_explanation}")


    def format_quiz(self, raw_quiz):
        lines = raw_quiz.split('\n')
        formatted_quiz = ""
        question_number = 1
        current_question = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue  # تخطي الأسطر الفارغة

            if line.lower().startswith("q") or "?" in line:
                # لو بدأ بسؤال
                if current_question:
                    formatted_quiz += f"{current_question}\n\n"
                current_question = f"Q{question_number}. {line}"
                question_number += 1
            elif line.lower().startswith(("a)", "b)", "c)", "d)")):
                # لو اختيار
                current_question += f"\n    {line}"
            else:
                # لو حاجة مش مفهومة أضفها كما هي
                current_question += f"\n    {line}"

        if current_question:
            formatted_quiz += f"{current_question}\n"

        return formatted_quiz.strip()
    

    def format_flashcards(self, raw_flashcards):
        lines = raw_flashcards.split('\n')
        formatted_flashcards = ""
        question_count = 1
        current_card = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.lower().startswith("q:"):
                if current_card:
                    formatted_flashcards += f"{current_card}\n\n"
                current_card = f"Flashcard {question_count}:\n{line}"
                question_count += 1
            elif line.lower().startswith("a:"):
                current_card += f"\n   {line}"
            else:
                current_card += f"\n   {line}"

        if current_card:
            formatted_flashcards += f"{current_card}\n"

        return formatted_flashcards.strip()


    def format_notes(self, raw_notes):
        lines = raw_notes.split('\n')
        formatted_notes = ""
        
        for line in lines:
            line = line.strip()
            if line:
                formatted_notes += f"• {line}\n\n"  # نضيف سطر فاضي بعد كل نقطة

        return formatted_notes.strip()






        
    
        


    def show_file_popup(self):
        if not self.file_path:
            self.append_chat_bubble("🤖", "⚠️ No file uploaded to view.")
            return

        from file_handler import load_file

        try:
            content = load_file(self.file_path)

            popup = ctk.CTkToplevel(self)
            popup.title("📖 File Content")
            popup.geometry("500x400")

            textbox = ctk.CTkTextbox(popup, wrap="word")
            textbox.insert("1.0", content)
            textbox.configure(state="disabled")  # خليه Read Only
            textbox.pack(padx=10, pady=10, fill="both", expand=True)

        except Exception as e:
            self.append_chat_bubble("🤖", f"⚠️ Error loading file for view: {str(e)}")





    def translate_last_response(self):
        from translator import translate_text
        user_input = self.entry.get().strip()
        if not user_input:
            self.append_chat_bubble("🤖", "⚠️ Please enter text to translate.")
            return
        translated = translate_text(user_input, dest="ar")
        self.append_chat_bubble("🤖", f"🌍 Translated:\n{translated}", align="right")


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

    def append_chat_bubble(self, sender, message, align="left"):
        anchor = "e" if sender == "👤" else "w"
        bg_color = "#128C7E" if sender == "👤" else "#E4E6EB"
        text_color = "white" if sender == "👤" else "black"

        bubble_frame = ctk.CTkFrame(self.chat_frame, fg_color=bg_color, corner_radius=12)
        bubble_frame.grid(row=self.chat_row, column=0, padx=10, pady=5, sticky=anchor)

        message_label = ctk.CTkLabel(
            bubble_frame,
            text=message,
            wraplength=400,
            justify=align,       # ✨ هنا بنستخدم المتغير الجديد
            text_color=text_color
        )
        message_label.pack(padx=10, pady=5)

        self.chat_row += 1
        self.chat_frame._parent_canvas.yview_moveto(1.0)


    def clean_response(self, text):
        import re

        # Remove Latex-like patterns: \boxed{...}, \text{...}, \begin{...}, \end{...}
        text = re.sub(r'\\boxed\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\begin\{[^}]*\}', '', text)
        text = re.sub(r'\\end\{[^}]*\}', '', text)
        text = re.sub(r'\$\$', '', text)  # Remove any double dollar signs (math mode)

        # Remove isolated LaTeX commands like \frac, \sqrt, etc.
        text = re.sub(r'\\[a-zA-Z]+\s*', '', text)

        # Replace common LaTeX linebreaks or spaces
        text = text.replace("\\n", "\n")
        text = text.replace("\\", "")

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()
     

    def animate_bot_response(self, text):
        import threading
        import time

        bubble = ctk.CTkLabel(self.chat_frame, text="", anchor="w", justify="left", wraplength=450)
        bubble.grid(row=self.chat_row, column=0, sticky="w", padx=10, pady=5)
        self.chat_row += 1

        def type_text():
            displayed_text = ""
            for char in text:
                displayed_text += char
                bubble.configure(text=displayed_text)
                self.update_idletasks()
                time.sleep(0.00001)  # سرعة الكتابة (كل 20 ملي ثانية حرف)

        # نشغل الكتابة في Thread عشان التطبيق ما يهنجش
        threading.Thread(target=type_text).start()


if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
