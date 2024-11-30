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
            {"role": "system", "content": "You are a professional software developer. Your task is to help the user develop software based on their descriptions."},
            {"role": "user", "content": f"Create a full Python package for {description}. Ask questions to refine the project description."}
        ]
    )
    return response['choices'][0]['message']['content']

# Streamlit UI for Web Deployment
st.title("AI Software Builder")
st.write("Let's build some software! I'll ask a few questions to help define your project.")

# Input box for user to provide description (if they choose to type instead of using voice)
description = st.text_input("Enter software description:")

# Chat-like interaction with follow-up questions
if description:
    speak(f"Great! You want to create software for: {description}. Let me ask you a few questions.")
    st.write(f"Great! You want to create software for: {description}. Let me ask you a few questions.")
    
    # Example questions to refine the project description
    st.write("What features would you like this software to have?")
    speak("What features would you like this software to have?")
    
    features = st.text_input("Enter features of the software:")
    
    if features:
        st.write(f"Thank you! Now, what programming langu