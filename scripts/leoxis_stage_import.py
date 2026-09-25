# LEOXIS_STAGE62_PERSISTENCE_V1
from pathlib import Path
import csv,json,sys,hashlib,datetime,subprocess
B=Path(__file__).resolve().parents[1]; V=B/"scripts/leoxis_validate_import.py"; ROOT=B/"data/staging"
if len(sys.argv)!=2: raise SystemExit("usage: python scripts/leoxis_stage_import.py <validated-folder>")
src=Path(sys.argv[1])
r=subprocess.run([sys.executable,str(V),str(src)],capture_output=True,text=True)
if r.returncode: print(r.stdout.strip()); raise SystemExit(1)
meta=json.loads(r.stdout); cid=meta["customer_id"]
def clean(x):
 x="".join(c for c in x if c.isalnum() or c in "._-")
 return x or "invalid"
cid=clean(cid); dest=ROOT/cid; dest.mkdir(parents=True,exist_ok=True)
# append-only batch: never overwrite a prior staged import
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
h=hashlib.sha256()
for fn in ("stores.csv","approved_cases.csv","outcomes.csv"): h.update((src/fn).read_bytes())
batch=f"{stamp}-{h.hexdigest()[:12]}"; bd=dest/batch
if bd.exists(): raise SystemExit("REJECTED: batch collision")
bd.mkdir()
manifest={"schema":"LEOXIS_EXPANSION_DATA_V1","customer_id":cid,"batch_id":batch,"staged_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"immutable":True,"source_sha256":{}}
for fn in ("stores.csv","approved_cases.csv","outcomes.csv"):
 raw=(src/fn).read_bytes(); (bd/fn).write_bytes(raw); manifest["source_sha256"][fn]=hashlib.sha256(raw).hexdigest()
(bd/"manifest.json").write_text(json.dumps(manifest,indent=2))
print(json.dumps({"status":"STAGED","customer_id":cid,"batch_id":batch,"path":str(bd),"immutable":True},indent=2))
