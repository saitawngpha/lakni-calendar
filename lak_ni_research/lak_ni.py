#!/usr/bin/env python3
"""Lak-Ni (Tai Ahom calendar) converter.

Converts Gregorian dates into the Tai Ahom Lak-Ni system:
  * Me-Pi 60-year cycle name (popular Ahom tradition, anchored 1193 CE =
    "Mungkeu", birth year of Sukaphaa; verified: 1215 = Katrau, 1268 = Taoni,
    1253 = Mungkeu again)
  * Structural Tai year name (Mother x Son/animal, aligned to the pan-Tai
    cycle where 1984 CE = Kra/Karp Jai, the Wood-Rat year)
  * Sakkaraj (Chula Sakarat) era year (= AD - 638)
  * Weekday, 60-day Mother-Son day name, and Myanmar-style lunar phase
    (waxing/waning day, full moon, new-moon day). The civil day containing
    the true new moon (Meeus algorithm) ENDS the old month; waxing day 1 is
    the next day. Default timezone UTC+6:30 (Myanmar); use --tz 5.5 for
    Assam, which can shift the boundary by one day.

CAVEATS
  * The popular 60-name Me-Pi list below comes from published popular sources
    and contains transliteration inconsistencies; replace ME_PI_60 with the
    Terwiel & Ranoo (1992) Table 4 readings for scholarly work.
  * DAY_ANCHOR_JDN is calibrated so index 0 = a jiazi (Kap-Jai) day, using
    the verified reference 1949-10-01 CE = jiazi day (JDN 2433191). This makes
    the 60-day count continuous with the shared Tai/Chinese day cycle, e.g.
    2026-08-23 = Kut-Sai. Use --calibrate only if a local tradition differs.
"""

import argparse
import datetime
import sys
from math import radians, sin

MOTHERS_TAI = [
    "Kra (Kha)", "Lup", "Hut (Hot)", "Muang (Mvng)", "Puek",
    "Kut", "Koat (Kwat)", "Hong (Hvng)", "Tao (Thao)", "Ka (Kap)",
]

SONS_TAI = [
    "Jai (rat)", "Ngok/Pao (ox)", "Khan/Yee (tiger)", "Mao (hare)",
    "Si (naga/dragon)", "Sai (snake)", "Singa/Nga (horse)", "Met (goat)",
    "Saan (monkey)", "Rao/Hao (cock)", "Set/Sed (dog)", "Kai (pig)",
]

MOTHERS_SHAN_SCRIPT = ["ၵၢပ်ႇ", "လပ်း", "ႁၢႆး", "မိူင်း", "ပိုၵ်း",
                       "ၵတ်း", "ၶုတ်း", "ႁုင်ႉ", "တဝ်ႇ", "ၵႃႇ"]
CHILDREN_SHAN_SCRIPT = ["ၸႂ်ႉ", "ပဝ်ႉ", "ယီး", "မဝ်ႉ", "သီ", "သႂ်ႉ",
                        "သီင", "မူတ်ႉ", "သၼ်", "ႁဝ်ႉ", "မဵတ်ႉ", "ၵႂ်ႉ"]

WEEKDAYS = [
    "Sun (Ngarng/Garuda)", "Mon (Kan/Chandra)", "Tue (Angarak/Mars)",
    "Wed (Budh/Mercury)", "Thu (Brihaspati/Jupiter)", "Fri (Sukra/Venus)",
    "Sat (Sanichar/Saturn)",
]

YEAR_ANCHOR_AD = 1193
YEAR_ANCHOR_NAME = "Mungkeu"

AHOM_STEMS = [
    ("Kap", "jia 甲", "wood"), ("Dap", "yi 乙", "wood"),
    ("Rai", "bing 丙", "fire"), ("Mueang", "ding 丁", "fire"),
    ("Plaek", "wu 戊", "earth"), ("Kat", "ji 己", "earth"),
    ("Khut", "geng 庚", "metal"), ("Rung", "xin 辛", "metal"),
    ("Tao", "ren 壬", "water"), ("Ka", "gui 癸", "water"),
]

SHAN_STEMS = ["Kra/Kap", "Lup/Lap", "Hut/Hai", "Muang/Möng", "Puek/Pök",
              "Kut/Kud", "Koat/Khot", "Hong/Hung", "Tao/Thao", "Ka"]

YEAR_BOUNDS = {"jan1": (1, 1), "lichun": (2, 4), "songkran": (4, 14)}
DEFAULT_BOUNDARY = "songkran"

EPOCH_STEM_BRANCH = 4

DAY_ANCHOR_JDN = 2433191

DEFAULT_TZ_HOURS = 6.5

