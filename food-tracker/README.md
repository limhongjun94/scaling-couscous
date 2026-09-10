# Food & Beverage Tracker

A personal monthly food and beverage spend tracker, built in the same house style as
`orizuru/petty-cash.html`. One self-contained HTML file — no build step, no server, no account.

Open `food-tracker/index.html` in any browser (double-click it, or host it as a static page).

Two hosted copies exist — see **Publishing** below:

| Copy | Link |
|---|---|
| GitHub Pages | `https://hj-ai-hub.github.io/scaling-couscous/food-tracker/` |
| claude.ai Artifact | <https://claude.ai/code/artifact/0f65cd25-a9b5-44b0-a004-d5b8dd1cceba> |

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
| Sharing | "Share this month" builds a link that carries that month's entries; whoever opens it sees a read-only copy |

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

## Sharing a month

Every device keeps its own ledger — there is no server and no shared database. To let someone
see your month, click **Share this month**. The entries for the selected month are packed into a
compact form, deflate-compressed, and encoded into the link's `#` fragment. A typical month runs
under 2 KB, small enough to send in any messaging app.

Whoever opens that link gets a read-only copy of the month: the same dashboard, charts and
ledger, with the entry form, budget panel and delete buttons removed. Their own tracker is
untouched — the shared view never writes to their browser, and **Open my own tracker** returns
them to it. Send a fresh link whenever you want them to see newer entries; the old one keeps
showing the month as it was when you sent it.

What a shared link does *not* carry: receipt photos (far too large for a URL), other months, and
any way to edit your ledger. Anyone holding the link can read that month, so treat it like a
forwarded screenshot.

## Publishing

`index.html` is the only file to edit. Both published copies are generated from it:

```bash
python3 food-tracker/build.py
```

| Output | Purpose |
|---|---|
| `docs/food-tracker/index.html` | verbatim copy; GitHub Pages serves `docs/` on `main` |
| `food-tracker/artifact.html` | the page body, with the document wrapper the Artifact host supplies |

The Pages copy goes live once the change is merged to `main` — the same arrangement as
`docs/orizuru-petty-cash/`. Republish `artifact.html` to its existing URL to update the Artifact.

The Artifact copy declares one runtime capability, `downloads`, so the export buttons can hand
files to the viewer's save prompt. Everywhere else the exports fall back to an ordinary browser
download. There is no cloud storage of any kind: on every host, entries live in that browser.
