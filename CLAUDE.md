# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

A single-script Python tool that generates a daily financial/AI market brief using Claude with live web search, then emails it as formatted HTML via Gmail SMTP. Designed to be run once a day via cron or Task Scheduler.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script (generates brief and sends email)
python market_brief.py

# Verify syntax without running
python -m py_compile market_brief.py

# Watch logs
tail -f market_brief.log
```

There are no automated tests. Manual testing means running `python market_brief.py` with valid credentials in `.env`.

## Configuration

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key with web search tool access |
| `GMAIL_ADDRESS` | Gmail address used as sender |
| `GMAIL_APP_PASSWORD` | 16-character Gmail App Password (requires 2-Step Verification) |
| `RECIPIENTS` | Comma-separated recipient email addresses |
| `LOG_FILE` | Optional log file path (default: `market_brief.log`) |

## Architecture

The entire application is `market_brief.py` (~212 lines), structured in three sequential phases:

1. **`generate_brief()`** — Calls `client.messages.create()` with the `web_search_20250305` tool enabled. Claude searches for current market data and returns HTML body content (no `<html>`/`<body>` tags). All text blocks from `response.content` are concatenated.

2. **`send_email(html_body)`** — Wraps the HTML fragment in a full email template with inline CSS, creates a `MIMEMultipart("alternative")` message with plain-text fallback, and sends via `smtplib.SMTP_SSL` on port 465.

3. **`main()`** — Validates that all required env vars are set before calling either function. Exits with code 1 on any failure.

### Key constants (top of file)

- `MODEL = "claude-sonnet-4-20250514"` — model used for brief generation
- `SYSTEM_PROMPT` — defines the economist persona and 7-section HTML output format
- `USER_PROMPT_TEMPLATE` — injected with today's date; instructs Claude what to search for

### Anthropic SDK usage

Uses the synchronous `anthropic.Anthropic` client. The web search tool is passed as:
```python
tools=[{"type": "web_search_20250305", "name": "web_search"}]
```
The API key requires a plan that includes web search tool access.
