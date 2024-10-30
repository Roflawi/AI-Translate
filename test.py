import streamlit as st
from googletrans import Translator
import os
import pyttsx3
import speech_recognition as sr

# Initialize the translator
translator = Translator()

# Title of the app
st.title("AI Translate")

# Function to recognized speech and convert it to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Please Speak...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio. Please try again.")
            return ""
        except sr.RequestError as e:
            st.error(f"Error contacting the service : {e}")
            return ""

# Variabel to save text
if 'text' not in st.session_state:
    st.session_state.text = ""

# Path to the logo
logo_path = "E:/NLP/mic.png"  # Replace with the correct path 

# Check if this files exist
if os.path.exists(logo_path):
     # Display logo in the top button
    st.image(logo_path, width=100)
     # Show logo image as button
    if st.button("Input Voice", key="start_input"):
        st.session_state.text = recognize_speech()
else:
    st.error(f"File doesn't exist: {logo_path}")
   

# Manual text input
text = st.text_area("Input Text :", value=st.session_state.text)

# Save input text to session_state
if text:
    st.session_state.text = text

# Function for text-to-speech
def speak(text):
    if text:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# If text is present and not empty
if st.session_state.text and st.session_state.text.strip():  # Ensure text is not empty
    detected_language = translator.detect(st.session_state.text).lang

    # Select target language
    languages = {'English': 'en', 'Indonesia': 'id'}  # Use correct language code
    target_language = st.selectbox("Language :", list(languages.keys()))

    # Button to translate
    if st.button("Translate"):
        if st.session_state.text:
            translation = translator.translate(st.session_state.text, dest=languages[target_language])
            st.session_state.translation = translation.text  # Save translation in session state
            st.success(f"Text Translate : {translation.text}")

            # Automatically read out the translation after displaying
            speak(translation.text)

            # Save history
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((st.session_state.text, translation.text, detected_language, target_language))
            
            # Show history
            st.subheader("History")
            for item in st.session_state.history:
                st.write(f"{item[0]}  →  {item[1]}")

        else:
            st.error("Input Text.")
