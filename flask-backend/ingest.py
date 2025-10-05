#!/usr/bin/env python3
"""
Ingest utilities for the backend.

What it does (today):
- build_cca25("chicago"): merge datasets/CCA_25_chi_csv.csv (attributes)
  with datasets/<community-areas-geojson> (polygons), write:
    datasets/processed/chicago_cca25.geojson

Usage:
  cd flask-backend
  python3 ingest.py cca25 chicago
"""

from pathlib import Path
import json
import sys
import pandas as pd

# ---------- Paths ----------
BACKEND = Path(__file__).resolve().parent       # /repo/flask-backend
ROOT = BACKEND.parent                           # /repo
DATASETS = ROOT / "datasets"
PROCESSED = DATASETS / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

# Filenames we look for
CCA_CSV = DATASETS / "CCA_25_chi_csv.csv"

# We try these candidate filenames for community areas polygons:
CA_CANDIDATES = [
    DATASETS / "chicago_community_areas.geojson",
    DATASETS / "Boundaries_-_Community_Areas.geojson",
    DATASETS / "Boundaries_-_Community_Areas_20251005.geojson",  # what your teammate uploaded
    # add more aliases as needed
]

# ---------- Helpers ----------
def _log(msg: str):
    print(msg, flush=True)

def _fail(msg: str):
    raise RuntimeError(msg)

def load_cca25_csv() -> pd.DataFrame:
    """
    Load the CCA 25 CSV and normalize ID + NAME columns.
    Expected columns commonly found:
        - id:   "GEOID" (1..77)
        - name: "GEOG"  (e.g., "Rogers Park")
    """
    if not CCA_CSV.exists():
        _fail(f"Missing CSV at {CCA_CSV}. Place CCA_25_chi_csv.csv under datasets/")

    _log(f"Reading CCA CSV: {CCA_CSV}")
    df = pd.read_csv(CCA_CSV)

    cols = {c.lower(): c for c in df.columns}

    # ID column (community area numeric id)
    id_col = None
    for k in ("geoid", "area_numbe", "area_num", "ca", "id"):
        if k in cols:
            id_col = cols[k]
            break
    if id_col is None:
        _fail(
            "CCA_25_chi_csv.csv must include a community id column "
            "(e.g., GEOID or area_numbe)."
        )

    # NAME column
    name_col = None
    for k in ("geog", "community", "name"):
        if k in cols:
            name_col = cols[k]
            break
    # Name isn't strictly required to merge, but keeping it is nice
    if name_col is None:
        _log("WARNING: name column not found (expected GEOG/community). Proceeding without name.")

    # Normalize
    df = df.copy()
    df["CA_ID"] = pd.to_numeric(df[id_col], errors="coerce").astype("Int64")
    if name_col:
        df["CA_NAME"] = df[name_col].astype(str)
    else:
        df["CA_NAME"] = None

    if df["CA_ID"].isna().any():
        _log("WARNING: Some CA_ID values are NaN after coercion; those rows will not join.")

    # Make CA_ID plain int where possible (keeps JSON light)
    try:
        df["CA_ID"] = df["CA_ID"].astype(int)
    except Exception:
        pass

    return df

def find_community_areas_geojson() -> Path:
    """
    Pick the first existing community area GeoJSON from candidates.
    """
    for p in CA_CANDIDATES:
        if p.exists():
            return p
    # If not found, try to guess by scanning datasets/ for a likely file
    for p in DATASETS.glob("*.geojson"):
        if "community" in p.name.lower() and "area" in p.name.lower():
            return p
    _fail(
        "Missing polygons. Put the City of Chicago 'Community Areas (current)' GeoJSON "
        "under datasets/ with a name like 'chicago_community_areas.geojson' or "
        "'Boundaries_-_Community_Areas_*.geojson'."
    )

def load_community_areas_geojson() -> dict:
    gj_path = find_community_areas_geojson()
    _log(f"Reading Community Areas GeoJSON: {gj_path}")
    try:
        return json.loads(gj_path.read_text())
    except Exception as e:
        _fail(f"Failed reading {gj_path}: {e}")

def _extract_ca_id_name(props: dict) -> tuple[int | None, str | None]:
    """
    Try common property names for community area id & name in the City GeoJSON.
    Typical keys:
      - id:   'area_numbe' (string) or 'area_num' or 'area_num_1'
      - name: 'community' (string)
    """
    # ID
    id_keys = ["area_numbe", "area_num", "area_num_1", "ca", "geoid"]
    ca_id = None
    for k in id_keys:
        if k in props and props[k] is not None:
            try:
                ca_id = int(str(props[k]).strip())
                break
            except Exception:
                continue

    # NAME
    name_keys = ["community", "name", "geog", "pri_neigh", "sec_neigh"]
    ca_name = None
    for k in name_keys:
        if k in props and props[k]:
            ca_name = str(props[k]).strip()
            break

    return ca_id, ca_name

def merge_cca_with_polygons(geojson: dict, cca: pd.DataFrame) -> dict:
    """
    Left-join polygons (community areas) with CCA attributes on CA_ID.
    """
    cca_ix = cca.set_index("CA_ID").to_dict(orient="index")
    out_feats = []

    feats = geojson.get("features", [])
    if not feats:
        _fail("Community Areas GeoJSON has no features.")

    missing = 0
    for f in feats:
        props = f.get("properties", {}) or {}
        ca_id, ca_name = _extract_ca_id_name(props)

        attach = {}
        if ca_id is not None and ca_id in cca_ix:
            attach = cca_ix[ca_id]
        else:
            missing += 1

        # Preserve original props and add normalized CA_ID/CA_NAME and CCA attrs
        merged_props = {**props, "CA_ID": ca_id, "CA_NAME": ca_name, **attach}
        out_feats.append({
            "type": "Feature",
            "geometry": f.get("geometry"),
            "properties": merged_props
        })

    if missing:
        _log(f"NOTE: {missing} polygons had no matching CCA row (by CA_ID).")

    return {"type": "FeatureCollection", "features": out_feats}

def build_cca25(city: str) -> Path:
    """
    Build the merged CCA 25 GeoJSON for a given city.
    Currently supports 'chicago' only (expects Chicago community areas).
    """
    city = (city or "").strip().lower()
    if city != "chicago":
        _fail("build_cca25 currently supports 'chicago' only.")

    cca = load_cca25_csv()
    gj = load_community_areas_geojson()
    merged = merge_cca_with_polygons(gj, cca)

    out = PROCESSED / f"{city}_cca25.geojson"
    out.write_text(json.dumps(merged))
    _log(f"Wrote {out} with {len(merged.get('features', []))} features")
    return out

# ---------- CLI ----------
def _cli():
    if len(sys.argv) < 3:
        print(
            "Usage:\n"
            "  python3 ingest.py cca25 chicago\n",
            file=sys.stderr
        )
        sys.exit(2)

    cmd = sys.argv[1].lower()
    arg = sys.argv[2].lower()

    if cmd == "cca25":
        build_cca25(arg)
    else:
        _fail(f"Unknown command '{cmd}'. Try: cca25")

if __name__ == "__main__":
    _cli()
