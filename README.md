# AI Resume Analyzer and Job Recommendation System — Complete Project

Streamlit application for resume analysis, role matching, skill-gap guidance, resume building, interview practice, cover-letter drafting, and internship tracking.

## Features
- Upload PDF, DOCX, PNG, or JPG resumes; OCR support requires Tesseract installed on the machine.
- Detect skills and resume sections, rank 26 technical roles, compare against a pasted job description, and produce a learning roadmap.
- Optional semantic matching with Sentence Transformers.
- Guided resume builder with Word/PDF/text export and honest-writing checks.
- Resume Q&A and optional Groq feedback/chat/AI polish (API key is optional).
- Interview coach, cover-letter template, internship application tracker, PDF report.
- Resume content is processed in memory by the app; AI features only send text when explicitly enabled.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder and create a virtual environment: `python -m venv .venv`
3. Activate it: Windows ` .venv\Scripts\activate `; macOS/Linux `source .venv/bin/activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run: `streamlit run app.py`.

OCR note: install the Tesseract application for your OS as well as the Python package. If OCR is unavailable, normal text PDFs and DOCX files can still be analyzed.

## Optional AI setup
Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`, add your own Groq API key, and enable AI features in the sidebar. Never commit secrets to GitHub. Without a key, offline features remain available.

## Tests
Run `python -m compileall .` to check Python syntax. Run `python -m unittest discover -s tests -v` for the unit tests, and `python tests/smoke_test_app.py` to run the real `app.py` and the resume builder end to end (no browser needed). `tests/test_sections.py` covers heading detection. The other test files can be run directly with `python tests/test_builder.py` and `python tests/test_problems.py`.

## Responsible use
Scores are estimates, not ATS pass/fail results or hiring decisions. Only include skills and accomplishments you can support honestly. Do not upload resumes without permission. The application does not guarantee interviews or employment.
