
"""
binance_testnet_bootstrap.py
Minimal bootstrap for Binance Spot Testnet using the official binance-connector.
- Creates a Spot Testnet client
- Pings API and fetches server time
- Sends a TEST order (validated but not executed)

Requirements:
  pip install binance-connector

Environment variables (set before running):
  BINANCE_SPOT_TEST_API_KEY
  BINANCE_SPOT_TEST_API_SECRET

Usage:
  python binance_testnet_bootstrap.py
"""
import os
import json
import logging
from typing import Optional, Dict, Any

# You need the official connector installed:
#   pip install binance-connector
try:
    from binance.spot import Spot as SpotClient
except Exception as e:
    raise SystemExit(
        "Missing dependency 'binance-connector'. Install with: pip install binance-connector\n"
        f"Import error: {e}"
    )

BINANCE_SPOT_TESTNET_BASE = "https://testnet.binance.vision"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("binance-testnet")


def init_spot_testnet_client(
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    timeout: Optional[int] = 10,
    show_limit_usage: bool = True,
) -> SpotClient:
    """Return an authenticated Spot client configured for the Binance Spot Testnet.

    Reads keys from env if not provided:
      BINANCE_SPOT_TEST_API_KEY, BINANCE_SPOT_TEST_API_SECRET
    """
    api_key = api_key or os.getenv("BINANCE_SPOT_TEST_API_KEY") or os.getenv("BINANCE_API_KEY_TEST")
    api_secret = api_secret or os.getenv("BINANCE_SPOT_TEST_API_SECRET") or os.getenv("BINANCE_API_SECRET_TEST")

    if not api_key or not api_secret:
        raise SystemExit(
            "API keys not found. Set BINANCE_SPOT_TEST_API_KEY and BINANCE_SPOT_TEST_API_SECRET."
        )

    client = SpotClient(
        api_key=api_key,
        api_secret=api_secret,
        base_url=BINANCE_SPOT_TESTNET_BASE,
        timeout=timeout,
        show_limit_usage=show_limit_usage,
    )
    return client


def ping_and_time(client: SpotClient) -> Dict[str, Any]:
    """Check connectivity and return server time payload."""
    ping_resp = client.ping()  # {} if OK
    time_resp = client.time()  # {'serverTime': ...} (wrapped with headers if show_limit_usage=True)
    return {"ping": ping_resp, "time": time_resp}


def send_test_order(
    client: SpotClient,
    symbol: str = "BTCUSDT",
    side: str = "BUY",
    type_: str = "MARKET",
    quote_order_qty: Optional[float] = 50.0,
    quantity: Optional[float] = None,
    **extra,
) -> Dict[str, Any]:
    """Validate an order via the TEST endpoint (no execution on the engine).

    For MARKET orders you must provide either `quantity` (base asset) or `quoteOrderQty` (quote asset).
    """
    params = {"symbol": symbol, "side": side, "type": type_}
    if quantity is not None:
        params["quantity"] = quantity
    elif quote_order_qty is not None:
        # API naming uses camelCase
        params["quoteOrderQty"] = quote_order_qty
    params.update(extra)
    # This calls POST /api/v3/order/test
    resp = client.new_order_test(**params)
    return resp  # Empty JSON {} on success


if __name__ == "__main__":
    try:
        client = init_spot_testnet_client()
        info = ping_and_time(client)
        log.info("Ping/Time: %s", json.dumps(info, ensure_ascii=False))

        test = send_test_order(client, symbol="BTCUSDT", side="BUY", type_="MARKET", quote_order_qty=25.0)
        log.info("TEST order response: %s", json.dumps(test, ensure_ascii=False))
        log.info("All good. You're connected to Binance Spot Testnet.")
    except Exception as exc:
        log.error("Setup or call failed: %s", exc)
        raise
