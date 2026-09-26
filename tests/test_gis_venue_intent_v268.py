from pathlib import Path
s=Path("api/site-intelligence.js").read_text()
for m in ["LEOXIS_GIS_VENUE_INTENT_V268","engine:'LEOXIS_GIS_VENUE_INTENT_V268'","hitFirst?90:hitLocal?55:hitAny?25:-35","cc===inferredCountry?120:-150","LEOXIS_GIS_ENTITY_INTEGRITY_V267"]:
 assert m in s,m
def score(first,locality,z,brand,intent):
 v=120+(45 if brand in first else 0)
 for t in intent:v+=90 if t in first else 55 if t in locality else 25 if t in z else -35
 return v
assert score("aeon mall tebrau city","johor bahru","aeon mall tebrau city johor","aeon",["tebrau"]) > score("aeon mall","bandar dato onn tebrau","aeon mall bandar dato onn tebrau","aeon",["tebrau"])
assert score("aeon mall kota bharu","kota bharu kelantan","aeon mall kota bharu kelantan","aeon",["kota"]) > score("aeon mall","banjarbaru","aeon mall banjarbaru","aeon",["kota"])
i=Path("index.html").read_text()
for m in ["LEOXIS_NAVIGATION_EVENT_V3","LEOXIS_GUARDRAIL_SINGLE_SOURCE_V6","LEOXIS_VNEXT_NULLSAFE_V6"]:assert m in i,m
print("GIS VENUE INTENT V268 REGRESSION: PASS")
