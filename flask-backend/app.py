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

# # ---------- helpers ----------
# def mock_featurecollection(city: str):
#     city = city.lower()
#     if city == "chicago":
#         feats = [
#             {
#                 "type": "Feature",
#                 "properties": {
#                     "geoid": "CHI_1",
#                     "name": "Mock Zone 1 (Chicago)",
#                     "NO2_mean_molec_cm2": 4.2e15,
#                     "NDVI_mean": 0.12,
#                     "pop_density_per_km2": 5200,
#                     "priority_norm": 0.82
#                 },
#                 "geometry": {"type": "Polygon", "coordinates": [[
#                     [-87.75, 41.84], [-87.68, 41.84], [-87.68, 41.88], [-87.75, 41.88], [-87.75, 41.84]
#                 ]]}
#             },
#             {
#                 "type": "Feature",
#                 "properties": {
#                     "geoid": "CHI_2",
#                     "name": "Mock Zone 2 (Chicago)",
#                     "NO2_mean_molec_cm2": 3.1e15,
#                     "NDVI_mean": 0.28,
#                     "pop_density_per_km2": 3800,
#                     "priority_norm": 0.46
#                 },
#                 "geometry": {"type": "Polygon", "coordinates": [[
#                     [-87.71, 41.86], [-87.64, 41.86], [-87.64, 41.92], [-87.71, 41.92], [-87.71, 41.86]
#                 ]]}
#             }
#         ]
#     else:  # champaign-urbana default
#         feats = [
#             {
#                 "type": "Feature",
#                 "properties": {
#                     "geoid": "C-U_1",
#                     "name": "Mock Zone 1 (C-U)",
#                     "NO2_mean_molec_cm2": 1.8e15,
#                     "NDVI_mean": 0.35,
#                     "pop_density_per_km2": 2100,
#                     "priority_norm": 0.33
#                 },
#                 "geometry": {"type": "Polygon", "coordinates": [[
#                     [-88.30, 40.10], [-88.25, 40.10], [-88.25, 40.14], [-88.30, 40.14], [-88.30, 40.10]
#                 ]]}
#             },
#             {
#                 "type": "Feature",
#                 "properties": {
#                     "geoid": "C-U_2",
#                     "name": "Mock Zone 2 (C-U)",
#                     "NO2_mean_molec_cm2": 2.2e15,
#                     "NDVI_mean": 0.18,
#                     "pop_density_per_km2": 2700,
#                     "priority_norm": 0.57
#                 },
#                 "geometry": {"type": "Polygon", "coordinates": [[
#                     [-88.23, 40.12], [-88.19, 40.12], [-88.19, 40.16], [-88.23, 40.16], [-88.23, 40.12]
#                 ]]}
#             }
#         ]
#     return {"type": "FeatureCollection", "features": feats}

# def load_geojson(city: str, level: str):
#     """
#     Try to serve real processed data first:
#       flask-backend/data/processed/{city}_{level}_stats.geojson
#     else return a mock FeatureCollection.
#     """
#     p = DATA_PROCESSED / f"{city.lower()}_{level.lower()}_stats.geojson"
#     if p.exists():
#         return json.loads(p.read_text())
#     return mock_featurecollection(city)

# def rules_based_suggest(props: dict) -> str:
#     no2 = props.get("NO2_mean_molec_cm2")
#     ndvi = props.get("NDVI_mean")
#     den = props.get("pop_density_per_km2")
#     pri = props.get("priority_norm")

#     findings = []
#     if no2 and no2 > 3.5e15: findings.append("elevated NO₂ exposure")
#     if ndvi is not None and ndvi < 0.2: findings.append("low vegetation cover")
#     if den and den > 4000: findings.append("high population density")

#     recs = []
#     if ndvi is not None and ndvi < 0.2: recs.append("add pocket parks, street trees, or community gardens")
#     if no2 and no2 > 3.5e15: recs.append("prioritize greening near traffic corridors and bus routes")
#     if den and den > 4000: recs.append("focus improvements where many residents will benefit")

#     msg = f"{props.get('name','This area')}: "
#     if findings:
#         msg += "Key issues: " + ", ".join(findings) + ". "
#     if recs:
#         msg += "Consider: " + "; ".join(recs) + ". "
#     msg += "Note: TEMPO is a beta dataset—validate with local sensors or site surveys before decisions."
#     return msg

# # ---------- routes ----------
# @app.get("/health")
# def health(): return {"ok": True}

# @app.get("/layers")
# def layers():
#     return jsonify({
#         "NO2_mean_molec_cm2": {"unit": "molecules/cm^2", "source": "NASA TEMPO (beta)"},
#         "NDVI_mean": {"unit": "unitless [-1..1]", "source": "MODIS/VIIRS"},
#         "pop_density_per_km2": {"unit": "people/km^2", "source": "WorldPop 2020"},
#         "priority_norm": {"unit": "0..1", "source": "derived priority index"}
#     })

# @app.get("/area")
# def area():
#     city = request.args.get("city", "chicago")
#     level = request.args.get("level", "zip")
#     fc = load_geojson(city, level)
#     return Response(json.dumps(fc), mimetype="application/json")

# @app.get("/area/<geoid>")
# def area_detail(geoid):
#     city = request.args.get("city", "chicago")
#     level = request.args.get("level", "zip")
#     fc = load_geojson(city, level)
#     for f in fc["features"]:
#         if f["properties"].get("geoid") == geoid:
#             return jsonify(f["properties"])
#     return jsonify({"error": "not found"}), 404

# @app.get("/suggest")
# def suggest():
#     geoid = request.args.get("geoid")
#     city = request.args.get("city", "chicago")
#     level = request.args.get("level", "zip")
#     if not geoid:
#         return jsonify({"error": "geoid required"}), 400
#     fc = load_geojson(city, level)
#     for f in fc["features"]:
#         if f["properties"].get("geoid") == geoid:
#             return jsonify({"geoid": geoid, "suggestion": rules_based_suggest(f["properties"])})
#     return jsonify({"error": "not found"}), 404

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
