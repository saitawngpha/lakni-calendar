#!/usr/bin/env python3
"""Sakkaraj (Chula Sakarat / Thet Kayit) era calculator.

Implements the mainland-SE-Asian mean lunisolar machinery descended from the
Surya Siddhanta, epoch 22 March 638 CE:
  * era conversions (CS, AD, Buddhist Era, Mahasakaraj/Saka, Anjana)
  * Myanmar algorithm (cool-emerald/mmcal): five historical calculation
    regimes, exception tables, year start ja, Thingyan akya/atat,
    watat/big-watat determination, and full moon of Second Waso
  * bidirectional conversion between integer JDN and Myanmar calendar dates
  * Thai-line avoman/kammacabala integers (La Loubere -> Faraut -> Eade)

All anchors reproduced in --test are taken from the published sources listed
in SAKKARAJ.md. Note: pure-formula excess days run ~0.00015 d (~13 s) ahead of
the officially tabulated values quoted in the sources; every day-level anchor
(full moons, New Year dates) matches exactly regardless.
"""

import argparse
import datetime
import sys

SY = 1577917828 / 4320000
LM = 1577917828 / 53433336
MO = 1954168.050623
SE3 = 1312
THIRD_ERA_FESTIVAL = 2.169918982
OLD_FESTIVAL = 2.1675

MYANMAR_MONTHS = {
    0: "First Waso", 1: "Tagu", 2: "Kason", 3: "Nayon",
    4: "Waso", 5: "Wagaung", 6: "Tawthalin", 7: "Thadingyut",
    8: "Tazaungmon", 9: "Nadaw", 10: "Pyatho", 11: "Tabodwe",
    12: "Tabaung", 13: "Late Tagu", 14: "Late Kason",
}


def to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def jdn_to_gregorian(jdn: int) -> datetime.date:
    j = jdn - 1721119
    y = (4 * j - 1) // 146097
    j = 4 * j - 1 - 146097 * y
    dd = j // 4
    j = (4 * dd + 3) // 1461
    dd = 4 * dd + 3 - 1461 * j
    dd = (dd + 4) // 4
    m = (5 * dd - 3) // 153
    dd = 5 * dd - 3 - 153 * m
    dd = (dd + 5) // 5
    y = 100 * y + j
    if m < 10:
        m += 3
    else:
        m -= 9
        y += 1
    return datetime.date(y, m, dd)


def cs_year_for(ad_year: int, month: int, day: int) -> int:
    candidate = ad_year - 638
    jdn = to_jdn(ad_year, month, day)
    return candidate if jdn >= thingyan(candidate)["new_year_day"] else candidate - 1


def eras(ad_year: int, month: int, day: int) -> dict:
    cs = cs_year_for(ad_year, month, day)
    return {
        "cs": cs,
        "ad": ad_year,
        "be_burma": cs + 1182,
        "be_thai": cs + 1181,
        "saka_maha": cs + 560,
        "anjana": cs + 1129,
        "myanmar_era_same_as_cs": True,
    }


def thingyan(my: int) -> dict:
    ja = SY * my + MO
    festival = THIRD_ERA_FESTIVAL if my >= SE3 else OLD_FESTIVAL
    jk = ja - festival
    atat_day, akya_day = round(ja), round(jk)
    return {
        "my": my,
        "ja_jd": round(ja, 6),
        "jk_jd": round(jk, 6),
        "akya_day": akya_day,
        "akyo_day": akya_day - 1,
        "atat_day": atat_day,
        "new_year_day": atat_day + 1,
    }


def jd_to_civil(jd: float) -> tuple[int, int, int]:
    d = jdn_to_gregorian(round(jd))
    frac = (jd + 0.5) % 1
    hours = frac * 24
    return d.year, d.month, d.day, hours


def excess_days(my: int) -> float:
    return (SY * (my + 3739)) % LM


