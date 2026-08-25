# Lakni and Lak Jeng: comparative Tai calendar algorithms

This repository is an educational, source-led toolkit for Tai communities studying
sexagenary year and day cycles. It keeps related traditions comparable without treating
them as one universal calendar.

> A shared 10-by-12 naming structure does not imply a shared epoch, New Year boundary,
> month system, spelling, or regional calendar authority.

## What is implemented

| Component | Community/tradition | What the program calculates |
|---|---|---|
| `lak_ni.py` | Tai Ahom | Historical 60-year Lakni names; explicitly reconstructed Dinching lunar months and New Year; no Nadaw-derived boundary |
| `lak_jeng.py` | Trans-border Tai/Shan | Lak Jeng worksheet; continuous day cycle; Tai New Year at month 1 waxing 1 |
| `sakkaraj.py` | Myanmar and regional CS research | Thingyan, five historical watat regimes, exception years, Myanmar date conversion, Thai avoman integers |

No external Python package is required.

```bash
cd python

python3 lak_ni.py 2026 8 23
python3 lak_jeng.py --date 2026 8 23
python3 sakkaraj.py 2015 7 31
python3 -m unittest discover -s ../tests -v
```

A dependency-free C11 port of all three calculation engines is available in
[`c/`](c/):

```bash
cmake -S c -B build/c
cmake --build build/c
ctest --test-dir build/c --output-on-failure

build/c/lakni 2026 8 23
build/c/lak-jeng --date 2026 8 23
build/c/sakkaraj 2015 7 31
```

An idiomatic C++17 API and matching command-line programs are available in
[`cpp/`](cpp/). They use the verified C calculation core and return owned C++
value types:

```bash
cmake -S cpp -B build/cpp
cmake --build build/cpp
ctest --test-dir build/cpp --output-on-failure

build/cpp/lakni-cpp 2026 8 23
build/cpp/lak-jeng-cpp --date 2026 8 23
build/cpp/sakkaraj-cpp 2015 7 31
```

Example corrected result:

```text
Gregorian date : 2026-08-23
Ahom Lakni*    : 18/60 Rung Shiu
Ahom month*    : reconstructed lunar month and day
Ganzhi compare : Rai-Singa = fire horse
Myanmar date   : ME 1388 Wagaung waxing 10
```

The asterisk is important: the Ahom result is a transparent reconstruction, not a claim
that the unpublished priestly calculation constants have been recovered.

## 1. Keep the year cycles separate

### Historical Ahom Lakni

Kapoor's reconstruction of the Ahom chronicles gives November 1228-November 1229 as
**Kap Cheu**, position 1; Dinching (Aghon) as the first Ahom month; a new cycle beginning
in 2008; and an Ahom cycle that ran independently from the Chinese cycle.

```text
Mothers : Kap Dap Rai Mung Plek Kat Khut Rung Tao Ka
Children: Cheu Plao Ngi Mao Shi Shiu Shinga Mut San Rao Mit Keu

1  Kap Cheu
18 Rung Shiu
60 Ka Keu
```

`ahom_lakni_for_cycle_year()` exposes the historical name table without deriving an
Ahom date from Myanmar Nadaw. `ahom_calendar_for_date()` separately implements the
published boundary statement—Lakni changes when Dinching begins on the civil day after
the new moon ending month 12—through this explicit reconstruction:

1. Dinching starts on the day after the first Assam-local new moon on or after 1 November.
2. The Lakni name and month both change at local midnight on that following civil day.
3. Successive local new moons start the remaining lunar months.
4. If thirteen lunations occur before the next Dinching, the reconstructed leap lunation
   is placed after month 8, following the comparative rule reported for the related Shan
   system.

The seasonal anchor, leap placement, and astronomical new-moon calculation remain
model assumptions because the complete historical Ahom priestly constants are not yet
available in a published, verifiable edition.

See [`LAKNI_NEW_YEAR_SOURCES.md`](LAKNI_NEW_YEAR_SOURCES.md) for the evidence hierarchy,
exact pages, institutional links, manuscript catalogue records, and the required wording
for citing a generated reconstructed date.

#### The twelve Ahom months

The published sequence is:

| Number | Ahom month | Approximate Assamese correspondence |
|---:|---|---|
| 1 | Din Ching / Dinching | Aghon |
| 2 | Din Kam | Puh / Poush |
| 3 | Din Sham | Magh |
| 4 | Din Shi | Falgun |
| 5 | Din Ha | Chaitra |
| 6 | Din Ruk | Baisakh |
| 7 | Din Chit | Jeth / Jaistha |
| 8 | Din Pet | Ahar |
| 9 | Din Kao | Sawon |
| 10 | Din Ship | Bhadra |
| 11 | Din Shipit | Ahin / Ashwin |
| 12 | Din Shipshang | Kartik |

