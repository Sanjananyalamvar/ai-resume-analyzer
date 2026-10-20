from career_tools import interview_questions, cover_letter_template, application_row, resume_action_plan

def test_interview_questions_role_specific():
    q = interview_questions("Data Analyst", ["SQL"])
    assert any("WHERE and HAVING" in x["question"] for x in q)
    assert any("SQL" in x["question"] for x in q)

def test_cover_letter_uses_placeholders_and_user_facts():
    draft = cover_letter_template("Asha", "AI Intern", "Example Co", ["Python"], "built a study helper")
    assert "Asha" in draft and "AI Intern" in draft and "Python" in draft
    assert "built a study helper" in draft
    assert "[Company name]" not in draft

def test_cover_letter_does_not_invent_numbers():
    draft = cover_letter_template("", "", "", [], "")
    assert "90%" not in draft and "increased revenue" not in draft
    assert "[Your name]" in draft and "[project you completed" in draft

def test_application_row():
    row = application_row("Example", "AI Intern", "Applied", "2026-10-19", "https://example.com", "Follow up")
    assert row["Company"] == "Example"
    assert row["Status"] == "Applied"
    assert row["Applied on"] == "2026-10-19"

def test_action_plan_mentions_missing_skills():
    steps = resume_action_plan(["SQL"], ["Projects"], "Data Analyst")
    assert any("Projects" in s for s in steps)
    assert any("SQL" in s for s in steps)
