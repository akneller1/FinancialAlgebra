"""Offline PDF renderer and layout validation for the Classroom HTML template.
Requires WeasyPrint 70.0. Browser build remains available via Playwright.
"""
import sys
from pathlib import Path
from weasyprint import HTML

def render_validate(source, output):
    doc = HTML(filename=str(source)).render()
    if len(doc.pages) != 2:
        raise ValueError(f'{source}: expected 2 pages, got {len(doc.pages)}')
    problems = []
    for number, page in enumerate(doc.pages, 1):
        if abs(page.width-816) > .1 or abs(page.height-1056) > .1:
            problems.append(f'Page {number} is not US Letter')
        panels = [b for b in page._page_box.descendants()
                  if type(b).__name__ == 'BlockBox' and b.element is not None
                  and b.element.get('class') == 'sec']
        if len(panels) != 6:
            problems.append(f'Page {number}: {len(panels)} panels instead of 6')
        for panel in panels:
            title = ''.join(next(e for e in panel.element if e.tag=='h2').itertext())
            x1, y1 = panel.border_box_x(), panel.border_box_y()
            x2, y2 = x1+panel.border_width(), y1+panel.border_height()
            if x1 < 0 or y1 < 0 or x2 > page.width or y2 > page.height:
                problems.append(f'{title}: panel crosses page bounds')
            for b in panel.descendants():
                if type(b).__name__ == 'TextBox':
                    # KaTeX zero-width struts are not text; inspect rendered glyph boxes.
                    if not b.text.strip(): continue
                    if b.position_x < x1+1 or b.position_y < y1+1 or b.position_x+b.width > x2-1 or b.position_y+b.height > y2-2:
                        problems.append(f'{title}: text outside panel: {b.text[:60]}')
    if problems:
        raise ValueError('\n'.join(dict.fromkeys(problems)))
    doc.write_pdf(str(output))
    print(f'Validated {Path(source).parent.name}: 2 Letter pages, 12 panels, no text overflow')

if __name__ == '__main__': render_validate(Path(sys.argv[1]),Path(sys.argv[2]))
