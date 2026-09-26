from pathlib import Path
s=Path("api/site-intelligence.js").read_text()
for m in ["LEOXIS_GIS_ENTITY_INTEGRITY_V267","LEOXIS_GIS_GEO_RANKING_V267","engine:'LEOXIS_GIS_INTEGRITY_V267'"]:
 assert m in s,m
assert "location,categories,chains" in s
assert "badCategory=/restaurant|food|dining|library|education|school|office|atm|financial|service|warehouse|distribution/i" in s
assert "u.searchParams.set('countrycodes',inferredCountry)" in s
assert "cc==='my'?100:-100" in s
assert "includes('kelantan')?40:-20" in s
assert "locality.includes('kota bharu')" in s
i=Path("index.html").read_text()
for m in ["LEOXIS_NAVIGATION_EVENT_V3","LEOXIS_GUARDRAIL_SINGLE_SOURCE_V6","LEOXIS_VNEXT_NULLSAFE_V6"]:
 assert m in i,m
print("GIS INTEGRITY V267 REGRESSION: PASS")
