# GitHub Public Surface Contract

This document records the small set of GitHub UI settings that sit outside the repository files and therefore cannot be changed by the currently connected GitHub actions.

## External visitor path

1. **Organization Overview** — understand the project and evidence flow.
2. **PSP** — verify the official result, model lineage, and artifact provenance.
3. **BS** — inspect the Plan 3-related OOF model bench and ensemble evidence.

Private research repositories remain named for provenance but are not linked as public destinations.

## Organization About target

- **Display name:** 난임걱정마삼조
- **Description:** Fertility prediction research · structural missingness · OOF validation · reproducible model lineage
- **Website:** https://dacon.io/competitions/official/236452
- **Location:** keep the existing Organization setting unless the team intentionally changes it
- **Public email:** leave blank unless the team explicitly wants a public contact address

## Pinned repositories target

Pin in this order:

1. **PSP** — official project SSOT
2. **BS** — public OOF / ensemble research workspace

The profile repository **.github should not be a featured pin**. It exists to render the Organization Overview, not to compete with the project repositories for reviewer attention.

## Repository About target

### PSP

Description:

> LG Aimers fertility prediction research — structural missingness, OOF validation, boosting ensembles and reproducible model lineage.

Recommended topics:

machine-learning · fertility · binary-classification · roc-auc · out-of-fold · ensemble-learning · catboost · lightgbm · xgboost · reproducibility

### BS

Description:

> Research workspace for Plan 3 fertility prediction models — 5-fold OOF and weighted/rank ensembles.

Recommended topics:

machine-learning · fertility · out-of-fold · ensemble-learning · catboost · lightgbm · xgboost · research-workspace

### .github

Recommended description:

> Organization profile and visual QA contracts for NANIM NO WORRY.

This repository does not need to be pinned.

## Canonical facts that must not drift

- Highest submitted AUC: **Plan 2 · 0.74232**
- Final adopted submission model: **Plan 3 · 0.74231**
- PSP is the official project SSOT.
- BS is a public modeling research workspace, not the official final artifact.
- planB and Research-Papers are private research/evidence repositories.
- No public surface may describe this work as a clinically validated diagnostic or medical decision system.

The machine-readable source is [profile/public-surface-contract.json](../profile/public-surface-contract.json).
