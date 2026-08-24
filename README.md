🇬🇧 [English](README.md) | 🟨🟩🟥 [Shan / Tai](README_SHN.md) | 🇲🇲 [မြန်မာ](README_MY.md)| 🇹🇭 [ภาษาไทย](README_TH.md)

# Lakni and Lak Jeng: comparative Tai calendar algorithms

<p align="center">
  <img
    src="src/poster_lakni_lakjeng.png"
    alt="Lak Ni and Lak Jeng Calendar Research"
    width="100%"
    height="450"
  />
</p>

This repository is an educational, source-led toolkit for Tai communities studying
sexagenary year and day cycles. It keeps related traditions comparable without treating
them as one universal calendar.

> A shared 10-by-12 naming structure does not imply a shared epoch, New Year boundary,
> month system, spelling, or regional calendar authority.

## What is implemented

| Component | Community/tradition | What the program calculates |
|---|---|---|
| `lak_ni.py` | Tai Ahom | Historical 60-year Lakni name; reconstructed Dinching/Nadaw boundary; comparative day and zodiac names |
| `lak_jeng.py` | Shan/Tai | Lak Jeng source worksheet; continuous day cycle; Shan year from conventional Nadaw waxing 1 |
| `sakkaraj.py` | Myanmar and regional CS research | Thingyan, five historical watat regimes, exception years, Myanmar date conversion, Thai avoman integers |

No external Python package is required.

```bash
cd lak_ni_research

python3 lak_ni.py 2026 8 23
python3 lak_jeng.py --date 2026 8 23
python3 sakkaraj.py 2015 7 31
python3 -m unittest discover -s ../tests -v
```

Example corrected result:

```text
Gregorian date : 2026-08-23
Ahom Lakni     : 18/60 Rung Shiu  [began 2025-11-20]
Ganzhi compare : Rai-Singa = fire horse
Myanmar date   : ME 1388 Wagaung waxing 10
```

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

`ahom_lakni_for_date()` anchors position 1 at 2008 and reconstructs Dinching by
aligning it to conventional Nadaw waxing 1. This is a transparent computational model,
not a claim that every historical locality observed the boundary on the same civil day.

### Shan/Tai year

The Shan year turns at conventional Nadaw waxing 1, the first day of the first Shan
lunar month. It is calculated from the complete Myanmar month engine instead of choosing
the last astronomical new moon in a November-December window.

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
python3 lak_ni_research/lak_ni.py --test
python3 lak_ni_research/lak_jeng.py --test
python3 lak_ni_research/sakkaraj.py --test
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
   Tables 7-9 and the November boundary support the corrected Ahom cycle.
   https://prints.iiap.res.in/handle/2248/7856
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

## Research status

Suitable for education, comparison, and reproducible research. Historical results
should cite a community, source, boundary model, and uncertainty. Contributions of dated
almanacs, inscriptions, manuscript readings, and community-reviewed terminology are
especially welcome.