def myanmar_year_constants(my: int) -> dict:
    """Return era-specific constants from Yan Naing Aye's mmcal algorithm."""
    if my >= 1312:
        era, wo, nm = 3, -0.5, 8
        full_moon_exceptions = {1377: 1}
        watat_exceptions = {1344, 1345}
    elif my >= 1217:
        era, wo, nm = 2, -1.0, 4
        full_moon_exceptions = {1234: 1, 1261: -1}
        watat_exceptions = {1263, 1264}
    elif my >= 1100:
        era, wo, nm = 1.3, -0.85, -1
        full_moon_exceptions = {
            1120: 1, 1126: -1, 1150: 1, 1172: -1, 1207: 1,
        }
        watat_exceptions = {1201, 1202}
    elif my >= 798:
        era, wo, nm = 1.2, -1.1, -1
        full_moon_exceptions = {
            813: -1, 849: -1, 851: -1, 854: -1, 927: -1,
            933: -1, 936: -1, 938: -1, 949: -1, 952: -1,
            963: -1, 968: -1, 1039: -1,
        }
        watat_exceptions = set()
    else:
        era, wo, nm = 1.1, -1.1, -1
        full_moon_exceptions = {
            205: 1, 246: 1, 471: 1, 572: -1, 651: 1,
            653: 2, 656: 1, 672: 1, 729: 1, 767: -1,
        }
        watat_exceptions = set()
    return {
        "era": era,
        "wo": wo + full_moon_exceptions.get(my, 0),
        "nm": nm,
        "watat_exception": my in watat_exceptions,
    }


def is_watat(my: int) -> dict:
    constants = myanmar_year_constants(my)
    ed = excess_days(my)
    nm = constants["nm"]
    ta = (12 - nm) * (SY / 12 - LM)
    adj = ed + LM if ed < ta else ed
    waso_fm = round(SY * my + MO - adj + 4.5 * LM + constants["wo"])
    if constants["era"] >= 2:
        tw = LM - nm * (SY / 12 - LM)
        watat = adj >= tw
    else:
        tw = None
        watat = ((my * 7 + 2) % 19) // 12 == 1
    if constants["watat_exception"]:
        watat = not watat
    return {
        "era": constants["era"],
        "ed_raw": round(ed, 7),
        "ed": round(adj, 7),
        "watat": watat,
        "threshold_tw": None if tw is None else round(tw, 7),
        "waso_fm": waso_fm,
    }


def second_wasoo_full_moon(my: int, ed: float) -> int:
    constants = myanmar_year_constants(my)
    return round(SY * my + MO - ed + 4.5 * LM + constants["wo"])


def watat_type(my: int) -> dict:
    info = is_watat(my)
    if not info["watat"]:
        return {**info, "type": "common (354)", "waso_fm": None}
    w = info["waso_fm"]
    prev = my - 1
    while not is_watat(prev)["watat"]:
        prev -= 1
    w_prev = is_watat(prev)["waso_fm"]
    rem = (w - w_prev) % 354
    if rem not in (30, 31):
        raise RuntimeError(f"watat discrepancy in ME {my}: remainder {rem}")
    kind = "big watat (385)" if rem == 31 else "little watat (384)"
    return {**info, "type": kind, "waso_fm": w, "prev_watat": prev}


def myanmar_year_info(my: int) -> dict:
    current = is_watat(my)
    distance = 0
    previous = None
    while previous is None or not previous["watat"]:
        distance += 1
        previous = is_watat(my - distance)
        if distance >= 3 and not previous["watat"]:
            raise RuntimeError(f"no previous watat year found near ME {my}")
    year_type = 0
    full_moon = previous["waso_fm"] + 354 * distance
    discrepancy = False
    if current["watat"]:
        remainder = (current["waso_fm"] - previous["waso_fm"]) % 354
        year_type = remainder // 31 + 1
        full_moon = current["waso_fm"]
        discrepancy = remainder not in (30, 31)
    return {
        "year_type": year_type,
        "tagu_1": previous["waso_fm"] + 354 * distance - 102,
        "waso_fm": full_moon,
        "discrepancy": discrepancy,
    }


