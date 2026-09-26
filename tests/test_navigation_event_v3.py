from pathlib import Path
s=Path("index.html").read_text()
assert "LEOXIS_NAVIGATION_EVENT_V3" in s
for target,label in [("conditions","View decision conditions"),("input","Edit assumptions"),("review","Back to review")]:
 assert f'data-nav-target="{target}"' in s,label
assert "document.addEventListener('pointerdown'" in s
assert "document.addEventListener('click'" in s
assert "leoxisNavigate(b.dataset.navTarget,e)" in s
assert "btn.addEventListener('click',editAssumptions" not in s
for old in ["onclick=\"showTab('conditions')\"","onclick=\"showTab('review')\""]:
 assert old not in s
for m in ["LEOXIS_NAVIGATION_DETERMINISM_V2","LEOXIS_GUARDRAIL_SINGLE_SOURCE_V6","LEOXIS_GUARDRAIL_CENTRAL_FLOW_V6","LEOXIS_VNEXT_NULLSAFE_V6"]:
 assert m in s,m
print("NAVIGATION EVENT V3 REGRESSION: PASS")
