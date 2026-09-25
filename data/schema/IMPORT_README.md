# Controlled CSV import v1
Required files: `stores.csv`, `approved_cases.csv`, `outcomes.csv`.
Validation is fail-closed: no partial acceptance. Mixed customers, missing required fields, invalid F90/F180/F365 periods, duplicates, and broken Store → Approved Case → Outcome references are rejected.
A PASS means structurally safe to stage; it does not verify evidence or write to production.
