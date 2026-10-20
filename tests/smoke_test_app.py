"""Smoke test that runs the REAL app.py end to end WITHOUT needing Streamlit, Plotly or a browser.

It installs a tiny fake `streamlit` (and `plotly`) so every line of app.py and builder_page.py runs
against real resume files. Any exception that would show as a red error box in the browser fails here.

Run:  python tests/smoke_test_app.py
"""
import io
import os
import runpy
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


class StopApp(Exception):
    pass


class Any:
    """Accepts any call / attribute / context-manager use, like a Streamlit element."""
    def __call__(self, *a, **k): return Any()
    def __getattr__(self, name): return Any()
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def __iter__(self): return iter(())
    def __bool__(self): return False


class State(dict):
    __getattr__ = dict.get
    def __setattr__(self, k, v): self[k] = v


class FakeUpload(io.BytesIO):
    def __init__(self, name, data):
        super().__init__(data); self.name = name; self.size = len(data)
    def getvalue(self): return super().getvalue()


class Sidebar(Any):
    def __init__(self, cfg): self.cfg = cfg
    def radio(self, label, options, **k): return self.cfg["page"]
    def checkbox(self, label, value=False, **k): return self.cfg["checks"].get(label, value)


def build_fake_streamlit(cfg):
    st = types.ModuleType("streamlit")
    st.session_state = State()
    st.secrets = type("S", (), {"__getitem__": lambda s, k: (_ for _ in ()).throw(KeyError(k))})()
    st.sidebar = Sidebar(cfg)
    st.cache_resource = lambda f: (lambda *a, _c={}, **k: _c.setdefault("v", f(*a, **k)))
    st.errors = []
    st.set_page_config = lambda **k: None
    def stop(): raise StopApp()
    st.stop = stop
    st.rerun = stop
    def columns(n, **k): return [Any() for _ in range(n if isinstance(n, int) else len(n))]
    st.columns = columns
    st.tabs = lambda labels: [Any() for _ in labels]
    st.file_uploader = lambda label, **k: cfg.get("upload_json") if "draft" in label else cfg["file"]
    st.radio = lambda label, options, **k: cfg["mode"] if "Match my resume" in label else list(options)[0]
    st.selectbox = lambda label, options, **k: cfg["selects"].get(label, list(options)[0])
    st.text_area = lambda label, value="", **k: cfg["texts"].get(label, k.get("key") and st.session_state.get(k["key"], value) or value)
    st.text_input = lambda label, value="", **k: value
    st.number_input = lambda label, value=0, **k: st.session_state.get(k.get("key"), value)
    st.multiselect = lambda label, options, **k: st.session_state.get(k.get("key"), [])
    st.button = lambda label, **k: label in cfg["buttons"]
    st.form_submit_button = lambda label, **k: label in cfg["buttons"]
    st.chat_input = lambda *a, **k: cfg.get("chat")
    st.date_input = lambda *a, value=None, **k: value
    def err(msg, *a, **k): st.errors.append(str(msg))
    st.error = err
    for name in ("success", "info", "warning", "write", "markdown", "caption", "title", "subheader", "header",
                 "divider", "metric", "plotly_chart", "dataframe", "download_button", "code", "spinner",
                 "expander", "container", "form", "chat_message", "text"):
        setattr(st, name, Any())
    return st


def install_fakes(cfg):
    sys.modules["streamlit"] = build_fake_streamlit(cfg)
    px = types.ModuleType("plotly.express")
    px.pie = px.bar = lambda *a, **k: Any()
    pl = types.ModuleType("plotly"); pl.express = px
    sys.modules["plotly"], sys.modules["plotly.express"] = pl, px
    for m in ("app", "builder_page"):
        sys.modules.pop(m, None)
    return sys.modules["streamlit"]


def run(cfg):
    base = {"page": "Analyze my resume", "checks": {}, "mode": "A job role from the list", "selects": {},
            "texts": {}, "buttons": set(), "file": None}
    base.update(cfg)
    st = install_fakes(base)
    try:
        runpy.run_path(str(ROOT / "app.py"), run_name="__main__")
    except StopApp:
        pass
    return st


