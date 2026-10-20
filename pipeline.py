from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import rank_roles
from evidence import weight_skills
from section_detector import detect_sections


def _alias_map(skill_df, names):
    """{skill: [aliases]} for the detected skills, so 'ML' counts as a mention of Machine Learning."""
    wanted, out = set(names), {}
    for _, r in skill_df.iterrows():
        skill = str(r.get('skill', '')).strip()
        if skill in wanted:
            out[skill] = [x.strip() for x in str(r.get('aliases', '')).split('|') if x.strip()]
    return out


def analyze(raw_text, skill_df, roles_df, use_evidence=True, semantic_sims=None):
    text = clean_text(raw_text)
    detected = extract_skills(raw_text, skill_df)
    skills = {}
    for skill, category in detected.items():
        skills.setdefault(category, []).append(skill)
    listed_only = []
    weights = {s: 1.0 for s in detected}
    # Evidence needs somewhere to show evidence: with no Projects or Experience heading, skills are not weighted.
    sections = detect_sections(raw_text)
    evidence_active = bool(use_evidence and (sections['Projects'] or sections['Experience']))
    if evidence_active:
        weights, listed_only = weight_skills(raw_text, list(detected.keys()), _alias_map(skill_df, detected.keys()))
    ranked = rank_roles(raw_text, detected, roles_df, semantic_sims=semantic_sims, skill_weights=weights)
    for row in ranked:
        row['listed_only'] = [s for s in row['matched'] if s in listed_only]
    return {'text': text, 'skills': skills, 'ranked': ranked, 'weights': weights, 'listed_only': listed_only,
            'evidence_on': evidence_active}
