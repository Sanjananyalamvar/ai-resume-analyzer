import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from section_detector import detect_sections, CORE_SECTIONS
from career_tools import cover_letter_template, interview_questions, application_row, resume_action_plan
from skill_extractor import load_skills, extract_skills
from job_matcher import load_roles

class CoreTests(unittest.TestCase):
    def test_sections(self):
        got=detect_sections('Skills\nPython\nProjects\nDemo app\nEducation\nBTech')
        self.assertTrue(got['Skills']); self.assertTrue(got['Projects']); self.assertFalse(got['Experience'])
    def test_data_loads(self):
        self.assertGreater(len(load_skills()), 50); self.assertGreaterEqual(len(load_roles()), 20)
    def test_skill_alias(self):
        self.assertIn('Python', extract_skills('Built an API in Python and used pandas.', load_skills()))
    def test_cover_letter_does_not_invent_metrics(self):
        draft=cover_letter_template('Alex','Python Intern','Example Co',['Python'],'Built a class project')
        self.assertIn('Built a class project', draft); self.assertNotIn('increased revenue by 50%', draft)
    def test_interview_questions(self):
        self.assertTrue(interview_questions('Python Developer'))
    def test_application_row(self):
        self.assertEqual(application_row('Company','Intern')['Company'],'Company')
    def test_action_plan(self):
        self.assertTrue(resume_action_plan(['SQL'],['Projects'],'Data Analyst'))

if __name__ == '__main__': unittest.main()
