import pandas as pd
from skill_extractor import extract_skills
CUSTOM_ROLE_NAME='Custom job description'
def build_custom_role(text, skill_df):
    found=extract_skills(text,skill_df)
    skills=list(found.keys())
    df=pd.DataFrame([{'role':CUSTOM_ROLE_NAME,'required_skills':skills,'keywords':text}])
    return df,found
