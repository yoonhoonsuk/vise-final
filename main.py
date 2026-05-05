from pathlib import Path

from blender import blend
from loader import load_models

CSV_PATH = Path(__file__).parent / "live_models.csv"


def print_model(m, limit: int | None = None) -> None:
    print(f"\n{m.name}  (total weight: {m.total_weight:.2f}, {len(m.tickers)} tickers)")
    print("-" * 60)
    rows = m.tickers if limit is None else m.tickers[:limit]
    for t in rows:
        print(f"  {t.symbol:<8} {t.weight:>6.2f}")
    if limit is not None and len(m.tickers) > limit:
        print(f"  ... {len(m.tickers) - limit} more")


def main() -> None:
    models = load_models(CSV_PATH)


    print("Available models: teseting")
    for name in models:
        print(f"  - {name}")

    growth = models["Vise Bluechip Growth"]
    value = models["Vise Bluechip Value"]

    proportion = 0.6
    blended = blend(growth, value, proportion)
    print_model(blended)


if __name__ == "__main__":
    main()
