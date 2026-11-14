"""Unit 10: Telling Time (telling-time). 1.MD.B.3. Hours and half hours only."""
from g1lib import *

UNIT_ID = "telling-time"


def hr(r):
    return r.randint(1, 12)


def nx(h):
    return h % 12 + 1


def pv(h):
    return 12 if h == 1 else h - 1


def tstr(h, m):
    return f"{h}:{m:02d}"


def say(h, m):
    return f"{h} o'clock" if m == 0 else f"half past {h}"


def time_w(h, m):
    out = [W(tstr(nx(h), m), "read the next hour" if m == 30 else "counted one hour too many"), W(tstr(h, 30 if m == 0 else 0), "mixed up o'clock and half past")]
    if m == 0:
        out.append(W(tstr(12, h * 5 % 60) if h != 12 else "3:00", "mixed up the hour hand and the minute hand"))
    else:
        out.append(W(tstr(h, 6) if h != 6 else "6:06", "read the minute hand number as minutes"))
    out.append(W(tstr(pv(h), m), "counted one hour too few"))
    return out


def clock_d(h, m):
    alt = f"Analog clock. The short hour hand points {'to the ' + str(h) if m == 0 else 'halfway between the ' + str(h) + ' and the ' + str(nx(h))}. The long minute hand points to the {12 if m == 0 else 6}."
    return Diagram("clock", {"h": h, "m": m}, alt)


# ============================================================== S1 Time to the Hour
@fam("012")
def h_read(r, L):
    h = hr(r)
    if L == 0:
        need(h in (1, 2, 3, 4, 5, 6, 7, 8, 9))
    return Item(pick(r, ["What time does the clock show? Write it like a digital clock.", "Write the time shown on the clock.", "What time is it?"]), tstr(h, 0),
                [f"The short hand points to {h}. The long hand points to 12.", f"It is {say(h, 0)}, written {tstr(h, 0)}."], time_w(h, 0),
                FN("clock", h=h, m=0), qtype="visual", diagram=clock_d(h, 0))


@fam("012", mode="mc")
def h_words(r, L):
    h = hr(r)
    good = say(h, 0)
    bad = [say(nx(h), 0), say(h, 30), f"12 o'clock" if h != 12 else "6 o'clock"]
    it = mc_key(pick(r, ["What time does the clock show?", "Which time matches the clock?"]), good, bad,
                [f"The short hand points to {h} and the long hand to 12.", f"It is {good}."], qtype="visual", diagram=clock_d(h, 0), r=r)
    it.check = FN("clock_say", h=h, m=0)
    return it


@fam("012")
def h_digital(r, L):
    h = hr(r)
    alt = f"Digital clock showing {tstr(h, 0)}."
    return Item(pick(r, ["The digital clock shows a time. Write it in words, like 4 o'clock.", "Say the time on the digital clock in words."]), say(h, 0),
                [f"{tstr(h, 0)} means {h} hours and 0 minutes.", f"It is {say(h, 0)}."],
                [W(say(nx(h), 0), "read the wrong hour"), W(say(h, 30), "mixed up o'clock and half past"), W("0 o'clock", "read the minutes as the hour")],
                FN("clock_say", h=h, m=0), qtype="visual", diagram=Diagram("digital", {"h": h, "m": 0}, alt))


@fam("012", mode="mc")
def h_hand(r, L):
    h = hr(r)
    hand = pick(r, ["hour", "minute"]) if L else "hour"
    if hand == "hour":
        good = f"At the {h}"
        bad = [f"At the {nx(h)}", "At the 12" if h != 12 else "At the 6", f"Between the {h} and the {nx(h)}"]
        it = mc_key(f"At {say(h, 0)}, where does the short hour hand point?", good, bad, ["At o'clock times the hour hand points right at the hour.", good], qtype="conceptual", r=r)
        it.check = FN("hour_hand", h=h, m=0)
        return it
    good = "At the 12"
    bad = [f"At the {h}" if h != 12 else "At the 6", "At the 6" if h != 6 else "At the 3", f"At the {nx(h)}"]
    return mc_key(f"At {say(h, 0)}, where does the long minute hand point?", good, bad, ["At o'clock times the minute hand points to the 12.", good], qtype="conceptual", r=r)


@fam("012")
def h_story(r, L):
    h = r.randint(7, 12) if L == 0 else hr(r)
    ev = pick(r, ["The game starts", "The party starts", "The movie starts", "Swim class starts", "Story time starts", "The puppet show starts", "The race starts"])
    if L < 2:
        return Item(f"{ev} at {say(h, 0)}. Write the time like a digital clock.", tstr(h, 0), [f"{say(h, 0)} means {h} hours and 0 minutes.", f"It is written {tstr(h, 0)}."],
                    time_w(h, 0), FN("clock", h=h, m=0), qtype="word-problem")
    return Item(f"{ev} at {say(h, 0)}. It lasts 1 hour. What time does it end? Write it like a digital clock.", tstr(nx(h), 0),
                [f"1 hour after {say(h, 0)} is {say(nx(h), 0)}.", f"It ends at {tstr(nx(h), 0)}."],
                [W(tstr(h, 0), "gave the start time"), W(tstr(h, 30), "added half an hour"), W(tstr(nx(nx(h)), 0), "added 2 hours")],
                FN("later_time", h=h, m=0, add=60), qtype="word-problem")


