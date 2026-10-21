#!/usr/bin/env python3
"""standing.py - small, dependency-free helper for the answer-standing skill.

Commands
  init  DIR                      create a working folder with blank templates
  tally ANSWERS.csv [--brand B]  mention rate (with 95% Wilson interval), first-named
                                 rate, framing, share of voice, per engine and question
  claims CLAIMS.csv              accuracy summary of claims about the brand, worst first
  compare BEFORE.csv AFTER.csv [--brand B]
                                 did the mention rate really move, or is it noise?

answers.csv columns (one row per answer you read):
  batch,date,engine,mode,question_id,family,repeat,mentioned,position,framing,names
    mentioned  y/n        was the brand named at all
    position   1,2,3..    order in which the brand was named among products (blank if not)
    framing    rec/neutral/warn/blank
    names      every product named, separated by ';' (used for share of voice)

claims.csv columns:
  question_id,engine,claim,verdict,truth_key,source,fix
    verdict    correct/stale/wrong/invented/conflated/unverifiable
"""
import csv, math, os, sys
from collections import defaultdict, Counter

VERDICTS = ["correct", "stale", "wrong", "invented", "conflated", "unverifiable"]
BAD = {"stale", "wrong", "invented", "conflated"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def pct(x):
    return f"{x * 100:5.1f}%"


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]
    if not rows:
        sys.exit(f"{path}: no rows")
    return rows


def yes(v):
    return v.lower() in {"y", "yes", "1", "true", "是"}


def cmd_init(d):
    os.makedirs(d, exist_ok=True)
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
    for name in sorted(os.listdir(here)):
        dst = os.path.join(d, name)
        if os.path.exists(dst):
            print(f"keep   {dst} (already exists)")
            continue
        with open(os.path.join(here, name), encoding="utf-8") as s, open(dst, "w", encoding="utf-8") as t:
            t.write(s.read())
        print(f"create {dst}")


def summarize(rows):
    n = len(rows)
    k = sum(yes(r.get("mentioned", "")) for r in rows)
    first = sum(1 for r in rows if r.get("position") == "1")
    fr = Counter(r.get("framing", "") or "-" for r in rows if yes(r.get("mentioned", "")))
    return n, k, first, fr


def cmd_tally(path, brand):
    rows = read(path)
    n, k, first, fr = summarize(rows)
    p, lo, hi = wilson(k, n)
    print(f"answers read: {n}   brand mentioned: {k}   rate {pct(p)}  (95% range {pct(lo)} - {pct(hi)})")
    print(f"named first: {first} ({pct(first / n)})   framing when mentioned: " + ", ".join(f"{a}={b}" for a, b in fr.most_common()))
    if n < 30:
        print("note: fewer than 30 answers - treat every rate as a rough band, not a number")
    print("\nby engine")
    for key in ("engine", "family", "question_id"):
        groups = defaultdict(list)
        for r in rows:
            groups[r.get(key, "") or "-"].append(r)
        if key != "engine":
            print(f"\nby {key}")
        for g, rs in sorted(groups.items()):
            gn, gk, gf, _ = summarize(rs)
            gp, glo, ghi = wilson(gk, gn)
            flag = "  <- never mentioned" if gk == 0 else ""
            print(f"  {g:<18} {gk:>3}/{gn:<3} {pct(gp)}  [{pct(glo)} - {pct(ghi)}]  first {gf}{flag}")
    names = Counter()
    for r in rows:
        for x in r.get("names", "").split(";"):
            x = x.strip()
            if x:
                names[x.lower()] += 1
    if names:
        total = sum(names.values())
        print("\nshare of voice (all product mentions across answers)")
        for name, c in names.most_common(10):
            mark = "  <- you" if brand and name == brand.lower() else ""
            print(f"  {name:<24} {c:>4}  {pct(c / total)}{mark}")


def cmd_claims(path):
    rows = read(path)
    v = Counter(r.get("verdict", "").lower() or "unmarked" for r in rows)
    graded = sum(v[x] for x in VERDICTS if x != "unverifiable")
    good = v["correct"]
    print(f"claims: {len(rows)}   " + ", ".join(f"{x}={v[x]}" for x in VERDICTS + ["unmarked"] if v[x]))
    if graded:
        p, lo, hi = wilson(good, graded)
        print(f"accuracy of checkable claims: {pct(p)}  (95% range {pct(lo)} - {pct(hi)})")
    bad = [r for r in rows if r.get("verdict", "").lower() in BAD]
    if not bad:
        print("no wrong claims to repair")
        return
    keyc = Counter(r.get("truth_key", "") or "-" for r in bad)
    print("\nwrong claims by fact (fix these first)")
    for key, c in keyc.most_common():
        srcs = Counter(r.get("source", "") or "no source found" for r in bad if (r.get("truth_key", "") or "-") == key)
        print(f"  {key:<20} {c:>3}x  sources: " + "; ".join(f"{s} ({n})" for s, n in srcs.most_common(3)))
    nofix = [r for r in bad if not r.get("fix")]
    if nofix:
        print(f"\n{len(nofix)} wrong claim(s) still have no fix assigned")


def cmd_compare(a, b, brand):
    ra, rb = read(a), read(b)
    na, ka, _, _ = summarize(ra)
    nb, kb, _, _ = summarize(rb)
    pa, la, ha = wilson(ka, na)
    pb, lb, hb = wilson(kb, nb)
    print(f"before: {ka}/{na} {pct(pa)} [{pct(la)} - {pct(ha)}]")
    print(f"after : {kb}/{nb} {pct(pb)} [{pct(lb)} - {pct(hb)}]")
    pool = (ka + kb) / (na + nb)
    se = math.sqrt(pool * (1 - pool) * (1 / na + 1 / nb)) if 0 < pool < 1 else 0
    z = (pb - pa) / se if se else 0.0
    if abs(z) >= 1.96:
        verdict = "real change (two-proportion test, |z| >= 1.96)" + (" - up" if z > 0 else " - DOWN")
    elif abs(z) >= 1.0:
        verdict = "maybe - direction is suggestive; collect more repeats before claiming it"
    else:
        verdict = "no detectable change - the difference is within normal answer-to-answer noise"
    print(f"z = {z:+.2f}  ->  {verdict}")
    qa = {r["question_id"] for r in ra}
    qb = {r["question_id"] for r in rb}
    if qa != qb:
        print("warning: the two batches do not use the same questions; the comparison is not like-for-like")
    ea = {r.get("engine") for r in ra}
    eb = {r.get("engine") for r in rb}
    if ea != eb:
        print("warning: engine mix differs between batches")


def main(argv):
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__)
        return
    brand = ""
    if "--brand" in argv:
        i = argv.index("--brand")
        brand = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    c = argv[1]
    if c == "init" and len(argv) == 3:
        cmd_init(argv[2])
    elif c == "tally" and len(argv) == 3:
        cmd_tally(argv[2], brand)
    elif c == "claims" and len(argv) == 3:
        cmd_claims(argv[2])
    elif c == "compare" and len(argv) == 4:
        cmd_compare(argv[2], argv[3], brand)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