# ---------------------------------------------------------------- sample resumes
def make_files():
    from resume_builder import LEVELS, new_resume, to_docx, to_pdf
    from skill_extractor import load_skills
    sdf = load_skills()
    r = new_resume()
    r.update(name="Asha Verma", email="asha@example.com", phone="+91 90000 00000", city="Hyderabad",
             target_role="Data Analyst", level=LEVELS[0], summary="Student aiming for a Data Analyst role.")
    r["skills"] = ["python", "sql", "excel", "pandas", "power bi", "statistics", "git"]
    r["projects"] = [{"title": "Sales Dashboard", "tools": "Power BI, SQL",
                      "bullets": "Built a dashboard in Power BI that tracks 12 months of sales\nCleaned 50,000 rows using Python."}]
    r["education"] = [{"degree": "B.Tech", "school": "Sample University", "years": "2023-2027", "score": ""}]
    return {"pdf": FakeUpload("resume_A.pdf", to_pdf(r, sdf)), "docx": FakeUpload("r.docx", to_docx(r, sdf)),
            "empty_pdf": None}


results = []


def check(name, ok, note=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({note})" if note else ""))


def main():
    files = make_files()
    from job_matcher import load_roles
    roles = list(load_roles()["role"])

    # 1. every role x PDF, evidence on and off
    for use_ev in (True, False):
        bad = []
        for role in roles:
            files["pdf"].seek(0)
            st = run({"file": files["pdf"], "selects": {"Select your target role": role},
                      "checks": {"Count skills less if they are only listed": use_ev},
                      "buttons": {"Python Developer"}})
            if st.errors: bad.append((role, st.errors[0]))
        check(f"Analyze: all {len(roles)} roles run without errors (evidence={use_ev})", not bad, str(bad[:2]))

    # 2. DOCX upload
    files["docx"].seek(0)
    st = run({"file": files["docx"]})
    check("Analyze: DOCX resume", not st.errors, str(st.errors))

    # 3. job description mode
    files["pdf"].seek(0)
    st = run({"file": files["pdf"], "mode": "A job description I paste",
              "texts": {"Paste the job description here": "We need Python, SQL, Docker, Git and REST API experience."}})
    check("Analyze: pasted job description", not st.errors, str(st.errors))

    # 4. every button on the analysis page (quick answers, cover letter, tracker, ...)
    import advice, career_tools
    all_buttons = set(advice.QUESTIONS) | {"Generate cover letter", "Add application", "Generate AI feedback",
                                            "Clear tracker for this session"}
    files["pdf"].seek(0)
    st = run({"file": files["pdf"], "buttons": all_buttons})
    check("Analyze: quick-answer / cover-letter / tracker buttons", not st.errors, str(st.errors))

    # 5. AI features with a mocked Groq reply
    import requests
    class R:
        status_code = 200
        def json(self): return {"choices": [{"message": {"content": "- Strength: projects\n- Gap: Docker"}}]}
    real_post = requests.post
    requests.post = lambda *a, **k: R()
    os.environ["GROQ_API_KEY"] = "test-key"
    try:
        files["pdf"].seek(0)
        st = run({"file": files["pdf"], "checks": {"Enable AI features: feedback and chat (Groq)": True},
                  "buttons": {"Generate AI feedback"}, "chat": "How do I show Docker?"})
        check("Analyze: AI feedback + chat (mocked)", not st.errors, str(st.errors))
        st.session_state.clear()
    finally:
        requests.post = real_post
        os.environ.pop("GROQ_API_KEY", None)

    # 6. unreadable / empty / oversize files give a message, not a crash
    st = run({"file": FakeUpload("bad.pdf", b"this is not a pdf")})
    check("Analyze: corrupt PDF shows a friendly error", len(st.errors) == 1 and "Could not read" in st.errors[0])
    st = run({"file": FakeUpload("big.pdf", b"0" * (6 * 1024 * 1024))})
    check("Analyze: file over 5 MB is rejected politely", len(st.errors) == 1 and "too large" in st.errors[0])

    # 7. resume builder page
    st = run({"page": "Create my resume"})
    check("Builder page renders", not st.errors, str(st.errors))
    for kw in ("I have no experience", "which skills should I list", "I feel hopeless"):
        st = run({"page": "Create my resume", "buttons": {"Get help"}, "texts": {"Your problem": kw}})
        check(f"Builder help: '{kw}'", not st.errors, str(st.errors))
    st = run({"page": "Create my resume", "selects": {"The role you are aiming for": "Computer Vision Engineer"}})
    check("Builder: role with a skill missing from the old dictionary", not st.errors, str(st.errors))

    print(f"\n{sum(results)} of {len(results)} checks passed")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
