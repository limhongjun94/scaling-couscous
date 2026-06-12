# JXRR Rapid Rescue — Project Documentation & Build Reference

> Complete reference for the JXRR website platform, member portal, reviews system, and advertising video production. Keep this file in your templates folder for future reference and handover.

**Company:** JXRR Rapid Rescue — 24-Hour Towing & Roadside Recovery, Malaysia
**Website:** https://www.jxrr.io
**Hotline:** 018-311 9595
**Email:** jx.rapidrescue24hr@gmail.com
**Instagram:** @jxrr_9595
**Hosting:** Netlify (drag-and-drop deploy)
**Main file:** `index.html` (single self-contained file)
**Last updated:** 2026 build session

---

## 1. ARCHITECTURE OVERVIEW

- The entire website is a **single `index.html` file** (static, no server-side code).
- Hosted on **Netlify** via drag-and-drop at https://app.netlify.com/drop
- Backend services powered by **Firebase** (Authentication, Firestore database, Storage).
- All custom platform features (portal, reviews, admin) are embedded directly inside `index.html` as `<script type="module">` blocks using the Firebase v10 modular SDK loaded from CDN.

### Key file locations (on this computer)
| File | Path |
|---|---|
| Live website file | `C:\Users\Richr\OneDrive\Desktop\index.html` |
| Backups | `index.html.bak-before-image-swap` (same folder) |
| Video ad project | `C:\Users\Richr\OneDrive\Desktop\JXRR-AD-PROJECT\` |
| End frame PNG | `JXRR-AD-PROJECT\JXRR-EndFrame-4K.png` |

---

## 2. FIREBASE SETUP

### Project
- **Project name:** jxrr-portal
- **Console:** https://console.firebase.google.com → project "jxrr-portal"

### Web config (safe to expose — client-side public key)
```js
const firebaseConfig = {
  apiKey: "AIzaSyCaMpF_pnlXFk9z2PiiU1GYoYJMCMfNdEE",
  authDomain: "jxrr-portal.firebaseapp.com",
  projectId: "jxrr-portal",
  storageBucket: "jxrr-portal.firebasestorage.app",
  messagingSenderId: "348405170373",
  appId: "1:348405170373:web:f072f3288bcbb5afbaf0ac"
};
```
Located in `index.html` — search for `firebaseConfig`.

### Services enabled
1. **Authentication** → Email/Password sign-in method enabled
2. **Firestore Database** → location `asia-southeast1` (Singapore)
3. **Storage** → for review photo uploads, location `asia-southeast1`

### Authorized domains (Authentication → Settings → Authorized domains)
Must include every domain the site runs on, or login fails with `auth/unauthorized-domain`:
- `localhost` (default)
- Your Netlify domain (e.g. `your-site.netlify.app`)
- `jxrr.io` and `www.jxrr.io` (when custom domain is connected)

### Firestore Security Rules (CURRENT — working version)
> IMPORTANT: `isAdmin()` checks the user's EMAIL from the auth token (not a Firestore lookup). This avoids a Firestore quirk where `get()` inside rules fails on list queries. To add admins, add their email to the array.

```
rules_version='2';
service cloud.firestore {
  match /databases/{db}/documents {
    function isAdmin() {
      return request.auth != null && request.auth.token.email in [
        "limhongjun94@gmail.com"
      ];
    }

    match /users/{uid} {
      allow read: if request.auth != null;
      allow create: if request.auth != null && request.auth.uid == uid;
      allow update: if request.auth != null && (request.auth.uid == uid || isAdmin());
    }

    match /deals/{id} {
      allow read: if request.auth != null && (isAdmin() || request.auth.uid in resource.data.participants);
      allow create: if request.auth != null && request.auth.uid == request.resource.data.createdBy;
      allow update: if request.auth != null && (isAdmin() || request.auth.uid == resource.data.createdBy);
    }

    match /reviews/{id} {
      allow read: if resource.data.approved == true;
      allow read: if isAdmin();
      allow create: if request.resource.data.approved == false
                    && request.resource.data.name is string
                    && request.resource.data.text is string
                    && request.resource.data.text.size() >= 15
                    && request.resource.data.text.size() <= 1000
                    && request.resource.data.rating is number
                    && request.resource.data.rating >= 1
                    && request.resource.data.rating <= 5;
      allow update, delete: if isAdmin();
    }
  }
}
```

### Storage Security Rules (for review photos)
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /reviews/{file} {
      allow read: if true;
      allow write: if request.resource.size < 5 * 1024 * 1024
                   && request.resource.contentType.matches('image/.*');
    }
  }
}
```

