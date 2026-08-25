#!/usr/bin/env python3
"""Comparative Tai Ahom Lakni calendar research tool.

Provides a reference table for the historical Tai Ahom Lak-Ni cycle and
comparative calculations:
  * Historical Ahom Lakni names, anchored at Kap Cheu in 2008, with the
    canonical Mother x Child table published by Kapoor (2021, Tables 7-9)
  * An explicitly reconstructed Ahom lunar calendar: Dinching begins on the
    civil day after the first Assam-local new moon on or after 1 November;
    a thirteenth lunation is placed after month 8
  * Structural Tai year name (Mother x Son/animal, aligned to the pan-Tai
    cycle where 1984 CE = Kra/Karp Jai, the Wood-Rat year)
  * Sakkaraj (Chula Sakarat) era year with its computed solar New Year boundary
  * Weekday, 60-day Mother-Son day name, conventional Myanmar calendar date,
    and a separately labelled true-conjunction phase estimate. The latter is
    astronomical evidence, not a traditional month conversion. The default
    timezone is UTC+5:30 for the Assam reconstruction.

CAVEATS
  * This module does not derive an Ahom Lakni date from Myanmar Nadaw. Tai
    month 1 waxing 1 belongs to the separate contemporary Tai/Shan converter
    in lak_jeng.py.
  * Published sources establish that the Lakni changes with Dinching, on the
    day following the new moon that ends month 12. They do not publish the
    Ahom priests' complete new-moon and intercalation constants. The seasonal
    anchor and leap-month placement used here are therefore labelled as a
    reconstruction.

SOURCE BASIS
  * R. C. Kapoor, JAHH 24(3), 2021, p. 668: the new Lakni came with
    Dinching, which begins on the day following the new moon ending month 12.
  * Kapoor, pp. 686-687, Tables 7-9: Ahom month order and the canonical
    10-Mother x 12-Child sequence.
  * Jean Meeus, Astronomical Algorithms, 2nd ed., ch. 49: modern new-moon
    approximation only, not the Ahom seasonal or intercalation rules.
  * See ../LAKNI_NEW_YEAR_SOURCES.md for institutional links, manuscript
    evidence, and a claim-by-claim confidence table.
  * ME_PI_60 is retained only as a legacy popular list and is not used for the
    default Ahom Lakni result.
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

AHOM_CYCLE_ANCHOR_YEAR = 2008
AHOM_CYCLE_ANCHOR_NAME = "Kap Cheu"

AHOM_LAKNI_MOTHERS = [
    "Kap", "Dap", "Rai", "Mung", "Plek", "Kat", "Khut", "Rung", "Tao", "Ka",
]
AHOM_LAKNI_CHILDREN = [
    "Cheu", "Plao", "Ngi", "Mao", "Shi", "Shiu", "Shinga", "Mut", "San", "Rao", "Mit", "Keu",
]
AHOM_LAKNI_60 = [
    f"{AHOM_LAKNI_MOTHERS[i % 10]} {AHOM_LAKNI_CHILDREN[i % 12]}"
    for i in range(60)
]

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
DEFAULT_BOUNDARY = "jan1"

EPOCH_STEM_BRANCH = 4

DAY_ANCHOR_JDN = 2433191

DEFAULT_TZ_HOURS = 5.5
DEFAULT_AHOM_TZ_HOURS = DEFAULT_TZ_HOURS

AHOM_MONTHS = [
    "Din Ching", "Din Kam", "Din Sham", "Din Shi", "Din Ha", "Din Ruk",
    "Din Chit", "Din Pet", "Din Kao", "Din Ship", "Din Shipit", "Din Shipshang",
]
AHOM_BOUNDARY_MODEL = (
    "reconstruction: Din Ching starts the day after the first Assam-local "
    "new moon on or after 1 November; leap lunation after month 8"
)

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
    """Legacy popular Me-Pi list; retained for comparison, not canonical dating."""
    year_anchor_ad = 1193
    pos = ((ad_year - year_anchor_ad) % 60) + 1
    return {
        "position": pos,
        "me_pi_popular": ME_PI_60[pos - 1],
        "cycle_number": ((ad_year - year_anchor_ad) // 60) + 1,
    }


def ahom_lakni_for_cycle_year(cycle_year: int) -> dict:
    """Return an Ahom cycle-table entry without assuming a month boundary."""
    pos = ((cycle_year - AHOM_CYCLE_ANCHOR_YEAR) % 60) + 1
    return {
        "position": pos,
        "name": AHOM_LAKNI_60[pos - 1],
        "cycle_year": cycle_year,
        "boundary_model": None,
    }


def jdn_to_date(jdn: int) -> datetime.date:
    return datetime.date.fromordinal(jdn - 1721425)


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


def ahom_dinching_start_jdn(gregorian_year: int,
                             tz_hours: float = DEFAULT_AHOM_TZ_HOURS) -> int:
    """Reconstruct Din Ching day 1 independently of the Myanmar calendar."""
    november_1 = to_jdn(gregorian_year, 11, 1)
    december_1 = to_jdn(gregorian_year, 12, 1)
    for jdn in range(november_1, december_1):
        if new_moon_day_before_or_on(jdn, tz_hours) == jdn:
            return jdn + 1
    raise RuntimeError(f"no reconstructed Din Ching new moon in {gregorian_year}")


def ahom_month_starts(cycle_year: int,
                      tz_hours: float = DEFAULT_AHOM_TZ_HOURS) -> list[int]:
    """Return the 12 or 13 reconstructed lunar-month starts in a Lakni year."""
    start = ahom_dinching_start_jdn(cycle_year, tz_hours)
    end = ahom_dinching_start_jdn(cycle_year + 1, tz_hours)
    starts = [start]
    for jdn in range(start, end):
        if new_moon_day_before_or_on(jdn, tz_hours) == jdn and jdn + 1 < end:
            starts.append(jdn + 1)
    if len(starts) not in (12, 13):
        raise RuntimeError(
            f"reconstructed Lakni year {cycle_year} has {len(starts)} lunar months")
    return starts


def ahom_calendar_for_date(y: int, m: int, d: int,
                           tz_hours: float = DEFAULT_AHOM_TZ_HOURS) -> dict:
    """Convert a Gregorian date using the explicitly reconstructed Ahom model.

    Boundary priority: the Lakni and month both change at local midnight on
    the civil day following the closing new moon of month 12.
    """
    jdn = to_jdn(y, m, d)
    this_start = ahom_dinching_start_jdn(y, tz_hours)
    cycle_year = y if jdn >= this_start else y - 1
    year_start = ahom_dinching_start_jdn(cycle_year, tz_hours)
    next_year_start = ahom_dinching_start_jdn(cycle_year + 1, tz_hours)
    starts = ahom_month_starts(cycle_year, tz_hours)
    month_index = max(i for i, start in enumerate(starts) if start <= jdn)
    has_leap_month = len(starts) == 13
    is_leap_month = has_leap_month and month_index == 8
    if is_leap_month:
        month_number = 8
        month_name = "Leap after Din Pet"
    else:
        month_number = month_index + 1 - (1 if has_leap_month and month_index > 8 else 0)
        month_name = AHOM_MONTHS[month_number - 1]
    month_end = starts[month_index + 1] if month_index + 1 < len(starts) else next_year_start
    lakni = ahom_lakni_for_cycle_year(cycle_year)
    offset = datetime.timezone(datetime.timedelta(hours=tz_hours))
    change_local = datetime.datetime.combine(jdn_to_date(year_start), datetime.time(), offset)
    return {
        **lakni,
        "year_start_jdn": year_start,
        "year_start_date": jdn_to_date(year_start),
        "preceding_new_moon_date": jdn_to_date(year_start - 1),
        "next_year_start_date": jdn_to_date(next_year_start),
        "new_year_change_local": change_local,
        "boundary_priority": "change Lakni and start Din Ching day 1 together",
        "month_number": month_number,
        "month_name": month_name,
        "month_day": jdn - starts[month_index] + 1,
        "month_length": month_end - starts[month_index],
        "is_leap_month": is_leap_month,
        "months_in_year": len(starts),
        "boundary_model": AHOM_BOUNDARY_MODEL,
    }


def full_report(y: int, m: int, d: int, tz_hours: float = DEFAULT_TZ_HOURS,
                rule: str = DEFAULT_BOUNDARY) -> str:
    import sakkaraj as _sakkaraj
    jdn = to_jdn(y, m, d)
    dt = datetime.date(y, m, d)
    ahom = ahom_calendar_for_date(y, m, d)
    ty = tai_year_for(y, m, d, rule)
    st = tai_structural_year(ty)
    dy = day_sexagenary(jdn)
    ld = lunar_phase(jdn, tz_hours)
    md = _sakkaraj.jdn_to_myanmar(jdn)
    phase_txt = ld["phase"] if ld["day"] is None else f"{ld['phase']} day {ld['day']}"
    cs = _sakkaraj.cs_year_for(y, m, d)
    sok_digit = cs % 10
    sok_names = ["samritthisok", "ekasok", "thosok", "trisok", "chattawasok",
                 "benchasok", "chosok", "sappasok", "atthasok", "noppasok"]
    lines = [
        f"Gregorian date : {dt.isoformat()} ({WEEKDAYS[(dt.weekday() + 1) % 7]})",
        f"Ahom Lakni*    : {ahom['position']}/60 {ahom['name']}  [changed {ahom['new_year_change_local'].isoformat()}; after new moon {ahom['preceding_new_moon_date']}]",
        f"Ahom month*    : {ahom['month_number']} {ahom['month_name']} day {ahom['month_day']}/{ahom['month_length']}  [{ahom['months_in_year']} lunar months]",
        f"Ganzhi compare : {st['name']} = {st['element']} {st['son'].split('(')[1][:-1]}  [civil year {ty}, boundary {rule}]",
        f"Shan spelling  : {st['shan_stem']}-{st['son'].split('/')[0].split()[0]}",
        f"Sakkaraj era   : {cs} CS (sok {sok_digit} = {sok_names[sok_digit]})",
        f"Day name       : {dy['name']}  ({dy['index']}/60) [{dy['mother']} x {dy['son']}]",
        f"Day in Shan    : {dy['shan']}  ({dy['mother_shan']} {dy['son_shan']})",
        f"Myanmar date   : ME {md['my']} {md['month_name']} {md['phase']} {md['fortnight_day']}",
        f"Moon estimate  : {phase_txt}  [true-conjunction estimate, UTC+{tz_hours:g}]",
        f"Julian Day No. : {jdn}",
        "* Ahom lunar date is an explicit seasonal/new-moon reconstruction; not a Nadaw conversion.",
    ]
    return "\n".join(lines)


def self_test() -> None:
    assert len(AHOM_LAKNI_60) == 60
    assert AHOM_LAKNI_60[0] == "Kap Cheu"
    assert AHOM_LAKNI_60[17] == "Rung Shiu"
    assert AHOM_LAKNI_60[59] == "Ka Keu"
    assert ahom_lakni_for_cycle_year(2008)["name"] == "Kap Cheu"
    assert ahom_lakni_for_cycle_year(2025)["name"] == "Rung Shiu"
    assert jdn_to_date(ahom_dinching_start_jdn(2025)) == datetime.date(2025, 11, 21)
    before = ahom_calendar_for_date(2025, 11, 20)
    after = ahom_calendar_for_date(2025, 11, 21)
    assert (before["cycle_year"], after["cycle_year"]) == (2024, 2025)
    assert (after["name"], after["month_name"], after["month_day"]) == (
        "Rung Shiu", "Din Ching", 1)
    assert ahom_calendar_for_date(2024, 11, 2)["months_in_year"] == 13
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
    assert tai_year_for(2026, 1, 1, "songkran") == 2025
    assert tai_year_for(2026, 4, 13, "songkran") == 2025
    assert tai_year_for(2026, 4, 14, "songkran") == 2026
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
        "phase": "waxing", "day": 11, "new_moon_jdn": to_jdn(2026, 8, 12)}
    assert lunar_phase(to_jdn(2026, 8, 23), tz_hours=5.5) == {
        "phase": "waxing", "day": 11, "new_moon_jdn": to_jdn(2026, 8, 12)}
    print("all self-tests passed")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Tai Ahom Lak-Ni calendar converter")
    p.add_argument("date", nargs="*", help="YYYY MM DD (defaults to today)")
    p.add_argument("--test", action="store_true", help="run self-tests")
    p.add_argument("--tz", type=float, default=DEFAULT_TZ_HOURS,
                   help="timezone offset hours for lunar phase (default 5.5 Assam)")
    p.add_argument("--boundary", choices=sorted(YEAR_BOUNDS), default=DEFAULT_BOUNDARY,
                   help="boundary for the comparative ganzhi year only")
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
