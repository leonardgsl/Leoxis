from pathlib import Path
s=Path("index.html").read_text()
assert s.count('id="editAssumptionsBtn"')==1
assert 'data-nav-target="input"' in s
assert s.count("function editAssumptions(e){")==1
fn=s[s.index("function editAssumptions(e){"):s.index("function num(",s.index("function editAssumptions(e){"))]
assert "showTab('input')" in fn and "clearCase" not in fn and "current=" not in fn
for m in ["LEOXIS_GUARDRAIL_SINGLE_SOURCE_V6","LEOXIS_GUARDRAIL_CENTRAL_FLOW_V6","LEOXIS_VNEXT_NULLSAFE_V6","LEOXIS_EXPANSION_RECOVERY_GUARD_V1"]: assert m in s,m
print("EDIT ASSUMPTIONS NAVIGATION REGRESSION: PASS")
