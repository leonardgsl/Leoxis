from pathlib import Path
import re
s=Path("index.html").read_text()
required=["LEOXIS_EXPANSION_RECOVERY_GUARD_V1",'onclick="leoxisOpenExpansionSafe()"',"function leoxisOpenExpansionSafe()",'id="homeView"','id="toolView"',"LEOXIS_STAGE51_APPROVED_VS_ACTUAL_V1","LEOXIS_STAGE4A_COLLAPSE_FIX_V6"]
missing=[x for x in required if x not in s]
if missing: raise SystemExit("PRECHECK FAIL missing: "+", ".join(missing))
if re.findall(r'\*/\\\\nfunction\s+',s): raise SystemExit("PRECHECK FAIL: malformed literal backslash-n before function")
scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',s,re.S|re.I)
Path(".leoxis_jscheck").mkdir(exist_ok=True)
for n,body in enumerate(scripts): Path(f".leoxis_jscheck/inline_{n}.js").write_text(body)
print(f"LEOXIS structural preflight PASS; extracted {len(scripts)} scripts")
