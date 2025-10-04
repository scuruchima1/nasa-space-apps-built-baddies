# flask-backend/app.py
from urllib import response
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from pathlib import Path
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env") 

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

@app.get("/chat")
def chat():
    response = client.responses.create(
        model="gpt-5",
        input="Write a short bedtime story about a unicorn."
    )
    print(response.output_text)
    
    return jsonify({"message": "ran chat", "response": response.output_text})

if __name__ == "__main__":
    # Use the same interpreter you installed Flask with
    app.run(host="0.0.0.0", port=5500, debug=True)
