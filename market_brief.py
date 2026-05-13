#!/usr/bin/env python3
"""
Daily Market & AI Brief — Automated Morning Email

Pulls live market news via web search, compiles a professional brief
using Claude, and emails it to your recipients every morning.

Setup:
1. pip install anthropic requests python-dotenv
2. Copy .env.example to .env and fill in your credentials
3. Run manually:  python market_brief.py
4. Schedule:      See README.md for cron / Task Scheduler instructions
"""

import os
import sys
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

try:
    import anthropic
except ImportError:
    print("ERROR: 'anthropic' package not found. Run: pip install anthropic")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

load_dotenv()

ANTHROPIC_API_KEY  = os.getenv("ANTHROPIC_API_KEY", "")
GMAIL_ADDRESS      = os.getenv("GMAIL_ADDRESS", "")           # your-email@gmail.com
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")      # 16-char app password
RECIPIENTS         = os.getenv("RECIPIENTS", "ngkailing03@gmail.com")  # comma-separated

LOG_FILE = os.getenv("LOG_FILE", "market_brief.log")
MODEL    = "claude-sonnet-4-20250514"

# ─────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Step 1: Use Claude with web search to gather and write the brief
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior economist and financial market analyst with 20+ years of experience.
Your job is to produce a concise, actionable morning market brief.

Structure the brief in HTML format with these sections:

1. **Market Snapshot** — Major index closes (S&P 500, Nasdaq, Dow, key Asian/European indices), key movers.
2. **Macro & Geopolitics** — Central bank moves, inflation data, geopolitical risks, summits, sanctions.
3. **Commodities & Energy** — Oil (Brent & WTI), gold, copper, uranium, agricultural commodities if relevant.
4. **AI & Tech Sector** — Major AI developments, chip stocks, IPOs, earnings, infrastructure deals.
5. **Investment Ideas** — 2-3 actionable thematic ideas with tickers where relevant.
6. **Key Watchlist Table** — HTML table with Ticker/Asset, Level, Trend, Significance.
7. **What to Watch Today** — 3-4 catalysts for the trading day ahead.

Rules:
- Be data-driven: include specific numbers, prices, percentages.
- Keep it scannable: bullet points, bold key figures.
- Total length: 800-1200 words.
- Output ONLY the HTML body content (no <html>, <head>, <body> tags).
- Add a footer: "Prepared by Claude AI • For informational purposes only • Not financial advice"
- Use web search to get the LATEST data. Today's date matters — search for current prices and news.
"""

USER_PROMPT_TEMPLATE = """Today is {date}.

Search for and compile the morning market brief. Use web search to find:

1. Yesterday's closing prices for S&P 500, Nasdaq, Dow Jones, and any notable Asian/European moves overnight
2. Latest oil prices (Brent and WTI)
3. Any major macro data releases (CPI, jobs, GDP, Fed decisions)
4. Top AI and technology news
5. Key geopolitical developments affecting markets
6. Notable earnings or IPOs this week
7. Gold, Bitcoin, bond yields

Compile everything into the formatted brief. Make it sharp and actionable."""


def generate_brief() -> str:
    """Call Claude API with web search to generate the market brief."""
    log.info("Calling Claude API with web search enabled...")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    today = datetime.now().strftime("%A, %B %d, %Y")
    user_prompt = USER_PROMPT_TEMPLATE.format(date=today)

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": user_prompt}],
    )

    html_parts = []
    for block in response.content:
        if block.type == "text":
            html_parts.append(block.text)

    html_body = "\n".join(html_parts)

    if not html_body.strip():
        raise RuntimeError("Claude returned an empty brief.")

    log.info("Brief generated successfully (%d characters).", len(html_body))
    return html_body


# ─────────────────────────────────────────────────────────────
# Step 2: Send the email via Gmail SMTP
# ─────────────────────────────────────────────────────────────

def send_email(html_body: str) -> None:
    """Send the brief as an HTML email via Gmail SMTP."""
    today = datetime.now().strftime("%A, %B %d, %Y")
    subject = f"Global Market & AI Brief — {today}"

    recipient_list = [r.strip() for r in RECIPIENTS.split(",") if r.strip()]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = ", ".join(recipient_list)

    plain = "Your daily market brief is ready. Please view in an HTML-capable email client."
    msg.attach(MIMEText(plain, "plain"))

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body  {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1a1a1a; max-width: 700px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
  h2   {{ color: #0d3b66; border-bottom: 2px solid #0d3b66; padding-bottom: 6px; }}
  h3   {{ color: #1a5276; margin-top: 24px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
  th   {{ background: #0d3b66; color: white; padding: 10px 12px; text-align: left; }}
  td   {{ padding: 8px 12px; border-bottom: 1px solid #ddd; }}
  tr:nth-child(even) {{ background: #f4f8fb; }}
  strong {{ color: #0d3b66; }}
  .footer {{ color: #888; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 10px; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    msg.attach(MIMEText(full_html, "html"))

    log.info("Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, recipient_list, msg.as_string())

    log.info("Email sent to: %s", ", ".join(recipient_list))


# ─────────────────────────────────────────────────────────────
# Step 3: Main
# ─────────────────────────────────────────────────────────────

def main():
    log.info("=" * 60)
    log.info("Daily Market Brief — %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("=" * 60)

    missing = []
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not GMAIL_ADDRESS:
        missing.append("GMAIL_ADDRESS")
    if not GMAIL_APP_PASSWORD:
        missing.append("GMAIL_APP_PASSWORD")

    if missing:
        log.error("Missing env vars: %s — see .env.example", ", ".join(missing))
        sys.exit(1)

    try:
        html_body = generate_brief()
        send_email(html_body)
        log.info("SUCCESS — Brief sent.")
    except Exception as e:
        log.exception("FAILED — %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
