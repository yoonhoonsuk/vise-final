# Vise Model Blender

A small monolithic web app for blending two portfolio models from `live_models.csv` into a new, named portfolio.

## Running

```sh
# install (one-time)
uv sync          # or: .venv/bin/pip install flask

# CLI smoke test
.venv/bin/python main.py

# web app
.venv/bin/python flask_app.py
# open http://127.0.0.1:5000/
```

## Problem

`live_models.csv` contains several Vise model portfolios. Each row is `model_name, ticker, weight`, with weights inside a model summing to ~100. We often want to combine two of these models into a single new portfolio at a chosen mix — for example, "60% Bluechip Growth + 40% Bluechip Value" — and give that combination its own name and version label.

This app provides:

- A loader that turns the CSV into typed model objects.
- A pure blend function that takes two models and a proportion and returns a new model. Tickers shared by both models are merged; tickers unique to one model are scaled down by that model's proportion.
- A web UI to pick the two source models, set a single proportion slider (the other side fills to 100%), give the result a name + instance label, and view the blended ticker table live.

---

TODO / Limitations:

 - .csv intake form has not been created in case people want to input new models.
 - The backend and database is not robust. Thus, new spin up of said app will refresh the memory of the models that has been blended.
 - The blends naming convention is not defined, and users can create two models of the same name.

## Technology

| Layer    | Tech                                                                |
| -------- | ------------------------------------------------------------------- |
| Backend  | Python 3.14, Flask 3                                                |
| Frontend | React 18 + Babel via CDN (no build step), single `index.html` + `app.js` |
| Data     | `live_models.csv` parsed with the Python stdlib `csv` module        |
| Packaging| `pyproject.toml` (managed with `uv`); virtualenv at `.venv/`        |

The structure is intentionally monolithic — the Flask app serves both the JSON API and the static React page from one process, so `python flask_app.py` is the only thing you need to run.

```
vise-final-1/
  live_models.csv
  models.py        # Ticker, LiveModel dataclasses
  loader.py        # CSV -> dict[str, LiveModel]
  blender.py       # blend(a, b, proportion_a) -> LiveModel
  flask_app.py     # JSON API + serves the static page
  main.py          # CLI smoke test
  static/
    index.html     # React via CDN
    app.js         # React component (JSX, transpiled in-browser by Babel)
```

## Models

The domain is captured by two dataclasses in `models.py`:

### `Ticker`

A frozen dataclass representing one position in a portfolio.

| Field    | Type    | Notes                                  |
| -------- | ------- | -------------------------------------- |
| `symbol` | `str`   | Ticker symbol (e.g. `AAPL`, `BRK.B`).  |
| `weight` | `float` | Percentage weight within its model.    |

### `LiveModel`

A named portfolio composed of `Ticker`s.

| Field / method            | Returns          | Notes                                                              |
| ------------------------- | ---------------- | ------------------------------------------------------------------ |
| `name`                    | `str`            | Display name (e.g. `Vise Bluechip Growth`).                        |
| `tickers`                 | `list[Ticker]`   | Positions in the model.                                            |
| `weight_for(symbol)`      | `float`          | Weight of `symbol`, or `0.0` if absent.                            |
| `symbols()`               | `set[str]`       | All ticker symbols in the model.                                   |
| `total_weight` (property) | `float`          | Sum of ticker weights — sanity check, should be ~100.              |
| `as_dict()`               | `dict[str,float]`| `{symbol: weight}` view, used by the blender and JSON serializer.  |

### Source models in `live_models.csv`

| Model                          | Style            | # Tickers | Total Weight |
| ------------------------------ | ---------------- | --------- | ------------ |
| `Vise Bluechip Growth`         | Large-cap growth | 20        | ~100         |
| `Vise Bluechip Value`          | Large-cap value  | 19        | ~100         |
| `Vise Custom Core Completion`  | Diversified core | 28        | ~100         |

### Blending

`blender.blend(a, b, proportion_a, *, name=None) -> LiveModel`

For each symbol in `a.symbols() | b.symbols()`:

```
blended_weight[s] = a.weight_for(s) * proportion_a + b.weight_for(s) * (1 - proportion_a)
```

Symbols with a resulting weight of 0 are dropped, and the output is sorted by weight descending. Properties:

- `blend(a, b, 1.0)` reproduces `a`.
- `blend(a, b, 0.0)` reproduces `b`.
- `blend(a, a, p)` reproduces `a` for any `p`.
- The blended `total_weight` stays ~100 if both inputs do.

The optional `name` overrides the default `"{a.name} (X%) + {b.name} (Y%)"` label — this is what the UI's *New model name* / *Instance name* fields feed into.
