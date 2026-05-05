import csv
from pathlib import Path

from models import LiveModel, Ticker


def load_models(csv_path: str | Path) -> dict[str, LiveModel]:
    models: dict[str, LiveModel] = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["model_name"].strip()
            symbol = row["ticker"].strip()
            weight = float(row["weight"])
            if name not in models:
                models[name] = LiveModel(name=name)
            models[name].tickers.append(Ticker(symbol=symbol, weight=weight))
    return models
