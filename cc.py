from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(api_key='AIzaSyAfXIC2XkKt8P8Piz1xK8GlLOtqFpunwes'))

def get_input_image_info(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()    ## read the file into bytes
        image_parts = [
            {
                "mime_type":uploaded_file.type,   ## get the type of file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Food Calorie")

st.header("Food Calories Web Application")

input = st.text_input("Ask any question:",key="input")
uploaded_file = st.file_uploader("Choose an Invoice image..",type=["jpg","jpeg","png"])
submit = st.button("Submit")

input_prompt = """You are an nutrition expert where you need to see the food items 
present in the input image and answer the question being asked, if the user don't ask
any question then calculate the total calories, also provide the details 
of each food items with calorie intake in below format:

1. Item 1 - no of calories
2. Item 2 - no of calories
------
------
"""

def get_gemini_model_response(input_prompt,image,question):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_prompt,image,question])
    return response.text

if submit:
    image_data = get_input_image_info(uploaded_file)
    model_response = get_gemini_model_response(input_prompt,image_data[0],input)
    st.write(model_response)

