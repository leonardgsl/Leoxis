# LEOXIS_STAGE61_CSV_IMPORT_VALIDATOR_V1
from pathlib import Path
import csv,json,sys,re
B=Path(__file__).resolve().parents[1]; S=json.loads((B/"data/schema/leoxis-expansion-data-v1.json").read_text())
F={"stores.csv":"store","approved_cases.csv":"approved_case","outcomes.csv":"outcome"}; ID=re.compile(r"^[A-Za-z0-9._:-]+$")
def main():
 d=Path(sys.argv[1]); cust=None; data={}
 for fn,en in F.items():
  p=d/fn
  if not p.exists(): raise ValueError("missing "+fn)
  with p.open(newline="",encoding="utf-8-sig") as f:r=csv.DictReader(f); rows=list(r); heads=r.fieldnames or []
  miss=[x for x in S["entities"][en]["required"] if x not in heads]
  if miss or not rows: raise ValueError(f"{fn}: missing {miss or 'data rows'}")
  for n,row in enumerate(rows,2):
   for x in S["entities"][en]["required"]:
    if not (row.get(x) or "").strip(): raise ValueError(f"{fn} row {n}: blank {x}")
   c=row["customer_id"].strip()
   if not ID.match(c): raise ValueError(f"{fn} row {n}: invalid customer_id")
   cust=cust or c
   if c!=cust: raise ValueError(f"{fn} row {n}: mixed customer_id rejected")
   if en=="outcome" and row["period"].strip() not in S["entities"]["outcome"]["period_enum"]: raise ValueError(f"{fn} row {n}: invalid period")
  data[en]=rows
 stores={r["store_id"].strip() for r in data["store"]}
 if len(stores)!=len(data["store"]): raise ValueError("duplicate store_id")
 cases={r["case_id"].strip():r for r in data["approved_case"]}
 if len(cases)!=len(data["approved_case"]): raise ValueError("duplicate case_id")
 for r in data["approved_case"]:
  if r["store_id"].strip() not in stores: raise ValueError("approved case references unknown store")
 seen=set()
 for r in data["outcome"]:
  k=(r["case_id"].strip(),r["period"].strip())
  if k in seen: raise ValueError("duplicate case-period outcome")
  seen.add(k)
  if k[0] not in cases: raise ValueError("outcome references unknown case")
  if r["store_id"].strip()!=cases[k[0]]["store_id"].strip(): raise ValueError("outcome store/case mismatch")
 print(json.dumps({"status":"PASS","schema":S["schema"],"customer_id":cust,"safe_to_stage":True}))
if __name__=="__main__":
 try: main()
 except Exception as e: print(json.dumps({"status":"REJECTED","safe_to_stage":False,"error":str(e)}));sys.exit(1)
