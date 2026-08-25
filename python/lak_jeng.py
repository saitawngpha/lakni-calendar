#!/usr/bin/env python3
"""Lak Jeng (Shan/Tai) calendar calculator.

Implements the integer-arithmetic procedure from "Method for Calculating the
Lak Jeng Cycle" (Sua Tai Mong, 21 Nov 2021), deriving from Surya Siddhanta
mean values: 292207/800 civil days per year, corrected 7 units per 1350
years, reproducing exactly 1577917828 civil days per 4320000 years.

Spelling note: Romanizations of the Tai/Shan names vary (Kap=Kra/Karp,
Kat=Kut/Kud, Mong=Muang, Pok=Puek, Khot=Koat, Hung=Hong, Mot=Met,
Kwai=Kai).

Gregorian day-cycle bridge uses the source's dated pair: 5 December 2021
had A = 772521 elapsed days. Tai/Shan year boundaries are Tai month 1 waxing
1, corresponding to conventional Myanmar Nadaw waxing 1. The complete
Myanmar calendar rules avoid guessing the last astronomical new moon of the
year. This contemporary Tai lunar boundary is not an Ahom Lakni calculation.

The source formula applied to T=2116 yields A=772531, ten days away from the
dated A value. ``calculate`` therefore reproduces the source worksheet as a
research hypothesis; it is not used to date Gregorian days.
"""

import argparse
import datetime
import sys

MOTHERS = ["Kap", "Lap", "Hai", "Mong", "Pok", "Kat", "Khut", "Hung", "Tao", "Ka"]
CHILDREN = ["Jai", "Pao", "Yi", "Mao", "Si", "Sai", "Singa", "Mot", "San",
            "Hao", "Met", "Kwai"]
MOTHERS_SHAN = ["ၵၢပ်ႇ", "လပ်း", "ႁၢႆး", "မိူင်း", "ပိုၵ်း",
                "ၵတ်း", "ၶုတ်း", "ႁုင်ႉ", "တဝ်ႇ", "ၵႃႇ"]
CHILDREN_SHAN = ["ၸႂ်ႉ", "ပဝ်ႉ", "ယီး", "မဝ်ႉ", "သီ", "သႂ်ႉ",
                 "သီင", "မူတ်ႉ", "သၼ်", "ႁဝ်ႉ", "မဵတ်ႉ", "ၵႂ်ႉ"]
WEEKDAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday"]

YEAR_BASE_DAYS = 292207
YEAR_DENOM = 800
CORR_PERIOD = 1350
CORR_UNITS = 7
CORR_STEP = 193
EPOCH_OFFSET_N = 6869
MISSING_MULT = 11
MISSING_SUB_DIV = 25
MISSING_ADD = 420
MISSING_DIV = 692

BRIDGE_JDN = 2459554
BRIDGE_A = 772521
NI_DAY_ANCHOR_JDN = 2433191


def to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def correction(y: int) -> int:
    q, r = divmod(y, CORR_PERIOD)
    return CORR_UNITS * q + r // CORR_STEP


def elapsed(n: int) -> dict:
    q, r = divmod(n, YEAR_DENOM)
    a = q + 1 if r > 0 else q
    return {"q": q, "old": r, "new": YEAR_DENOM - r, "a": a}


def missing_days(a: int, y: int) -> tuple[int, int]:
    m = MISSING_MULT * a - y // MISSING_SUB_DIV + MISSING_ADD
    return divmod(m, MISSING_DIV)


def day_index_from_a(a: int) -> int:
    return (a + 2) % 60


def day_index_from_jdn(jdn: int) -> int:
    return (jdn - NI_DAY_ANCHOR_JDN) % 60


def day_names(index: int) -> tuple[str, str]:
    return MOTHERS[index % 10], CHILDREN[index % 12]


def shan_script_names(index: int) -> tuple[str, str]:
    return MOTHERS_SHAN[index % 10], CHILDREN_SHAN[index % 12]


def weekday_from_a(a: int) -> str:
    return WEEKDAYS[a % 7]


def a_for_date(y: int, m: int, d: int) -> int:
    return BRIDGE_A + (to_jdn(y, m, d) - BRIDGE_JDN)


def year_cycle(tai_year: int) -> tuple[str, str]:
    yy = tai_year - 1
    return MOTHERS[(yy + 3) % 10], CHILDREN[(yy - 1) % 12]


def calculate(tai_year: int) -> dict:
    y = tai_year - 1
    c = correction(y)
    n = YEAR_BASE_DAYS * y + c + EPOCH_OFFSET_N
    el = elapsed(n)
    d_miss, p_miss = missing_days(el["a"], y)
    months, month_pos = divmod(el["a"] + d_miss, 30)
    idx = day_index_from_a(el["a"])
    mother, child = day_names(idx)
    sm, sl = shan_script_names(idx)
    return {
        "t": tai_year, "y": y, "c": c, "n": n,
        **el, "m": MISSING_MULT * el["a"] - y // MISSING_SUB_DIV + MISSING_ADD,
        "d_miss": d_miss, "p_miss": p_miss,
        "months": months, "month_pos": month_pos,
        "weekday": weekday_from_a(el["a"]),
        "index": idx, "mother": mother, "child": child,
        "shan": f"{sm}{sl}",
        "year_mother": year_cycle(tai_year)[0],
        "year_child": year_cycle(tai_year)[1],
    }


