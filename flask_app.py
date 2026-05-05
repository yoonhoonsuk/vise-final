from pathlib import Path

from flask import Flask, jsonify, request

from blender import blend
from loader import load_models
from models import LiveModel

ROOT = Path(__file__).parent
CSV_PATH = ROOT / "live_models.csv"

app = Flask(__name__, static_folder=str(ROOT / "static"), static_url_path="")

MODELS: dict[str, LiveModel] = load_models(CSV_PATH)


def model_to_json(m: LiveModel) -> dict:
    return {
        "name": m.name,
        "total_weight": round(m.total_weight, 4),
        "tickers": [{"symbol": t.symbol, "weight": t.weight} for t in m.tickers],
    }


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/models")
def list_models():
    return jsonify([model_to_json(m) for m in MODELS.values()])


@app.post("/api/blend")
def blend_models():
    data = request.get_json(force=True)
    name_a = data["model_a"]
    name_b = data["model_b"]
    proportion_a = float(data["proportion_a"])
    model_name = (data.get("model_name") or "").strip()
    instance_name = (data.get("instance_name") or "").strip()

    if name_a not in MODELS:
        return jsonify({"error": f"unknown model: {name_a}"}), 400
    if name_b not in MODELS:
        return jsonify({"error": f"unknown model: {name_b}"}), 400

    if model_name and instance_name:
        result_name = f"{model_name} — {instance_name}"
    elif model_name or instance_name:
        result_name = model_name or instance_name
    else:
        result_name = None

    result = blend(MODELS[name_a], MODELS[name_b], proportion_a, name=result_name)
    MODELS[result.name] = result
    return jsonify({
        **model_to_json(result),
        "model_name": model_name,
        "instance_name": instance_name,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