ME_PI_60 = [
    "Mungkeu", "Plekteu", "Katplao", "Khutni", "Rungmau", "Tauchi",
    "Kacheu", "Kapchinga", "Dapmut", "Raison",
    "Mungrau", "Plackmit", "Katkeu", "Khuttyeu", "Rungplao", "Taoni",
    "Kamau", "Kapchi", "Dapcheu", "Raichingaa",
    "Mungmut", "Plaksan", "Katrau", "Mutmit", "Rungkeu", "Taotyeu",
    "Kaplau", "Kapli", "Dapmau", "Raici",
    "Mungcheu", "Plakchinga", "Katmut", "Khutsan", "Rungrau", "Taumit",
    "Kakeu", "Kapteu", "Dapplao", "Raini",
    "Mungmau", "Plakchi", "Katcheu", "Khutchinga", "Rungmut", "Tausan",
    "Karau", "Kapmit", "Dapcheu*", "Raiteu",
    "Mungplau", "Plakni", "Katmau", "Khutchi", "Rungcheu", "Tauchinga",
    "Kamut", "Kapsaan", "Daprau", "Raimit",
]


def to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def lak_ni_year(ad_year: int) -> dict:
    pos = ((ad_year - YEAR_ANCHOR_AD) % 60) + 1
    return {
        "position": pos,
        "me_pi_popular": ME_PI_60[pos - 1],
        "cycle_number": ((ad_year - YEAR_ANCHOR_AD) // 60) + 1,
    }


def tai_structural_year(ad_year: int) -> dict:
    si = (ad_year - EPOCH_STEM_BRANCH) % 10
    zi = (ad_year - EPOCH_STEM_BRANCH) % 12
    stem_name, stem_cn, element = AHOM_STEMS[si]
    return {
        "stem": stem_name,
        "stem_chinese": stem_cn,
        "element": element,
        "shan_stem": SHAN_STEMS[si],
        "son": SONS_TAI[zi],
        "name": f"{stem_name}-{SONS_TAI[zi].split('/')[0].split()[0]}",
        "cycle_index": (ad_year - EPOCH_STEM_BRANCH) % 60,
    }


def tai_year_for(y: int, m: int, d: int, rule: str = DEFAULT_BOUNDARY) -> int:
    b = YEAR_BOUNDS[rule]
    return y - 1 if (m, d) < b else y


def sakkaraj(ad_year: int) -> int:
    return ad_year - 638


def day_sexagenary(jdn: int) -> dict:
    i = (jdn - DAY_ANCHOR_JDN) % 60
    return {
        "index": i,
        "mother": MOTHERS_TAI[i % 10],
        "son": SONS_TAI[i % 12],
        "mother_shan": MOTHERS_SHAN_SCRIPT[i % 10],
        "son_shan": CHILDREN_SHAN_SCRIPT[i % 12],
        "shan": f"{MOTHERS_SHAN_SCRIPT[i % 10]}{CHILDREN_SHAN_SCRIPT[i % 12]}",
        "name": f"{MOTHERS_TAI[i % 10].split()[0]}-{SONS_TAI[i % 12].split('/')[0].split()[0]}",
    }


def true_new_moon_jde(k: int) -> float:
    T = k / 1236.85
    jde = (2451550.09766 + 29.530588861 * k + 0.00015437 * T * T
           - 0.000000150 * T ** 3 + 0.00000000073 * T ** 4)
    e = 1 - 0.002516 * T - 0.0000074 * T * T
    m = radians(2.5534 + 29.10535670 * k - 0.0000014 * T * T - 0.00000011 * T ** 3)
    mp = radians(201.5643 + 385.81693528 * k + 0.0107582 * T * T
                 + 0.00001238 * T ** 3 - 0.000000058 * T ** 4)
    f = radians(160.7108 + 390.67050284 * k - 0.0016118 * T * T
                - 0.00000227 * T ** 3 + 0.000000011 * T ** 4)
    o = radians(124.7746 - 1.56375588 * k + 0.0020672 * T * T + 0.00000215 * T ** 3)
    corr = (-0.40720 * sin(mp) + 0.17241 * e * sin(m) + 0.01608 * sin(2 * mp)
            + 0.01039 * sin(2 * f) + 0.00739 * e * sin(mp - m)
            - 0.00514 * e * sin(mp + m) + 0.00208 * e * e * sin(2 * m)
            - 0.00111 * sin(mp - 2 * f) - 0.00057 * sin(mp + 2 * f)
            + 0.00056 * e * sin(2 * mp + m) - 0.00042 * sin(3 * mp)
            + 0.00042 * e * sin(m + 2 * f) + 0.00038 * e * sin(m - 2 * f)
            - 0.00024 * e * sin(2 * mp - m) - 0.00017 * sin(o)
            - 0.00007 * sin(mp + 2 * m) + 0.00004 * sin(2 * mp - 2 * f)
            + 0.00004 * sin(3 * m) + 0.00003 * sin(mp + m - 2 * f)
            + 0.00003 * sin(2 * mp + 2 * f) - 0.00003 * sin(mp + m + 2 * f)
            + 0.00003 * sin(mp - m + 2 * f) - 0.00002 * sin(mp - m - 2 * f)
            - 0.00002 * sin(3 * mp + m) + 0.00002 * sin(4 * mp))
    amps = [299.77 + 0.107408 * k - 0.009173 * T * T, 251.88 + 0.016321 * k,
            251.83 + 26.651886 * k, 349.42 + 36.412478 * k, 84.66 + 18.206239 * k,
            141.74 + 53.303771 * k, 207.14 + 2.453732 * k, 154.84 + 7.306860 * k,
            34.52 + 27.261239 * k, 207.19 + 0.121824 * k, 291.34 + 1.844379 * k,
            161.72 + 24.198154 * k, 239.56 + 25.513099 * k, 331.55 + 3.592518 * k]
    coeffs = [0.000325, 0.000165, 0.000164, 0.000126, 0.000110, 0.000062,
              0.000060, 0.000056, 0.000047, 0.000042, 0.000040, 0.000037,
              0.000035, 0.000023]
    return jde + corr + sum(coeffs[i] * sin(radians(amps[i])) for i in range(14))


def new_moon_day_before_or_on(jdn: int, tz_hours: float = DEFAULT_TZ_HOURS) -> int:
    k0 = round((jdn - 2451550.09766) / 29.530588861)
    conj_day = None
    for k in (k0 - 1, k0, k0 + 1):
        d = int(true_new_moon_jde(k) + tz_hours / 24 + 0.5)
        if d <= jdn:
            conj_day = d
    if conj_day is None:
        raise RuntimeError("no new moon found")
    return conj_day


def lunar_phase(jdn: int, tz_hours: float = DEFAULT_TZ_HOURS) -> dict:
    nm_day = new_moon_day_before_or_on(jdn, tz_hours)
    delta = jdn - nm_day
    if delta == 0:
        phase, num = "new moon day (ends old month)", None
    elif delta <= 14:
        phase, num = "waxing", delta
    elif delta == 15:
        phase, num = "full moon", 15
    else:
        phase, num = "waning", delta - 15
    return {"phase": phase, "day": num, "new_moon_jdn": nm_day}


def full_report(y: int, m: int, d: int, tz_hours: float = DEFAULT_TZ_HOURS,
                rule: str = DEFAULT_BOUNDARY) -> str:
    jdn = to_jdn(y, m, d)
    dt = datetime.date(y, m, d)
    ty = tai_year_for(y, m, d, rule)
    yr = lak_ni_year(ty)
    st = tai_structural_year(ty)
    dy = day_sexagenary(jdn)
    ld = lunar_phase(jdn, tz_hours)
    phase_txt = ld["phase"] if ld["day"] is None else f"{ld['phase']} day {ld['day']}"
    cs = sakkaraj(ty)
    sok_digit = cs % 10
    sok_names = ["samritthisok", "ekasok", "thosok", "trisok", "chattawasok",
                 "benchasok", "chosok", "sappasok", "atthasok", "noppasok"]
    lines = [
        f"Gregorian date : {dt.isoformat()} ({WEEKDAYS[(dt.weekday() + 1) % 7]})",
        f"Tai year       : {ty} (turns {rule}; Jan-Aug dates may use y-1)",
        f"Lak-Ni year    : {yr['position']}/60 \"{yr['me_pi_popular']}\" (folk Me-Pi count, anchored 1193 CE)",
        f"Year name      : {st['name']} = {st['element']} {st['son'].split('(')[1][:-1]}  [{st['stem']} ({st['stem_chinese']}) x {st['son']}]",
        f"Shan variant   : {st['shan_stem']}-{st['son'].split('/')[0].split()[0]}",
        f"Sakkaraj era   : {cs} CS (sok {sok_digit} = {sok_names[sok_digit]})",
        f"Day name       : {dy['name']}  ({dy['index']}/60) [{dy['mother']} x {dy['son']}]",
        f"Day in Shan    : {dy['shan']}  ({dy['mother_shan']} {dy['son_shan']})",
        f"Lunar phase    : {phase_txt}  [UTC+{tz_hours:g}, Myanmar-style]",
        f"Julian Day No. : {jdn}",
    ]
    return "\n".join(lines)


def self_test() -> None:
    assert len(ME_PI_60) == 60
    assert lak_ni_year(1193)["me_pi_popular"] == "Mungkeu"
    assert lak_ni_year(1215)["me_pi_popular"] == "Katrau"
    assert lak_ni_year(1215)["position"] == 23
    assert lak_ni_year(1268)["me_pi_popular"] == "Taoni"
    assert lak_ni_year(1268)["position"] == 16
    assert lak_ni_year(1253)["me_pi_popular"] == "Mungkeu"
    assert tai_structural_year(1984)["stem"] == "Kap"
    assert tai_structural_year(1984)["son"] == SONS_TAI[0]
    st26 = tai_structural_year(2026)
    assert st26["stem"] == "Rai" and st26["element"] == "fire"
    assert st26["son"].startswith("Singa") and st26["cycle_index"] == 42
    assert tai_structural_year(2025)["stem"] == "Dap"
    assert tai_structural_year(2025)["son"].startswith("Sai")
    assert tai_year_for(2026, 1, 1) == 2025
    assert tai_year_for(2026, 4, 13) == 2025
    assert tai_year_for(2026, 4, 14) == 2026
    assert tai_year_for(2026, 2, 3, "lichun") == 2025
    assert tai_year_for(2026, 12, 31, "jan1") == 2026
    assert sakkaraj(2026) == 1388
    assert to_jdn(2000, 1, 1) == 2451545
    assert WEEKDAYS[(datetime.date(2026, 8, 23).weekday() + 1) % 7].startswith("Sun")
    assert day_sexagenary(to_jdn(1949, 10, 1))["name"] == "Kra-Jai"
    assert day_sexagenary(to_jdn(2026, 8, 23))["name"] == "Kut-Sai"
    assert len(MOTHERS_SHAN_SCRIPT) == 10 and len(CHILDREN_SHAN_SCRIPT) == 12
    _dy = day_sexagenary(to_jdn(2026, 8, 23))
    assert (_dy["mother_shan"], _dy["son_shan"]) == ("ၵတ်း", "သႂ်ႉ")
    assert abs(true_new_moon_jde(0) - 2451550.25993) < 0.001
    assert abs(true_new_moon_jde(round((2021.92 - 2000) * 12.3685)) - 2459552.8224) < 0.01
    assert lunar_phase(to_jdn(2021, 12, 5)) == {
        "phase": "waxing", "day": 1, "new_moon_jdn": to_jdn(2021, 12, 4)}
    assert lunar_phase(to_jdn(2021, 12, 4))["phase"].startswith("new moon")
    assert lunar_phase(to_jdn(2026, 8, 23)) == {
        "phase": "waxing", "day": 10, "new_moon_jdn": to_jdn(2026, 8, 13)}
    assert lunar_phase(to_jdn(2026, 8, 23), tz_hours=5.5) == {
        "phase": "waxing", "day": 11, "new_moon_jdn": to_jdn(2026, 8, 12)}
    print("all self-tests passed")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Tai Ahom Lak-Ni calendar converter")
    p.add_argument("date", nargs="*", help="YYYY MM DD (defaults to today)")
    p.add_argument("--test", action="store_true", help="run self-tests")
    p.add_argument("--tz", type=float, default=DEFAULT_TZ_HOURS,
                   help="timezone offset hours for lunar phase (default 6.5 Myanmar; 5.5 Assam)")
    p.add_argument("--boundary", choices=sorted(YEAR_BOUNDS), default=DEFAULT_BOUNDARY,
                   help="year-turn rule: songkran (Apr 14, Tai/Ahom), lichun (Feb 4, Chinese), jan1")
    p.add_argument("--calibrate", nargs=2, metavar=("DATE", "ANIMAL"),
                   help="print candidate DAY_ANCHOR_JDN for a known day-animal")
    args = p.parse_args(argv)

    if args.test:
        self_test()
        return 0

    if args.calibrate:
        ds, animal = args.calibrate
        y, m, d = (int(x) for x in ds.split("-"))
        print(f"DAY_ANCHOR_JDN candidates for {ds} ({animal}):")
        for c in solve_anchor_candidates(y, m, d, animal):
            print(f"  {c}")
        return 0

    try:
        if args.date:
            y, m, d = (int(x) for x in args.date[:3])
            datetime.date(y, m, d)
        else:
            t = datetime.date.today()
            y, m, d = t.year, t.month, t.day
    except (ValueError, IndexError):
        p.error("date must be given as YYYY MM DD")

    print(full_report(y, m, d, args.tz, args.boundary))
    return 0


def solve_anchor_candidates(y: int, m: int, d: int, son_name: str) -> list[int]:
    jdn = to_jdn(y, m, d)
    sons_lower = [s.split("/")[0].split()[0].lower() for s in SONS_TAI]
    target = son_name.lower()
    if target not in sons_lower:
        raise ValueError(f"unknown son/animal '{son_name}'; options: {sons_lower}")
    s_idx = sons_lower.index(target)
    out = []
    base = (jdn - DAY_ANCHOR_JDN) % 60
    for i in range(60):
        if i % 12 == s_idx:
            shift = (base - i) % 60
            out.append(DAY_ANCHOR_JDN + shift)
    return sorted(set(out))


if __name__ == "__main__":
    sys.exit(main())
