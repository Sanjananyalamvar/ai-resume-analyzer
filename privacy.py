import re

def strip_personal_info(text):
    t = text or ''
    patterns = [r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', r'(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)', r'https?://\S+', r'\b(?:date of birth|dob|gender|religion|marital status|nationality|caste)\s*:?[^\n]*']
    for p in patterns: t = re.sub(p, '[REDACTED]', t, flags=re.I)
    return t
