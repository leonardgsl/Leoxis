from pathlib import Path
s=Path("index.html").read_text()
assert "LEOXIS_NAVIGATION_DETERMINISM_V2" in s
a=s.index("function showTab(id){"); b=s.index("function editAssumptions",a)
show=s[a:b]
assert "behavior:'smooth'" not in show
assert "window.scrollTo(0,0)" in show
assert "return target.classList.contains('active')" in show
a=s.index("function editAssumptions(e){"); b=s.index("document.addEventListener('DOMContentLoaded'",a)
edit=s[a:b]
assert "preventDefault()" in edit and "stopPropagation()" in edit
assert "return showTab('input')" in edit
for m in ["LEOXIS_GUARDRAIL_SINGLE_SOURCE_V6","LEOXIS_GUARDRAIL_CENTRAL_FLOW_V6","LEOXIS_VNEXT_NULLSAFE_V6","LEOXIS_EDIT_ASSUMPTIONS_ONECLICK_V1"]:
    assert m in s,m
print("NAVIGATION DETERMINISM REGRESSION: PASS")
