# Daily Market & AI Brief

Automated morning email that uses Claude AI with live web search to compile a concise, data-driven global market and AI brief, then sends it to your inbox every day.

## What you get

Each morning the email covers:

- **Market Snapshot** — S&P 500, Nasdaq, Dow, key Asian/European indices
- **Macro & Geopolitics** — Central bank decisions, inflation data, geopolitical risks
- **Commodities & Energy** — Brent/WTI oil, gold, copper and more
- **AI & Tech Sector** — Top AI news, chip stocks, earnings, IPOs
- **Investment Ideas** — 2–3 actionable thematic ideas with tickers
- **Key Watchlist Table** — Ticker, level, trend, significance
- **What to Watch Today** — 3–4 catalysts for the trading day ahead

## Setup

### 1. Prerequisites

- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com/) (requires a plan that includes web search tool access)
- A Gmail account with [2-Step Verification](https://myaccount.google.com/security) enabled

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GMAIL_ADDRESS` | Gmail address used to send the brief |
| `GMAIL_APP_PASSWORD` | 16-character [App Password](https://myaccount.google.com/apppasswords) |
| `RECIPIENTS` | Comma-separated recipient addresses |

### 4. Test it manually

```bash
python market_brief.py
```

You should see log output and receive the email within ~30 seconds.

---

## Scheduling

### Linux / macOS — cron

Run at 7:00 AM every day:

```bash
crontab -e
```

Add:

```
0 7 * * * cd /path/to/scaling-couscous && /usr/bin/python3 market_brief.py >> market_brief.log 2>&1
```

### Windows — Task Scheduler

1. Open **Task Scheduler** → **Create Basic Task**
2. Trigger: **Daily** at your preferred time
3. Action: **Start a program**
   - Program: `C:\Python3x\python.exe`
   - Arguments: `C:\path\to\scaling-couscous\market_brief.py`
   - Start in: `C:\path\to\scaling-couscous`

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Missing env vars` | Check your `.env` file is in the same directory and all values are filled in |
| Gmail auth error | Re-generate your App Password; make sure 2-Step Verification is on |
| Empty brief | Check your Anthropic API key has web search tool access |
| No email received | Check spam folder; verify `RECIPIENTS` is correct |

Logs are written to `market_brief.log` (configurable via `LOG_FILE` in `.env`).
