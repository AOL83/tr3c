# TR3C Repository

Mission: provide an audit-grade, Markdown-first repository scaffold with a strict INBOX-only write model for parallel authoring terminals (T01 to T08).

Scope:
- Canonical folders are read-only by policy and are populated only through promotion.
- All authoring changes must be staged under INBOX/YYYYMMDD/Txx/.
- Promotions use deterministic rules based on front-matter metadata.

INBOX-only model:
- Terminals write only under INBOX/YYYYMMDD/Txx/.
- Each drop must include front-matter with required keys.
- Lints run locally and in CI to enforce compliance.

## Folder map

| Folder | Purpose |
| --- | --- |
| 00_ONBOARDING | Required inputs and onboarding checklists |
| 01_GOVERNANCE | Policies, naming rules, and workflow |
| 02_LICENSES | Third-party notices |
| 03_MODULES | Module placeholders, promoted only |
| 04_CALIBRATION | Calibration schedule and UID registry |
| 05_DATA | Raw, processed, materials, onboarding data |
| 06_TEMPLATES | Templates and drop helper |
| 07_AUDIT | Promotion reports and conflicts |
| INBOX | Authoring drops only |
| scripts | Linting, hooks, promotion tooling |

## Quick start for terminals

1) Export terminal id and create a drop package:

export TR3C_TERM=T03
make drop TERM=T03

2) Create files under INBOX/YYYYMMDD/T03/ using the naming convention.

3) Open a PR for review and promotion.
