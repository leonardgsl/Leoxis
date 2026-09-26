from pathlib import Path
s=Path("api/site-intelligence.js").read_text()
assert "LEOXIS_GIS_SEARCH_FALLBACK_V266" in s
assert "add(parts.join(', ')); add(q);" in s
assert "const core=words.filter" in s
assert "t==='bahru'?['bahru','bharu']" in s
assert "queriesTried:variants.length" in s
i=Path("index.html").read_text()
for m in ["LEOXIS_NAVIGATION_EVENT_V3","LEOXIS_GUARDRAIL_SINGLE_SOURCE_V6","LEOXIS_VNEXT_NULLSAFE_V6"]:
 assert m in i,m
print("GIS SEARCH V266 REGRESSION: PASS")
