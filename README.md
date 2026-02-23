# ◎ SolScope

**Automated Solana wallet intelligence. Discover and track the top-performing traders on Solana in real time — powered by GMGN smart money data.**

---

## What it does

SolScope automatically finds the best-performing wallets on Solana by pulling from GMGN's smart money leaderboards and trending token data. No manual wallet hunting. Just hit **Auto-Discover** and get a ranked table of elite traders with their stats.

Every wallet shows:
- **Realized PnL** — how much they've actually made
- **Win Rate** — percentage of trades that were profitable
- **Avg Hold Time** — are they a flipper or a swing trader?
- **Trade Count** — how active they are
- **One-click GMGN link** — open any wallet on GMGN instantly

---

## Features

- 🔍 **Auto-discovery** — pulls top 200 wallets from 6 GMGN leaderboards (1d/7d/30d PnL + WinRate) plus trending token buyers
- 📊 **Real stats** — PnL, win rate, hold time, trade count all pre-computed by GMGN
- 🎯 **Min/max filters** — filter by any combination of PnL, win rate, hold time, and trades
- 🏷️ **Auto-tagging** — whales, smart money, and bots are automatically labeled
- 🔗 **GMGN deep links** — one click opens any wallet on gmgn.ai
- 💾 **Persistent storage** — wallets saved in your browser across sessions
- ⚡ **Live updates** — table populates in real time as wallets are discovered

---

## Sources

| Source | What it pulls |
|---|---|
| GMGN 1d/7d/30d PnL Leaderboard | Top 200 wallets by realized profit |
| GMGN 1d/7d/30d WinRate Leaderboard | Top 200 wallets by win rate |
| GMGN Trending Token Buyers | Active traders on the hottest tokens right now |

---

## How it works

GMGN provides pre-computed wallet stats (PnL, win rate, hold time) via their leaderboard API. SolScope fetches these through a lightweight Python proxy that handles CORS, then renders everything in a clean dashboard.

```
Browser → Flask proxy (server.py) → GMGN API → back to browser
```

---

## Deploy your own (free)

1. Fork or upload this repo to your GitHub
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select this repo — Railway auto-detects Python and deploys
4. After ~2 min: **Settings → Networking → Generate Domain**
5. Share your link

Railway's free tier costs ~$0.50–1.00/month, well within the $5/month free credit.

---

## Run locally

```bash
pip install flask gunicorn
python3 server.py
# open http://localhost:8080
```

---

## Updating

Edit `wallet-tracker.html` directly on GitHub (pencil icon → save). Railway auto-redeploys in ~60 seconds.

---

## Stack

- **Frontend** — vanilla HTML/CSS/JS
- **Backend** — Python + Flask (CORS proxy)
- **Data** — [GMGN.ai](https://gmgn.ai) smart money API (free, no key required)
- **Hosting** — [Railway](https://railway.app)
