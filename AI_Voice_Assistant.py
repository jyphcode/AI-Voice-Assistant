'''
    Joe Phung
    12/20/2025
    AI Vocie assistant
    This program uses speech recognition from Google Web Speech API
    and Ollama to listen to user's questions and answer them using a locally run LLM.
'''

import customtkinter as ctk
import speech_recognition as sr
import ollama 
import threading 

ctk.set_appearance_mode("system") # can support system/dark/light mode
ctk.set_default_color_theme("blue") # colors are kinda limited

class AIAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Speech-to-Text Assistant")
        self.geometry("720x720")
        self.iconbitmap("logo_icon.ico")

        self.miclabel = ctk.CTkLabel(self, text="Select Microphone:", font = ("Arial", 14, "bold"))
        self.miclabel.pack(pady=(20,5))

        self.micOptions = self.getMicrophoneList() # need to implement this
        self.micDropdown = ctk.CTkOptionMenu(self, values = self.micOptions)
        self.micDropdown.pack(pady=10)

        self.statusLabel = ctk.CTkLabel(self, text="Ready...", text_color="gray")
        self.statusLabel.pack(pady=5)
        
        self.button = ctk.CTkButton(self, text = "Start Listening", font = ("Arial", 14, "bold"), height = 40, command=self.startThread)
        self.button.pack(pady=20)

        self.outputLabel = ctk.CTkLabel(self, text = "Output:", anchor= "w")
        self.outputLabel.pack(pady =(10, 0), padx=20, anchor = "w")

        self.textbox = ctk.CTkTextbox(self, font=("Consolas", 14))
        self.textbox.pack(pady=10, padx = 20, fill = "both", expand = True)

    def getMicrophoneList(self):
        try:
            mics = sr.Microphone.list_microphone_names()
            return [f"{i}: {name}" for i, name in enumerate(mics)]
        except:
            return ["0: Default Microphone"]

    def startThread(self):
        self.button.configure(state = "disabled", text = "Running...")
        self.statusLabel.configure(text="Initializing...", text_color="#3B8ED0")

        threading.Thread(target=self.logic).start()
        
    def logic(self):

        # choose our mic
        recognizer = sr.Recognizer()
        transcribe = ""
        reply = ""

        try:
            mic = self.micDropdown.get()
            index = int(mic.split(":")[0])

            with sr.Microphone(device_index=index) as source:
                
                self.updateStatus("Adjusting...", "orange")
                recognizer.adjust_for_ambient_noise(source, duration = 1)

                self.updateStatus("Listening...", "green")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)

                self.updateStatus("Processing...", "orange")
                transcribe = recognizer.recognize_google(audio)

                self.textbox.insert("end", f"YOU: {transcribe}\n")
                self.textbox.see("end")

                self.updateStatus("Thinking...", "blue")

                response = ollama.chat(model = 'llama3', messages = [{'role': 'user', 'content': transcribe}])

                reply = response['message']['content']

                self.textbox.insert("end", f"AI: {reply}\n\n" + "-" * 40 + "\n\n")
                self.textbox.see("end")

                self.updateStatus("Ready", "gray")
        except Exception as e:
            self.textbox.insert("end", f"Error: {e}\n")
            self.updateStatus("Error", "red")

        finally:
            self.button.configure(state = "normal", text = "Start Listening")

    def updateStatus(self, text, color):
        self.statusLabel.configure(text=text, text_color=color)

if __name__ == "__main__":
    app = AIAssistant()
    app.mainloop()
