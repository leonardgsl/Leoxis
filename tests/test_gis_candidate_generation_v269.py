from pathlib import Path
s=Path("api/site-intelligence.js").read_text()
for m in [
 "LEOXIS_GIS_CANDIDATE_GENERATION_V269",
 "engine:'LEOXIS_GIS_CANDIDATE_GENERATION_V269'",
 "u.searchParams.set('namedetails','1')",
 "candidateCount:j.length",
 "add(`${qt[0]} ${qt.slice(1).join(' ')} mall`)"
]:
    assert m in s,m
assert "if(all.length>=8)break" not in s
assert "LEOXIS_GIS_ENTITY_INTEGRITY_V267" in s
assert "LEOXIS_GIS_VENUE_INTENT_V268" in s
i=Path("index.html").read_text()
for m in ["LEOXIS_NAVIGATION_EVENT_V3","LEOXIS_GUARDRAIL_SINGLE_SOURCE_V6","LEOXIS_VNEXT_NULLSAFE_V6"]:
    assert m in i,m
print("GIS CANDIDATE GENERATION V269 REGRESSION: PASS")
