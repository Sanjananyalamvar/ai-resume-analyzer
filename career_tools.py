"""Practical, offline career tools for the AI Resume Analyzer.

These helpers deliberately use templates and the candidate's own facts. They do not
invent qualifications, metrics, employers, or experience.
"""
from datetime import date

INTERVIEW_BANK = {
    "Python Developer": [
        ("Tell me about yourself.", "Give a 30–60 second summary: your current studies, Python skills, one project, and the role you want."),
        ("How do lists and tuples differ?", "Lists are mutable; tuples are immutable. Choose based on whether the collection should change."),
        ("How do you handle errors in Python?", "Use try/except for expected errors, catch specific exception types, and provide a useful fallback or message."),
        ("Describe a project you built.", "Explain the problem, your role, tools, one challenge, how you tested it, and the result. Use only results you can verify."),
        ("How would you debug code that fails?", "Reproduce the issue, read the traceback, isolate the smallest failing case, inspect inputs, fix it, and retest."),
    ],
    "Data Analyst": [
        ("Tell me about yourself.", "Connect your studies, Python/SQL/Excel or BI skills, a data project, and why you want an analyst role."),
        ("What is the difference between WHERE and HAVING?", "WHERE filters rows before grouping; HAVING filters grouped results after GROUP BY."),
        ("How do you handle missing data?", "Inspect why values are missing, measure the extent, then justify dropping, imputing, or flagging values."),
        ("How would you explain an insight to a non-technical person?", "Lead with the finding, explain why it matters, support it with a clear chart or number, and state a caveat."),
        ("Describe your data-analysis project.", "Cover the question, dataset, cleaning, analysis, key finding, limitations, and what you would do next."),
    ],
    "Data Scientist": [
        ("What is overfitting?", "A model learns training-specific patterns and performs poorly on unseen data. Use validation, regularization, and simpler models where appropriate."),
        ("Why split data into train and test sets?", "To estimate performance on data not used for fitting; avoid leaking test information into preprocessing or model selection."),
        ("Explain precision and recall.", "Precision measures how many predicted positives were correct; recall measures how many actual positives were found."),
        ("How would you handle an imbalanced dataset?", "Choose metrics appropriate to the problem, establish a baseline, and consider class weights or resampling inside training folds."),
        ("Describe an ML project.", "Explain the target, data, baseline, preprocessing, model choice, evaluation metric, result, and limitations."),
    ],
    "AI Engineer": [
        ("What is an LLM?", "A large language model is trained on text or other data to generate or transform content; it can still produce incorrect answers."),
        ("What is retrieval-augmented generation (RAG)?", "RAG retrieves relevant documents and supplies them to a language model so answers can be grounded in those sources."),
        ("How would you reduce hallucinations in a chatbot?", "Use trusted sources, retrieval, citations, explicit uncertainty, tests, and a fallback when evidence is insufficient."),
        ("How do you protect user data in an AI app?", "Minimize collection, redact sensitive data, restrict access, explain external processing, and set retention rules."),
        ("Describe an AI project.", "Explain the user problem, data/source material, model or API, evaluation, safeguards, and what you would improve."),
    ],
    "Machine Learning Engineer": [
        ("What is data leakage?", "Information unavailable at prediction time enters training or validation, creating misleadingly high performance."),
        ("How would you serve a model?", "Package preprocessing and prediction consistently, expose a validated API, test edge cases, and monitor errors and drift."),
        ("How do you compare models?", "Use a suitable baseline, the same splits and metric, validation or cross-validation, and consider latency and maintainability."),
        ("What is a reproducible ML pipeline?", "A repeatable sequence for data validation, preprocessing, training, evaluation, and artifact/version tracking."),
        ("Describe an ML deployment or project.", "State what you built, how it was tested, how predictions are served, and known limitations."),
    ],
}
DEFAULT_INTERVIEW = [
    ("Tell me about yourself.", "Summarize your education, relevant skills, one real project, and the role you want."),
    ("Why do you want this role?", "Connect the work to your interests and mention one relevant skill or project."),
    ("Tell me about a challenge.", "Use a real example: situation, your action, outcome, and what you learned."),
    ("What are you currently learning?", "Name a specific skill, how you practise it, and what you have built with it."),
    ("What questions do you have for us?", "Ask about the team's work, intern responsibilities, mentorship, or success criteria."),
]

def interview_questions(role, missing_skills=None):
    """Return role-specific questions and practical answer guidance."""
    questions = INTERVIEW_BANK.get(role, DEFAULT_INTERVIEW)
    missing = list(missing_skills or [])
    output = [{"question": q, "guidance": a} for q, a in questions]
    if missing:
        output.append({
            "question": f"How are you working on {missing[0]}?",
            "guidance": f"Be transparent about your current level in {missing[0]}. Describe a learning resource, a small practice task, and a project you plan to complete. Do not claim proficiency before you can demonstrate it."
        })
    return output

def cover_letter_template(name, role, company, skills, project, why_company=""):
    """Create a factual cover-letter draft with placeholders where information is missing."""
    name = name.strip() or "[Your name]"
    role = role.strip() or "[Role title]"
    company = company.strip() or "[Company name]"
    skills = [s.strip() for s in skills if s and s.strip()]
    skill_text = ", ".join(skills[:4]) if skills else "[relevant skills you can demonstrate]"
    project = project.strip() or "[project you completed and your contribution]"
    motivation = why_company.strip() or f"I am interested in the {role} opportunity at {company} because it aligns with the work I want to develop my skills in."
    return (
        f"Dear Hiring Team at {company},\n\n"
        f"I am applying for the {role} position. I am building my skills in {skill_text} and am keen to contribute while continuing to learn.\n\n"
        f"One relevant example is {project}. Through this work, I practised solving a problem, applying technical tools, and explaining the result. "
        "I would be happy to discuss my specific contribution and what I learned.\n\n"
        f"{motivation}\n\n"
        "Thank you for considering my application. I would welcome the opportunity to discuss how my current skills and learning mindset fit the role.\n\n"
        f"Sincerely,\n{name}"
    )

def application_row(company, role, status="Interested", applied_on=None, link="", next_step=""):
    return {
        "Company": company.strip(),
        "Role": role.strip(),
        "Status": status,
        "Applied on": applied_on or date.today().isoformat(),
        "Job link": link.strip(),
        "Next step": next_step.strip(),
    }

def resume_action_plan(missing_skills, missing_sections, target_role):
    steps = []
    if missing_sections:
        steps.append("Add or verify these sections if relevant: " + ", ".join(missing_sections) + ".")
    if missing_skills:
        steps.append("Prioritise one role-relevant skill at a time: " + ", ".join(missing_skills[:5]) + ". Only list skills you can discuss honestly.")
    steps.append(f"Build or improve one project that demonstrates the skills required for {target_role}; include your contribution, tools, and a verifiable outcome.")
    steps.append("Tailor the resume to the actual job description, use standard headings, and export a text-based PDF or DOCX.")
    steps.append("Ask a person to review it, then practise explaining every skill and project bullet aloud.")
    return steps
