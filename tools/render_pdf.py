"""Render the short academic report from docs/lab-01.md."""
from pathlib import Path
import re, hashlib, json
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4

BASE=Path(__file__).resolve().parents[1]
DOC=BASE/'docs';VER=BASE/'verification'
font_candidates=[(Path('C:/Windows/Fonts/arial.ttf'),Path('C:/Windows/Fonts/arialbd.ttf')),(Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))]
regular,bold=next((a,b) for a,b in font_candidates if a.exists() and b.exists())
pdfmetrics.registerFont(TTFont('UA',str(regular)));pdfmetrics.registerFont(TTFont('UABold',str(bold)))
body=ParagraphStyle('Body',fontName='UA',fontSize=11,leading=15.3,spaceAfter=8,textColor=colors.HexColor('#263341'))
title=ParagraphStyle('Title',parent=body,fontName='UABold',fontSize=18.5,leading=22,spaceAfter=12,textColor=colors.HexColor('#12364D'))
section=ParagraphStyle('Section',parent=body,fontName='UABold',fontSize=12,leading=15,spaceBefore=9,spaceAfter=6,keepWithNext=True)
def inline(s):
    s=escape(s)
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:m.group(1),s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'\1',s)
    return s.replace('—','-').replace('–','-')
story=[]
for block in (DOC/'lab-01.md').read_text(encoding='utf-8').strip().split('\n\n'):
    style=body
    if block.startswith('# '):block=block[2:];style=title
    elif block.startswith('## '):block=block[3:];style=section
    if re.match(r'^1\. ',block):
        for item in block.splitlines():story.append(Paragraph(inline(item),style))
    else:story.append(Paragraph(inline(block.replace('\n',' ')),style))
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#DCE4E9'));canvas.line(46,40,A4[0]-46,40)
    canvas.setFont('UA',8);canvas.setFillColor(colors.HexColor('#607384'))
    canvas.drawString(46,27,'Luden | ЛР1 | Фінальна редакція 20.11.2026')
    canvas.drawRightString(A4[0]-46,27,str(doc.page))
SimpleDocTemplate(str(DOC/'lab-01.pdf'),pagesize=A4,leftMargin=46,rightMargin=46,topMargin=42,bottomMargin=53,title='ЛР1 Luden — фінальна редакція',author='Luden team; documentation revision by Codex').build(story,onFirstPage=footer,onLaterPages=footer)
(VER/'pdf-source.sha256').write_text(hashlib.sha256((DOC/'lab-01.md').read_bytes()).hexdigest()+'  docs/lab-01.md\n',encoding='utf-8')
try:
    import pypdfium2 as pdfium
    output=BASE.parents[1]/'work/final-pdf-review';output.mkdir(parents=True,exist_ok=True)
    pdf=pdfium.PdfDocument(str(DOC/'lab-01.pdf'))
    for i,page in enumerate(pdf):page.render(scale=1.4).to_pil().save(output/f'page-{i+1}.png')
    print(json.dumps({'pages':len(pdf),'preview_directory':str(output)},ensure_ascii=False))
except ImportError:print('PDF created; install pypdfium2 to produce visual review PNGs')
