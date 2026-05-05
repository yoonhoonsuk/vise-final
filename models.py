from dataclasses import dataclass, field


@dataclass(frozen=True)
class Ticker:
    symbol: str
    weight: float


@dataclass
class LiveModel:
    name: str
    tickers: list[Ticker] = field(default_factory=list)

    def weight_for(self, symbol: str) -> float:
        for t in self.tickers:
            if t.symbol == symbol:
                return t.weight
        return 0.0

    def symbols(self) -> set[str]:
        return {t.symbol for t in self.tickers}

    @property
    def total_weight(self) -> float:
        return sum(t.weight for t in self.tickers)

    def as_dict(self) -> dict[str, float]:
        return {t.symbol: t.weight for t in self.tickers}
