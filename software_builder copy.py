import openai
import pyttsx3
import speech_recognition as sr
import os
import streamlit as st

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set up OpenAI API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Get the key from environment variable for security

# Function to speak the text (Text-to-Speech)
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to voice commands (Speech-to-Text)
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for instructions...")
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command
        except Exception as e:
            print(f"Error: {str(e)}")
            speak("Sorry, I couldn't understand. Please try again.")
            return None

# Function to generate software code using OpenAI API
def generate_software_code(description):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional software developer."},
            {"role": "user", "content": f"Create a full Python package for {description}."}
        ]
    )
    return response['choices'][0]['message']['content']

# Streamlit UI for Web Deployment
st.title("AI Software Builder")
st.write("Speak or enter the description of the software you want to build!")

# Input box for user to provide description (if they choose to type instead of using voice)
description = st.text_input("Enter software description:")

# Button to trigger code generation based on user input
if st.button("Generate Code"):
    if description:
        speak(f"Generating code for {description}")
        code = generate_software_code(description)
        st.code(code, language="python")
    else:
        speak("Please enter a description for the software.")
        st.write("Please enter a description in the input box or use voice commands.")

# Voice-based interaction (button to start listening)
if st.button("Start Voice Command"):
    command = listen()
    if command:
        speak(f"Generating code for: {command}")
        code = generate_software_code(command)
        st.code(code, language="python")
        speak("Code has been generated and displayed on the screen.")
