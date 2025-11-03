import json
import os
import yfinance as yf

WATCHLIST_FILE = "watchlist.json"

# --- carregar e guardar lista ---
def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_watchlist(tickers):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(tickers, f)


# --- buscar dados de uma ação ---
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")

        if data.empty:
            return None

        info = stock.info
        last_row = data.iloc[-1]

        return {
            "ticker": ticker.upper(),
            "price": round(last_row["Close"], 2),
            "change": round(last_row["Close"] - last_row["Open"], 2),
            "change_pct": round(((last_row["Close"] - last_row["Open"]) / last_row["Open"]) * 100, 2),
            "high": round(last_row["High"], 2),
            "low": round(last_row["Low"], 2),
            "volume": int(last_row["Volume"]),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "dividend_yield": info.get("dividendYield"),
            "sector": info.get("sector"),
        }

    except Exception as e:
        print(f"Erro ao buscar dados de {ticker}: {e}")
        return None
