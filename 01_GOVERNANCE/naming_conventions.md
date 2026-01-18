# Naming Conventions

## INBOX filename pattern
YYYYMMDD_Txx_AREA_TYPE_slug_vMAJOR.MINOR.ext

## Allowed AREA values
GOV, ONB, CAL, AUD, LIC, FRE, CPS, PEPP, WAVNS, AURA, AIFC, SPF

## Allowed TYPE values
README, POLICY, TEMPLATE, MODULE, TESTPLAN, RISK, EVIDENCE, NOTE, TABLE

## Required front-matter block
Markdown files must include a front-matter block at the top. The first non-empty line must be "<!--" and the block must close with "-->".

Required keys:
- tr3c_terminal
- area
- type
- version
- status
- intended_path
- source_inputs
# INBOX

INBOX is the only writable area for authoring. All drops must be placed under INBOX/YYYYMMDD/Txx/.

Filename pattern:
YYYYMMDD_Txx_AREA_TYPE_slug_vMAJOR.MINOR.ext

Markdown front-matter is required and must include keys:
tr3c_terminal, area, type, version, status, intended_path, source_inputs
