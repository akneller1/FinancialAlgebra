"""Unit 10: Time and Money (time-money). 2.MD.C.7, 2.MD.C.8.
Money: amounts under a dollar are written with ¢ (45¢); whole-dollar amounts with $ ($13); amounts with both are written
as dollars and cents ($3 and 45¢), so no decimal notation is needed in Grade 2."""
from g2lib import *

UNIT_ID = "time-money"


def tm5(r, L):
    h = r.randint(1, 12)
    m = 5 * r.randint(1, 11) if L else 5 * pick(r, [0, 3, 6, 9, 1, 2, 4, 8])
    return h, m


def clock_d(h, m):
    alt = f"An analog clock. The hour hand is {'on the ' + str(h) if m == 0 else 'between the ' + str(h) + ' and the ' + str(h % 12 + 1)}. The minute hand points to the {m // 5 if m else 12}."
    return Diagram("clock", {"h": h, "m": m}, alt)


def time_w(h, m):
    out = [W(tm(h, m // 5) if m // 5 != m else tm(h, m + 5) if m < 55 else tm(h, 0), "read the minute hand as the number it points to"),
           W(tm(m // 5 if m else 12, h * 5 if h * 5 < 60 else 0), "mixed up the hour hand and the minute hand"),
           W(tm(h % 12 + 1, m), "read the next hour") if m >= 30 else W(tm(h - 1 if h > 1 else 12, m), "read the hour before")]
    return out


# ============================================================== S1 Telling Time to Five Minutes
@fam("012")
def tm_read(r, L):
    h, m = tm5(r, L)
    need(not (m // 5 == h))
    return Item("What time does the clock show?", tm(h, m), [f"The hour hand is {'on' if m == 0 else 'just past'} the {h}. The minute hand is on the {m // 5 if m else 12}.", f"Count by 5s: {m} minutes. The time is {tm(h, m)}."],
                time_w(h, m), FN("clock", h=h, m=m), qtype="visual", diagram=clock_d(h, m))


@fam("012")
def tm_minutes(r, L):
    k = r.randint(1, 11)
    return Item(f"The minute hand points to the {k}. How many minutes after the hour is it?", f"{5 * k} minutes", [f"Count by 5s from the 12 to the {k}.", f"{k} jumps of 5 is {5 * k} minutes."],
                [W(f"{k} minutes", "read the number instead of counting by 5s"), W(f"{5 * k + 5} minutes", "counted one extra 5"), W(f"{10 * k} minutes", "counted by 10s")],
                FN("min_after", hand=k, unit="minutes"), qtype="conceptual", claim=f"Minutes after the hour when the minute hand points to the {k}")


@fam("012")
def tm_point(r, L):
    h, m = tm5(r, L)
    need(m)
    alt = f"A digital clock showing {tm(h, m)}."
    return Item(f"The digital clock shows {tm(h, m)}. On an analog clock, which number does the minute hand point to?", m // 5,
                [f"Each number on the clock is 5 minutes.", f"{m} minutes is {m // 5} jumps of 5, so the minute hand points to the {m // 5}."],
                [W(m if m <= 12 else m // 10, "used the minutes as the number"), W(h, "gave the hour"), W(m // 5 + 1, "counted one extra 5")],
                FN("min_point", m=m), qtype="visual", diagram=Diagram("digital", {"h": h, "m": m}, alt))


@fam("012", mode="mc")
def tm_mc(r, L):
    h, m = tm5(r, L)
    need(m // 5 != h)
    return Item("What time does the clock show?", tm(h, m), [f"Hour hand: {h}. Minute hand: {m} minutes.", f"The time is {tm(h, m)}."], time_w(h, m) + [W(tm(h, (m + 5) % 60), "counted one extra 5")],
                FN("clock", h=h, m=m), qtype="visual", diagram=clock_d(h, m), mode="mc")


@fam("012")
def tm_words(r, L):
    h = r.randint(1, 12)
    k = pick(r, [15, 30]) if L == 0 else pick(r, [5, 10, 15, 20, 25, 30])
    phrase = {15: "quarter past", 30: "half past"}.get(k, f"{k} minutes after") if r.random() < 0.6 else f"{k} minutes after"
    return Item(f"Write the time that is {phrase} {h}.", tm(h, k), [f"{phrase.capitalize()} {h} means {k} minutes after {h}:00.", f"The time is {tm(h, k)}."],
                [W(tm(h, k // 5) if k // 5 != k else tm(h, 1), "wrote the wrong minutes"), W(tm(h - 1 if h > 1 else 12, k), "used the hour before"), W(tm(h, 45) if k == 15 else tm(h, 50), "counted the minutes from the wrong side")],
                FN("clock", h=h, m=k), qtype="procedural", claim=f"{phrase} {h}")


@fam("12", mode="mc")
def tm_error(r, L):
    h = r.randint(1, 11)
    k = r.randint(2, 11)
    need(k != h)
    nm = name(r)
    good = f"No. The minute hand on the {k} means {5 * k} minutes, so the time is {tm(h, 5 * k)}."
    bad = [f"Yes. The minute hand is on the {k}, so it is {tm(h, k)}.", f"No. The time is {tm(k, h * 5 if h * 5 < 60 else 0)}.", f"No. The time is {tm(h + 1, 5 * k)}."]
    it = mc_key(f"The hour hand is just past the {h} and the minute hand is on the {k}. {nm} says the time is {tm(h, k)}. Is {nm} right?", good, bad,
                ["Count the minutes by 5s.", f"The time is {tm(h, 5 * k)}."], qtype="error-analysis", tags={"misconception"}, r=r, diagram=clock_d(h, 5 * k))
    it.check = FN("clock_reason", h=h, m=5 * k)
    return it


@fam("2")
def tm_later(r, L):
    h, m = tm5(r, 2)
    d = pick(r, [5, 10, 15, 30])
    nh, nm_ = add_min(h, m, d)
    return Item(f"It is {tm(h, m)}. What time will it be in {d} minutes?", tm(nh, nm_), [f"Count on {d} minutes by 5s from {tm(h, m)}.", f"The time will be {tm(nh, nm_)}."],
                [W(tm(h, (m + d) % 60), "did not change the hour") if m + d >= 60 else W(tm(nh, nm_ + 5) if nm_ < 55 else tm(nh, 0), "counted one extra 5"), W(tm(h + d // 5, m) if h + d // 5 <= 12 else tm(1, m), "added to the hour"), W(tm(nh, nm_ - 5) if nm_ >= 5 else tm(h, 55), "counted one 5 too few")],
                FN("end_time", a=tm(h, m), d=d), qtype="explain", tags={"reasoning"})


# ============================================================== S2 A.M. and P.M.
EVENTS = [("eats breakfast", 6, 9), ("rides the bus to school", 7, 9), ("eats lunch at school", 11, 13), ("plays after school", 15, 18),
          ("eats dinner", 17, 20), ("goes to bed", 19, 22), ("wakes up", 5, 8), ("has a morning recess", 9, 11), ("watches the sunset", 17, 20)]


def ev_time(r, ev):
    lo, hi = ev[1], ev[2]
    h24 = r.randint(lo, hi - 1)
    m = 5 * r.randint(0, 11)
    return h24, m


def show(h24, m):
    return f"{tm(h24 % 12 or 12, m)} {ampm(h24)}"


@fam("012", mode="sa")
def ap_event(r, L):
    ev = pick(r, [e for e in EVENTS if e[2] <= 12 or e[1] >= 12])
    h24, m = ev_time(r, ev)
    nm = name(r)
    return Item(f"{nm} {ev[0]} at {tm(h24 % 12 or 12, m)}. Is that AM or PM?", ampm(h24),
                ["AM is from midnight to noon (morning). PM is from noon to midnight (afternoon and night).", f"{nm} {ev[0]} in the {'morning' if h24 < 12 else 'afternoon or evening'}, so it is {ampm(h24)}."],
                [W("PM" if h24 < 12 else "AM", "mixed up AM and PM")], FN("ampm_of", h24=h24), qtype="conceptual", tags={"real-world"})


@fam("012", mode="mc")
def ap_which(r, L):
    ev = pick(r, EVENTS)
    h24, m = ev_time(r, ev)
    good = show(h24, m)
    flip = (h24 + 12) % 24
    bad = [show(flip, m), show((h24 + 6) % 24, m), show((h24 + 18) % 24, m)]
    need(len(set(bad)) == 3 and good not in bad)
    it = mc_key(f"Which time makes the most sense? A child {ev[0]}.", good, bad, ["Think about the time of day for this event.", f"{good} fits."], qtype="conceptual", tags={"real-world"}, r=r)
    it.check = FN("event_time", lo=ev[1], hi=ev[2])
    return it


@fam("012")
def ap_digital(r, L):
    ev = pick(r, [e for e in EVENTS if e[2] <= 12 or e[1] >= 12])
    h24, m = ev_time(r, ev)
    nm = name(r)
    alt = f"An analog clock showing {tm(h24 % 12 or 12, m)}."
    return Item(f"The clock shows when {nm} {ev[0]}. Write the time. Include AM or PM", show(h24, m),
                [f"The clock shows {tm(h24 % 12 or 12, m)}.", f"{nm} {ev[0]} in the {'morning' if h24 < 12 else 'afternoon or evening'}, so it is {show(h24, m)}."],
                [W(show((h24 + 12) % 24, m), "used the wrong AM or PM"), W(f"{tm(h24 % 12 or 12, m)}", "left out AM or PM")],
                FN("time_ampm", h=h24 % 12 or 12, m=m, h24=h24), qtype="visual", diagram=clock_d(h24 % 12 or 12, m))


@fam("012", mode="mc")
def ap_first(r, L):
    a, b = r.sample(range(0, 24), 2)
    need(a % 12 != b % 12 or L == 2)
    ma, mb = 5 * r.randint(0, 11), 5 * r.randint(0, 11)
    sa, sb = show(a, ma), show(b, mb)
    first = sa if (a, ma) < (b, mb) else sb
    second = sb if first == sa else sa
    good = first
    it = mc_key(f"Both times are on the same day. Which time comes first: {sa} or {sb}?", good, [second, "They happen at the same time.", "You cannot tell."],
                ["AM times come before PM times on the same day.", f"{first} comes first."], qtype="conceptual", r=r)
    it.check = FN("earlier", times=[sa, sb])
    return it


@fam("12")
def ap_after(r, L):
    h24 = r.randint(8, 11)
    m = 5 * r.randint(0, 11)
    d = r.randint(2, 4)
    e = h24 + d
    return Item(f"{name(r)} starts a hike at {show(h24, m)} and hikes for {d} hours. What time does the hike end? Write AM or PM", show(e, m),
                [f"Count on {d} hours from {tm(h24 % 12 or 12, m)}.", f"Noon is passed, so the end time is {show(e, m)}."],
                [W(f"{tm(e % 12 or 12, m)} AM", "did not switch to PM after noon"), W(show(e - 1, m), "counted one hour too few"), W(show(e + 1, m), "counted one hour too many")],
                FN("time_ampm", h=e % 12 or 12, m=m, h24=e), qtype="multi-step", tags={"multistep"})


@fam("2", mode="mc")
def ap_noon(r, L):
    nm = name(r)
    which = pick(r, ["noon", "midnight"])
    good = "PM" if which == "noon" else "AM"
    it = mc_key(f"Is 12:00 {which} written as AM or PM?", f"12:00 {good}",
                [f"12:00 {'AM' if good == 'PM' else 'PM'}", "12:00 noon AM and PM", "12:00 with no label"], ["AM runs from midnight to noon; PM runs from noon to midnight.", f"12:00 {which} is 12:00 {good}."], r=r)
    return it


@fam("012", mode="sa")
def ap_part(r, L):
    h24 = pick(r, [r.randint(6, 10), r.randint(13, 16), r.randint(19, 21)])
    m = 5 * r.randint(0, 11)
    part = "morning" if h24 < 12 else "afternoon" if h24 < 18 else "night"
    return Item(f"Is {show(h24, m)} in the morning, the afternoon, or at night?", part,
                ["AM times are after midnight and before noon. PM times are after noon.", f"{show(h24, m)} is in the {part}." if part != "night" else f"{show(h24, m)} is at night."],
                [W(x, "mixed up AM and PM") for x in ("morning", "afternoon", "night") if x != part], FN("day_part", h24=h24), qtype="conceptual", tags={"real-world"})


# ============================================================== S3 Counting Coins
def coins_for(r, L):
    n = r.randint(3, 5) if L == 0 else r.randint(4, 7)
    kinds = ["dime", "nickel", "penny"] if L == 0 else ["quarter", "dime", "nickel", "penny"]
    cs = sorted((pick(r, kinds) for _ in range(n)), key=lambda k: -COINV[k])
    v = sum(COINV[c] for c in cs)
    need(v < 100)
    return cs, v


def coin_alt(cs):
    return "Coins: " + coin_list(cs) + "."


@fam("012")
def cc_count(r, L):
    cs, v = coins_for(r, L)
    show_ = L == 0
    return Item("How much money is shown?", cents(v), ["Start with the coins worth the most and skip count.", f"{' + '.join(str(COINV[c]) for c in cs)} = {v}¢."],
                [W(cents(len(cs)), "counted the coins instead of their values"), W(cents(v + 5), "counted one coin wrong"), W(cents(v - 1), "made a counting mistake"), W(f"${v}", "used the dollar sign")],
                FN("coins_calc", plus=cs, unit="¢"), qtype="visual", diagram=Diagram("money", {"coins": cs, "show_value": show_}, coin_alt(cs)))


@fam("012")
def cc_text(r, L):
    cs, v = coins_for(r, L)
    nm = name(r)
    return Item(f"{nm} has {coin_list(cs)}. How much money does {nm} have?", cents(v), [f"Values: quarter 25¢, dime 10¢, nickel 5¢, penny 1¢.", f"{' + '.join(str(COINV[c]) for c in cs)} = {v}¢."],
                [W(cents(len(cs)), "counted the coins instead of their values"), W(cents(v + 5), "mixed up a dime and a nickel") if "nickel" in cs or "dime" in cs else W(cents(v + 1), "made a counting mistake"), W(cents(v - 1), "made a counting mistake")],
                FN("coins_calc", plus=cs, unit="¢"), qtype="procedural", claim=f"{coin_list(cs)}")


@fam("012", mode="mc")
def cc_make(r, L):
    cs, v = coins_for(r, L)
    good = coin_list(cs)
    def alt_set(k):
        rr = sub(r, k)
        while True:
            c2, v2 = coins_for(rr, L)
            if v2 != v:
                return coin_list(c2)
    bad = list(dict.fromkeys(alt_set(k) for k in range(1, 6)))[:3]
    need(len(bad) == 3 and good not in bad)
    it = mc_key(f"Which group of coins is worth {cents(v)}?", good, bad, ["Find the value of each group.", f"{good} = {v}¢."], r=r)
    it.check = FN("coin_value", v=v)
    return it


@fam("012", mode="mc")
def cc_which_coin(r, L):
    c = pick(r, ["penny", "nickel", "dime", "quarter"])
    form = pick(r, ["value", "name"])
    if form == "value":
        it = mc_key(f"How much is one {c} worth?", cents(COINV[c]), [cents(x) for x in (1, 5, 10, 25) if x != COINV[c]], [f"A {c} is worth {COINV[c]}¢.", f"{cents(COINV[c])}."], r=r)
        it.check = FN("coin_is", coin=c, what="value")
    else:
        it = mc_key(f"Which coin is worth {cents(COINV[c])}?", c, [k for k in ("penny", "nickel", "dime", "quarter") if k != c], [f"{cents(COINV[c])} is a {c}.", c], r=r)
        it.check = FN("coin_is", coin=c, what="name")
    return it


@fam("12")
def cc_fewest(r, L):
    v = 5 * r.randint(3, 19) + (pick(r, [0, 1, 2, 3, 4]) if L == 2 else 0)
    need(v < 100)
    out, rest = [], v
    for k in ("quarter", "dime", "nickel", "penny"):
        while rest >= COINV[k]:
            out.append(k)
            rest -= COINV[k]
    return Item(f"Use the fewest coins to make {cents(v)}. Which coins do you use?", coin_list(out), ["Use as many of the biggest coins as you can first.", f"{coin_list(out)} = {v}¢."],
                [W(coin_list(["dime"] * (v // 10) + ["nickel"] * (v % 10 // 5) + ["penny"] * (v % 5)), "did not use quarters") if v >= 25 else W(coin_list(["nickel"] * (v // 5) + ["penny"] * (v % 5)), "did not use dimes")],
                FN("fewest", v=v), qtype="explain", tags={"reasoning"})


@fam("012")
def cc_compare(r, L):
    c1, v1 = coins_for(r, L)
    c2, v2 = coins_for(sub(r, 7), L)
    need(v1 != v2)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    big = n1 if v1 > v2 else n2
    return Item(f"{n1} has {coin_list(c1)}. {n2} has {coin_list(c2)}. How much more money does {big} have?", cents(abs(v1 - v2)),
                [f"{n1}: {v1}¢. {n2}: {v2}¢.", f"{max(v1, v2)} − {min(v1, v2)} = {abs(v1 - v2)}¢."],
                [W(cents(v1 + v2), "added the amounts"), W(cents(abs(len(c1) - len(c2))) if abs(len(c1) - len(c2)) != abs(v1 - v2) else cents(abs(v1 - v2) + 1), "compared the number of coins"), W(cents(max(v1, v2)), "gave the bigger amount")],
                FN("coins_calc", plus=c1 if v1 > v2 else c2, minus=c2 if v1 > v2 else c1, unit="¢"),
                qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Counting Bills and Coins
def bills_for(r, L):
    n = r.randint(2, 4) if L == 0 else r.randint(3, 5)
    bs = sorted((pick(r, [1, 5] if L == 0 else [1, 5, 10, 20]) for _ in range(n)), reverse=True)
    need(sum(bs) < 100)
    return bs, sum(bs)


def bill_list(bs):
    from collections import Counter
    c = Counter(bs)
    parts = [f"{c[v]} ${v} bill{'s' if c[v] != 1 else ''}" for v in sorted(c, reverse=True)]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


@fam("012")
def bc_bills(r, L):
    bs, v = bills_for(r, L)
    alt = "Dollar bills: " + bill_list(bs) + "."
    return Item("How many dollars are shown?", f"${v}", [f"Count the bills with the greatest value first.", f"{' + '.join(map(str, bs))} = {v}, so ${v}."],
                [W(f"${len(bs)}", "counted the bills, not their values"), W(f"{v}¢", "used the cent sign"), W(f"${v + 5}", "counted one bill wrong")],
                EX("+".join(map(str, bs)), unit="$"), qtype="visual", diagram=Diagram("money", {"bills": bs}, alt))


@fam("012")
def bc_both(r, L):
    bs, bv = bills_for(r, L)
    cs, cv = coins_for(r, L)
    alt = "Dollar bills: " + bill_list(bs) + ". " + coin_alt(cs)
    ans = f"${bv} and {cv}¢"
    return Item("How much money is shown? Write the dollars and the cents.", ans, [f"Bills: {bv} dollars. Coins: {cv} cents.", f"The total is {ans}."],
                [W(f"${bv + cv}", "added dollars and cents as if they were the same"), W(f"${bv} and {cv + 5}¢", "counted one coin wrong"), W(f"${len(bs)} and {len(cs)}¢", "counted bills and coins instead of values")],
                FN("dollars_cents", d=bv, c=cv), qtype="visual", diagram=Diagram("money", {"bills": bs, "coins": cs, "show_value": L == 0}, alt))


@fam("012")
def bc_text(r, L):
    bs, v = bills_for(r, L)
    nm = name(r)
    return Item(f"{nm} has {bill_list(bs)}. How many dollars does {nm} have?", f"${v}", [f"Add the bill values: {' + '.join(map(str, bs))}.", f"{nm} has ${v}."],
                [W(f"${len(bs)}", "counted the bills, not their values"), W(f"${v + 1}", "made a counting mistake"), W(f"{v}¢", "used the cent sign")],
                EX("+".join(map(str, bs)), unit="$"), qtype="procedural", claim=f"{bill_list(bs)}")


@fam("012", mode="mc")
def bc_symbol(r, L):
    v = r.randint(11, 99)
    form = pick(r, ["cents", "dollars"])
    if form == "cents":
        good = f"{v}¢"
        bad = [f"${v}", f"${v}¢", f"{v}$"]
        q = f"Which shows {words(v)} cents written correctly?"
    else:
        good = f"${v}"
        bad = [f"{v}¢", f"{v}$", f"$¢{v}"]
        q = f"Which shows {words(v)} dollars written correctly?"
    it = mc_key(q, good, bad, ["Use ¢ after a number of cents. Use $ before a number of dollars.", good], r=r)
    it.check = FN("money_sym", v=v, form=form)
    return it


@fam("012")
def bc_more_dollar(r, L):
    cs, v = coins_for(r, L)
    nm = name(r)
    return Item(f"{nm} has {coin_list(cs)}. 100¢ is the same as $1. How many more cents does {nm} need to have $1?", cents(100 - v),
                [f"{nm} has {v}¢.", f"100 − {v} = {100 - v}¢."], [W(cents(v), "gave the amount " + nm + " has"), W(cents(100 - v + 10), "made a regrouping mistake"), W(cents(100 + v), "added instead of subtracting")],
                FN("coins_calc", add=100, minus=cs, unit="¢"), qtype="multi-step", tags={"multistep"})


@fam("2")
def bc_cents_total(r, L):
    k = r.randint(1, 3)
    cs, v = coins_for(r, 2)
    return Item(f"100¢ = $1. How many cents is ${k} and {v}¢?", cents(100 * k + v), [f"${k} = {100 * k}¢.", f"{100 * k} + {v} = {100 * k + v}¢."],
                [W(cents(k + v), "counted each dollar as 1 cent"), W(cents(10 * k + v), "counted each dollar as 10 cents"), W(f"${k + v}", "added dollars and cents together")],
                EX(f"{k}×100+{v}", unit="¢"), qtype="explain", tags={"reasoning"})


# ============================================================== S5 Money Word Problems
ITEMS = [("pencil", 15, 45), ("eraser", 10, 35), ("sticker", 5, 30), ("apple", 25, 60), ("ruler", 30, 70), ("ball", 40, 85), ("bookmark", 12, 40)]
TOYS = [("kite", 8, 25), ("book", 5, 18), ("puzzle", 9, 30), ("game", 12, 40), ("toy car", 3, 15), ("backpack", 15, 45)]


def price(r, rng_):
    nm, lo, hi = rng_
    return nm, r.randint(lo, hi)


@fam("012")
def mw_total(r, L):
    (i1, a), (i2, b) = price(r, pick(r, ITEMS)), price(sub(r, 2), pick(sub(r, 3), ITEMS))
    need(i1 != i2 and a + b < 100)
    return Item(f"{Art(i1)} costs {a}¢. {Art(i2)} costs {b}¢. How much do they cost together?", cents(a + b), [f"Add {a}¢ + {b}¢.", f"{a} + {b} = {a + b}¢."],
                [W(cents(abs(a - b)), "subtracted instead of adding"), W(cents(a + b + 10), "made a regrouping mistake"), W(f"${a + b}", "used the dollar sign")],
                EX(f"{a}+{b}", unit="¢"), qtype="word-problem", tags={"modeling", "real-world"})


@fam("012")
def mw_left(r, L):
    i1, a = price(r, pick(r, ITEMS))
    have = r.randint(a + 5, 99)
    nm = name(r)
    return Item(f"{nm} has {have}¢. {nm} buys {art(i1)} for {a}¢. How much money does {nm} have left?", cents(have - a), [f"Subtract {have} − {a}.", f"{have} − {a} = {have - a}¢."],
                [W(cents(have + a), "added instead of subtracting"), W(cents(have - a + 10), "made a regrouping mistake"), W(cents(a), "gave the price")],
                EX(f"{have}-{a}", unit="¢"), qtype="word-problem", tags={"modeling", "real-world"})


@fam("012")
def mw_more(r, L):
    t, cost = price(r, pick(r, TOYS))
    have = r.randint(1, cost - 1)
    nm = name(r)
    return Item(f"{Art(t)} costs ${cost}. {nm} has ${have}. How many more dollars does {nm} need?", f"${cost - have}", [f"{have} + ? = {cost}.", f"{cost} − {have} = {cost - have}, so ${cost - have}."],
                [W(f"${cost + have}", "added instead of subtracting"), W(f"${cost}", "gave the price"), W(f"{cost - have}¢", "used the cent sign")],
                EX(f"{cost}-{have}", unit="$"), qtype="word-problem", tags={"modeling", "real-world"})


@fam("012", mode="mc")
def mw_eq(r, L):
    i1, a = price(r, pick(r, ITEMS))
    have = r.randint(a + 5, 99)
    nm = name(r)
    good = f"{have} − {a} = ?"
    bad = [f"{have} + {a} = ?", f"{a} − ? = {have}", f"? − {have} = {a}"]
    it = mc_key(f"{nm} has {have}¢ and buys {art(i1)} for {a}¢. Which equation finds how much money is left?", good, bad, ["Spending takes money away.", f"{have} − {a} = {have - a}¢."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("story_eq", ans=have - a, given=[a, have])
    return it


@fam("012")
def mw_coins_buy(r, L):
    cs, v = coins_for(r, L)
    i1, a = price(r, pick(r, ITEMS))
    need(a < v)
    nm = name(r)
    return Item(f"{nm} has {coin_list(cs)}. {nm} buys {art(i1)} for {a}¢. How much money is left?", cents(v - a), [f"{nm} has {v}¢.", f"{v} − {a} = {v - a}¢."],
                [W(cents(v), "forgot to subtract the price"), W(cents(v + a), "added the price"), W(cents(len(cs) - a) if len(cs) > a else cents(v - a + 5), "counted coins, not values")],
                FN("coins_calc", plus=cs, sub=a, unit="¢"), qtype="multi-step", tags={"multistep", "real-world"})


@fam("12")
def mw_two_items(r, L):
    (i1, a), (i2, b) = price(r, pick(r, TOYS)), price(sub(r, 2), pick(sub(r, 3), TOYS))
    need(i1 != i2)
    have = r.randint(a + b + 1, min(99, a + b + 40))
    nm = name(r)
    return Item(f"{nm} has ${have}. {nm} buys {art(i1)} for ${a} and also {art(i2)} for ${b}. How many dollars are left?", f"${have - a - b}",
                [f"Spent: {a} + {b} = {a + b} dollars.", f"{have} − {a + b} = {have - a - b}, so ${have - a - b}."],
                [W(f"${have - a}", "subtracted only one price"), W(f"${a + b}", "found the amount spent"), W(f"${have - a + b}", "added the second price")],
                EX(f"{have}-{a}-{b}", unit="$"), qtype="multi-step", tags={"multistep", "real-world"})


@fam("2", mode="mc")
def mw_enough(r, L):
    cs, v = coins_for(r, 2)
    i1, a = price(r, pick(r, ITEMS))
    need(a != v)
    nm = name(r)
    if v >= a:
        good = f"Yes. {nm} has {v}¢, which is {v - a}¢ more than {a}¢."
        bad = [f"No. {nm} needs {a - v if a > v else v - a + 5}¢ more.", f"No. {nm} has only {len(cs)}¢.", f"Yes. {nm} has exactly {a}¢."]
    else:
        good = f"No. {nm} has {v}¢ and needs {a - v}¢ more."
        bad = [f"Yes. {nm} has {v}¢, which is more than {a}¢.", f"Yes. {nm} has {len(cs)} coins.", f"No. {nm} needs {a}¢ more."]
    it = mc_key(f"{nm} has {coin_list(cs)}. Is that enough to buy {art(i1)} for {a}¢?", good, bad, [f"{nm} has {v}¢.", good], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("enough", v=v, price=a)
    return it


SKILLS = {
    1: dict(name="Telling Time to Five Minutes", fams=[tm_read, tm_minutes, tm_point, tm_mc, tm_words, tm_error, tm_later]),
    2: dict(name="AM and PM", fams=[ap_event, ap_which, ap_digital, ap_first, ap_after, ap_noon, ap_part]),
    3: dict(name="Counting Coins", fams=[cc_count, cc_text, cc_make, cc_which_coin, cc_fewest, cc_compare]),
    4: dict(name="Counting Bills and Coins", fams=[bc_bills, bc_both, bc_text, bc_symbol, bc_more_dollar, bc_cents_total]),
    5: dict(name="Money Word Problems", fams=[mw_total, mw_left, mw_more, mw_eq, mw_coins_buy, mw_two_items, mw_enough]),
}
