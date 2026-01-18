# Document Control Policy

## INBOX-only rule
All authoring changes must be created under INBOX/YYYYMMDD/Txx/. Canonical folders are read-only by policy and are populated only through promotion.

## Promotion concept
Each drop includes front-matter with intended_path. Promotion copies content from INBOX into the canonical destination. If intended_path is missing, a deterministic fallback mapping based on area and type is applied.

## Versioning
Version format is vMAJOR.MINOR. Patch level is tracked by git sha and promotion reports.

## Allowed extensions
Allowed extensions: md, txt, yml, yaml, csv, ics, pdf, png, jpg, jpeg, tiff, tif, xlsx, xls, dxf, step, stp, zip.

## Immutable raw data
Raw data under 05_DATA/raw is immutable. Corrections must be new files with new UIDs and proper linkage to prior versions.

## Phase-gate tagging
Use phase_gate_YYYYMMDD tags to mark phase transitions. Tags are created only after approved promotion.
