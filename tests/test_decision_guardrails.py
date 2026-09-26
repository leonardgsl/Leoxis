from pathlib import Path
import math
s=Path('index.html').read_text()
def valid(raw,k):
    try:
        if raw is None or str(raw).strip()=='': return False
        v=float(raw)
    except: return False
    if not math.isfinite(v): return False
    return 0<v<=100 if k=='m' else v>0
for x in ['', '0','101','-1','abc','Infinity']: assert not valid(x,'m')
for x in ['.1','12','100']: assert valid(x,'m')
for x in ['', '0','-5','abc','Infinity']: assert not valid(x,'p')
for x in ['.1','30','1000']: assert valid(x,'p')
sales=190000; fixed=62700; c=.44-.015; inv=472000
ms=fixed/(c-.12); ps=(fixed+inv/30)/c
assert round(ms)==205574 and round(ps)==184549 and round((ms/sales-1)*100,1)==8.2 and ps<sales and max(ms,ps)==ms
for x in ['function readGuardrails(){','function buildGuardrailResult(i,g){','function refreshDecisionConditions(){','LEOXIS_VNEXT_NULLSAFE_V6','aria-invalid','Correct the guardrail inputs to refresh Decision Conditions.']: assert x in s,x
v=s[s.index('async function runVNextStage1(i,g){'):s.index('function decisionInputErrors(',s.index('async function runVNextStage1(i,g){'))]
assert 'box.style' not in v
print('AUTOMATED GUARDRAIL TESTS: PASS')
print(round(ms),round(ps),round((ms/sales-1)*100,1),round(max(ms,ps)))