def jdn_to_myanmar(jdn: int) -> dict:
    """Convert an integer Gregorian JDN to a conventional Myanmar date."""
    jdn = round(jdn)
    my = int((jdn - 0.5 - MO) // SY)
    info = myanmar_year_info(my)
    day_count = jdn - info["tagu_1"] + 1
    big = info["year_type"] // 2
    common = 1 // (info["year_type"] + 1)
    year_length = 354 + (1 - common) * 30 + big
    late = (day_count - 1) // year_length
    day_count -= late * year_length
    threshold = (day_count + 423) // 512
    month = int((day_count - big * threshold + common * threshold * 30 + 29.26) // 29.544)
    e = (month + 12) // 16
    f = (month + 11) // 16
    month_day = day_count - int(29.544 * month - 29.26) - big * e + common * f * 30
    month += f * 3 - e * 4 + 12 * late
    month_length = 30 - month % 2 + (info["year_type"] // 2 if month == 3 else 0)
    if month_day == 15:
        phase, fortnight_day = "full moon", 15
    elif month_day == month_length:
        phase, fortnight_day = "new moon", 15
    elif month_day < 15:
        phase, fortnight_day = "waxing", month_day
    else:
        phase, fortnight_day = "waning", month_day - 15
    return {
        "my": my,
        "year_type": info["year_type"],
        "month": month,
        "month_name": MYANMAR_MONTHS[month],
        "month_day": month_day,
        "month_length": month_length,
        "phase": phase,
        "fortnight_day": fortnight_day,
    }


def myanmar_to_jdn(my: int, month: int, month_day: int) -> int:
    info = myanmar_year_info(my)
    late = month // 13
    adjusted_month = month % 13 + late
    big = info["year_type"] // 2
    common = 1 - (info["year_type"] + 1) // 2
    adjusted_month += 4 - ((adjusted_month + 15) // 16) * 4 + (adjusted_month + 12) // 16
    day_count = (
        month_day + int(29.544 * adjusted_month - 29.26)
        - common * ((adjusted_month + 11) // 16) * 30
        + big * ((adjusted_month + 12) // 16)
    )
    year_length = 354 + (1 - common) * 30 + big
    return day_count + late * year_length + info["tagu_1"] - 1


def thai_new_year_integers(cs: int) -> dict:
    q, r = divmod(cs * 292207 + 373, 800)
    h0 = q + 1
    a0 = (h0 * 11 + 650) % 692
    kammacabala = 800 - r
    return {"ahargana": h0, "remainder_r": r, "kammacabala": kammacabala,
            "solar_leap": kammacabala <= 207, "avoman": a0}


def report(ad_year: int, month: int, day: int) -> str:
    e = eras(ad_year, month, day)
    cs = e["cs"]
    tg = thingyan(cs)
    ay, am, ad_, hh = jd_to_civil(tg["ja_jd"])
    wt = watat_type(cs)
    th = thai_new_year_integers(cs)
    lines = [
        f"Gregorian      : {ad_year}-{month:02d}-{day:02d}",
        f"Sakkaraj (CS)  : {cs}   [BE(Burma) {e['be_burma']} | BE(Thai) {e['be_thai']} | Saka {e['saka_maha']} | Anjana {e['anjana']}]",
        f"CS New Year    : Thingyan atat JD {tg['ja_jd']} ~ {ay}-{am:02d}-{ad_:02d} ({hh:.1f}h local)",
        f"Myanmar year   : {'watat — ' + wt['type'] if wt['watat'] else 'common (354)'}  "
        f"(excess ed={wt['ed']}, TW={wt['threshold_tw']})",
    ]
    if wt["waso_fm"]:
        fy, fm, fd, _ = jd_to_civil(float(wt["waso_fm"]))
        lines.append(f"2nd Waso FM    : JDN {wt['waso_fm']} = {fy}-{fm:02d}-{fd:02d}")
    lines.append(f"Thai integers  : ahargana {th['ahargana']}, kammacabala {th['kammacabala']} "
                 f"({'solar leap' if th['solar_leap'] else 'normal'}), avoman {th['avoman']}")
    return "\n".join(lines)


def self_test() -> None:
    assert to_jdn(2000, 1, 1) == 2451545
    assert jdn_to_gregorian(2451545) == datetime.date(2000, 1, 1)

    tg = thingyan(1375)
    assert abs(tg["ja_jd"] - 2456398.8407875) < 1e-4
    ay, am, ad_, hh = jd_to_civil(tg["ja_jd"])
    assert (ay, am, ad_) == (2013, 4, 16) and abs(hh - 8.17) < 0.1

    i74 = is_watat(1374)
    assert abs(i74["ed"] - 24.1094385) < 3e-4 and i74["watat"]
    assert second_wasoo_full_moon(1374, i74["ed"]) == 2456142
    fy, fm, fd, _ = jd_to_civil(2456142.0)
    assert (fy, fm, fd) == (2012, 8, 2)
    t74 = watat_type(1374)
    assert t74["type"].startswith("little") and t74["prev_watat"] == 1372

    i72 = is_watat(1372)
    assert second_wasoo_full_moon(1372, i72["ed"]) == 2455404

    th1238 = thai_new_year_integers(1238)
    assert th1238["ahargana"] == 452191
    assert th1238["kammacabala"] == 161 and th1238["solar_leap"]
    assert th1238["avoman"] == 655

    assert cs_year_for(1980, 3, 31) == 1341
    assert cs_year_for(1980, 4, 15) == 1341
    assert cs_year_for(1980, 4, 16) == 1342
    assert eras(2026, 8, 23)["cs"] == 1388 and eras(2026, 8, 23)["saka_maha"] == 1948

    assert not is_watat(1345)["watat"] and is_watat(1344)["watat"]
    assert not is_watat(1264)["watat"] and is_watat(1263)["watat"]
    assert watat_type(1377)["type"].startswith("big")
    assert watat_type(1377)["waso_fm"] == 2457235
    nadaw = jdn_to_myanmar(to_jdn(2025, 11, 20))
    assert (nadaw["my"], nadaw["month"], nadaw["month_day"]) == (1387, 9, 1)
    assert myanmar_to_jdn(1387, 9, 1) == to_jdn(2025, 11, 20)

    print("all self-tests passed "
          "(cool-emerald, Gislen and Sao Saimong anchors reproduced)")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Sakkaraj (Chula Sakarat) calculator")
    p.add_argument("date", nargs="*", help="AD YYYY MM DD (defaults to today)")
    p.add_argument("--year", type=int, help="report for a CS/Myanmar year instead of a date")
    p.add_argument("--test", action="store_true")
    args = p.parse_args(argv)

    if args.test:
        self_test()
        return 0

    if args.year is not None:
        tg = thingyan(args.year)
        wt = watat_type(args.year)
        th = thai_new_year_integers(args.year)
        ay, am, ad_, hh = jd_to_civil(tg["ja_jd"])
        print(f"CS/Myanmar year : {args.year}")
        print(f"New Year (atat) : JD {tg['ja_jd']} ~ {ay}-{am:02d}-{ad_:02d} {hh:.1f}h")
        print(f"Akya (festival) : JD {tg['jk_jd']}")
        print(f"Year type       : {'watat — ' + wt['type'] if wt['watat'] else 'common (354)'}")
        if wt["waso_fm"]:
            fy, fm, fd, _ = jd_to_civil(float(wt["waso_fm"]))
            print(f"2nd Waso FM     : JDN {wt['waso_fm']} = {fy}-{fm:02d}-{fd:02d}")
        print(f"Thai integers   : h0={th['ahargana']} kammacabala={th['kammacabala']} "
              f"solar_leap={th['solar_leap']} avoman={th['avoman']}")
        return 0

    try:
        if args.date:
            y, m, d = (int(x) for x in args.date[:3])
            datetime.date(y, m, d)
        else:
            t = datetime.date.today()
            y, m, d = t.year, t.month, t.day
    except (ValueError, IndexError):
        p.error("date must be YYYY MM DD")

    print(report(y, m, d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
