# EcoSphere: ESG Management Platform

## 🌍 The Problem
Odoo 19 Enterprise just shipped a native ESG app for carbon accounting — which tells us this problem matters to Odoo too. EcoSphere runs on **100% free Community edition** and adds the piece their own app doesn't have: making sustainability something employees actually *want* to engage with, not just something Finance reports on.

## ✨ Features
- **Auto Emission Calculation**: Intercepts standard Odoo models (Purchase, Expense, Fleet) to automatically calculate CO2e equivalents without manual data entry.
- **Gamification Engine**: Challenges, Badges, XP, and a Reward Redemption system to incentivize positive environmental and social impact.
- **Dynamic Scorecard**: Real-time Environmental, Social, and Governance scoring, weighted by module configuration, driving the custom Dashboard.
- **Custom Report Builder**: Generates tailored PDF, Excel, and CSV ESG reports on the fly.
- **Native Notifications**: Zero-code integration with Odoo's Chatter and Activity streams to escalate overdue audits or celebrate badge unlocks.

## 🚀 Quick Start (Docker)

To run this module locally using Docker:

1. Spin up the environment:
```bash
docker compose up -d
```
2. Navigate to `http://localhost:8069`
3. Create a new database with demo data enabled.
4. Log in as Admin and install the **EcoSphere: ESG Management** app from the Apps menu.

*(Alternatively, if running locally without the UI, `python odoo-bin -d ecosphere -i ecosphere_esg`)*

## 📖 Documentation
- [Data Model & Architecture](docs/data-model.md)
- [Demo Script](docs/demo-script.md)

## 📸 Screenshots
*(Coming soon)*
- Overall ESG Score Dashboard
- Carbon Emission Trend Line
- Gamification Leaderboard
- Reward Redemption Validations
