"""Tests for resume section detection and the 'only listed' evidence check."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evidence import weight_skills
from job_matcher import load_roles
from pipeline import analyze
from section_detector import detect_sections, section_text, split_sections
from skill_extractor import load_skills


def found(text):
    return {n for n, ok in detect_sections(text).items() if ok}


class SectionDetection(unittest.TestCase):
    def test_words_inside_sentences_are_not_headings(self):
        self.assertNotIn("Summary", found("Asha\nLinkedIn profile: linkedin.com/in/asha\nSKILLS\nPython"))
        self.assertNotIn("Experience", found("SKILLS\nPython\nI have no work experience yet"))
        self.assertNotIn("Projects", found("SKILLS\nPython\nLed several projects at college"))
        self.assertNotIn("Education", found("SKILLS\nPython\nGood education and teamwork"))

    def test_common_heading_styles(self):
        cases = {
            "WORK HISTORY\nAcme": "Experience", "Professional Experience:\nAcme": "Experience",
            "INTERNSHIPS\nAcme": "Experience", "ACADEMIC QUALIFICATIONS\nB.Tech": "Education",
            "Educational Background\nB.Tech": "Education", "KEY SKILLS\nPython": "Skills",
            "Technical Proficiency\nPython": "Skills", "Technical Skills & Tools\nPython": "Skills",
            "S K I L L S\nPython": "Skills", "1. Projects\nApp": "Projects", "• Academic Projects\nApp": "Projects",
            "━━ CERTIFICATIONS ━━\nX": "Certifications", "Career Objective\nGet a job": "Summary",
            "Professional Profile\nStudent": "Summary", "Skills: Python, SQL": "Skills",
            "Courses & Certifications\nX": "Certifications",
        }
        for text, section in cases.items():
            self.assertIn(section, found(text), text)

    def test_combined_heading_marks_both(self):
        self.assertTrue({"Education", "Certifications"} <= found("Education and Certifications\nB.Tech"))

    def test_label_inside_a_project_is_not_a_skills_heading(self):
        text = "Projects\nSales Dashboard\nTools: Python, SQL\nBuilt a dashboard\nEducation\nB.Tech"
        self.assertNotIn("Skills", found(text))
        self.assertIn("Python", section_text(text, "Projects"))

    def test_section_bodies(self):
        text = "SKILLS\nPython, SQL\nAchievements\nWon a hackathon\nPROJECTS\nSales app"
        parts = split_sections(text)
        self.assertEqual(parts["Skills"], "Python, SQL")          # ends at the 'Achievements' heading
        self.assertEqual(parts["Projects"], "Sales app")
        self.assertEqual(section_text("Skills: Python, SQL\nProjects\nx", "Skills"), "Python, SQL")

    def test_empty_and_headingless_text(self):
        self.assertFalse(any(detect_sections("").values()))
        self.assertFalse(any(detect_sections(None).values()))
        self.assertTrue(detect_sections("my skills and projects")["Skills"])    # old fallback still works


class Evidence(unittest.TestCase):
    TEXT = "Summary\nStudent\nSKILLS\nPython, SQL, ML\nPROJECTS\nBuilt a tool in Python.\nEducation\nBTech"

    def test_only_listed_skills_are_found_by_name_and_alias(self):
        w, listed = weight_skills(self.TEXT, ["Python", "SQL", "Machine Learning"],
                                  {"Machine Learning": ["ml"]})
        self.assertEqual(sorted(listed), ["Machine Learning", "SQL"])
        self.assertEqual((w["Python"], w["SQL"]), (1.0, 0.6))

    def test_short_skill_names_do_not_match_inside_words(self):
        _, listed = weight_skills("SKILLS\nC\nPROJECTS\nA classic project with cloud tools", ["C"])
        self.assertEqual(listed, ["C"])

    def test_no_skills_heading_means_no_penalty(self):
        _, listed = weight_skills("Projects\nBuilt in Python", ["Python"])
        self.assertEqual(listed, [])

    def test_no_projects_or_experience_heading_turns_weighting_off(self):
        res = analyze("SKILLS\nPython, SQL\nEducation\nBTech", load_skills(), load_roles())
        self.assertFalse(res["evidence_on"])
        self.assertEqual(res["listed_only"], [])


if __name__ == "__main__":
    unittest.main()
