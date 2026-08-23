#!/usr/bin/env python3
"""Sakkaraj (Chula Sakarat / Thet Kayit) era calculator.

Implements the mainland-SE-Asian mean lunisolar machinery descended from the
Surya Siddhanta, epoch 22 March 638 CE:
  * era conversions (CS, AD, Buddhist Era, Mahasakaraj/Saka, Anjana)
  * Myanmar current-era algorithm (cool-emerald): year start ja, Thingyan
    akya/atat, excess days, watat/big-watat determination, full moon of
    Second Waso
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
    return ad_year - 639 if (month, day) < (4, 14) else ad_year - 638


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


def is_watat(my: int) -> dict:
    ed = excess_days(my)
    nm = 8 if my >= SE3 else 4
    ta = (12 - nm) * (SY / 12 - LM)
    tw = LM - nm * (SY / 12 - LM)
    adj = ed + LM if ed < ta else ed
    return {"ed_raw": round(ed, 7), "ed": round(adj, 7), "watat": adj >= tw,
            "threshold_tw": round(tw, 7)}


def second_wasoo_full_moon(my: int, ed: float) -> int:
    wo = -0.5 if my >= SE3 else -1.0
    return round(SY * my + MO - ed + 4.5 * LM + wo)


def watat_type(my: int) -> dict:
    info = is_watat(my)
    if not info["watat"]:
        return {**info, "type": "common (354)", "waso_fm": None}
    w = second_wasoo_full_moon(my, info["ed"])
    prev = my - 1
    while not is_watat(prev)["watat"]:
        prev -= 1
    w_prev = second_wasoo_full_moon(prev, is_watat(prev)["ed"])
    rem = (w - w_prev) % 354
    kind = "big watat (385)" if rem == 31 else "little watat (384)"
    return {**info, "type": kind, "waso_fm": w, "prev_wasat": prev}


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
    assert t74["type"].startswith("little") and t74["prev_wasat"] == 1372

    i72 = is_watat(1372)
    assert second_wasoo_full_moon(1372, i72["ed"]) == 2455404

    th1238 = thai_new_year_integers(1238)
    assert th1238["ahargana"] == 452191
    assert th1238["kammacabala"] == 161 and th1238["solar_leap"]
    assert th1238["avoman"] == 655

    assert cs_year_for(1980, 3, 31) == 1341
    assert cs_year_for(1980, 4, 15) == 1342
    assert eras(2026, 8, 23)["cs"] == 1388 and eras(2026, 8, 23)["saka_maha"] == 1948

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
