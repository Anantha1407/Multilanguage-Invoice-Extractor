from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
from google import genai
from google.genai import types

client = genai.Client()

#Function to 

def get_gemini_response(input,image,prompt):
    response=client.models.generate_content(
        model="gemini-2.5-pro",
        config=types.GenerateContentConfig(
            system_instruction=input
        ),
        contents=[image,prompt],

    )
    return response.text

def input_image_setup(image):
    if image is not None:
        bytes_data = image.getvalue()
        image_parts = types.Part.from_bytes( data=bytes_data, mime_type=image.type)
        return image_parts
    else:
        return FileNotFoundError("No image uploaded")

st.set_page_config(
    page_title="MultiLanguae Invoice Extractor",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.header("MultiLanguae Invoice Extractor")

input=st.text_input("Input Prompt:",key="input")

uploaded_file = st.file_uploader("Upload an image of invoice", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit_button = st.button("Submit")

input_prompt="You are an expert in understanding invoices.We will upload an image of invoice and you will have to answer any questions based on the uploaded invoice image"

if submit_button:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.write(response)