The correspondences are seasonal comparisons, not equations with the Assamese month
boundaries. The sequence is published in Kapoor 2021, Appendix, p. 686, following
Terwiel's study of Tai time-reckoning. See the direct links in
[`LAKNI_NEW_YEAR_SOURCES.md`](LAKNI_NEW_YEAR_SOURCES.md).

#### Why Shan says month 9 while Ahom says month 10

On 23 August 2026 the calendars use three different ordinal systems:

| Calendar | Date label |
|---|---|
| Reconstructed Ahom | Din Ship, month 10, day 11 |
| Shan | Lön Kao, month 9 |
| Myanmar | Wagaung waxing 10, Myanmar month 5 |

Myanmar Era 1388 is a big `watat` year. It contains the additional First Waso.
Numbering the lunations from the Shan New Year therefore gives:

```text
1   Nadaw / Lön Seng
2   Pyatho
3   Tabodwe
4   Tabaung
5   Tagu
6   Kason
7   Nayon
8a  First Waso — extra month
8b  Waso
9   Wagaung / Lön Kao
```

The historical [*Gazetteer of Upper Burma and the Shan
States*](https://myanmar-law-library.org/IMG/pdf/shan_state_part_i_volume_ii.pdf)
identifies Lön Seng as Shan month 1 corresponding to Nadaw, and Lön Kao as Shan
month 9 corresponding to Wagaung. In the national Myanmar sequence, however, Wagaung
is month 5; “Shan month 9” and “Myanmar month 9” do not mean the same month.

The current Ahom reconstruction did not insert a leap month in its 2025-26 Lakni year:

```text
1   Din Ching       21 Nov 2025
2   Din Kam         21 Dec 2025
3   Din Sham        20 Jan 2026
4   Din Shi         18 Feb 2026
5   Din Ha          20 Mar 2026
6   Din Ruk         18 Apr 2026
7   Din Chit        18 May 2026
8   Din Pet         16 Jun 2026
9   Din Kao         15 Jul 2026
10  Din Ship        13 Aug 2026
11  Din Shipit      12 Sep 2026
12  Din Shipshang   11 Oct 2026
```

Consequently, the August lunation is Ahom month 10 but Shan month 9. They refer to
approximately the same lunar period, but the Shan ordinal is one behind after its
repeated eighth month. This comparison does **not** prove the historical Ahom leap-month
placement: the Ahom dates above are generated by the explicitly reconstructed model,
and an edited Ahom intercalation table could change the result.

### Contemporary Tai/Shan lunar year

The Tai year turns on waxing day 1 of Tai month 1. In the Myanmar calendar this
corresponds to Nadaw waxing 1. `sakkaraj.tai_lunar_new_year()` calculates the
correspondence with the complete Myanmar month engine instead of choosing the last
astronomical new moon in a November-December window.

This describes the trans-border Tai lunar tradition used by Shan/Tai Yai and related
communities in Myanmar, Yunnan, and northern Thailand. It is not a claim about the
official national New Year rule of Myanmar, China, or Thailand.

```text
Tai year 2120 began 2025-11-20
Tai year 2121 begins 2026-12-10
```

### Chinese-aligned comparison

`tai_structural_year()` retains `(year - 4) mod 60` so learners can compare Tai
spellings with Chinese ganzhi. It is explicitly printed as a comparison, not as the
historical Ahom Lakni year.

## 2. Continuous 60-day cycle

The modern comparative day counter uses:

```text
index = (JDN - 2433191) mod 60
```

The anchor states that 1949-10-01 was a jiazi/Kap-Jai day. Mothers and children are
selected by `index mod 10` and `index mod 12`. More independently dated Ahom records are
needed before claiming that every historical locality used this exact absolute offset.

## 3. Lak Jeng source worksheet

`lak_jeng.calculate(T)` preserves the integer procedure documented by Sua Tai Mong:

```text
Y = T - 1
C = 7 floor(Y/1350) + floor((Y mod 1350)/193)
N = 292207Y + C + 6869
A = ceil(N/800)
M = 11A - floor(Y/25) + 420
D, P = divmod(M, 692)
```

This is a reproducible source worksheet, not silently forced into the Gregorian
converter. The formula gives `A=772531` for T=2116 while the source's dated statement
gives `A=772521`, a ten-day disagreement. Both are preserved as separate evidence until
the epoch offsets can be derived from stronger sources.

## 4. Myanmar/Sakkaraj machinery

For the focused answer to whether Songkran and Thingyan use the same Sakkaraj calendar,
see [`SONGKRAN_THINGYAN.md`](SONGKRAN_THINGYAN.md). They share an era family and an
Aries-ingress New Year idea, but not one interchangeable regional calendar algorithm.

The engine follows Yan Naing Aye's published `mmcal` method and includes:

- Makaranta system 1, ME <= 797;
- Makaranta system 2, ME 798-1099;
- Thandeikta, ME 1100-1216;
- colonial era, ME 1217-1311;
- post-independence era, ME >= 1312;
- full-moon corrections and exceptional watat years;
- common, little-watat, and big-watat detection;
- conversion in both directions between JDN and Myanmar dates.

Exception tables materially change results:

| Myanmar year | Correct result |
|---|---|
| 1263 | big watat |
| 1264 | common |
| 1344 | little watat |
| 1345 | common |
| 1377 | big watat; Second Waso full moon JDN 2457235 (2015-07-31) |

Future official Myanmar calendars may still be adjusted by calendar authorities. An
algorithm can reproduce a published method; it cannot create future cultural authority.

## 5. Conventional calendar versus Moon estimate

`lak_ni.py` prints two deliberately separate results:

- **Myanmar date**: conventional mean-calendar month, phase, and fortnight day;
- **Moon estimate**: phase estimated from a Meeus true-conjunction calculation.

True and mean new moons can fall on different civil days. The astronomical estimate is
useful evidence, but it is not a traditional calendar conversion.

## 6. Verification

```bash
python3 -m unittest discover -s tests -v
python3 python/lak_ni.py --test
python3 python/lak_jeng.py --test
python3 python/sakkaraj.py --test
```

Regression tests pin source-based facts rather than only comparing functions that share
the same constant: Ahom Table 9 positions, the 2008 restart, 2025 Shan New Year,
Myanmar exception years, published Waso anchors, JDN/Myanmar round trips, and the
unresolved Lak Jeng ten-day discrepancy.

## 7. Terminology and scope

- **Lakni / Lak Ni**: Ahom calendrical dating; context may mean the current sexagenary
  year or the broader system of year, month, day, and time.
- **Lak Jeng**: the Shan/Tai calculation procedure studied here.
- **Mother/Child**: the 10- and 12-name wheels producing 60 pairs.
- **Sakkaraj / CS / ME**: related era terminology whose regional boundary must be stated.
- **Watat**: intercalary Myanmar year; a big watat also adds a day to Nayon.

Romanization varies. A spelling difference is not automatically a cycle-position
difference.

## 8. Sources

1. R. C. Kapoor, "Fixing the Chronology in Tai-Ahom Chronicles by Using Astronomical
   References," *Journal of Astronomical History and Heritage* 24(3), 2021, pp. 665-687.
   Page 668 supports the Dinching/New Moon boundary; pp. 686-687 and Tables 7-9 support
   the month order and 60 Lakni names. Institutional record and full paper:
   https://prints.iiap.res.in/handle/2248/7856
   https://prints.iiap.res.in/bitstream/handle/2248/7856/Fixing%20the%20chronology%20in%20tai-ahom%20chronicles%20by%20using%20astronomical%20references.pdf?sequence=1
2. Yan Naing Aye, "Algorithm, Program and Calculation of Myanmar Calendar," and the
   MIT-licensed `mmcal` reference implementation. https://github.com/yan9a/mmcal
3. B. J. Terwiel and Ranoo Wichasin, [*Tai Ahoms and the Stars*](https://www.cornellpress.cornell.edu/book/9780877277095/tai-ahoms-and-the-stars/),
   Cornell Southeast Asia Program, 1992, ISBN 978-0-87727-709-5.
4. Sua Tai Mong, ["Method for Calculating the Lak Jeng Cycle"](https://www.facebook.com/share/1DqdDNsA1o/?mibextid=wwXIfr),
   21 November 2021. This community-source link may require a Facebook login.
5. Jean Meeus, [*Astronomical Algorithms*](https://1535.sydneyplus.com/genieplus/final/ViewRecord.aspx?record=9ff397d1-1fba-479f-85ab-8a51de0ca72c&template=Books),
   2nd ed., Willmann-Bell, 1998, chapter 49, ISBN 0-943396-61-1.
6. Ebenezer Burgess (trans.), [*Translation of the Surya-Siddhanta*](https://commons.wikimedia.org/wiki/File%3ATRANSLATION_OF_THE_SURYA-SIDDHANTA_%28IA_dli.bengal.10689.17955%29.pdf),
   American Oriental Society, 1860, chapter I (public-domain scan).
7. Golap Chandra Barua (ed. and trans.), *Ahom-Buranji*, Assam Administration,
   1930, p. 327, as cited and interpreted by Kapoor. Public NVLI scan:
   https://ocrdigitalfile.nvli.in/cslrepository/4028/RB860-ocr.pdf
8. British Library, EAP373/14/5, Ahom manuscript catalogue record; documents the
   repeating 60-year ambiguity and one-to-two-year variation among conversions:
   https://searcharchives.bl.uk/catalog/040-003345135

## Research status

Suitable for education, comparison, and reproducible research. Historical results
should cite a community, source, boundary model, and uncertainty. Contributions of dated
almanacs, inscriptions, manuscript readings, and community-reviewed terminology are
especially welcome.
