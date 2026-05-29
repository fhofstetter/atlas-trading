"""atlas-trading — crypto, stocks, news service."""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

PORT = int(os.getenv("PORT", "3458"))
DATA_DIR = os.getenv("DATA_DIR", "./data")

app = FastAPI(title="atlas-trading", docs_url=None, redoc_url=None)


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "atlas-trading", "port": PORT}


# ── Widget contract ───────────────────────────────────────────────────────────

@app.get("/api/widget/summary")
def widget_summary():
    """Dashboard card consumed by atlas-core overview."""
    return {
        "service": "atlas-trading",
        "title": "Trading",
        "status": "ok",
        "lines": [
            "Crypto: Binance testnet connected",
            "Stocks: not configured yet",
            "News: not configured yet",
        ],
        "actions": [
            {"label": "Portfolio", "url": f"http://localhost:{PORT}/portfolio"},
        ],
    }


# ── Briefing (consumed by atlas-core plan-day) ────────────────────────────────

@app.get("/api/briefing")
def briefing():
    """Overnight market summary for the morning briefing."""
    return {
        "summary": "No market data configured yet.",
        "movers": [],
        "news": [],
    }


# ── Crypto ────────────────────────────────────────────────────────────────────

@app.get("/api/crypto/status")
def crypto_status():
    return {"connected": False, "note": "Binance integration pending — see src/crypto/"}


# ── Stocks ────────────────────────────────────────────────────────────────────

@app.get("/api/stocks/status")
def stocks_status():
    return {"connected": False, "note": "Stocks provider not configured — see Phase 3 todos"}


# ── News ─────────────────────────────────────────────────────────────────────

@app.get("/api/news/latest")
def news_latest():
    return {"items": [], "note": "News aggregation not configured — see Phase 4 todos"}


# ── Entry ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"atlas-trading running on port {PORT}")
    print(f"DATA_DIR: {DATA_DIR}")
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=False)
