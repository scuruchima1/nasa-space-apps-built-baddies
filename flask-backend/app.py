# flask-backend/app.py
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from pathlib import Path
import os, json
from dotenv import load_dotenv
from openai import OpenAI
import requests

# ---------- Paths ----------
BASE = Path(__file__).resolve().parent          # /repo/flask-backend
ROOT = BASE.parent                              # /repo
DATASETS = ROOT / "datasets"
DATA_PROCESSED = DATASETS / "processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# ---------- Env ----------
# Put your .env in flask-backend/.env with OPENAI_API_KEY, etc.
load_dotenv(BASE / ".env")

# ---------- OpenAI ----------
client = OpenAI()

# ---------- App ----------
app = Flask(
    __name__,
    template_folder=str(BASE / "templates"),
    static_folder=str(BASE / "static"),
    static_url_path="/static",
)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------- Helpers ----------
def _read_geojson(path: Path) -> Response:
    if not path.exists():
        empty = {"type": "FeatureCollection", "features": []}
        return Response(json.dumps(empty), mimetype="application/geo+json")
    return Response(path.read_text(), mimetype="application/geo+json")

# ---------- Routes ----------
@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.get("/")
def home():
    if (BASE / "templates" / "index.html").exists():
        return render_template("index.html")
    return jsonify({"message": "Backend running. Try /cca25?city=chicago or POST /chat"})

# ---- Data layers (served as GeoJSON) ----
@app.get("/cca25")
def cca25():
    city = (request.args.get("city") or "chicago").lower()
    p = DATA_PROCESSED / f"{city}_cca25.geojson"
    return _read_geojson(p)

@app.get("/food_access")
def food_access():
    city = (request.args.get("city") or "chicago").lower()
    p = DATA_PROCESSED / f"{city}_food_access.geojson"
    return _read_geojson(p)

# ---- AI suggestion endpoint ----
@app.post("/chat")
def chat():
    # Expect JSON body: { neighborhood, aqi, stores, cover }
    data = request.get_json(silent=True) or {}
    neighborhood = data.get("neighborhood", "Avondale")
    aqi = data.get("aqi", 120)          # historical AQI
    stores = data.get("stores", 1)      # grocery stores within 2 miles
    cover = data.get("cover", 23)       # % tree canopy cover

    prompt = f"""
    You are an advisor to a city planner. Using the metrics provided, decide whether
    the neighborhood is suitable for new residential development, what to improve,
    and why. Keep it under 200 words. Be specific and action-oriented.

    Neighborhood: {neighborhood}
    Historical AQI: {aqi}
    Grocery stores within 2 miles: {stores}
    Tree canopy cover (%): {cover}

    Return 3 short sections:
    - Suitability (Yes/No + one-sentence reason)
    - Key issues
    - Recommended actions (bulleted)
    """

    try:
        rsp = client.responses.create(model=os.getenv("OPENAI_MODEL", "gpt-5"), input=prompt)
        return jsonify({"message": "ran chat", "response": rsp.output_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---- Optional EPA AQS sample ----
@app.get("/pollutiondata")
def pollution_data():
    # 88101 = PM2.5 FRM/FEM mass  | 44201 = Ozone
    EPA_EMAIL = os.getenv("EPA_API_EMAIL")
    EPA_KEY = os.getenv("EPA_API_KEY")
    if not EPA_EMAIL or not EPA_KEY:
        return jsonify({"error": "Set EPA_API_EMAIL and EPA_API_KEY in .env"}), 400

    url = "https://aqs.epa.gov/data/api/dailyData/byCounty"
    params = {
        "email": EPA_EMAIL,
        "key": EPA_KEY,
        "param": "88101",
        "bdate": "20160101",
        "edate": "20160229",
        "state": "17",   # Illinois
        "county": "031"  # Cook County
    }
    r = requests.get(url, params=params, timeout=30)
    return jsonify(r.json()), r.status_code

# --- list community areas (id + name) ---
@app.get("/cca25/names")
def cca25_names():
    city = (request.args.get("city") or "chicago").lower()
    p = DATA_PROCESSED / f"{city}_cca25.geojson"
    if not p.exists():
        return jsonify([])
    fc = json.loads(p.read_text())
    rows = []
    for f in fc.get("features", []):
        pr = f.get("properties", {}) or {}
        rows.append({
            "id": pr.get("CA_ID") or pr.get("area_numbe") or pr.get("area_num"),
            "name": pr.get("CA_NAME") or pr.get("community") or pr.get("GEOG"),
        })
    # de-dup and sort by name
    uniq = {(r["id"], r["name"]) for r in rows if r["id"] is not None}
    out = [{"id": i, "name": n} for (i, n) in sorted(uniq, key=lambda t: (t[1] or ""))]
    return jsonify(out)

# --- fetch one area’s properties by id ---
@app.get("/cca25/area")
def cca25_area():
    city = (request.args.get("city") or "chicago").lower()
    ca_id = request.args.get("id")
    if not ca_id:
        return jsonify({"error": "missing ?id=<CA_ID>"}), 400

    p = DATA_PROCESSED / f"{city}_cca25.geojson"
    if not p.exists():
        return jsonify({"error": "dataset missing"}), 404
    fc = json.loads(p.read_text())
    for f in fc.get("features", []):
        pr = f.get("properties", {}) or {}
        pid = pr.get("CA_ID") or pr.get("area_numbe") or pr.get("area_num")
        # accept numeric or string id
        if str(pid) == str(ca_id):
            return jsonify(pr)
    return jsonify({"error": "not found"}), 404

# ---------- Main ----------
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5500"))
    app.run(host="0.0.0.0", port=port, debug=True)
