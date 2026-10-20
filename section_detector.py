"""Find resume sections by their HEADINGS (not by any word that appears anywhere in the text).

A line counts as a heading when it is short and is made only of a known heading name, for example
"SKILLS", "Technical Skills:", "1. Work History", "S K I L L S" or "Skills: Python, SQL".
A sentence such as "I have no work experience" or a contact line such as "LinkedIn profile" is NOT a heading.
"""
import re

CORE_SECTIONS = ["Summary", "Skills", "Projects", "Education", "Experience", "Certifications"]

# Old word-search patterns. They are used only as a last resort when no heading line is found at all
# (for example when text extraction put the whole resume on a single line).
ALIASES = {
    "Summary": r"\b(summary|professional summary|profile|objective|career objective|about me)\b",
    "Skills": r"\b(skills|technical skills|core competencies|technologies)\b",
    "Projects": r"\b(projects|academic projects|personal projects|selected projects)\b",
    "Education": r"\b(education|academic background|qualifications)\b",
    "Experience": r"\b(experience|work experience|employment|internship|professional experience)\b",
    "Certifications": r"\b(certifications|certificates|courses|licenses)\b",
}

_MOD = (r"(?:(?:key|core|technical|professional|relevant|additional|academic|educational|personal|selected|"
        r"major|notable|work|career|industrial|executive|it|my|other|areas of)\s+)*")
_HEADING_WORDS = {
    "Summary": r"summary|profile|objective|about me|about|overview|statement|summary of qualifications",
    "Skills": r"skills?|skill set|skillset|competenc(?:y|ies)|proficienc(?:y|ies)|expertise|technologies|tools|"
              r"programming languages|tech stack|technical stack",
    "Projects": r"projects?|project work|project experience|projects undertaken|mini projects?|major projects?",
    "Education": r"education|education details|academics|academic record|academic background|educational background|"
                 r"qualifications?|scholastic record",
    "Experience": r"experience|employment(?: history| record)?|work history|internships?|internship experience|"
                  r"apprenticeships?|industrial training|career history|professional background",
    "Certifications": r"certifications?|certificates?|licen[sc]es?|courses|online courses|courses completed|"
                      r"training|trainings|workshops|moocs?",
    # Real headings that are not core sections. They still END the section above them.
    "_other": r"achievements?|accomplishments|awards?|honou?rs|hobbies|interests|languages|references|publications|"
              r"research|volunteering|volunteer experience|extra-?curricular activities|co-?curricular activities|"
              r"activities|declaration|personal details|personal information|contact|contact details|links|"
              r"positions of responsibility|leadership|strengths|responsibilities",
}
_PATTERNS = {name: re.compile(rf"^{_MOD}(?:{words})$") for name, words in _HEADING_WORDS.items()}

# With text after the colon ("Tools: Git, Docker") these are ordinary labels inside a project, not headings.
_AMBIGUOUS_WHEN_INLINE = {"tools", "technologies", "tech stack", "technical stack", "training", "courses",
                          "research", "overview", "about", "links", "contact", "leadership", "responsibilities",
                          "strengths", "activities", "workshops", "languages", "skill", "project"}

_BULLETS = re.compile(r"^[\s\-\*\u2022\u00b7\u25aa\u25cf\u25a0\u25c6\u25ba>#|\d.)(]+")
_INLINE = re.compile(r"^([^:|]{2,45}?)\s*(?::|\s[-\u2013\u2014]\s|\s\|\s)\s*(.*)$")


def _match_head(head):
    """Return the set of sections a heading text stands for, or None if it is not a heading."""
    head = re.sub(r"^[^a-z0-9]+|[^a-z0-9.]+$", "", head.lower().strip()).strip(". ")
    if re.fullmatch(r"(?:[a-z]\s){3,}[a-z]", head):            # "s k i l l s" from PDF letter-spacing
        head = head.replace(" ", "")
    if not head or len(head.split()) > 7:
        return None
    found = set()
    for part in re.split(r"\s*(?:,|/|&|\+|\band\b)\s*", head):
        part = part.strip()
        hit = [name for name, pat in _PATTERNS.items() if pat.match(part)]
        if not hit:
            return None
        found.update(n for n in hit if n != "_other")
    return found, head


def _heading_of(line):
    """Return (sections, rest_of_line) when the line is a heading, else None."""
    s = line.strip()
    if not s or len(s) > 90:
        return None
    s = _BULLETS.sub("", s)
    m = _INLINE.match(s)
    head, rest = (m.group(1), m.group(2).strip()) if m else (s, "")
    result = _match_head(head)
    if result is None:
        return None
    sections, norm = result
    if rest and norm in _AMBIGUOUS_WHEN_INLINE:
        return None
    return sections, rest


def find_headings(text):
    """[(heading_start, body_start, set_of_core_sections)] in reading order."""
    out, pos = [], 0
    for line in (text or "").splitlines(keepends=True):
        hit = _heading_of(line)
        if hit is not None:
            sections, rest = hit
            body_start = pos + (line.index(rest, 0) if rest and rest in line else len(line))
            out.append((pos, body_start, sections))
        pos += len(line)
    return out


def detect_sections(text):
    text = text or ""
    found = {s for _, _, sections in find_headings(text) for s in sections}
    if not find_headings(text):                                  # last resort: old word search
        low = text.lower()
        return {name: bool(re.search(pattern, low)) for name, pattern in ALIASES.items()}
    return {name: name in found for name in ALIASES}


def split_sections(text):
    """{section name: the text under its heading(s)} for every section that has a heading."""
    text = text or ""
    heads = find_headings(text)
    bodies = {}
    for i, (_, body_start, sections) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(text)
        for name in sections:
            bodies[name] = (bodies.get(name, "") + "\n" + text[body_start:end]).strip()
    return bodies


def section_text(text, name):
    return split_sections(text).get(name, "")
