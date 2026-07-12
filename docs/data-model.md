# EcoSphere ESG Data Model & Architecture

This document describes the models and scoring logic that power EcoSphere.

## Phase 1: Foundation
- `esg.department`: Extends Odoo's native HR departments for ESG grouping.
- `esg.category`: Master tags for emissions and activities (e.g., `scope1`, `csr_activity`).

## Phase 2: Environmental
- `esg.emission.factor`: Reference table linking categories to `co2e_per_unit`.
- `esg.product.profile`: Overrides product templates to attach emission factors.
- `esg.carbon.transaction`: The core ledger. Triggered seamlessly by `base_automation` (Purchase, Expense, Fleet) when the Auto Emission Calculation config is active.
- `esg.environmental.goal`: Tracks `current_value` vs `target_value`.

## Phase 3: Social & Governance
- `esg.csr.activity` & `esg.employee.participation`: Tracks volunteering/training. Approvals optionally enforce proof-of-evidence checks.
- `esg.policy` & `esg.policy.acknowledgement`: Tracks governance document compliance.
- `esg.audit` & `esg.compliance.issue`: Tracks internal/external audits. Overdue issues are flagged automatically by a daily cron job.

## Phase 4: Gamification & Scoring
- `esg.challenge` & `esg.challenge.participation`: XP-bearing activities.
- `esg.badge`: Auto-awarded based on XP, Challenges, or CSR thresholds via python hooks.
- `esg.reward` & `esg.reward.redemption`: Exchange points for items; strictly validates stock and point balances.
- `esg.points.ledger`: Immutable record of point generation (from approvals) and burn (from redemptions).

### Department Scoring Logic (`esg.department.score`)
Recalculated synchronously (or via 15-minute fallback cron):
- **Environmental**: Average % progress across all active environmental goals.
- **Social**: `(approved CSR + approved challenges) / (eligible employees × expected activities) × 100`
- **Governance**: `100 - Σ(severity_weight for open issues) - (unacknowledged required policies penalty)`
- **Total**: The sum of the sub-scores multiplied by their globally configured weights.
