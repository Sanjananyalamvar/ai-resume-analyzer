# AI Resume Analyzer and Job Recommendation System

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Sanjananyalamvar/ai-resume-analyzer/blob/main/Run_in_Colab.ipynb)

A Streamlit web app that reads a resume, shows how well it matches 26 technical job roles, finds missing skills, and builds a week-by-week learning roadmap. It also includes a resume builder, an interview coach, a cover-letter helper and an internship tracker.

**Live demo:** _add your Streamlit link here_  |  **Demo video:** _add your YouTube link here_

## Screenshots
_Add 3 to 4 screenshots here (results page, skill gap and roadmap, resume builder). Put the images in a `screenshots` folder, then use:_
`![Results](screenshots/results.png)`

## What it does
- **Reads resumes** in PDF, DOCX, PNG or JPG format (photos use OCR).
- **Finds skills and sections** by recognising headings such as Skills, Projects, Education and Experience.
- **Scores your match** against 26 roles, or against a job description you paste. Skills shown only in a skills list count 60%; skills backed by a project or experience count fully.
- **Skill gap and roadmap:** missing skills, a weekly plan, and links to official docs and video tutorials.
- **Resume builder** with honest-writing checks and Word, PDF and text export.
- **Extras:** resume Q&A, interview coach, cover-letter template, application tracker and a downloadable PDF report.
- **Optional AI feedback and chat** using Groq. The app works fully without it.

## How it works
1. The resume text is extracted (PDF, DOCX or OCR) and cleaned.
2. Skills are matched against a skill dictionary (`data/skill_dictionary.csv`) using names and aliases.
3. Headings are detected to find the Skills, Projects and Experience sections.
4. Each role in `data/job_roles.csv` is scored on how many of its required skills are found, with optional semantic matching.
5. Missing skills are turned into a roadmap and a PDF report.

## Tech stack
Python, Streamlit, pandas, Plotly, scikit-learn, PyMuPDF / pypdf, python-docx, ReportLab, Tesseract OCR (optional), Groq API (optional).

## Run locally
1. Install Python 3.10 or newer.
2. In a terminal in this folder: `python -m venv .venv`
3. Activate it: Windows `.venv\Scripts\activate`, macOS/Linux `source .venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Run: `streamlit run app.py`

Try it with `sample_resumes/sample_data_analyst_resume.pdf`.

OCR note: to read photo resumes, install the Tesseract application as well. Normal PDF and DOCX files work without it.

## Run in Google Colab
Click the **Open in Colab** badge above, then run the three code cells in order. Cell 3 prints a temporary public link to the app.

## Optional AI setup
Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your own Groq API key:
`GROQ_API_KEY = "your-key"`. Then tick **Enable AI features** in the sidebar. Never upload `secrets.toml` to GitHub. On Streamlit Community Cloud, paste the key under **Advanced settings, Secrets**.

## Tests
- `python -m compileall .` checks the code for syntax errors.
- `python -m unittest discover -s tests -v` runs the unit tests.
- `python tests/smoke_test_app.py` runs the real `app.py` and the resume builder end to end, without a browser.
- `python tests/test_builder.py` and `python tests/test_problems.py` run the builder checks.

## Project structure
```
app.py                 main Streamlit app
builder_page.py        resume builder page
pipeline.py            runs the full analysis
section_detector.py    finds resume headings
skill_extractor.py     finds skills
job_matcher.py         scores roles
roadmap_generator.py   learning roadmap
data/                  skill dictionary and job roles
tests/                 unit and end-to-end tests
```

## Responsible use
Scores are estimates, not ATS pass/fail results or hiring decisions. Only include skills and accomplishments you can support honestly. Do not upload other people's resumes without permission. The app does not guarantee interviews or employment.
