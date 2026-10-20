"""Create a downloadable PDF report."""
from io import BytesIO

def build_pdf(target, selected, ranked, skills, sections, roadmap, feedback=None, listed_only=None):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
        from xml.sax.saxutils import escape
    except ImportError as exc:
        raise RuntimeError('Install reportlab to generate PDF reports.') from exc
    buffer=BytesIO(); doc=SimpleDocTemplate(buffer,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=16*mm)
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='Small',parent=styles['BodyText'],fontSize=8,leading=10))
    story=[Paragraph('AI Resume Analyzer — Report',styles['Title']),Paragraph('Target role: '+escape(str(target)),styles['Heading2']),
           Paragraph('Estimated match score: '+escape(str(selected.get('score','—')))+'%',styles['Heading2']),
           Paragraph('Scores are estimates for guidance, not recruiter or ATS decisions.',styles['Italic']),Spacer(1,8)]
    story.append(Paragraph('Skills detected',styles['Heading2']))
    all_skills=[s for values in skills.values() for s in values]
    story.append(Paragraph(escape(', '.join(all_skills) if all_skills else 'No dictionary skills detected.'),styles['BodyText']))
    story.append(Spacer(1,6)); story.append(Paragraph('Role matches',styles['Heading2']))
    data=[['Role','Score','Matched skills','Missing skills']]
    for r in ranked[:8]: data.append([str(r.get('role','')),str(r.get('score',''))+'%',', '.join(r.get('matched',[])) or '—',', '.join(r.get('missing',[])) or '—'])
    table=Table([[Paragraph(escape(str(c)),styles['Small']) for c in row] for row in data],colWidths=[35*mm,15*mm,58*mm,58*mm],repeatRows=1)
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#26324A')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.4,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP'),('PADDING',(0,0),(-1,-1),5)])); story.append(table)
    story.append(Spacer(1,8)); story.append(Paragraph('Resume sections',styles['Heading2']))
    story.append(Paragraph(escape(', '.join(f'{k}: {"found" if v else "not detected"}' for k,v in sections.items())),styles['BodyText']))
    story.append(Spacer(1,6)); story.append(Paragraph('Suggested learning roadmap',styles['Heading2']))
    if roadmap:
        for item in roadmap[:20]: story.append(Paragraph(escape(f"Week {item['week']}: {item['skill']} — {item['topic']} ({item['url']})"),styles['Small']))
    else: story.append(Paragraph('No skill gaps were detected against this role.',styles['BodyText']))
    if feedback:
        story.append(Spacer(1,8)); story.append(Paragraph('AI feedback',styles['Heading2']))
        for line in str(feedback).splitlines():
            if line.strip(): story.append(Paragraph(escape(line),styles['BodyText']))
    story.append(Spacer(1,10)); story.append(Paragraph('Privacy note: Uploaded resume content is processed by this application. Optional AI services may receive redacted resume text if enabled.',styles['Small']))
    doc.build(story); return buffer.getvalue()
