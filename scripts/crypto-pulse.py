#!/usr/bin/env python3
"""
crypto-pulse.py
Fetches live prices for BTC, SOL, and CLANKER from CoinGecko (free API, no key needed).
Outputs a single clean line for injection into meet-puneet skill context.
"""

import urllib.request
import urllib.error
import json
import sys

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,solana,clanker"
    "&vs_currencies=usd"
    "&include_24hr_change=true"
)

FALLBACK = "🪙 Live prices unavailable right now — check back in a moment."


def format_price(price: float) -> str:
    if price >= 1000:
        return f"${price:,.0f}"
    elif price >= 1:
        return f"${price:,.2f}"
    else:
        return f"${price:.6f}"


def format_token(name: str, price: float, change) -> str:
    parts = [name, format_price(price)]
    if change is not None:
        arrow = "↑" if change >= 0 else "↓"
        parts.append(f"{arrow}{abs(change):.1f}%")
    return " ".join(parts)


def fetch_prices() -> str:
    try:
        req = urllib.request.Request(
            COINGECKO_URL,
            headers={"User-Agent": "meet-puneet-skill/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

        btc_price   = data["bitcoin"]["usd"]
        btc_change  = data["bitcoin"]["usd_24h_change"]
        sol_price   = data["solana"]["usd"]
        sol_change  = data["solana"]["usd_24h_change"]
        clnk_price  = data["clanker"]["usd"]
        clnk_change = data["clanker"]["usd_24h_change"]

        tokens = " | ".join([
            format_token("BTC", btc_price, btc_change),
            format_token("SOL", sol_price, sol_change),
            format_token("CLANKER", clnk_price, clnk_change),
        ])
        return f"🪙 Live: {tokens}"

    except (urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError):
        return FALLBACK


if __name__ == "__main__":
    print(fetch_prices())