@fam("0")
def h_which_clock(r, L):
    h = hr(r)
    good = tstr(h, 0)
    bad = [tstr(nx(h), 0), tstr(h, 30), tstr(12, 0) if h != 12 else "6:00"]
    it = mc_key(f"Which digital time means {say(h, 0)}?", good, bad, [f"{say(h, 0)} has 0 minutes.", f"It is {good}."], qtype="procedural", r=r)
    it.check = FN("clock", h=h, m=0)
    return it


# ============================================================== S2 Time to the Half Hour
@fam("012")
def hh_read(r, L):
    h = hr(r)
    return Item(pick(r, ["What time does the clock show? Write it like a digital clock.", "Write the time shown on the clock.", "What time is it?"]), tstr(h, 30),
                [f"The hour hand is between {h} and {nx(h)}, so the hour is {h}. The minute hand points to 6, which means 30 minutes.", f"It is {say(h, 30)}, or {tstr(h, 30)}."],
                time_w(h, 30), FN("clock", h=h, m=30), qtype="visual", diagram=clock_d(h, 30))


@fam("012", mode="mc")
def hh_words(r, L):
    h = hr(r)
    good = say(h, 30)
    bad = [say(nx(h), 30), say(h, 0), say(nx(h), 0)]
    it = mc_key(pick(r, ["What time does the clock show?", "Which time matches the clock?"]), good, bad,
                [f"The hour hand has passed {h}. The minute hand points to 6.", f"It is {good}."], qtype="visual", tags={"misconception"}, diagram=clock_d(h, 30), r=r)
    it.check = FN("clock_say", h=h, m=30)
    return it


@fam("012")
def hh_digital(r, L):
    h = hr(r)
    alt = f"Digital clock showing {tstr(h, 30)}."
    return Item(pick(r, ["The digital clock shows a time. Write it in words, like half past 4.", "Say the time on the digital clock in words."]), say(h, 30),
                [f"{tstr(h, 30)} means 30 minutes after {h}.", f"It is {say(h, 30)}."],
                [W(say(nx(h), 30), "read the next hour"), W(say(h, 0), "left out the half hour"), W("half past 30", "read the minutes as the hour")],
                FN("clock_say", h=h, m=30), qtype="visual", diagram=Diagram("digital", {"h": h, "m": 30}, alt))


@fam("012", mode="mc")
def hh_hand(r, L):
    h = hr(r)
    hand = pick(r, ["hour", "minute"]) if L else "minute"
    if hand == "hour":
        good = f"Between the {h} and the {nx(h)}"
        bad = [f"At the {h}", f"At the {nx(h)}", f"Between the {pv(h)} and the {h}"]
        it = mc_key(f"At {say(h, 30)}, where does the short hour hand point?", good, bad, ["At half past, the hour hand is halfway to the next hour.", good],
                    qtype="conceptual", tags={"misconception"}, r=r)
        it.check = FN("hour_hand", h=h, m=30)
        return it
    good = "At the 6"
    bad = ["At the 12", f"At the {h}" if h != 6 else "At the 3", "At the 3" if h != 3 else "At the 9"]
    return mc_key(f"At {say(h, 30)}, where does the long minute hand point?", good, bad, ["Half past means 30 minutes; the minute hand points to 6.", good], qtype="conceptual", r=r)


@fam("12")
def hh_mixed(r, L):
    h = hr(r)
    m = pick(r, [0, 30])
    return Item(pick(r, ["Read the clock. Write the time like a digital clock.", "What time is shown? Write it with numbers."]), tstr(h, m),
                [("The hour hand points to " + str(h)) if m == 0 else f"The hour hand is past {h}", f"It is {tstr(h, m)}."], time_w(h, m),
                FN("clock", h=h, m=m), qtype="visual", diagram=clock_d(h, m))


@fam("012", mode="mc")
def hh_which(r, L):
    h = hr(r)
    good = tstr(h, 30)
    bad = [tstr(nx(h), 30), tstr(h, 0), tstr(h, 3) if L else tstr(h, 6)]
    it = mc_key(f"Which digital time means {say(h, 30)}?", good, bad, [f"Half past {h} is 30 minutes after {h}.", f"It is {good}."], qtype="procedural", r=r)
    it.check = FN("clock", h=h, m=30)
    return it