---

## 3. MEMBER PORTAL

Accessible via the **"Portal"** link in the nav (and the mobile hamburger menu).

### Features
- **Sign up / Login** with email + password
- **6 user roles:** Callman, Truck Driver, Workshop Panel, Insurance Panel, Insurance Adjustor, Freelance
- **Referral system (dual):**
  - Each user gets an auto-generated referral code (e.g. `LIMHKPK1`)
  - Shareable link `?ref=CODE` — visitors arriving via it get the portal auto-opened + code pre-filled
  - Signup referrals tracked (who referred whom)
- **Deal logging with commission tracking:**
  - User logs a deal with a counterparty (by email), description, amount, commission %
  - Specifies if they're the Referrer (earns) or Executor (pays)
  - System calculates commission, tracks status: pending → confirmed → paid
  - Real-time updates via Firestore `onSnapshot`

### Firestore collections
| Collection | Holds |
|---|---|
| `users` | Member profiles (name, email, phone, role, company, referralCode, referredBy, isAdmin) |
| `deals` | Logged deals (referrerUid, executorUid, amount, commissionPct, commissionAmount, status, participants[]) |
| `reviews` | Customer reviews (name, role, text, rating, photoUrl, approved) |

---

## 4. ADMIN PANEL

Appears as a purple **"Admin Panel"** button in the portal dashboard — ONLY for users with `isAdmin: true` AND whose email is in the rules `isAdmin()` array.

### Tabs
1. **Overview** — total members, deals, deal volume, commission (earned/paid/pending), members by role
2. **Users** — searchable list (name/email/phone), role filter, Make/Revoke Admin buttons
3. **All Deals** — status filter, change deal status, Export CSV
4. **Reviews** — Pending vs Approved, Approve/Unapprove/Delete reviews

### HOW TO ADD A NEW ADMIN (two layers required)
1. **The person signs up** on the website first (Portal → Sign Up) using the email that will be made admin
2. **Add their email** to the Firestore Rules `isAdmin()` array:
   ```
   return request.auth != null && request.auth.token.email in [
     "limhongjun94@gmail.com",
     "newadmin@example.com"
   ];
   ```
   Then click **Publish** in Firebase Console.
3. **Flip their `isAdmin` field:**
   - Easy: existing admin → Admin Panel → Users → click "Make Admin" on their row
   - Manual: Firestore → Data → users → their doc → Add field `isAdmin` (boolean) = `true`
4. **They log out and back in** (refreshes cached profile → Admin Panel button appears)

### HOW TO REMOVE AN ADMIN
1. Remove their email from the `isAdmin()` rules array → Publish
2. Admin Panel → Users → "Revoke Admin"

### FIRST ADMIN (bootstrap)
The current admin is `limhongjun94@gmail.com` (Lim Hong Jun). The first admin must be set manually in Firebase Console (Firestore → users doc → `isAdmin: true` boolean) because the UI button only appears for existing admins.

---

## 5. LIVE REVIEWS SYSTEM

### Public side
- **"Leave a Review"** button below the reviews grid → opens a modal
- Fields: Name, Role/Company (optional), 5-star rating picker, Review text (15+ chars), Email (optional, private), Photo (optional, max 5MB)
- Submitted reviews are saved with `approved: false` → they DO NOT appear publicly until approved
- Approved reviews auto-render in the grid alongside the 5 original seed reviews
- Each review card has **WhatsApp / Facebook / X share buttons**
- **Rating summary card** at top of reviews section: "X.X/5 from N verified reviews" (auto-calculates from 5 seed @ 5★ + live reviews)
- **Hero badge** under the hero subtitle shows the same rating ("5.0/5 from N+ clients")

### Moderation
- Admin Panel → Reviews tab → Approve / Unapprove / Delete
- Deleting also removes the photo from Storage

