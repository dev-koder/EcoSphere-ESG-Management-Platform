# EcoSphere — ESG Management Platform

A native **Odoo 17.0 Community** addon (`ecosphere_esg`) that turns ESG (Environmental, Social,
Governance) management into a real, day-to-day part of the ERP — with a gamification layer
(challenges, badges, XP, rewards, leaderboards) that Odoo's own Enterprise ESG app doesn't offer.

## Why this approach

- **Native Odoo addon, not a standalone app.** The brief is written in Odoo's own language
  (Purchase / Expenses / Fleet integration, Odoo best practices), so building a real module gets
  list/kanban/graph views, QWeb PDF reports, chatter notifications, cron jobs, and security
  groups for free — letting effort go into what's actually novel.
- **Odoo Community, not Enterprise.** Keeps the project 100% free to run and reinforces the
  positioning that EcoSphere adds an employee-engagement layer Odoo's paid ESG app lacks.
- **Real-time data only.** Every screen reads from live Odoo ORM / Postgres records — no static
  JSON or mock data.
- **Build in phases.** The project is developed in five phases (Foundation → Environmental →
  Social/Governance → Gamification/Dashboard → Polish & Ship), each ending in a working, tested,
  committed state.

## Tech Stack

| Layer | Choice |
|---|---|
| Platform | Odoo 17.0 Community |
| Deployment | Docker Compose (`odoo:17.0` + `postgres:15`) |
| Backend | Python ORM models + `base_automation` |
| Frontend | Stock Odoo views + one custom OWL2 dashboard |
| Charts | Odoo's bundled Chart.js |
| Reports | QWeb (PDF) + `xlsxwriter` (Excel) |
| Notifications | `mail.thread` / `mail.activity` / `bus.bus` |
| Auth | `res.groups` + `ir.rule` |

## Features

- Environmental: carbon transactions, emission factors, sustainability goals, auto emission
  calculation from Purchase/Expense/Fleet
- Social: CSR activities, employee participation, challenges
- Governance: policies, acknowledgements, audits, compliance issue tracking with overdue alerts
- Gamification: XP, badges, points ledger, reward redemption, leaderboards
- Unified dashboard with department ESG scoring and rankings

## Getting Started

```bash
git clone https://github.com/dev-koder/EcoSphere-ESG-Management-Platform.git
cd EcoSphere-ESG-Management-Platform
docker compose up -d
# create a database, then install the ecosphere_esg app
```

## Project Status

🚧 In active development, built in phases per the internal implementation plan. See commit
history for phase-by-phase progress.

## License

TBD