# ============================================================== S3 Matching and Using Clock Times
@fam("012", mode="mc")
def u_match(r, L):
    h = hr(r)
    m = pick(r, [0, 30])
    good = tstr(h, m)
    bad = [x for x, _ in time_w(h, m)][:3]
    it = mc_key("Which digital clock time matches the clock?", good, bad, [f"Read the hour hand, then the minute hand.", f"The clock shows {good}."],
                qtype="visual", diagram=clock_d(h, m), r=r)
    it.check = FN("clock", h=h, m=m)
    return it


@fam("012")
def u_later(r, L):
    h = hr(r)
    m = pick(r, [0, 30]) if L else 0
    add = 60 if L == 0 else pick(r, [60, 30]) if L == 1 else pick(r, [30, 60, 90])
    word = {30: "half an hour", 60: "1 hour", 90: "1 hour and a half"}[add]
    tot = (h % 12) * 60 + m + add
    hh, mm = divmod(tot % 720, 60)
    hh = 12 if hh == 0 else hh
    return Item(f"It is {tstr(h, m)}. What time will it be in {word}? Write it like a digital clock.", tstr(hh, mm),
                [f"Start at {tstr(h, m)} and move ahead {word}.", f"The time will be {tstr(hh, mm)}."],
                [W(tstr(h, m), "did not move ahead"), W(tstr(h, (m + 30) % 60) if add != 30 else tstr(nx(h), m), "moved the wrong amount"), W(tstr(hh, 30 - mm if mm in (0, 30) else 0), "mixed up o'clock and half past")],
                FN("later_time", h=h, m=m, add=add), qtype="word-problem", tags={"modeling"})


@fam("2")
def u_earlier(r, L):
    h = hr(r)
    m = pick(r, [0, 30])
    back = pick(r, [30, 60])
    word = {30: "half an hour", 60: "1 hour"}[back]
    tot = (h % 12) * 60 + m - back
    hh, mm = divmod(tot % 720, 60)
    hh = 12 if hh == 0 else hh
    return Item(f"Recess ends at {tstr(h, m)}. It started {word} earlier. What time did recess start?", tstr(hh, mm),
                [f"Go back {word} from {tstr(h, m)}.", f"Recess started at {tstr(hh, mm)}."],
                [W(tstr(h, m), "gave the end time"), W(tstr(nx(h), m), "went forward instead of back"), W(tstr(hh, 30 - mm), "moved the wrong amount")],
                FN("later_time", h=h, m=m, add=-back), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def u_first(r, L):
    h = r.randint(1, 11)
    n1, n2 = r.sample(NAMES, 2)
    opts = [(h, 0), (h, 30), (h + 1, 0)]
    x, y = r.sample(opts, 2)
    if r.random() < 0.5:
        x, y = y, x
    t1, t2 = tstr(*x), tstr(*y)
    first = n1 if x[0] * 60 + x[1] < y[0] * 60 + y[1] else n2
    good = first
    bad = [n2 if first == n1 else n1, "They start at the same time.", "You cannot tell."]
    return mc_key(f"{n1} starts reading at {t1}. {n2} starts reading at {t2}. Who starts first?", good, bad,
                  ["Compare the hours first, then the minutes.", f"{good} starts first."], qtype="reasoning", r=r)


@fam("012")
def u_clock_story(r, L):
    h = r.randint(1, 11)
    m = pick(r, [0, 30]) if L else 0
    add = 60 if L < 2 else pick(r, [30, 60])
    word = {30: "half an hour", 60: "1 hour"}[add]
    tot = h * 60 + m + add
    hh, mm = divmod(tot % 720, 60)
    hh = 12 if hh == 0 else hh
    return Item(f"The clock shows the time the game starts. The game lasts {word}. What time does it end? Write it like a digital clock.", tstr(hh, mm),
                [f"The clock shows {tstr(h, m)}.", f"{word} later is {tstr(hh, mm)}."],
                [W(tstr(h, m), "gave the start time"), W(tstr(nx(hh), mm), "added too much time"), W(tstr(hh, 30 - mm), "mixed up o'clock and half past")],
                FN("later_time", h=h, m=m, add=add), qtype="visual", diagram=clock_d(h, m))


@fam("012", mode="mc")
def u_same(r, L):
    h = hr(r)
    m = pick(r, [0, 30])
    good = say(h, m)
    bad = [say(nx(h), m), say(h, 30 - m), say(pv(h), m)]
    it = mc_key(f"Which words mean the same as {tstr(h, m)}?", good, bad, [f"{tstr(h, m)} is {h} hours and {m} minutes.", f"It is {good}."], qtype="procedural", r=r)
    it.check = FN("clock_say", h=h, m=m)
    return it


SKILLS = {
    1: dict(name="Time to the Hour", fams=[h_read, h_words, h_digital, h_hand, h_story, h_which_clock]),
    2: dict(name="Time to the Half Hour", fams=[hh_read, hh_words, hh_digital, hh_hand, hh_mixed, hh_which]),
    3: dict(name="Matching and Using Clock Times", fams=[u_match, u_later, u_earlier, u_first, u_clock_story, u_same]),
}
