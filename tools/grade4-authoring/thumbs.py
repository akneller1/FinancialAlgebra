"""Grade 4 thumbnails (SVG, the site's 720 x 450 card convention) and unit icons (160 x 120).
Every game, study-guide activity, interactive tool and project gets its own drawn scene that shows what the activity is.
Usage: python3 thumbs.py   -> writes thumbs/math4-*.svg"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("G4_ROOT", os.path.abspath(os.path.join(HERE, "..", "..")))
T = os.path.join(ROOT, "thumbs")
F1 = "Bricolage Grotesque,DejaVu Sans,Verdana,sans-serif"
F2 = "Atkinson Hyperlegible,DejaVu Sans,Verdana,sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def card(title, tag, c1, c2, scene, panel="#FFFDF7"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 450" role="img" aria-label="{esc(title)}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient><clipPath id="c"><rect x="40" y="40" width="640" height="276" rx="20"/></clipPath></defs>'
            f'<rect width="720" height="450" rx="36" fill="url(#g)"/><rect x="28" y="28" width="664" height="300" rx="26" fill="{panel}"/><g clip-path="url(#c)">{scene}</g>'
            f'<text x="40" y="384" font-family="{F1}" font-size="44" font-weight="800" fill="#fff">{esc(title)}</text>'
            f'<text x="40" y="424" font-family="{F2}" font-size="22" fill="#fff" opacity=".95">{esc(tag)}</text></svg>')


def txt(x, y, s, size=30, fill="#1E293B", anchor="middle", weight="800"):
    return f'<text x="{x}" y="{y}" font-family="{F1}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{esc(s)}</text>'


def star(cx, cy, r, fill):
    pts = " ".join(f"{cx + (r if k % 2 == 0 else r * .45) * math.sin(k * math.pi / 5):.1f},{cy - (r if k % 2 == 0 else r * .45) * math.cos(k * math.pi / 5):.1f}" for k in range(10))
    return f'<polygon points="{pts}" fill="{fill}"/>'


def frac(x, y, n, d, size=34, fill="#1E293B"):
    return txt(x, y - 6, str(n), size, fill) + f'<line x1="{x - size * .55}" y1="{y + 2}" x2="{x + size * .55}" y2="{y + 2}" stroke="{fill}" stroke-width="4"/>' + txt(x, y + size * .95, str(d), size, fill)


def dots(x, y, r, c, s=26, fill="#2563EB"):
    return "".join(f'<circle cx="{x + j * s}" cy="{y + i * s}" r="{s * .36:.1f}" fill="{fill}"/>' for i in range(r) for j in range(c))


def short(t, n=60):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


S = {}
S["treasure"] = ('<rect x="40" y="40" width="640" height="276" fill="#FDF1D6"/><path d="M40 250 Q200 210 360 250 T680 235 V316 H40Z" fill="#F6DCA5"/>'
                 '<path d="M90 270 C170 200 230 290 310 220 S450 150 560 200" stroke="#92400E" stroke-width="7" stroke-dasharray="14 12" fill="none"/>'
                 '<circle cx="90" cy="270" r="15" fill="#16A34A"/><circle cx="310" cy="220" r="15" fill="#F59E0B"/>'
                 '<path d="M545 185 l30 30 M575 185 l-30 30" stroke="#DC2626" stroke-width="9" stroke-linecap="round"/>'
                 '<rect x="560" y="230" width="90" height="56" rx="8" fill="#B45309"/><rect x="560" y="230" width="90" height="20" rx="8" fill="#92400E"/><rect x="598" y="244" width="14" height="18" fill="#FDE047"/>'
                 '<polygon points="480,110 500,80 520,110 500,140" fill="#22D3EE"/><polygon points="170,110 186,86 202,110 186,134" fill="#F472B6"/><path d="M110 120 q10 -40 40 -30 q-24 4 -22 30z" fill="#16A34A"/><rect x="126" y="116" width="6" height="60" fill="#92400E"/>')
S["space"] = ('<rect x="40" y="40" width="640" height="276" fill="#1B2350"/>' + "".join(f'<circle cx="{60 + (k * 97) % 620}" cy="{50 + (k * 53) % 250}" r="{1 + k % 3}" fill="#fff" opacity=".8"/>' for k in range(40)) +
              '<circle cx="560" cy="110" r="52" fill="#F97316"/><ellipse cx="560" cy="110" rx="84" ry="16" fill="none" stroke="#FDE68A" stroke-width="6"/><circle cx="150" cy="240" r="40" fill="#38BDF8"/>'
              '<g transform="translate(330 170) rotate(35)"><path d="M0 -70 q34 40 20 100 h-40 q-14 -60 20 -100z" fill="#E2E8F0"/><circle cx="0" cy="-20" r="13" fill="#38BDF8"/><path d="M-20 20 l-22 30 h22z M20 20 l22 30 h-22z" fill="#EF4444"/><path d="M-10 32 q10 40 20 0z" fill="#FBBF24"/></g>'
              '<circle cx="455" cy="230" r="16" fill="#fff"/><rect x="443" y="244" width="24" height="26" rx="8" fill="#fff"/><circle cx="455" cy="230" r="9" fill="#1E3A8A"/>')
S["island"] = ('<rect x="40" y="40" width="640" height="276" fill="#CDEFFD"/><path d="M40 240 q40 -16 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0 V316 H40Z" fill="#38BDF8"/>'
               '<ellipse cx="170" cy="250" rx="90" ry="26" fill="#FDE68A"/><rect x="164" y="160" width="10" height="88" fill="#92400E"/><path d="M170 160 q-50 -20 -70 20 q36 -18 70 -8 q30 -40 76 -14 q-44 -4 -76 14z" fill="#16A34A"/>'
               '<ellipse cx="520" cy="258" rx="110" ry="28" fill="#FDE68A"/>'
               '<path d="M470 150 h44 v-12 a12 12 0 0 1 24 0 v12 h32 v44 h-12 a12 12 0 0 0 0 24 h12 v32 h-100z" fill="#A855F7" stroke="#6B21A8" stroke-width="4"/>'
               '<path d="M300 236 l44 0 l-10 18 h-24z" fill="#B45309"/><path d="M322 236 v-60 l34 44z" fill="#fff" stroke="#64748B" stroke-width="3"/>')
S["castle"] = ('<rect x="40" y="40" width="640" height="276" fill="#DFF1FF"/><circle cx="600" cy="90" r="30" fill="#FDE047"/><path d="M40 270 Q360 230 680 270 V316 H40Z" fill="#86EFAC"/>'
               '<rect x="250" y="170" width="220" height="100" fill="#CBD5E1" stroke="#475569" stroke-width="4"/><rect x="200" y="120" width="64" height="150" fill="#B6C0CE" stroke="#475569" stroke-width="4"/><rect x="456" y="120" width="64" height="150" fill="#B6C0CE" stroke="#475569" stroke-width="4"/>'
               '<path d="M194 120 l38 -46 l38 46z" fill="#DB2777"/><path d="M450 120 l38 -46 l38 46z" fill="#2563EB"/><path d="M330 270 v-50 a30 30 0 0 1 60 0 v50z" fill="#92400E"/>'
               '<path d="M250 170 v-16 h22 v16 h22 v-16 h22 v16 h22 v-16 h22 v16 h22 v-16 h22 v16 h22 v-16 h22 v16" fill="#CBD5E1" stroke="#475569" stroke-width="4"/>'
               '<line x1="232" y1="74" x2="232" y2="46" stroke="#475569" stroke-width="4"/><path d="M232 46 l24 8 l-24 8z" fill="#F97316"/>' + txt(120, 120, "+1", 44, "#16A34A"))
S["detective"] = ('<rect x="40" y="40" width="640" height="276" fill="#1D2A55"/>' + "".join(f'<rect x="{40 + (i % 4) * 160}" y="{40 + (i // 4) * 92}" width="160" height="92" fill="{["#F97316", "#10B981", "#DB2777", "#0EA5E9"][(i + i // 4) % 4]}" stroke="#fff" stroke-width="3"/>' for i in range(12) if i not in (5, 6, 9, 10)) +
                  '<rect x="200" y="132" width="320" height="184" fill="#33427A"/><path d="M330 216 h60 v14 a30 30 0 0 1 -60 0z" fill="#FDE047"/><rect x="354" y="258" width="12" height="18" fill="#FDE047"/><rect x="336" y="276" width="48" height="12" rx="3" fill="#FDE047"/>'
                  '<circle cx="560" cy="150" r="56" fill="#E0F2FE" stroke="#0F172A" stroke-width="10" opacity=".95"/><line x1="600" y1="192" x2="650" y2="250" stroke="#0F172A" stroke-width="16" stroke-linecap="round"/>' + txt(560, 164, "?", 60, "#0F172A"))
S["monster"] = ('<rect x="40" y="40" width="640" height="276" fill="#F3E8FF"/>'
                '<rect x="80" y="80" width="150" height="190" rx="18" fill="#fff" stroke="#A855F7" stroke-width="6"/>' + txt(155, 190, "6 × 7", 40) +
                '<rect x="490" y="80" width="150" height="190" rx="18" fill="#fff" stroke="#F59E0B" stroke-width="6"/>' + txt(565, 190, "42", 50) + star(565, 112, 18, "#F59E0B") +
                '<ellipse cx="360" cy="190" rx="78" ry="70" fill="#22C55E"/><circle cx="332" cy="170" r="20" fill="#fff"/><circle cx="388" cy="170" r="20" fill="#fff"/><circle cx="336" cy="174" r="9" fill="#111"/><circle cx="384" cy="174" r="9" fill="#111"/>'
                '<path d="M324 214 q36 30 72 0" stroke="#14532D" stroke-width="6" fill="none"/><path d="M300 126 l-14 -30 M420 126 l14 -30" stroke="#22C55E" stroke-width="8" stroke-linecap="round"/><circle cx="286" cy="94" r="9" fill="#F472B6"/><circle cx="434" cy="94" r="9" fill="#F472B6"/>')
S["race"] = ('<rect x="40" y="40" width="640" height="276" fill="#27306B"/>' + "".join(f'<line x1="{120 + i * 70}" y1="40" x2="{120 + i * 70}" y2="316" stroke="#fff" stroke-width="{8 if i == 7 else 2}" stroke-dasharray="{"8 8" if i == 7 else "0"}" opacity=".7"/>' for i in range(8)) +
             "".join(f'<rect x="52" y="{66 + k * 62}" width="46" height="34" rx="10" fill="{c}"/><g transform="translate({x} {84 + k * 62}) rotate(90)"><path d="M0 -30 q16 18 9 46 h-18 q-7 -28 9 -46z" fill="#E2E8F0"/><circle cx="0" cy="-8" r="6" fill="{c}"/><path d="M-5 16 q5 20 10 0z" fill="#FBBF24"/></g>'
                     for k, (c, x) in enumerate([("#2F7FD8", 420), ("#F08C1A", 300), ("#1AA37A", 520), ("#D63C7A", 230)])))
S["soccer"] = ('<rect x="40" y="40" width="640" height="276" fill="#3FAE5A"/>' + "".join(f'<rect x="{40 + i * 128}" y="40" width="64" height="276" fill="#45B862"/>' for i in range(5)) +
               '<rect x="60" y="60" width="600" height="236" fill="none" stroke="#fff" stroke-width="5"/><line x1="360" y1="60" x2="360" y2="296" stroke="#fff" stroke-width="4"/><circle cx="360" cy="178" r="48" fill="none" stroke="#fff" stroke-width="4"/>'
               '<rect x="40" y="130" width="24" height="96" fill="#fff" opacity=".85"/><rect x="656" y="130" width="24" height="96" fill="#fff" opacity=".85"/>'
               '<circle cx="450" cy="178" r="26" fill="#fff" stroke="#111" stroke-width="4"/><polygon points="450,164 463,174 458,190 442,190 437,174" fill="#111"/>')
S["four"] = ('<rect x="40" y="40" width="640" height="276" fill="#DBEAFE"/><rect x="170" y="52" width="380" height="252" rx="18" fill="#2F5FD8"/>' +
             "".join(f'<circle cx="{202 + c * 53}" cy="{82 + r * 48}" r="19" fill="{col}"/>' for r in range(5) for c in range(7)
                     for col in [{(4, 1): "#F08C1A", (4, 2): "#2F7FD8", (4, 3): "#F08C1A", (3, 2): "#F08C1A", (3, 3): "#38BDF8", (2, 3): "#F08C1A", (4, 4): "#38BDF8", (3, 4): "#38BDF8", (2, 4): "#38BDF8", (1, 4): "#F08C1A", (4, 5): "#38BDF8"}.get((r, c), "#EEF4FF")]))
S["fraction"] = ('<rect x="40" y="40" width="640" height="276" fill="#FFF1E0"/>' +
                 "".join(f'<path d="M190 178 L{190 + 96 * math.cos(-math.pi / 2 + 2 * math.pi * i / 8):.1f} {178 + 96 * math.sin(-math.pi / 2 + 2 * math.pi * i / 8):.1f} A96 96 0 0 1 {190 + 96 * math.cos(-math.pi / 2 + 2 * math.pi * (i + 1) / 8):.1f} {178 + 96 * math.sin(-math.pi / 2 + 2 * math.pi * (i + 1) / 8):.1f}Z" fill="{"#FDBA74" if i < 6 else "#fff"}" stroke="#9A3412" stroke-width="4"/>' for i in range(8)) +
                 txt(355, 190, "=", 60) + '<rect x="420" y="100" width="110" height="156" rx="16" fill="#fff" stroke="#EA580C" stroke-width="5"/>' + frac(475, 168, 3, 4, 44) +
                 '<rect x="550" y="100" width="110" height="156" rx="16" fill="#fff" stroke="#CBD5E1" stroke-width="5"/>' + frac(605, 168, 6, 8, 44))
S["array"] = ('<rect x="40" y="40" width="640" height="276" fill="#E0F2FE"/>' + dots(110, 96, 4, 5, 44, "#2563EB") + dots(330, 96, 4, 2, 44, "#F97316") +
              '<line x1="308" y1="72" x2="308" y2="252" stroke="#0F172A" stroke-width="4" stroke-dasharray="8 7"/>' + txt(540, 150, "4 × 7", 50) + txt(540, 215, "= 28", 50, "#16A34A"))
S["flashcards"] = ('<rect x="40" y="40" width="640" height="276" fill="#ECFDF5"/><g transform="rotate(-7 300 180)"><rect x="130" y="76" width="300" height="200" rx="22" fill="#fff" stroke="#10B981" stroke-width="6"/>' + txt(280, 150, "numerator", 36) + frac(280, 205, 3, 4, 30, "#10B981") + '</g>'
                   '<g transform="rotate(6 500 200)"><rect x="380" y="100" width="280" height="180" rx="22" fill="#FEF9C3" stroke="#F59E0B" stroke-width="6"/>' + txt(520, 180, "the top number", 30) + txt(520, 222, "how many parts", 24, "#92400E", weight="600") + '</g>')
S["check"] = ('<rect x="40" y="40" width="640" height="276" fill="#F0F9FF"/><rect x="110" y="70" width="330" height="216" rx="20" fill="#fff" stroke="#0EA5E9" stroke-width="6"/>' +
              "".join(f'<rect x="140" y="{104 + i * 56}" width="34" height="34" rx="8" fill="{c}"/><path d="M148 {122 + i * 56} l7 8 l13 -15" stroke="#fff" stroke-width="5" fill="none"/><rect x="190" y="{112 + i * 56}" width="{w}" height="16" rx="8" fill="#CBD5E1"/>' for i, (c, w) in enumerate([("#22C55E", 210), ("#22C55E", 170), ("#F59E0B", 190)])) +
              '<circle cx="560" cy="170" r="74" fill="#FDE047"/><circle cx="534" cy="150" r="9" fill="#1E293B"/><circle cx="586" cy="150" r="9" fill="#1E293B"/><path d="M522 186 q38 36 76 0" stroke="#1E293B" stroke-width="7" fill="none" stroke-linecap="round"/>' + star(640, 86, 22, "#F97316"))

GAME_CARDS = {  # thumb key -> (colors)
    "treasure": ("#F59E0B", "#DC2626"), "space": ("#4338CA", "#0EA5E9"), "island": ("#0EA5E9", "#22C55E"), "castle": ("#7C3AED", "#DB2777"), "detective": ("#0F172A", "#6366F1"),
    "monster": ("#22C55E", "#A855F7"), "race": ("#1E3A8A", "#F97316"), "soccer": ("#16A34A", "#0EA5E9"), "four": ("#2563EB", "#F97316"), "fraction": ("#EA580C", "#F59E0B"), "array": ("#2563EB", "#14B8A6")}

# ---------------------------------------------------------------- unit icons (160 x 120)
def icon(body, tint):
    return (f'<svg width="160" height="120" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120" role="img" aria-label="Unit icon" style="font-family:{F2}"><title>Unit icon</title>'
            f'<rect width="160" height="120" fill="{tint}" rx="18"/>{body}</svg>')


def t2(x, y, s, size=20, fill="#1E293B"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="800" text-anchor="middle" fill="{fill}">{esc(s)}</text>'


UNIT_ICONS = {
    "place-value-number-sense": ("#DBEAFE", "".join(f'<rect x="{18 + i * 21}" y="34" width="19" height="52" rx="4" fill="{c}"/>' + t2(27.5 + i * 21, 67, d, 22, "#fff") for i, (d, c) in enumerate(zip("452,068".replace(",", ""), ["#1D4ED8", "#2563EB", "#3B82F6", "#0EA5E9", "#06B6D4", "#14B8A6"]))) + '<circle cx="82" cy="92" r="3" fill="#1E293B"/>'),
    "multi-digit-addition-subtraction": ("#DCFCE7", t2(92, 44, "4,768", 24) + t2(92, 72, "+ 2,595", 24) + '<line x1="34" y1="80" x2="132" y2="80" stroke="#15803D" stroke-width="4"/>' + t2(92, 104, "7,363", 24, "#15803D")),
    "multiplication-strategies": ("#FEE2E2", '<rect x="24" y="28" width="76" height="64" fill="#FCA5A5" stroke="#991B1B" stroke-width="3"/><rect x="100" y="28" width="36" height="64" fill="#FDBA74" stroke="#991B1B" stroke-width="3"/>' + t2(62, 68, "240", 20) + t2(118, 68, "42", 20) + t2(62, 22, "40", 14) + t2(118, 22, "7", 14) + t2(14, 66, "6", 14)),
    "division-remainders": ("#EDE9FE", "".join(f'<circle cx="{30 + (i % 5) * 20}" cy="{40 + (i // 5) * 20}" r="7" fill="#7C3AED"/>' for i in range(15)) + '<circle cx="134" cy="50" r="7" fill="#F59E0B"/><circle cx="134" cy="72" r="7" fill="#F59E0B"/>' + t2(80, 108, "17 ÷ 5 = 3 R 2", 15)),
    "factors-multiples-patterns": ("#CFFAFE", "".join(f'<circle cx="{28 + (i % 6) * 21}" cy="{34 + (i // 6) * 21}" r="8" fill="{"#0891B2" if (i // 6) % 2 == 0 else "#F59E0B"}"/>' for i in range(18)) + t2(80, 108, "3 × 6 = 18", 16)),
    "fractions-equivalent-fractions": ("#FCE7F3", "".join(f'<rect x="{20 + i * 40}" y="26" width="40" height="26" fill="{"#F472B6" if i < 2 else "#fff"}" stroke="#9D174D" stroke-width="2.5"/>' for i in range(3)) + "".join(f'<rect x="{20 + i * 20}" y="62" width="20" height="26" fill="{"#F9A8D4" if i < 4 else "#fff"}" stroke="#9D174D" stroke-width="2.5"/>' for i in range(6))),
    "fraction-operations-decimals": ("#FFEDD5", "".join(f'<rect x="{22 + (i % 10) * 7}" y="{22 + (i // 10) * 7}" width="7" height="7" fill="{"#FB923C" if i % 10 < 3 or (i % 10 == 3 and i // 10 < 4) else "#fff"}" stroke="#9A3412" stroke-width=".6"/>' for i in range(100)) + t2(124, 66, "0.34", 20)),
    "measurement-unit-conversions": ("#E0E7FF", '<rect x="16" y="40" width="128" height="34" rx="5" fill="#FDE68A" stroke="#92400E" stroke-width="3"/>' + "".join(f'<line x1="{24 + i * 10}" y1="40" x2="{24 + i * 10}" y2="{56 if i % 4 == 0 else 49}" stroke="#92400E" stroke-width="2"/>' for i in range(13)) + t2(80, 100, "1 ft = 12 in", 16)),
    "geometry-angles-symmetry": ("#FFE4E6", '<path d="M26 92 A60 60 0 0 1 134 92Z" fill="#fff" stroke="#9F1239" stroke-width="3"/><line x1="80" y1="92" x2="118" y2="40" stroke="#1E293B" stroke-width="4"/><line x1="80" y1="92" x2="140" y2="92" stroke="#1E293B" stroke-width="4"/><path d="M104 92 A24 24 0 0 0 94 72" stroke="#E11D48" stroke-width="3" fill="none"/>' + t2(118, 80, "55°", 14, "#9F1239")),
    "data-line-plots-word-problems": ("#DCFCE7", '<line x1="18" y1="88" x2="142" y2="88" stroke="#1E293B" stroke-width="3"/>' + "".join(f'<line x1="{28 + i * 26}" y1="83" x2="{28 + i * 26}" y2="93" stroke="#1E293B" stroke-width="2"/>' for i in range(5)) +
                                      "".join(f'<path d="M{28 + c * 26 - 6} {72 - k * 16 - 6} l12 12 m0 -12 l-12 12" stroke="#16A34A" stroke-width="3.5"/>' for c, n in enumerate([1, 3, 2, 1, 2]) for k in range(n)) + t2(80, 110, "inches", 13)),
}

# ---------------------------------------------------------------- interactive tools and projects
TOOLS = {
    "math4-place-value-blocks": ("Place-Value Blocks", "Build numbers with thousands, hundreds, tens and ones", "#2563EB", "#06B6D4",
        '<rect x="40" y="40" width="640" height="276" fill="#EFF6FF"/><rect x="80" y="110" width="110" height="110" fill="#60A5FA" stroke="#1E3A8A" stroke-width="3"/><path d="M80 110 l22 -22 h110 l-22 22z M190 110 l22 -22 v110 l-22 22z" fill="#3B82F6" stroke="#1E3A8A" stroke-width="3"/>' +
        "".join(f'<rect x="{250 + i * 62}" y="100" width="48" height="48" fill="#34D399" stroke="#065F46" stroke-width="3"/>' for i in range(3)) + "".join(f'<rect x="{250 + i * 20}" y="170" width="12" height="80" fill="#FBBF24" stroke="#92400E" stroke-width="2"/>' for i in range(5)) +
        "".join(f'<rect x="{390 + i * 20}" y="238" width="12" height="12" fill="#F472B6" stroke="#9D174D" stroke-width="2"/>' for i in range(6)) + txt(560, 190, "1,356", 54, "#1E3A8A")),
    "math4-array-area-models": ("Arrays and Area Models", "See multiplication as rows, columns and partial products", "#DC2626", "#F59E0B",
        '<rect x="40" y="40" width="640" height="276" fill="#FEF2F2"/><rect x="100" y="90" width="260" height="170" fill="#FCA5A5" stroke="#7F1D1D" stroke-width="4"/><rect x="360" y="90" width="110" height="170" fill="#FDBA74" stroke="#7F1D1D" stroke-width="4"/>' + txt(230, 188, "6 × 20", 36) + txt(415, 188, "6 × 7", 30) + txt(230, 78, "20", 26) + txt(415, 78, "7", 26) + txt(76, 186, "6", 26) + txt(570, 188, "= 162", 44, "#B91C1C")),
    "math4-division-groups": ("Division: Groups and Arrays", "Share counters into equal groups and see the remainder", "#7C3AED", "#EC4899",
        '<rect x="40" y="40" width="640" height="276" fill="#F5F3FF"/>' + "".join(f'<rect x="{80 + g * 140}" y="90" width="120" height="130" rx="18" fill="#fff" stroke="#7C3AED" stroke-width="4"/>' + dots(104 + g * 140, 118, 2, 3, 36, "#7C3AED") for g in range(3)) + dots(540, 140, 1, 2, 40, "#F59E0B") + txt(360, 276, "20 ÷ 3 = 6 R 2", 36, "#5B21B6")),
    "math4-equivalent-fractions": ("Equivalent Fraction Models", "Cut the same whole into more pieces and compare", "#DB2777", "#F97316",
        '<rect x="40" y="40" width="640" height="276" fill="#FDF2F8"/>' + "".join(f'<rect x="{120 + i * 160}" y="84" width="160" height="70" fill="{"#F472B6" if i < 2 else "#fff"}" stroke="#831843" stroke-width="4"/>' for i in range(3)) +
        "".join(f'<rect x="{120 + i * 80}" y="186" width="80" height="70" fill="{"#F9A8D4" if i < 4 else "#fff"}" stroke="#831843" stroke-width="4"/>' for i in range(6)) + frac(660 - 30, 110, 2, 3, 26) + frac(660 - 30, 212, 4, 6, 26)),
    "math4-fraction-number-line": ("Fraction Number Line", "Place fractions and mixed numbers; jump by unit fractions", "#0891B2", "#22C55E",
        '<rect x="40" y="40" width="640" height="276" fill="#ECFEFF"/><line x1="90" y1="210" x2="630" y2="210" stroke="#0F172A" stroke-width="5"/>' + "".join(f'<line x1="{110 + i * 62.5}" y1="{196 if i % 4 else 186}" x2="{110 + i * 62.5}" y2="{224 if i % 4 else 234}" stroke="#0F172A" stroke-width="{3 if i % 4 else 5}"/>' for i in range(9)) +
        txt(110, 268, "0", 28) + txt(360, 268, "1", 28) + txt(610, 268, "2", 28) + '<path d="M110 200 Q141 130 172.5 200 M172.5 200 Q204 130 235 200 M235 200 Q266 130 297.5 200" stroke="#F97316" stroke-width="5" fill="none"/><circle cx="297.5" cy="210" r="12" fill="#DB2777"/>' + frac(297, 110, 3, 4, 30, "#BE185D")),
    "math4-decimal-grids": ("Decimal Grids", "Shade tenths and hundredths; read the decimal and the fraction", "#EA580C", "#FACC15",
        '<rect x="40" y="40" width="640" height="276" fill="#FFF7ED"/>' + "".join(f'<rect x="{110 + (i % 10) * 20}" y="{78 + (i // 10) * 20}" width="20" height="20" fill="{"#FB923C" if i % 10 < 4 or (i % 10 == 4 and i // 10 < 7) else "#fff"}" stroke="#7C2D12" stroke-width="1.5"/>' for i in range(100)) + txt(480, 160, "0.47", 64, "#C2410C") + frac(480, 236, 47, 100, 30)),
    "math4-angle-explorer": ("Angle Explorer", "Turn a ray, read the protractor and name the angle", "#E11D48", "#F59E0B",
        '<rect x="40" y="40" width="640" height="276" fill="#FFF1F2"/><path d="M160 280 A200 200 0 0 1 560 280Z" fill="#fff" stroke="#9F1239" stroke-width="4"/>' + "".join(f'<line x1="{360 + 200 * math.cos(math.radians(a)):.1f}" y1="{280 - 200 * math.sin(math.radians(a)):.1f}" x2="{360 + 182 * math.cos(math.radians(a)):.1f}" y2="{280 - 182 * math.sin(math.radians(a)):.1f}" stroke="#9F1239" stroke-width="2"/>' for a in range(0, 181, 10)) +
        '<line x1="360" y1="280" x2="600" y2="280" stroke="#0F172A" stroke-width="7"/><line x1="360" y1="280" x2="490" y2="88" stroke="#0F172A" stroke-width="7"/><path d="M420 280 A60 60 0 0 0 394 230" stroke="#E11D48" stroke-width="6" fill="none"/>' + txt(456, 252, "56°", 34, "#BE123C")),
    "math4-area-perimeter": ("Area and Perimeter Explorer", "Stretch a rectangle; watch area and perimeter change", "#4F46E5", "#22C55E",
        '<rect x="40" y="40" width="640" height="276" fill="#EEF2FF"/>' + "".join(f'<rect x="{110 + (i % 7) * 44}" y="{84 + (i // 7) * 44}" width="44" height="44" fill="#A5B4FC" stroke="#3730A3" stroke-width="2"/>' for i in range(28)) + '<rect x="110" y="84" width="308" height="176" fill="none" stroke="#16A34A" stroke-width="7"/>' + txt(548, 150, "A = 28", 38, "#3730A3") + txt(548, 210, "P = 22", 38, "#15803D")),
    "math4-symmetry-shapes": ("Symmetry and Shapes", "Fold shapes on a line and sort them by their properties", "#9333EA", "#06B6D4",
        '<rect x="40" y="40" width="640" height="276" fill="#FAF5FF"/><polygon points="230,80 330,170 280,280 180,280 130,170" fill="#D8B4FE" stroke="#581C87" stroke-width="5"/><line x1="230" y1="56" x2="230" y2="304" stroke="#DB2777" stroke-width="5" stroke-dasharray="12 9"/>'
        '<polygon points="420,110 600,110 560,250 380,250" fill="#67E8F9" stroke="#155E75" stroke-width="5"/><path d="M500 104 l12 6 l-12 6 M470 244 l12 6 l-12 6" stroke="#DB2777" stroke-width="4" fill="none"/>'),
}
PROJECT_SCENES = {
    "math4-project-city-population-report": ("#2563EB", "#14B8A6", '<rect x="40" y="40" width="640" height="276" fill="#E0F2FE"/>' + "".join(f'<rect x="{90 + i * 80}" y="{240 - h}" width="60" height="{h + 30}" fill="{c}"/>' for i, (h, c) in enumerate([(120, "#3B82F6"), (70, "#22C55E"), (160, "#F97316"), (100, "#A855F7"), (50, "#EC4899")])) + txt(590, 130, "452,068", 40) + txt(590, 180, "≈ 450,000", 30, "#0369A1")),
    "math4-project-school-fundraiser-ledger": ("#16A34A", "#84CC16", '<rect x="40" y="40" width="640" height="276" fill="#F0FDF4"/><rect x="130" y="70" width="280" height="216" rx="14" fill="#fff" stroke="#15803D" stroke-width="5"/>' + txt(270, 120, "$4,768", 34) + txt(270, 168, "+ $2,595", 34) + '<line x1="170" y1="184" x2="370" y2="184" stroke="#15803D" stroke-width="4"/>' + txt(270, 232, "$7,363", 38, "#15803D") + '<circle cx="540" cy="170" r="70" fill="#FDE047" stroke="#A16207" stroke-width="6"/>' + txt(540, 190, "$", 70, "#A16207")),
    "math4-project-design-a-theater": ("#DC2626", "#7C3AED", '<rect x="40" y="40" width="640" height="276" fill="#FEF2F2"/><path d="M60 60 h600 v60 q-300 60 -600 0z" fill="#B91C1C"/>' + "".join(f'<rect x="{150 + c * 44}" y="{150 + r * 36}" width="34" height="26" rx="8" fill="{"#7C3AED" if c < 6 else "#F59E0B"}"/>' for r in range(4) for c in range(10)) + txt(600, 230, "24 × 18", 28)),
    "math4-project-party-planner": ("#7C3AED", "#EC4899", '<rect x="40" y="40" width="640" height="276" fill="#FAF5FF"/>' + "".join(f'<ellipse cx="{120 + i * 90}" cy="{120 + (i % 2) * 20}" rx="34" ry="44" fill="{c}"/><line x1="{120 + i * 90}" y1="{164 + (i % 2) * 20}" x2="{124 + i * 90}" y2="250" stroke="#64748B" stroke-width="3"/>' for i, c in enumerate(["#F472B6", "#60A5FA", "#FBBF24", "#34D399", "#A78BFA", "#FB923C"])) + txt(360, 290, "50 guests ÷ 8 per table = 6 R 2", 28)),
    "math4-project-pattern-quilt": ("#0891B2", "#A855F7", '<rect x="40" y="40" width="640" height="276" fill="#ECFEFF"/>' + "".join(f'<rect x="{190 + c * 56}" y="{66 + r * 56}" width="56" height="56" fill="{["#06B6D4", "#F59E0B", "#A855F7"][(r + c) % 3]}" stroke="#fff" stroke-width="4"/>' + (f'<polygon points="{218 + c * 56},{76 + r * 56} {236 + c * 56},{112 + r * 56} {200 + c * 56},{112 + r * 56}" fill="#fff" opacity=".8"/>' if (r + c) % 3 == 1 else "") for r in range(4) for c in range(6))),
    "math4-project-fraction-pizza-shop": ("#EA580C", "#DC2626", '<rect x="40" y="40" width="640" height="276" fill="#FFF7ED"/><circle cx="250" cy="178" r="110" fill="#FDBA74" stroke="#9A3412" stroke-width="8"/>' + "".join(f'<line x1="250" y1="178" x2="{250 + 110 * math.cos(math.pi * i / 4):.1f}" y2="{178 + 110 * math.sin(math.pi * i / 4):.1f}" stroke="#9A3412" stroke-width="4"/>' for i in range(8)) + "".join(f'<circle cx="{250 + 60 * math.cos(a):.1f}" cy="{178 + 60 * math.sin(a):.1f}" r="12" fill="#DC2626"/>' for a in [0.4, 1.2, 2.0, 2.8, 3.6, 4.4, 5.2, 6.0]) + frac(480, 150, 3, 8, 44) + txt(560, 170, "<", 50) + frac(630, 150, 1, 2, 44)),
    "math4-project-recipe-for-a-crowd": ("#F59E0B", "#EF4444", '<rect x="40" y="40" width="640" height="276" fill="#FFFBEB"/><path d="M150 150 h240 l-30 120 h-180z" fill="#fff" stroke="#92400E" stroke-width="6"/><ellipse cx="270" cy="150" rx="120" ry="24" fill="#FDE68A" stroke="#92400E" stroke-width="6"/>' + txt(520, 140, "4 ×", 44) + frac(610, 120, 3, 4, 44) + txt(540, 240, "= 3 cups", 40, "#B45309")),
    "math4-project-playground-blueprint": ("#4F46E5", "#22C55E", '<rect x="40" y="40" width="640" height="276" fill="#1E3A8A"/>' + "".join(f'<line x1="{40 + i * 40}" y1="40" x2="{40 + i * 40}" y2="316" stroke="#fff" opacity=".15"/>' for i in range(17)) + "".join(f'<line x1="40" y1="{40 + i * 40}" x2="680" y2="{40 + i * 40}" stroke="#fff" opacity=".15"/>' for i in range(8)) +
        '<rect x="120" y="80" width="240" height="160" fill="none" stroke="#fff" stroke-width="5"/><rect x="400" y="120" width="200" height="120" fill="none" stroke="#FDE047" stroke-width="5"/>' + txt(240, 170, "12 m × 8 m", 26, "#fff") + txt(500, 190, "A = 60", 26, "#FDE047")),
    "math4-project-angle-art-studio": ("#E11D48", "#F59E0B", '<rect x="40" y="40" width="640" height="276" fill="#FFF1F2"/>' + "".join(f'<line x1="360" y1="178" x2="{360 + 130 * math.cos(math.radians(a)):.1f}" y2="{178 - 130 * math.sin(math.radians(a)):.1f}" stroke="{c}" stroke-width="10" stroke-linecap="round"/>' for a, c in zip(range(0, 360, 30), ["#E11D48", "#F97316", "#F59E0B", "#84CC16", "#22C55E", "#14B8A6", "#06B6D4", "#3B82F6", "#6366F1", "#8B5CF6", "#D946EF", "#EC4899"])) + '<circle cx="360" cy="178" r="16" fill="#1E293B"/>' + txt(590, 100, "30°", 40, "#BE123C")),
    "math4-project-class-measurement-survey": ("#16A34A", "#0EA5E9", '<rect x="40" y="40" width="640" height="276" fill="#F0FDF4"/><line x1="100" y1="250" x2="620" y2="250" stroke="#0F172A" stroke-width="5"/>' + "".join(f'<line x1="{120 + i * 60}" y1="240" x2="{120 + i * 60}" y2="260" stroke="#0F172A" stroke-width="4"/>' for i in range(9)) +
        "".join(f'<path d="M{120 + c * 60 - 14} {220 - k * 40 - 14} l28 28 m0 -28 l-28 28" stroke="#16A34A" stroke-width="8" stroke-linecap="round"/>' for c, n in enumerate([1, 2, 4, 3, 1, 0, 2, 1, 1]) for k in range(n))),
}
PROJECT_TITLES = {}


# ---------------------------------------------------------------- the four shared generators (staging class page cards)
def _page(x, y, w=150, h=196, fill="#fff"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#1E293B" stroke-width="4"/>'


def _lines(x, y, n, w=110, gap=22, col="#94A3B8"):
    return "".join(f'<rect x="{x}" y="{y + i * gap}" width="{w - (i % 3) * 18}" height="7" rx="3.5" fill="{col}"/>' for i in range(n))


GENERATORS = {
    "math4-generator-lesson": ("Lesson Plan Generator", "Notes, worked examples and practice to print.", "#2563EB", "#10B981",
        _page(150, 74) + '<rect x="150" y="74" width="150" height="34" rx="10" fill="#2563EB"/>' + txt(225, 98, "Notes", 20, "#fff") + _lines(170, 126, 6) +
        _page(330, 74) + '<rect x="330" y="74" width="150" height="34" rx="10" fill="#10B981"/>' + txt(405, 98, "Examples", 20, "#fff") + txt(405, 150, "24 × 3", 26) + '<path d="M352 166 h106" stroke="#1E293B" stroke-width="3"/>' + txt(405, 198, "72", 28, "#DC2626") + _lines(350, 222, 2) +
        _page(510, 74) + '<rect x="510" y="74" width="150" height="34" rx="10" fill="#F59E0B"/>' + txt(585, 98, "Practice", 20, "#fff") + "".join(txt(532, 140 + i * 30, f"{i + 1}.", 20, anchor="start") + f'<rect x="562" y="{126 + i * 30}" width="76" height="6" rx="3" fill="#94A3B8"/>' for i in range(4))),
    "math4-generator-worksheet": ("Worksheet Generator", "Pick skills, level and work space.", "#0D9488", "#84CC16",
        _page(210, 60, 300, 230) + txt(360, 96, "Name ____________", 20, "#475569") + "".join(txt(236, 142 + i * 44, f"{i + 1}.", 22, anchor="start") + txt(292, 142 + i * 44, ["36 + 47", "8 × 7", "125 ÷ 5"][i], 24, anchor="start") + f'<rect x="420" y="{120 + i * 44}" width="64" height="30" rx="6" fill="#ECFDF5" stroke="#0D9488" stroke-width="3"/>' for i in range(3)) +
        '<path d="M560 110 l34 -34 l22 22 l-34 34 l-30 8 z" fill="#FACC15" stroke="#1E293B" stroke-width="4"/>'),
    "math4-generator-assessment": ("Assessment Generator", "Quizzes and tests with answer keys.", "#EA580C", "#DB2777",
        _page(230, 60, 260, 230) + txt(360, 98, "Unit Check", 24) + "".join(f'<circle cx="262" cy="{134 + i * 36}" r="11" fill="{"#16A34A" if i == 1 else "#fff"}" stroke="#1E293B" stroke-width="3.5"/>' + f'<rect x="290" y="{129 + i * 36}" width="{150 - i * 16}" height="9" rx="4.5" fill="#94A3B8"/>' for i in range(4)) +
        '<circle cx="548" cy="118" r="44" fill="#DCFCE7" stroke="#16A34A" stroke-width="6"/><path d="M526 118 l16 18 l30 -36" fill="none" stroke="#16A34A" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'),
    "math4-generator-activity": ("Activity Generator", "Mazes, puzzles, stations and more.", "#7C3AED", "#0EA5E9",
        "".join(f'<rect x="{150 + c * 56}" y="{70 + r_ * 56}" width="56" height="56" fill="{"#FDE68A" if (r_, c) in ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3)) else "#fff"}" stroke="#1E293B" stroke-width="3"/>' for r_ in range(4) for c in range(4)) +
        txt(178, 108, "Go", 20) + txt(346, 276, "End", 18) + '<polygon points="470,270 560,110 650,270" fill="#DDD6FE" stroke="#1E293B" stroke-width="4"/><polygon points="515,190 605,190 560,270" fill="#A7F3D0" stroke="#1E293B" stroke-width="4"/>' + txt(560, 180, "6×4", 20) + txt(560, 230, "24", 22)),
}


def main():
    os.makedirs(T, exist_ok=True)
    games = json.load(open(os.path.join(HERE, "games.json"), encoding="utf-8"))["games"]
    n = 0
    for g in games:
        c1, c2 = GAME_CARDS[g["thumb"]]
        open(os.path.join(T, f"math4-game-{g['thumb']}.svg"), "w", encoding="utf-8").write(card(g["title"], short(g["description"].split(".")[0] + "."), c1, c2, S[g["thumb"]]))
        n += 1
    for slug, (title, tag, c1, c2, scene) in GENERATORS.items():
        open(os.path.join(T, slug + ".svg"), "w", encoding="utf-8").write(card(title, tag, c1, c2, scene))
        n += 1
    open(os.path.join(T, "math4-flashcards.svg"), "w", encoding="utf-8").write(card("Flashcards", "Words, key facts, pictures and big ideas.", "#10B981", "#0EA5E9", S["flashcards"]))
    open(os.path.join(T, "math4-understanding-check.svg"), "w", encoding="utf-8").write(card("Understanding Check", "Show what you know. Hints and worked solutions.", "#0EA5E9", "#6366F1", S["check"]))
    n += 2
    for uid, (tint, body) in UNIT_ICONS.items():
        open(os.path.join(T, f"math4-unit-{uid}.svg"), "w", encoding="utf-8").write(icon(body, tint))
        n += 1
    for slug, (title, tag, c1, c2, scene) in TOOLS.items():
        open(os.path.join(T, slug + ".svg"), "w", encoding="utf-8").write(card(title, tag, c1, c2, scene))
        n += 1
    reg = os.path.join(HERE, "projects", "projects-registry.json")
    if os.path.exists(reg):
        for key, lst in json.load(open(reg, encoding="utf-8")).items():
            for p in lst:
                c1, c2, scene = PROJECT_SCENES[p["folder"]]
                open(os.path.join(T, p["folder"] + ".svg"), "w", encoding="utf-8").write(card("Project: " + p["title"], p["theme"], c1, c2, scene))
                n += 1
    print(n, "thumbnails written")


if __name__ == "__main__":
    main()
