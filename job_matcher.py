from pathlib import Path
import pandas as pd
from text_cleaner import clean_text
from skill_extractor import extract_skills
BASE=Path(__file__).parent

def load_roles():
    df=pd.read_csv(BASE/'data'/'job_roles.csv').fillna('')
    df['required_skills']=df['required_skills'].apply(lambda x:[v.strip() for v in str(x).split('|') if v.strip()])
    return df

def rank_roles(text, skills, roles_df, semantic_sims=None, skill_weights=None):
    raw=' '+clean_text(text)+' '; found=set()
    if isinstance(skills,dict):
        for v in skills.values():
            if isinstance(v,(list,set,tuple)): found.update(v)
            elif isinstance(v,dict): found.update(v.keys())
        if not found: found.update(skills.keys())
    elif isinstance(skills,(list,set,tuple)): found.update(skills)
    found={str(x).lower() for x in found}
    wmap={str(k).lower(): float(v) for k, v in (skill_weights or {}).items()}
    rows=[]
    for idx,(_,r) in enumerate(roles_df.iterrows()):
        required=r['required_skills'] if isinstance(r['required_skills'],list) else [x.strip() for x in str(r['required_skills']).split('|') if x.strip()]
        matched=[s for s in required if s.lower() in found or (' '+clean_text(s)+' ') in raw]
        missing=[s for s in required if s not in matched]
        # Skills that are only listed (not shown in a project) count less, as the app tells the user.
        coverage=100*sum(wmap.get(s.lower(),1.0) for s in matched)/max(1,len(required))
        # Lightweight lexical similarity keeps the baseline transparent and deterministic.
        vocab=set(clean_text(str(r.get('keywords',''))+' '+' '.join(required)).split())
        words=set(raw.split()); union=vocab|words
        tfidf=100*len(vocab&words)/max(1,len(union))
        sem=0
        if semantic_sims is not None:
            try: sem=float(semantic_sims[idx])*100
            except Exception: sem=0
        score=round(max(0,min(100,0.7*coverage+0.3*tfidf)),1)
        if semantic_sims is not None: score=round(max(0,min(100,0.6*coverage+0.15*tfidf+0.25*sem)),1)
        rows.append({'role':str(r['role']),'score':score,'matched':matched,'missing':missing,'listed_only':[], 'required':required})
    return sorted(rows,key=lambda x:x['score'],reverse=True)