### KNOWN GOTCHAS (solved)
- Reviews query uses `where("approved","==",true)` WITHOUT `orderBy` to avoid needing a Firestore composite index. Sorting is done in JavaScript instead.
- Dynamically-added review cards get the `visible` class directly (the IntersectionObserver only runs once at page load and won't catch them).

---

## 6. IMAGE MANAGEMENT

Images are hosted **externally on ImgBB** (keeps the HTML file small) and referenced by URL in `index.html`.

### Current images (ImgBB)
| Section | URL |
|---|---|
| 21FT Flatbed spec | `https://i.ibb.co/Y4jWJXqS/image-1.jpg` |
| Merchandise (JXRR Collection) | `https://i.ibb.co/F4P3rQHT/image-2.png` (HD 1920×1200) |
| Fleet hero + Nationwide Fleet gallery + Service card 04 | `https://i.ibb.co/mV14KfqD/image-3.jpg` |
| Towing Service card 01 | `https://i.ibb.co/DHwdxQzT/image-4.jpg` |

### HOW TO SWAP AN IMAGE
1. Go to https://imgbb.com → upload the new image (no login needed)
2. After upload, click **Embed codes** dropdown → select **"HTML full image"** to get the ORIGINAL resolution URL (NOT "medium" — that gives a resized blurry version!)
3. Paste the `<a href...><img src="..."></a>` block — the direct URL is inside `src="..."`
4. In `index.html`, find the old URL and replace with the new one

### IMAGE RESOLUTION TIP
- ImgBB stores 3 sizes; the auto "Direct link" is sometimes the 640px medium (blurry when stretched).
- Always grab the FULL image URL. For full-width sections, use at least 1920px wide; 2400px+ for collages with small labels.

### Communication pattern for image swaps
When requesting image swaps, list each numbered image with its target section name (e.g. "Swap image 1 to 21FT Flatbed spec section"). The sections are referenced by on-screen names, not HTML IDs.

---

## 7. WHATSAPP FLOATING BUTTON

A persistent floating button (bottom-right of every page).

### Features
- **Neon pink** (#EC4899) brand color with pulsing glow animation
- Opens WhatsApp to **+60 18-311 9595** with a pre-filled message
- **Language-aware:** message + label switch between EN / BM / 中文 with the site language toggle
- **Auto-attaches GPS location** (if user grants permission) as a Google Maps link — huge time-saver for dispatch
- **Responsive:** full pill on desktop → icon-only circle on small phones

### Config (in index.html)
- `WA_PHONE = "60183119595"`
- Messages and labels defined in `WA_MESSAGES` and `WA_LABELS` objects

---

## 8. MOBILE NAVIGATION

- Hamburger menu (☰) appears on screens ≤760px wide
- Tapping opens a full-width dropdown with all nav links including Portal
- Animates to an X when open; auto-closes when a link is tapped
- Fixes the original issue where Portal/nav was hidden on mobile with no way to open it

---

## 9. DEPLOYMENT (NETLIFY)

### To deploy/update the site
1. Make edits to `C:\Users\Richr\OneDrive\Desktop\index.html`
2. Go to https://app.netlify.com/drop
3. Drag `index.html` into the drop zone
4. Netlify gives a live URL (e.g. `random-name.netlify.app`)
5. **After first deploy:** add the Netlify domain to Firebase → Authentication → Settings → Authorized domains
6. Hard-refresh the live site (Ctrl+Shift+R) to clear cached version

### Custom domain (jxrr.io)
- Netlify → Site settings → Domain management → Add custom domain → point DNS to Netlify
- Add `jxrr.io` + `www.jxrr.io` to Firebase authorized domains

### Common deploy issues
| Problem | Fix |
|---|---|
| "Not Found" after drop | Drop into the dashed zone at app.netlify.com/drop; visit the exact URL Netlify returns |
| Login fails on live site | Add the domain to Firebase authorized domains |
| Old version showing | Hard refresh (Ctrl+Shift+R) or clear browser cache |

---

## 10. ADVERTISING VIDEO PRODUCTION

### Concept
20-second cinematic ad: "From Breakdown to Back on the Road" — a stranded family at night, JXRR pink truck arrives fast, everyone safe. Style: Fast-Paced Action × Premium Commercial. Tagline: **"WE GO FAST. WE RESCUE. WE CARE."**

### Brand positioning (from client)
- Objectives: direct customer calls + premium brand awareness
- Differentiator: FAST, covers all areas, worry-free one-stop solution from accident to vehicle return, safe even for female drivers at 11pm
- Audience: all Malaysian car owners, family-focused

### 12-Shot storyboard (each generated 5 sec in Runway, trimmed in CapCut)
| Shot | Scene | Final length | Timeline |
|---|---|---|---|
| 1 | Aerial — stranded car, rainy Melaka highway night | 2.0s | 0:00–0:02 |
| 2 | Driver interior — worried mum + kids | 1.0s | 0:02–0:03 |
| 3 | Phone tap — pink WhatsApp button | 1.0s | 0:03–0:04 |
| 4 | Depot ignition — pink truck starts | 2.0s | 0:04–0:06 |
| 5 | Highway speed — truck racing (HERO shot) | 2.0s | 0:06–0:08 |
| 6 | Arrival hero — truck stops beside car | 2.0s | 0:08–0:10 |
| 7 | Ranger steps out, umbrella, slow-mo | 1.0s | 0:10–0:11 |
| 8 | Family relief — into dry cabin | 2.0s | 0:11–0:13 |
| 9 | EV secured — winched onto flatbed | 1.0s | 0:13–0:14 |
| 10 | Fleet drone — coverage across Malaysia | 2.0s | 0:14–0:16 |
| 11 | Tagline reveal (text on black) | 2.0s | 0:16–0:18 |
| 12 | End frame CTA (JXRR-EndFrame-4K.png) | 2.0s | 0:18–0:20 |

### Voiceover scripts
**English:**
- 0:04 "When everything stops..."
- 0:08 "...we move faster."
- 0:14 "JXRR Rapid Rescue. Anytime. Anywhere."
- 0:18 "Call zero one eight, three one one, nine five nine five."

**Bahasa Malaysia:**
- 0:04 "Bila semua berhenti..."
- 0:08 "...kami bergerak lebih pantas."
- 0:14 "JXRR Rapid Rescue. Bila-bila masa. Di mana sahaja."
- 0:18 "Hubungi kosong satu lapan, tiga satu satu, sembilan lima sembilan lima."

### Production tools used (Path A — DIY, ~RM 150-200)
| Tool | Purpose | Cost |
|---|---|---|
| Runway (Gen-4 Turbo / Nano Banana image) | Generate AI video clips (image-to-video) | Standard plan ~RM 70/mo |
| CapCut Desktop | Edit & assemble | Free |
| CapCut Text-to-Speech | Voiceover | Free |
| CapCut Music library | Background music | Free |

### Runway workflow (image-to-video)
1. **Image tab** → pick "Nano Banana Pro" model → paste image prompt → 16:9 → Generate (regenerate until good)
2. **Video tab** → use the still as First Video Frame → add a motion-only prompt → Gen-4 Turbo → Generate → download MP4
3. AI clips are SILENT — all audio added later in CapCut
4. AI cannot render the JXRR logo cleanly — frame around it or overlay the real logo in editing

### CapCut editing stages
1. Import all clips + end frame
2. Set 16:9, drag clips in order, trim each to target length
3. Transitions (optional — hard cuts look good; use Black Fade sparingly)
4. Voiceover: Text → type line → Text to speech → Generate → set text opacity 0 → position audio
5. Tagline animation on end frame (Animation → Zoom/Fade In)
6. Music: Audio → Music → search "cinematic/epic trailer" → add → trim 20s → fade out → volume ~35%
7. Color polish: Filters → cinematic, Apply to all (50-70%)
8. Export 16:9 master (4K/1080p, 30fps, MP4)

### Output versions to produce
| File | Length | Lang | Ratio | Use |
|---|---|---|---|---|
| JXRR-Ad-EN-16x9 | 20s | EN | 16:9 | Website, YouTube |
| JXRR-Ad-BM-16x9 | 20s | BM | 16:9 | Facebook MY |
| JXRR-Ad-6s-BM-16x9 | 6s | BM | 16:9 | YouTube bumper |
| JXRR-Ad-BM-9x16 | 20s | BM | 9:16 | TikTok / Reels |

### To make variants in CapCut
- **Duplicate project:** Menu → Back to home page → hover project → "⋯" → Copy (NOT in File menu)
- **BM version:** copy project → delete EN voice clips → add BM voice lines at same timings
- **9:16 vertical:** copy project → change ratio to 9:16 → scale each clip ~180-200% & recenter → add big BM text overlays (people watch muted)
- **6-sec bumper:** copy project → keep only shots 5, 6, end frame → trim to 6.0s

### 9:16 vertical text overlays (BM)
- 0:00–0:03 "Terkandas. Lewat malam. 🌧️"
- 0:04–0:08 "Kami bergerak lebih pantas."
- 0:09–0:13 "Dari kerosakan ke keselamatan."
- 0:14–0:20 "📞 018-311 9595"

---

## 11. END FRAME DESIGN

- File: `JXRR-AD-PROJECT\JXRR-EndFrame-4K.png` (3840×2160)
- Design philosophy: "Neon Vigil" — black void, single neon-pink accent as a light source
- Built with Python/PIL using Barlow Condensed fonts (matches website)
- Contains: JXRR wordmark, tagline, pink subtitle, hero phone number 018-311 9595 with phone icon, contact row, "24/7 NATIONWIDE" badge, pink grid background, cinematic vignette
- A 9:16 vertical version (1080×1920) can be generated for TikTok/Reels
- Regenerate script: `JXRR-AD-PROJECT\build_endframe.py`

---

## 12. BRAND ASSETS

| Element | Value |
|---|---|
| Primary pink | #EC4899 |
| Light pink | #F472B6 |
| Background black | #0D0D0D |
| Heading font | Barlow Condensed (900/Black for display) |
| Body font | Barlow |
| Chinese font | Noto Sans SC |
| Tagline | WE GO FAST. WE RESCUE. WE CARE. |
| Support line | Anytime. Anywhere. Worry-Free. |
| Languages | EN / BM (Bahasa Malaysia) / 中文 |

---

## 13. FUTURE FEATURE IDEAS (not yet built)

High impact (revenue/ops):
- Live "Request Service" form with auto-dispatch + customer status tracking
- Driver mobile dashboard (accept jobs, GPS capture, scene photos)
- Online quotation calculator (pickup→dropoff distance estimate)
- Insurance panel portal expansion (claim submission, tracking, invoices)

Growth/trust:
- Live KPI ticker (rescues this month, avg response time)
- Live coverage map (truck locations)
- WhatsApp/SMS broadcast for promos
- Loyalty/repeat-customer rewards

Marketing/SEO:
- Multilingual SEO (BM + 中文 meta + structured data)
- Location landing pages (/towing-melaka, /towing-kl, etc.)
- Blog/resources section

Operational:
- Admin notifications (email/WhatsApp when new review/signup/deal)
- Deal counterparty confirmation (both sides confirm)
- Export users to CSV + monthly auto-reports
- 2FA for admin accounts
- PWA (Add to Home Screen, offline, push notifications)

---

## 14. QUICK TROUBLESHOOTING REFERENCE

| Symptom | Cause | Fix |
|---|---|---|
| "Missing or insufficient permissions" | Firestore rules don't cover the collection, or admin email not in rules | Update & Publish rules; verify email in isAdmin() array |
| Admin panel button missing | User's `isAdmin` field not true, or not re-logged-in | Set isAdmin:true; logout & login |
| Review not showing on homepage | Not approved yet, OR needs index, OR reveal class hidden | Approve in admin; query has no orderBy; card gets `visible` class |
| "query requires an index" | Firestore composite index needed | Remove orderBy, sort in JS (already done) |
| Image blurry | Used ImgBB medium (640px) URL | Use "HTML full image" URL for original resolution |
| Login fails on live site | Domain not authorized | Add domain to Firebase authorized domains |
| Mobile nav/Portal hidden | (Fixed) hamburger menu added | — |
| AI video has no sound | Normal — AI clips are silent | Add VO + music in CapCut |

---

*End of documentation. Keep updated as new features are added.*
