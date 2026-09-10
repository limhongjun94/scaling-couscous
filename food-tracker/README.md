# Food & Beverage Tracker

A personal monthly food and beverage spend tracker, built in the same house style as
`orizuru/petty-cash.html`. One self-contained HTML file — no build step, no server, no account.

Open `food-tracker/index.html` in any browser (double-click it, or host it as a static page).

A hosted copy runs at <https://claude.ai/code/artifact/0f65cd25-a9b5-44b0-a004-d5b8dd1cceba> —
see **Hosted version** below.

## What it does

| Area | Detail |
|---|---|
| Currency | MYR (RM), personal use |
| Entry fields | Date, amount, category, venue/outlet, payment method, with/tag, note, receipt photo |
| Categories | Breakfast, Lunch, Dinner, Coffee, Snacks, Drinks, Groceries, Delivery, Other |
| Payment methods | Cash, Debit card, Credit card, E-wallet, Bank transfer, Other |
| Month view | Month picker across every month that has entries |
| Budget | Per-month budget with a default fallback budget for months you haven't set |
| Metrics | Spent, remaining, % of budget used, daily average, projected month-end, top category |
| Charts | Category donut with legend, daily spend bars with a daily-allowance line |
| Ledger | Grouped by day with day subtotals, plus search / category / method filters |
| Receipts | Photo attached per entry, compressed client-side to ~900 KB, viewable and downloadable |
| Export | Excel (Ledger + Summary + Daily sheets), CSV, and full JSON backup/restore |

## Where the data lives

Everything is in this browser's `localStorage` under three keys:

- `fnb.entries.v1` — the entries
- `fnb.settings.v1` — budgets (per month and default)
- `fnb.receipts.v1` — receipt photos as compressed JPEG data URLs

Nothing is uploaded anywhere. That also means:

- Clearing site data, or using a different browser or device, means starting empty.
- **Use "Backup JSON" regularly.** "Restore" reads that file back.
- Receipt photos are the bulk of the storage. Browsers cap `localStorage` at roughly 5–10 MB, so
  expect a few dozen receipts before it fills. The app warns you when a save fails.

## First run

1. Open the page.
2. Set **Default monthly budget** in the Budget panel (e.g. 1500).
3. Log entries as you go, or click **Load sample month** in the empty ledger to see the layout
   populated — sample rows are labelled in their note and can be deleted individually.

## External dependencies

Two CDN loads, both optional:

- Google Fonts (IBM Plex Sans / Mono) — falls back to system fonts.
- SheetJS from cdnjs, for the Excel export — if it fails to load, the Excel button falls back to CSV.

The app works fully offline apart from those two conveniences.

## Publishing it

`netlify.toml` at the repo root currently publishes `sun-smart/website`. To put this page online
instead, either point `publish` at `food-tracker`, or copy `index.html` into whichever site
directory you're deploying.

## Hosted version

`artifact.html` is the same page published as a claude.ai Artifact:
<https://claude.ai/code/artifact/0f65cd25-a9b5-44b0-a004-d5b8dd1cceba>

It is derived from `index.html` — edit `index.html`, then:

```bash
python3 food-tracker/build_artifact.py   # regenerates artifact.html
```

Republish `artifact.html` to the same URL to update the live page.

When the page runs there, three runtime capabilities light up. Opened as a local file they
stay dormant and the page behaves exactly as described above.

| Capability | What it does |
|---|---|
| `db` | Entries and budgets sync across every device you sign in from, live |
| `assets` | Receipt photos upload to the artifact's storage instead of localStorage |
| `downloads` | Excel / CSV / backup files go through the viewer's save prompt |

The page always writes to localStorage as well, so it keeps working when sync is unavailable —
the pill beside the month picker shows which mode you're in. If a browser holds entries that
aren't in the cloud yet, an "Upload N local entries" button appears next to it.

Cloud limits: 5,000 entries per artifact, and the ledger subscribes to the most recent 1,000.
