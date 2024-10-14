import streamlit as st
import pandas as pd
import requests
import json
import cv2

# Replace with your API key and endpoint
api_key = "e4a92ac014b24410b5534a5dd0686236"
api_endpoint = "https://api.spoonacular.com/food/search.json"

#  Define a function to find calories based on food name or image
def find_calories(query):
    params = {
        "apiKey": api_key,
        "query": query,
    }

    response = requests.get(api_endpoint, params=params)
    data = json.loads(response.text)

    if "results" in data and data["results"]:
        # Process results from API
        results = data["results"]
        # You can extract calorie information from the results
        calorie_info = [result["title"], result["calories"]]
        return calorie_info
    else:
        # If no results from API, check local database (optional)
        result = food_data[food_data["food_name"].str.contains(query, case=False)]
        if result.empty:
            return "No data found for that food."
        else:
            return result[["food_name", "calories"]]


# Streamlit app
st.title("Calorie_Finder")

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
      # Image upload
uploaded_image = st.file_uploader("Upload a food image")

# Text input for food name
food_name = st.text_input("Enter a food name:")

# Button to trigger the search
if st.button("Find Calories"):
    if uploaded_image:
        # Process the uploaded image (e.g., using a vision API)
        # Replace this with your image processing logic
        query = "image_of_food"
    else:
        query = food_name

    result = find_calories(query)
    st.write(result)  # ... (rest of the API response processing)
