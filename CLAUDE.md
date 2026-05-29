# atlas-trading

Crypto, stocks, and news aggregation service. Part of the Atlas ecosystem.

## Stack

Python 3.12 + FastAPI + Docker. Port 3458.

## Layout

| Path | Purpose |
|------|---------|
| `server.py` | FastAPI app — all routes |
| `src/crypto/` | Binance connector, positions, P&L |
| `src/stocks/` | Stock price feeds, watchlist, portfolio |
| `src/news/` | News aggregation, sentiment tagging |
| `src/api/` | Shared API utilities |
| `data/` | Local JSON state (gitignored) |

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python server.py
```

## API contract

| Endpoint | Purpose |
|----------|---------|
| `GET /api/health` | Container health check |
| `GET /api/widget/summary` | Dashboard card for atlas-core |
| `GET /api/briefing` | Overnight summary for plan-day |
| `GET /api/news/latest` | Recent headlines |

## Environment variables

| Var | Default | Purpose |
|-----|---------|---------|
| `PORT` | `3458` | Listen port |
| `DATA_DIR` | `./data` | Local data directory |
| `BINANCE_SPOT_TEST_API_KEY` | — | Binance testnet key |
| `BINANCE_SPOT_TEST_API_SECRET` | — | Binance testnet secret |

## Build phases

See `plans/todos/atlas-trading.md` in atlas-core for the full roadmap.
Phase 1 (scaffold) is done. Phase 2 (crypto) is next.
