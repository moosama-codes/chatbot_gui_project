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
        self.geometry("600x600")

                # Tools Dropdown Menu (Top-left)
        self.tools_var = ctk.StringVar(value="🛠 Tools")
        self.tools_menu = ctk.CTkOptionMenu(
            self,
            values=["📄 Upload File", "🌍 Translate", "🔊 Speak", "📝 Summarize"],
            command=self.handle_tool_selection,
            variable=self.tools_var,
            width=200
        )
        self.tools_menu.place(x=10, y=10)  # Top-left position


        # Optional: Add a label just to confirm it's working
        label = ctk.CTkLabel(self, text="Welcome to Smart Chatbot")
        label.pack(pady=20)
        
        # Output Textbox
        # Chat History Textbox with Scroll
        # Scrollable chat area for chat bubbles
        self.chat_frame = ctk.CTkScrollableFrame(self, width=500, height=500)
        self.chat_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.chat_row = 0  # to track message position

        # Initial greeting message as a bubble
        self.append_chat_bubble("🤖", "👋 Hello! Ask me anything or upload a file.")


        # Input Field
        # Input Row with Entry + Send Button
        input_row = ctk.CTkFrame(self, fg_color="transparent")
        input_row.pack(pady=10)

        self.entry = ctk.CTkEntry(input_row, placeholder_text="Type your message...", width=400, font=("Arial", 14))
        self.entry.pack(side="left", padx=(0, 10))

        self.entry.bind("<Return>", lambda event: self.ask_general_question())

        self.send_button = ctk.CTkButton(input_row, text="📨 Send", command=self.ask_general_question, width=80)
        self.send_button.pack(side="left")

        # Ask Buttonse
        # Button Row 1 (Ask + Upload) 
        """
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
        self.dummy_button.pack(side="left", padx=10)  """
        


        self.chat_history = []


    def ask_general_question(self):
        user_input = self.entry.get().strip()

        if not user_input:
            self.append_chat_bubble("🤖", "⚠️ Please type something before clicking Send!")
            return

        # ✅ Display user's message as a bubble
        self.append_chat_bubble("👤", user_input)

        try:
            from chatbot_general import chat_with_deepseek

            # If a file is uploaded, include it in the prompt
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

        # ✅ Display bot's response as a bubble
        self.append_chat_bubble("🤖", response)
        self.entry.delete(0,'end')

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


    def handle_tool_selection(self, selection):
        if selection == "📄 Upload File":
            self.upload_file()
        elif selection == "🌍 Translate":
            self.translate_last_response()
        elif selection == "🔊 Speak":
            self.speak_last_response()
        elif selection == "📝 Summarize":
            self.summarize_file()

        self.tools_var.set("🛠 Tools")  # Reset menu text


    def append_chat_bubble(self, sender, message):
        if sender == "👤":
            anchor = "e"  # right side
            bg_color = "#128C7E"  # greenish (like WhatsApp)
            text_color = "white"
        else:
            anchor = "w"  # left side
            bg_color = "#E4E6EB"  # light gray
            text_color = "black"

        # Create a chat bubble frame
        bubble_frame = ctk.CTkFrame(self.chat_frame, fg_color=bg_color, corner_radius=12)
        bubble_frame.grid(row=self.chat_row, column=0, padx=10, pady=5, sticky=anchor)

        # Label inside the bubble
        message_label = ctk.CTkLabel(
            bubble_frame,
            text=message,
            wraplength=400,
            justify="left",
            text_color=text_color
        )
        message_label.pack(padx=10, pady=5)

        self.chat_row += 1

        # ✅ Auto-scroll to bottom
        self.chat_frame._parent_canvas.yview_moveto(1.0)





















































if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
