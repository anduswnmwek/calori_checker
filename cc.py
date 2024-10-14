import streamlit as st
import pandas as pd
import requests
import json
import cv2

# Replace with your API key and endpoint
api_key = "e4a92ac014b24410b5534a5dd0686236"
api_endpoint = "https://api.spoonacular.com/food/search.json"

# ... (rest of your code)

# Streamlit app
st.title("Calorie Finder")

# Camera feature
if st.button("Take Photo"):
    img_bytes = st.camera_input("Take a photo of the food")
    if img_bytes:
        # Process the image (e.g., resize, convert to base64)
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), 1)
        img = cv2.resize(img, (224, 224))
        img_base64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

        # Send the image to the API
        params = {
            "apiKey": api_key,
            "image": img_base64,
        }

        response = requests.get(api_endpoint, params=params)
        # ... (rest of the API response processing)
