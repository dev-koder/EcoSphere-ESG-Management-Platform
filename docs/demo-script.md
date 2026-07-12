# EcoSphere Demo Script (2–3 minutes)

This script is designed for live demonstrations to highlight the platform's key technical and UX differentiators.

## 1. The Dashboard (0:00 - 0:30)
*Action: Open the EcoSphere app. The default landing page is the ESG Dashboard.*
- Show the **Overall ESG Score** (big number).
- Show the department ranking chart and carbon trend line.
- *"This dashboard aggregates live data across all our models, reducing N queries to one optimized RPC payload."*

## 2. Auto Emission Calculation (0:30 - 1:00)
*Action: Navigate to Purchase (or Expense/Fleet) and confirm a record. Then switch back to Carbon Transactions.*
- Show the newly minted `esg.carbon.transaction` row.
- *"This isn't mock data — Odoo's native automation engine just fired. No manual entry is required by the sustainability team."*

## 3. Governance Automation (1:00 - 1:30)
*Action: Show an overdue Compliance Issue, then show the related Owner's activity inbox.*
- Highlight the scheduled To-Do activity and the chatter notification.
- *"Overdue issues trigger the native Odoo activity schedule automatically via a daily cron, keeping compliance proactive."*

## 4. Gamification (1:30 - 2:30)
*Action: Approve a pending Challenge participation for a demo employee.*
- Show the XP increase on the Leaderboard.
- Show the Badge auto-unlocking in the Chatter.
*Action: Attempt a Reward Redemption with insufficient points.*
- Emphasize the `ValidationError` blocking the transaction.
- *"This proves our robust data validation. It's not just a UI element; the backend strictly enforces point and stock balances."*

## 5. The Closing Pitch (2:30 - 3:00)
- *"Odoo 19 Enterprise just shipped a native ESG app for carbon accounting — which tells us this problem matters to Odoo too. EcoSphere runs on 100% free Community edition and adds the piece their own app doesn't have: making sustainability something employees actually want to engage with, not just something Finance reports on."*
