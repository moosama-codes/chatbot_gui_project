# main.py
import customtkinter as ctk
import tkinter.filedialog as fd

# Step 1: Set appearance and theme
ctk.set_appearance_mode("Dark")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Blue theme

# Step 2: Create the App class
class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window title and size
        self.title("Smart Chatbot")
        self.geometry("600x900")

        # Optional: Add a label just to confirm it's working
        label = ctk.CTkLabel(self, text="Welcome to Smart Chatbot")
        label.pack(pady=20)
        
        # Output Textbox
        # Chat History Textbox with Scroll
        self.textbox = ctk.CTkTextbox(
            self,
            width=400,
            height=300,
            font=("Arial", 14),
            wrap="word",     # wrap lines cleanly
        )
        self.textbox.pack(padx=20, pady=10, fill="both", expand=True)
        self.textbox.insert("end", "👋 Hello! Ask me anything or upload a file.\n")
        self.textbox.configure(state="disabled")

        # Input Field
        self.entry = ctk.CTkEntry(self, placeholder_text="Ask something...", width=400, font=("Arial", 14))
        self.entry.pack(pady=10)

        # Ask Buttonse
        # Button Row 1 (Ask + Upload)
        button_row1 = ctk.CTkFrame(self, fg_color="transparent")
        button_row1.pack(pady=5)

        self.ask_button = ctk.CTkButton(button_row1, text="✅ Ask", command=self.ask_general_question, fg_color="green", hover_color="#006400", width=200)
        self.ask_button.pack(side="left", padx=10)

        self.upload_button = ctk.CTkButton(button_row1, text="📄 Upload File", command=self.upload_file, fg_color="red", hover_color="#8B0000", width=200)
        self.upload_button.pack(side="left", padx=10)


        # Button Row 2 (Translate + Speak)
        button_row2 = ctk.CTkFrame(self, fg_color="transparent")
        button_row2.pack(pady=5)

        self.translate_button = ctk.CTkButton(button_row2, text="🌍 Translate", command=self.translate_last_response, fg_color="purple", hover_color="#4B0082", width=200)
        self.translate_button.pack(side="left", padx=10)

        self.speak_button = ctk.CTkButton(button_row2, text="🔊 Speak", command=self.speak_last_response, fg_color="orange", hover_color="#FF8C00", width=200)
        self.speak_button.pack(side="left", padx=10)

        # Summarize Button
      
        # Button Row 3 (Summarize + Empty)
        button_row3 = ctk.CTkFrame(self, fg_color="transparent")
        button_row3.pack(pady=5)

        self.summarize_button = ctk.CTkButton(button_row3, text="📝 Summarize", command=self.summarize_file, fg_color="blue", hover_color="#003366", width=200)
        self.summarize_button.pack(side="left", padx=10)

        # Optional placeholder button for symmetry
        self.dummy_button = ctk.CTkButton(button_row3, text="", state="disabled", width=200)
        self.dummy_button.pack(side="left", padx=10)



        self.chat_history = []


    def ask_general_question(self):
            user_input = self.entry.get().strip()

            if not user_input:
                self.textbox.configure(state="normal")
                self.textbox.insert("end", "\n⚠️ Please type something before clicking Ask!\n")
                self.textbox.configure(state="disabled")
                return

            self.textbox.configure(state="normal")
            self.textbox.insert("end", f"\n👤 You said: {user_input}\n")

            try:
                from chatbot_general import chat_with_deepseek

                if hasattr(self, "file_path") and self.file_path:
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()

                    combined_prompt = f"Based on the following document:\n\n{file_content}\n\nAnswer this question:\n{user_input}"
                    response, self.chat_history = chat_with_deepseek(combined_prompt, self.chat_history)

                else:
                    response, self.chat_history = chat_with_deepseek(user_input, self.chat_history)

                self.last_bot_reply = response

            except Exception as e:
                response = f"⚠️ Error: {str(e)}"

            self.textbox.insert("end", f"🤖 ChatBuddy replied: {response}\n")
            self.textbox.configure(state="disabled")
            self.entry.delete(0, 'end')

    def upload_file(self):
        import tkinter.filedialog as fd
        import os

        file_path = fd.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if not file_path:
            return  # User cancelled

        # Validate extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ['.pdf', '.txt']:
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "\n⚠️ Unsupported file type. Please upload a .pdf or .txt file.\n")
            self.textbox.configure(state="disabled")
            return

    # Save and confirm file
        self.file_path = file_path
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"\n📁 File uploaded: {os.path.basename(file_path)}\n")
        self.textbox.configure(state="disabled")

    # 🔜 Placeholder: Prepare the file when `chatbot_askfile.py` is ready
    # from chatbot_askfile import prepare_file
    # prepare_file(self.file_path)

    

    

    def summarize_file(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "\n⚠️ Please upload a file first to summarize.\n")
            self.textbox.configure(state="disabled")
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            prompt = f"Please summarize the following document:\n\n{content}"

            from chatbot_general import chat_with_deepseek
            summary, self.chat_history = chat_with_deepseek(prompt, self.chat_history)

        except Exception as e:
            summary = f"⚠️ Error summarizing file: {str(e)}"

        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"\n📄 Summary:\n{summary}\n")
        self.textbox.configure(state="disabled")






    def translate_last_response(self):
        from translator import translate_text

        user_input = self.entry.get().strip()

        if not user_input:
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "\n⚠️ Please enter text to translate.\n")
            self.textbox.configure(state="disabled")
            return

        translated = translate_text(user_input, dest="ar")

        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"🌍 Translated: {translated}\n")
        self.textbox.configure(state="disabled")

    def speak_last_response(self):
        from tts import speak

        if not hasattr(self, 'last_bot_reply') or not self.last_bot_reply:
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "\n⚠️ Nothing to speak yet.\n")
            self.textbox.configure(state="disabled")
            return

        speak(self.last_bot_reply)

































































if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
