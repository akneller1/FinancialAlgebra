"""Verify generated PDF dimensions, local HTML assets and unchanged manifest links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json, re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src'):self.links.append(v)

manifest=json.loads((ROOT/'financial/resources.json').read_text())
units=manifest['units']; assert len(units)==10
count=0
for unit in units:
    pdf=ROOT/unit['resources']['cheatSheet'];folder=pdf.parent
    assert folder.name==f"financial-algebra-{unit['unitId']}-cheat-sheet"
    reader=PdfReader(pdf);assert len(reader.pages)==2, pdf
    for i,p in enumerate(reader.pages):
        assert abs(float(p.mediabox.width)-612)<.1 and abs(float(p.mediabox.height)-792)<.1
        txt=p.extract_text(); assert ('Front' if i==0 else 'Back') in txt
        assert 'Fictional examples' in txt
        assert len(txt)>1500
        assert not any(x in txt for x in ['NaN','undefined','⟨','⟩','[['])
    for name in ('index.html','cheat-sheet.html'):
        path=folder/name;html=path.read_text();parser=Links();parser.feed(html)
        refs=parser.links+re.findall(r'url\(["\x27]?([^\)"\x27]+)',html)
        for ref in refs:
            assert not re.match(r'(https?:|file:|//)',ref),f'Nonportable asset: {ref}'
            assert (folder/unquote(urlsplit(ref).path)).is_file(),f'Missing local link: {ref}'
        if name=='cheat-sheet.html':
            assert html.count('class="pg"')==2
            assert html.count('class="sec"')==12
            assert 'font-size:9pt' in html and 'font-size:11.5pt' in html
            assert 'katex-error' not in html
            assert 'grid-template-rows:repeat(3,minmax(0,1fr))' in html
    count+=1
css=ROOT/'financial/lib/cheat-sheets/katex/katex.min.css'
for ref in re.findall(r'url\(([^)]+)\)',css.read_text()):assert (css.parent/ref).is_file(),ref
print(f'{count} sheets: 20 Letter PDF pages, 120 panels; all manifest, HTML, PDF and font links resolve locally.')
