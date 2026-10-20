import re

from section_detector import section_text
from text_cleaner import clean_text


def _mentions(cleaned_text, names):
    """How many times any of the names appears as a whole word in already-cleaned text."""
    total = 0
    for n in names:
        c = clean_text(n)
        if c:
            total += len(re.findall(r"(?<!\S)" + re.escape(c) + r"(?!\S)", cleaned_text))
    return total


def weight_skills(text, skills, aliases=None):
    """Return (weights, listed_only).

    A skill is "only listed" when every mention of it (by its name or any alias, e.g. "ML") sits inside the
    Skills section. A skill that is also mentioned elsewhere (a project, experience, summary...) has evidence
    and counts fully (1.0). Only-listed skills count 0.6. If the resume has no Skills heading nothing can be
    judged, so every skill counts fully.
    """
    t = text or ""
    skills_body = section_text(t, "Skills")[:1500]
    whole, in_skills = " " + clean_text(t) + " ", " " + clean_text(skills_body) + " "
    weights, listed_only = {}, []
    for s in skills:
        names = [s] + list((aliases or {}).get(s, []))
        inside = _mentions(in_skills, names) if skills_body else 0
        if inside > 0 and _mentions(whole, names) - inside <= 0:
            weights[s] = 0.6
            listed_only.append(s)
        else:
            weights[s] = 1.0
    return weights, listed_only
