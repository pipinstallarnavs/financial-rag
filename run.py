import argparse, json, math, urllib.request
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
ROOT=Path(__file__).parent; URL='https://raw.githubusercontent.com/czyssrs/FinQA/main/dataset/'
def load(split,root=ROOT/'data'):
 root.mkdir(exist_ok=True); p=root/(split+'.json')
 if not p.exists(): p.write_bytes(urllib.request.urlopen(URL+split+'.json',timeout=40).read())
 return json.loads(p.read_text())
def corpus(row):
 # answers/programs are excluded by construction.
 return list(row.get('pre_text',[]))+list(row.get('post_text',[]))+[' | '.join(map(str,r)) for r in row.get('table',[])]
def retrieve(query,docs,k=5):
 v=TfidfVectorizer(stop_words='english'); X=v.fit_transform(docs+[query]); scores=(X[:-1]@X[-1].T).toarray().ravel(); return np.argsort(-scores)[:k],scores
def number(x):
 return float(str(x).replace(',','').replace('%',''))
def calc(program,table):
 import re
 # FinQA uses both `op(a,b)` and `op ; a ; b` spellings.
 parts=[]
 if ';' in program:
  tokens=[x.strip() for x in program.lower().split(';') if x.strip()]
  if tokens: parts=[tokens]
 else:
  parts=[]
  for m in re.finditer(r'([a-z_]+)\s*\(([^)]*)\)',program.lower()):
   parts.append([m.group(1)]+[x.strip() for x in m.group(2).split(',')])
 vals=[]
 for part in parts:
  op,*args=part
  a=number(args[0]) if args[0].replace('.','',1).replace('-','',1).isdigit() else None
  if a is None:
   for row in table:
    for cell in row:
     if str(cell)==args[0]: a=number(row[-1]); break
    if a is not None: break
  b=number(args[1]) if len(args)>1 else None
  if op=='add': vals.append(a+b); 
  elif op=='subtract': vals.append(a-b)
  elif op=='multiply': vals.append(a*b)
  elif op=='divide': vals.append(a/b)
  elif op=='exp': vals.append(math.exp(a))
  else: raise ValueError(op)
 return vals[-1]
def run(limit=300):
 rows=load('dev')[:limit]; hit=0; exact=0; total=0
 for row in rows:
  docs=corpus(row); idx,_=retrieve(row['qa']['question'],docs); gold=' '.join(str(x) for x in row.get('qa',{}).get('gold_inds',{}))
  hit+=int(any(str(i) in gold for i in idx));
  try: pred=calc(row['qa']['program'],row['table']); exact+=int(abs(pred-number(row['qa']['answer']))<1e-5)
  except (ValueError,IndexError,ZeroDivisionError,TypeError): pass
  total+=1
 return {'split':'dev','rows':total,'retrieval_hit_at_5':hit/total,'program_numeric_accuracy':exact/total,'limit':limit}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int,default=300);a=ap.parse_args();r=run(a.limit);(ROOT/'results').mkdir(exist_ok=True);(ROOT/'results/report.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
if __name__=='__main__':main()
