from models import LiveModel, Ticker


def blend(
    a: LiveModel,
    b: LiveModel,
    proportion_a: float,
    *,
    name: str | None = None,
) -> LiveModel:
    if not 0.0 <= proportion_a <= 1.0:
        raise ValueError(f"proportion_a must be in [0, 1], got {proportion_a}")

    proportion_b = 1.0 - proportion_a
    a_weights = a.as_dict()
    b_weights = b.as_dict()

    blended: list[Ticker] = []
    for symbol in a_weights.keys() | b_weights.keys():
        w = a_weights.get(symbol, 0.0) * proportion_a + b_weights.get(symbol, 0.0) * proportion_b
        if w > 0:
            blended.append(Ticker(symbol=symbol, weight=w))

    blended.sort(key=lambda t: t.weight, reverse=True)

    if name is None:
        name = f"{a.name} ({proportion_a:.0%}) + {b.name} ({proportion_b:.0%})"

    return LiveModel(name=name, tickers=blended)
