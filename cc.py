import streamlit as st
import pandas as pd
import requests
import json
import cv2
import numpy as np
import base64

# Replace with your correct API key and endpoint
api_key = "e4a92ac014b24410b5534a5dd0686236"
api_endpoint = "https://api.spoonacular.com/food/products/search"

# Define a function to find calories based on food name or image
def find_calories(query, is_image=False):
    params = {
        "apiKey": api_key,
        "query": query,
    }

    if is_image:
        # Handle image separately if needed
        params["image"] = query

    response = requests.get(api_endpoint, params=params)
    data = json.loads(response.text)

    if response.status_code == 200 and "products" in data and data["products"]:
        # Process results from API
        products = data["products"][0]  # Assuming we take the first result
        return f"{products['title']} has {products['nutrition']['calories']} calories per serving"
    else:
        return "No data found for that food."

# Streamlit app
st.title("Calorie Finder")

# Camera feature
if st.button("Take Photo"):
    img_bytes = st.camera_input("Take a photo of the food")
    if img_bytes:
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), 1)
        img = cv2.resize(img, (224, 224))
        img_base64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
        result = find_calories(img_base64, is_image=True)
        st.write(result)

# Image upload
uploaded_image = st.file_uploader("Upload a food image")

# Text input for food name
food_name = st.text_input("Enter a food name:")

# Button to trigger the search
if st.button("Find Calories"):
    if uploaded_image:
        img = cv2.imdecode(np.frombuffer(uploaded_image.getvalue(), np.uint8), 1)
        img = cv2.resize(img, (224, 224))
        img_base64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
        query = img_base64
        is_image = True
    else:
        query = food_name
        is_image = False

    result = find_calories(query, is_image)
    st.write(result)

