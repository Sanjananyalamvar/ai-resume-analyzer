HONESTY_NOTE = "Only list skills and achievements you can explain honestly. Do not invent experience or numbers."

def skill_priority(missing, roles_df=None):
    """Return missing skills paired with a simple, stable priority rank."""
    items = list(missing or [])
    return [(skill, len(items) - index) for index, skill in enumerate(items)]

QUESTIONS=[
'How can I improve my resume?', 'I have no work experience. What should I add?',
'How do I make my resume ATS-friendly?', 'How can I show my skills through projects?',
'Why am I not getting interview calls?']
def answer(question, context=None, roles_df=None):
    q=(question or '').lower(); ctx=context or {}; missing=ctx.get('missing',[]); target=ctx.get('target','your target role')
    if any(x in q for x in ['no experience','fresher','experience']):
        return 'As a fresher, put relevant academic or personal projects before experience. For each project, explain the problem, tools used, what you built, and a result you can honestly support. Include internships, hackathons and certifications only when accurate.'
    if 'ats' in q or 'keyword' in q:
        return 'Use standard headings, a simple single-column layout, text-based PDF or DOCX, and wording that truthfully matches the job description. Add a keyword only when you genuinely have that skill. A match score is an estimate, not an ATS pass/fail result.'
    if 'interview' in q or 'calls' in q:
        return 'Check whether your resume is tailored to the role, your projects show evidence of skills, and your contact links work. Apply to roles that fit your current level and ask a trusted person to review the resume. A low response rate is not proof that you lack ability.'
    if 'project' in q or 'skill' in q:
        return f'For {target}, connect each important skill to a project or experience bullet. Current gaps from this analysis: {", ".join(missing[:6]) or "no major gaps detected"}. Build a small project for one gap, then describe what you actually implemented.'
    return 'Use a clear one-page resume as a fresher: summary, technical skills, projects, education, and relevant certifications. Tailor it to one role, use action verbs, and describe your own contribution with truthful specifics. If you share the target job description, I can help prioritise changes.'
