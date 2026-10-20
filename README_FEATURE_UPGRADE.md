# AI Resume Analyzer — feature upgrade

## Added features
- **Interview Coach:** role-specific interview questions, answer guidance, and a prompt tailored to the selected resume's missing skills.
- **Cover Letter Builder:** editable cover letter draft and `.txt` export. Uses user-provided facts and placeholders instead of inventing achievements.
- **Internship Application Tracker:** track company, role, status, date, link, and next step; export to CSV.
- **Next-action checklist:** turns missing resume sections and role skills into practical next steps.
- Existing resume-analysis and resume-question features remain in place.

## Important archive note
The uploaded ZIP did not include several modules imported by `app.py`, including `job_description.py`, `job_matcher.py`, `advice.py`, `pipeline.py`, `privacy.py`, `report_generator.py`, `resume_parser.py`, `roadmap_generator.py`, `section_detector.py`, `semantic_matcher.py`, `skill_extractor.py`, `text_cleaner.py`, and `usage_limiter.py`.

This means the uploaded archive by itself is not a complete runnable copy of the app. The new features have been integrated into `app.py`, but merge the updated files (`app.py` and `career_tools.py`) into your complete original project folder, which contains those modules, before running it.

## Run
From the complete project directory:
```bash
pip install -r requirements.txt
streamlit run app.py
```
If you do not have a `requirements.txt`, install the dependencies listed in your original project's setup instructions. Do not share your API key in screenshots or source code.

## Data and privacy notes
- The application tracker is stored in Streamlit session state only; it is not a database and may disappear when the session restarts. Download the CSV to keep a copy.
- Cover-letter drafts are templates; verify all details before sending.
- Interview guidance is for practice and cannot guarantee selection.
