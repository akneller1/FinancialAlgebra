"""Registry shared by the Grade 1–3 Interactive Math tool definitions (tools_g1.py, tools_g2.py, tools_g3.py)."""
TOOLS = []
COURSES = {1: ("grade1", "1st Grade Math"), 2: ("grade2", "2nd Grade Math"), 3: ("grade3", "3rd Grade Math")}


def tool(grade, slug, units, title, description, intro, topics, standards, body, script, worksheet, notice, teacher):
    """slug without the mathN- prefix. units: unit ids (first one is the Back link). worksheet: 7 (question, answer) pairs;
    the last one is the Reflect question. script: JS run inside an IIFE with T = TOOL, $ = T.$, K = ELK and META (pass to
    T.init) in scope; engine tools call ELK.*Tool(Object.assign({}, META, …)) instead of T.init."""
    assert len(worksheet) == 7, slug
    TOOLS.append(dict(grade=grade, slug=f"math{grade}-{slug}", units=units, title=title, description=description, intro=intro,
                      topics=topics, standards=standards, body=body, script=script, worksheet=worksheet, notice=notice, teacher=teacher))
