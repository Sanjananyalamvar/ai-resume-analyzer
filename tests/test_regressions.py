"""Regression tests for bugs found while debugging the app (each one crashed or gave wrong results)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from job_matcher import load_roles, rank_roles
from pipeline import analyze
from resume_builder import build_sections, display_skill, group_skills, new_resume
from roadmap_generator import make_roadmap_with_links
from skill_extractor import extract_skills, load_skills
from text_cleaner import clean_text

SKILLS, ROLES = load_skills(), load_roles()


class Regressions(unittest.TestCase):
    def test_roadmap_has_every_key_app_uses(self):
        item = make_roadmap_with_links(["Python", "C++", "Some New Tool"])[2]
        for key in ("week", "skill", "topic", "docs", "video", "url", "task"):
            self.assertIn(key, item)
        self.assertEqual([i["week"] for i in make_roadmap_with_links(list("abcd"))], [1, 1, 2, 2])
        self.assertIn("C%2B%2B", make_roadmap_with_links(["C++"])[0]["video"])   # URL-safe

    def test_skills_found_next_to_punctuation(self):
        found = extract_skills("Built tools in Python. Skills: Python/SQL, node.js, C++.", SKILLS)
        for skill in ("Python", "SQL", "Node.js", "C++"):
            self.assertIn(skill, found)
        self.assertEqual(clean_text("Used Python."), "used python")
        self.assertIn(".net", clean_text("Knows .NET"))

    def test_listed_only_skills_really_count_less(self):
        text = "Skills\nPython\nSQL\nProjects\nBuilt a tool in Python\nEducation\nBTech"
        res = analyze(text, SKILLS, ROLES, use_evidence=True)
        self.assertIn("SQL", res["listed_only"])
        self.assertNotIn("Python", res["listed_only"])
        on = {r["role"]: r["score"] for r in res["ranked"]}
        off = {r["role"]: r["score"] for r in analyze(text, SKILLS, ROLES, use_evidence=False)["ranked"]}
        self.assertLess(on["Data Analyst"], off["Data Analyst"])

    def test_listed_only_is_a_list_not_a_set(self):
        res = analyze("Skills\nPython\nProjects\nx", SKILLS, ROLES)
        all_skills = {s for v in res["skills"].values() for s in v}
        all_skills - set(res["listed_only"])          # the original line 243 crashed here
        self.assertIsInstance(res["listed_only"], list)

    def test_every_role_skill_is_in_dictionary(self):
        known = {s.lower() for s in SKILLS["skill"]}
        for _, r in ROLES.iterrows():
            for s in r["required_skills"]:
                self.assertIn(s.lower(), known, f"{r['role']}: {s}")

    def test_resume_skills_are_grouped_and_deduplicated(self):
        groups = group_skills(["python", "Python", "sql", "power bi"], SKILLS)
        self.assertEqual(sum(len(v) for v in groups.values()), 3)
        self.assertNotIn("Other", groups)
        r = dict(new_resume(), skills=["python", "sql"])
        heads = [v[0] for _, items in build_sections(r, SKILLS) for k, v in items if k == "skills"]
        self.assertNotIn("Other", heads)
        self.assertEqual(display_skill("numpy"), "NumPy")

    def test_rank_roles_accepts_weights_for_unknown_skills(self):
        rows = rank_roles("python sql", {"Python": "Programming"}, ROLES, skill_weights={"Zzz": 0.1})
        self.assertEqual(len(rows), len(ROLES))


if __name__ == "__main__":
    unittest.main()
