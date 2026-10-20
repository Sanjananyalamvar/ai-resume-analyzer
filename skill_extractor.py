from pathlib import Path
import pandas as pd
from text_cleaner import clean_text
BASE=Path(__file__).parent

def load_skills():
    p=BASE/'data'/'skill_dictionary.csv'
    return pd.read_csv(p).fillna('')

def extract_skills(text, skill_df=None):
    df=skill_df if skill_df is not None else load_skills(); t=' '+clean_text(text)+' '; found={}
    for _,r in df.iterrows():
        canonical=str(r.get('skill','')).strip()
        if not canonical: continue
        aliases=[canonical]+[x.strip() for x in str(r.get('aliases','')).split('|') if x.strip()]
        for a in aliases:
            needle=' '+clean_text(a)+' '
            if needle.strip() and needle in t:
                found[canonical]=str(r.get('category','Other')); break
    return found