def report_year(t: int) -> str:
    r = calculate(t)
    return "\n".join([
        f"Lak Jeng calculation for Tai Year {r['t']}",
        f"  calculation year Y   : {r['y']}",
        f"  correction C         : {r['c']}",
        f"  numerator N          : {r['n']}",
        f"  N/800 quotient       : {r['q']}  remainder(old pos) {r['old']}  (new pos {r['new']})",
        f"  elapsed days A       : {r['a']}",
        f"  missing M            : {r['m']}  -> D={r['d_miss']}  P={r['p_miss']}",
        f"  lunar months         : {r['months']} completed, position {r['month_pos']}",
        f"  weekday              : {r['weekday']}",
        f"  day cycle            : {r['mother']} {r['child']} / {r['shan']}  (index {r['index']}/60)",
        f"  year cycle           : {r['year_mother']} {r['year_child']}",
    ])


def tai_new_year_jdn(gregorian_year: int, tz_hours: float = None) -> int:
    del tz_hours  # Conventional calendar dates do not move with true-conjunction timezones.
    import sakkaraj
    return sakkaraj.tai_lunar_new_year_jdn(gregorian_year)


def tai_year_from_gregorian(y: int, m: int, d: int) -> int:
    jdn = to_jdn(y, m, d)
    return y + 95 if jdn >= tai_new_year_jdn(y) else y + 94


def report_date(y: int, m: int, d: int) -> str:
    a = a_for_date(y, m, d)
    idx = day_index_from_a(a)
    mother, child = day_names(idx)
    sm, sl = shan_script_names(idx)
    t = tai_year_from_gregorian(y, m, d)
    jdn = to_jdn(y, m, d)
    this_ny = tai_new_year_jdn(y)
    if jdn >= this_ny:
        ny_prev, ny_next = this_ny, tai_new_year_jdn(y + 1)
    else:
        ny_prev, ny_next = tai_new_year_jdn(y - 1), this_ny
    import datetime as _dt
    fmt = lambda j: _dt.date.fromordinal(_dt.date(1858, 11, 17).toordinal() + j - 2400001).isoformat()
    market = "yes (Hai/Hut or Hung/Hong stem)" if idx % 10 in (2, 7) else "no"
    return "\n".join([
        f"Gregorian       : {datetime.date(y, m, d).isoformat()} ({weekday_from_a(a)})",
        f"Tai (Shan) year : {t}  [began {fmt(ny_prev)}, next NY {fmt(ny_next)}]",
        f"elapsed days A  : {a}",
        f"day cycle       : {mother} {child} / {sm}{sl}  (index {idx}/60)",
        f"market day      : {market}",
    ])


def self_test() -> None:
    r = calculate(2115)
    assert r["y"] == 2114 and r["c"] == 10
    assert r["n"] == 617732477
    assert r["q"] == 772165 and r["old"] == 477 and r["new"] == 323
    assert r["a"] == 772166
    assert r["m"] == 8494162 and r["d_miss"] == 12274 and r["p_miss"] == 554
    assert r["months"] == 26148 and r["month_pos"] == 0
    assert r["weekday"] == "Tuesday"
    assert (r["mother"], r["child"]) == ("Tao", "Si") and r["index"] == 28
    assert (r["year_mother"], r["year_child"]) == ("Hung", "Pao")

    assert to_jdn(2021, 12, 5) == BRIDGE_JDN
    assert a_for_date(2021, 12, 5) == BRIDGE_A
    assert weekday_from_a(BRIDGE_A) == "Sunday"
    assert day_index_from_a(BRIDGE_A) == 23

    a_today = a_for_date(2026, 8, 23)
    assert weekday_from_a(a_today) == "Sunday"
    m_, c_ = day_names(day_index_from_a(a_today))
    assert (m_, c_) == ("Kat", "Sai")
    sm_, sl_ = shan_script_names(day_index_from_a(a_today))
    assert (sm_, sl_) == ("ၵတ်း", "သႂ်ႉ")
    assert len(MOTHERS_SHAN) == 10 and len(CHILDREN_SHAN) == 12
    s2115 = calculate(2115)
    assert s2115["shan"] == "တဝ်ႇသီ"
    assert tai_year_from_gregorian(2026, 8, 23) == 2120
    assert tai_year_from_gregorian(2021, 12, 4) == 2116
    assert tai_year_from_gregorian(2021, 12, 3) == 2115
    assert tai_new_year_jdn(2025) == to_jdn(2025, 11, 20)
    assert tai_year_from_gregorian(2025, 12, 31) == 2120
    print("all self-tests passed "
          "(worked example reproduced; Shan year 2120 verified)")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Lak Jeng (Shan/Tai) calendar calculator")
    p.add_argument("tai_year", nargs="?", type=int, help="Tai year, e.g. 2115")
    p.add_argument("--date", nargs=3, metavar=("Y", "M", "D"), type=int,
                   help="Gregorian Y M D -> day cycle via bridge")
    p.add_argument("--test", action="store_true")
    args = p.parse_args(argv)

    if args.test:
        self_test()
        return 0

    if args.date:
        y, m, d = args.date
        datetime.date(y, m, d)
        print(report_date(y, m, d))
        return 0

    if args.tai_year:
        print(report_year(args.tai_year))
        return 0

    t = datetime.date.today()
    print(report_date(t.year, t.month, t.day))
    return 0


if __name__ == "__main__":
    sys.exit(main())
