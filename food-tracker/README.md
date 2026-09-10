# Food & Beverage Tracker

A personal monthly food and beverage spend tracker, built in the same house style as
`orizuru/petty-cash.html`. One self-contained HTML file — no build step, no server, no account.

Open `food-tracker/index.html` in any browser (double-click it, or host it as a static page).

Two hosted copies exist — see **Publishing** below:

| Copy | Link | Who can open it |
|---|---|---|
| GitHub Pages | `https://hj-ai-hub.github.io/scaling-couscous/food-tracker/` | anyone with the link |
| claude.ai Artifact | <https://claude.ai/code/artifact/0f65cd25-a9b5-44b0-a004-d5b8dd1cceba> | members of your Claude workspace |

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

## Publishing

`index.html` is the only file to edit. Both published copies are generated from it:

```bash
python3 food-tracker/build.py
```

| Output | Purpose |
|---|---|
| `docs/food-tracker/index.html` | verbatim copy; GitHub Pages serves `docs/` on `main` |
| `food-tracker/artifact.html` | the page body, with the document wrapper the Artifact host supplies |

The Pages copy goes live once the change is merged to `main` — same arrangement as
`docs/orizuru-petty-cash/`. Republish `artifact.html` to its existing URL to update the Artifact.

### Where the data lives, per copy

The page picks a backend at load time and says which one it is in the pill beside the month picker.

| Running as | Entries and budgets | Receipt photos |
|---|---|---|
| Local file | this browser | this browser |
| GitHub Pages, no Firebase config | this browser (each visitor gets their own) | this browser |
| GitHub Pages + Firebase config | one shared ledger, live for everyone with the link | this browser |
| claude.ai Artifact | synced across your devices, workspace members only | artifact storage |

### Turning on the shared ledger (GitHub Pages)

Without this, everyone who opens the Pages link gets a private ledger in their own browser.
To make it one shared ledger with no login:

1. In the [Firebase console](https://console.firebase.google.com), create a project.
2. **Build → Firestore Database → Create database**, location `asia-southeast1` (Singapore).
3. **Project settings → Your apps → Web** — register an app and copy the `firebaseConfig` object.
4. Paste its values into `FIREBASE_CONFIG` at the top of the `<script>` block in `index.html`.
5. Set Firestore rules to:

   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /entries/{id}  { allow read, write: if true; }
       match /settings/{id} { allow read, write: if true; }
     }
   }
   ```

6. Run `python3 food-tracker/build.py`, commit, and merge to `main`.

**Understand what those rules mean:** anyone who has the link — or who reads the config out of the
page source, which is public — can read and edit the ledger. That is the trade for "no login".
It suits a household food budget; do not put anything confidential in it. To lock it down later,
add Firebase Email/Password auth and gate the rules on `request.auth != null`, the same pattern
`templates/jx-assist/JXRR_Project_Documentation.md` documents for JXRR.

Receipt photos stay in each viewer's browser in Firebase mode — sharing those needs Firebase
Storage, which is not wired up.

### claude.ai Artifact capabilities

When the page runs as an Artifact, three runtime capabilities light up. Anywhere else they
stay dormant.

| Capability | What it does |
|---|---|
| `db` | Entries and budgets sync across every device you sign in from, live |
| `assets` | Receipt photos upload to the artifact's storage instead of localStorage |
| `downloads` | Excel / CSV / backup files go through the viewer's save prompt |

The page always writes to localStorage as well, so it keeps working when the shared ledger is
unavailable. If a browser holds entries that aren't in the shared ledger yet, an
"Upload N local entries" button appears next to the month picker.

Artifact storage limits: 5,000 entries, and the ledger subscribes to the most recent 1,000.
The Firestore copy subscribes to the most recent 1,000 entries too.
