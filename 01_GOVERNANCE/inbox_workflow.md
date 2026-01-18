# INBOX Workflow

## Purpose
Provide a strict, auditable ingestion model for parallel authoring while protecting canonical folders.

## Hard rules
- All authoring content is created only under INBOX/YYYYMMDD/Txx/.
- Canonical folders are read-only by policy and are populated only through promotion.
- Every Markdown file must include the required front-matter block.

## Area and type mapping
If intended_path is missing, fallback mapping uses area and type to compute a destination:
- GOV -> 01_GOVERNANCE
- ONB -> 00_ONBOARDING
- CAL -> 04_CALIBRATION
- AUD -> 07_AUDIT
- LIC -> 02_LICENSES
- FRE, CPS, PEPP, WAVNS, AURA, AIFC, SPF -> 03_MODULES/<AREA>
- Default type mapping:
  - README, POLICY, TEMPLATE, MODULE, TESTPLAN, RISK, EVIDENCE, NOTE, TABLE -> placed under the area folder

## Promotion process
1) Drop content in INBOX using naming rules and front-matter.
2) Run lint checks locally and in CI.
3) Open a PR and obtain required approvals.
4) Run promotion to copy content to canonical folders.

## Conflict handling
If destination exists and content differs, copy both files into 07_AUDIT/conflicts/YYYYMMDD/Txx/ and record in the promotion report. The INBOX source is never deleted.

## Reports
Promotion reports are written to 07_AUDIT/promotion_reports/promotion_report_YYYYMMDD.md with lists of promoted files, conflicts, and missing required artifacts.

## Enforcement
- Local pre-commit hook checks ASCII, INBOX-only path, filename pattern, and front-matter.
- CI runs the same checks on pull requests.

## Drop-package helper
Use the provided helper to create a drop package:

./06_TEMPLATES/drop_package.sh T03

The helper creates INBOX/YYYYMMDD/T03/ and a manifest stub with placeholders.
