AI Voice Assistant
------------------------------------
This is a private and local AI assistant that listens to your voice, transcribes your question, and answers using a locally running LLM (currently using LLama 3 by META).

Features
------------------------------------
- Uses customTkinter as a GUI interface
- Uses Google Web Speed API (SpeechRecognition) to listen and transcribe
- Uses Ollama to run Llama 3 offline for privacy

Requirements
------------------------------------
- Download Python (https://www.python.org/downloads/)
- Download necessary libraries: pip install customtkinter SpeechRecognition ollama pyaudio
- Download Ollama (https://ollama.com)
- Download your AI model (ollama pull llama3). You can use any AI model you desire but you will have to edit the code.

How-to-Use
------------------------------------
1.) Run application
2.) Select your microphone
3.) Press start and start speaking
