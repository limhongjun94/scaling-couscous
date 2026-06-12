# JX Assist Sdn Bhd — Project Memory

> Transferred from Claude.ai project: "New startup business proposal with details capex, opex, all kind of necessary cost and expenses, all kind of income streams"
> Synced: 2026-06-12

---

## Purpose & Context

HJ is building **JX Assist Sdn Bhd** (registration 202601019575), a towing and roadside recovery business headquartered in Melaka, Malaysia, with ambitions for nationwide expansion. The business operates 21-foot heavy-duty flatbed tow trucks under a distinctive **neon pink brand identity** with 24/7 GPS-dispatched operations. HJ is developing this as an investor- and partner-facing venture, with documentation and financial modeling done to a professional, presentation-ready standard.

The core business model has two tracks running in parallel:
- **Towing operations**: Drivers on pure commission (no base salary), with multiple ancillary income streams including workshop referral commissions, insurance claim handling fees, storage yard income, and scrap vehicle income.
- **Truck rental model**: Drivers rent trucks as independent contractors (not employees), with a monthly flat rental structure and a 15% insurance payout profit-sharing arrangement as a separate mechanism.

Key collaborators/stakeholders: partners and shareholders are the primary audience for business documentation.

---

## Current State

Three major deliverables have been completed across recent conversations:

1. **Tow Truck Rental Agreement** (tri-lingual: English, Bahasa Malaysia, Chinese Mandarin) — a full 15-clause professional agreement under JX Assist Sdn Bhd, including Schedule A (truck details/equipment checklist) and Annexure B (insurance payout advance and 15% profit sharing). Independent contractor relationship is explicitly established throughout.

2. **Bilingual (Chinese-English) Business Plan** — a 13-page partner/shareholder-facing document covering executive summary, market analysis, competitive analysis (six competitors), financial projections, growth roadmap, and investment thesis. Uses Navy/Teal/Pink color scheme with Microsoft YaHei and Calibri fonts, A4 format.

3. **Investor-grade Excel financial models** — two models (single-truck and multi-truck 2→5 growth scenario), both HP-financed. Contain 900+ formulas across tabs covering Assumptions, CAPEX, OPEX, Trip Economics, multiple P&L scenarios (Towing Only, With Rental, Workshop Commission), Truck Rental Income with self-funding fleet expansion timeline, Extra Income Streams, and Per-KM Charge.

---

## On the Horizon

- Fleet expansion is planned in phases: 1 truck for early months, self-funding the second truck via rental income by around month 8, scaling to 5 trucks by Year 3 and targeting 100 trucks nationally long-term.
- The rental model and independent contractor framework are now documented and could be operationalized as HJ begins onboarding drivers.

---

## Key Learnings & Principles

- **Phased fleet self-funding**: Year 1 is modeled as 17 truck-months (not 24) due to the staggered acquisition timeline — a key insight that materially affects revenue projections.
- **Diesel cost allocation**: When trucks are rented to drivers, diesel is the driver's cost, not the company's — this significantly improves rental model OPEX and IRR.
- **RM10 maintenance charge**: Treated as a company cost, not a customer-facing charge — an early correction that shaped the financial model structure.
- **Document generation efficiency**: For multi-language document production, Python-based text replacement (python-docx) is faster and more reliable than building full Node.js templates from scratch.
- **Contractor vs. employee distinction**: Carefully maintained throughout legal documentation to reflect the actual independent contractor relationship.

---

## Approach & Patterns

- HJ works iteratively, providing corrections and refinements as outputs are reviewed — precision on inputs (exact figures, cost classifications, structural choices) is important.
- Prefers structured Q&A before major deliverables to confirm key parameters before execution.
- Values speed in document generation; willing to switch technical approaches if needed.
- Roles assigned to Claude have been specific and professional (e.g., "senior HR consultant," "finance professional with 20 years startup experience," "marketing manager with 15 years experience").
- Business documents are consistently bilingual (Chinese-English) or trilingual for different audiences, reflecting the multilingual business environment in Malaysia.

---

## Tools & Resources

- **Document formats**: DOCX and PDF as primary deliverables; Word-compatible formatting expected.
- **Spreadsheet**: Excel with multi-tab financial models.
- **Document generation**: Python (python-docx) preferred over Node.js for templated multi-language document production.
- **Design conventions**: Navy/Teal/Neon Pink brand palette; Microsoft YaHei for Chinese, Calibri/Barlow Condensed for English; A4 format; confidential markings on investor documents.

---

## Original Project Brief

> I want to create a comprehensive and realistic startup business proposal for a car towing and roadside assistance business in Malaysia, starting from 1 truck and scalable into a multi-truck operation.
>
> The proposal must include:
> - Complete business model structure
> - Startup roadmap and scaling strategy
> - CAPEX breakdown (truck purchase, equipment, licenses, insurance, deposits, setup costs, etc.)
> - OPEX breakdown (fuel, salary, maintenance, loan instalments, road tax, insurance renewals, marketing, office/storage yard costs, etc.)
> - Detailed cash flow projection
> - Revenue projections and profitability analysis
> - Break-even analysis
> - Financing structure and loan scenarios
> - Risk analysis and mitigation plans
> - Operational workflow
> - Team structure and staffing requirements
> - Marketing and customer acquisition strategy
> - Digital lead generation strategy
> - Competitive landscape in Malaysia towing industry
>
> All possible income streams analyzed: direct towing charges, highway/accident recovery, workshop referral commissions, insurance claims handling commissions, storage yard income, fleet contracts, truck rental income, dispatch/subcontract margins, scrap car/total loss vehicle deals, salvage and used parts, roadside assistance, vehicle repossession, accident management ecosystem revenue.
>
> Realistic Malaysia market pricing, estimated income ranges, operational assumptions, and scalable business strategies based on actual towing industry practices in Malaysia. Investor-grade, highly detailed, financially realistic.
