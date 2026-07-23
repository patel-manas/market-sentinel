from datetime import datetime
import pandas as pd
from pydantic import BaseModel, Field
import yfinance as yf


class USMarketSnapshot(BaseModel):
    symbol: str
    name: str
    price: float
    change_pct: float
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class USMarketCollector:
    TICKERS = {
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "^DJI": "Dow Jones",
        "^VIX": "CBOE VIX",
    }

    def fetch(self) -> list[USMarketSnapshot]:
        symbols = list(self.TICKERS.keys())

        # Fetch last 5 days of data for the tickers
        df = yf.download(
            tickers=symbols,
            period="5d",
            interval="1d",
            group_by="ticker",
            progress=False,
        )

        snapshots = []
        for ticker, name in self.TICKERS.items():
            ticker_df = (
                df[ticker].dropna()
                if isinstance(df.columns, pd.MultiIndex)
                else df.dropna()
            )

            closes = ticker_df["Close"]
            latest_price = round(float(closes.iloc[-1]), 2)
            prev_price = round(float(closes.iloc[-2]), 2)

            change_pct = round(
                ((latest_price - prev_price) / prev_price) * 100, 2
            )

            snapshots.append(
                USMarketSnapshot(
                    symbol=ticker,
                    name=name,
                    price=latest_price,
                    change_pct=change_pct,
                )
            )

        return snapshots