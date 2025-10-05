# flask-backend/app.py
from urllib import response
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from pathlib import Path
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import 'leaflet/dist/leaflet.css';

BASE = Path(__file__).resolve().parent
load_dotenv()

BASE = Path(__file__).resolve().parent
DATA_PROCESSED = BASE / "data" / "processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

client = OpenAI()

app = Flask(
    __name__,
    template_folder=str(BASE / "templates"),
    static_folder=str(BASE / "static"),
    static_url_path="/static",
)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.get("/")
def home():
    # optional simple page
    if (BASE / "templates" / "index.html").exists():
        return render_template("index.html")
    return jsonify({"message": "Backend running. Try /area?city=chicago&level=zip"})

@app.post("/chat")
def chat():
    # Parse JSON body
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    neighborhood = data.get("neighborhood", "Avondale")
    aqi = data.get("aqi", 120)
    stores = data.get("stores", 1)
    cover = data.get("cover", 23)
    prompt = f"""
    You are an advisor to a city planner that takes in data about a neighborhood in Chicago 
    to give suggestions on what needs to be improved in the area, 
    whether or not it is suitable for new residential development, 
    and give reasons to your decision. Limit your response to 200 words.
    
    We have the following information about the {neighborhood}: This neighborhood has a historical AQI of {aqi}. This neighborhood has {stores} grocery stores within 2 miles. This neighborhood has {cover}% canopy cover.
    """

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )
    #gives prompt to Ai
    print(response.output_text)
    
    return jsonify({"message": "ran chat", "response": response.output_text})

@app.get("/pollutiondata")
def pollution_data():
    EPA_EMAIL = os.getenv("EPA_API_EMAIL")
    EPA_KEY = os.getenv("EPA_API_KEY")

    url = "https://aqs.epa.gov/data/api/dailyData/byCounty"
    params = {
        "email": EPA_EMAIL,
        "key": EPA_KEY,
        "param": "88101",      # Ozone
        "bdate": "20160101",   # Start date
        "edate": "20160229",   # End date
        "state": "17",         # Illinois
        "county": "031"        # Cook County
    }
    
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}

if __name__ == "__main__":
    # Use the same interpreter you installed Flask with
    app.run(host="0.0.0.0", port=5500, debug=True)

