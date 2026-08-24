# The Sakkaraj Era — Deep Research Notes

Research companion to `lak_ni.py` / `lak_jeng.py`. Covers the **Chula Sakarat**
(သက္ကရာဇ် *Thet Kayit*, จุลศักราช *Chula Sakarat*, ចុល្លសករាជ) — the "small era"
that became the master clock of mainland Southeast Asia: Myanmar, Thailand, Laos,
Cambodia, the Shan states, Sipsongpanna, and — alongside Lak-Ni — the Ahom kingdom.

Implementation: **`sakkaraj.py`** (same folder), verified against published anchor data.

---

## 1. The Sakkaraj family of eras

"Sakkaraj" (Pali *sakkarāja*, Skt. *śakakāla*, "era of the Śaka") names a whole family
of stacked epochs. Mainland traditions remember them as successive royal re-numberings:

| Era | Epoch (traditional) | Zero-point date | Notes |
|---|---|---|---|
| **Anjanasakaraj** (မဟာ သက္ကရာဇ်) | King Anjana | 10 March **691 BCE** | device for pre-Buddhist dates, avoids negative years |
| **Buddha Sakaraj** (သာသနာ သက္ကရာဇ်) | Parinibbāna | 11–13 May **544 BCE** | BE = CS + 1182 (Burma/Ceylon); Thailand counts one less |
| **Mahāsakaraj / Śaka** | Kaṇiṣka accession (legend); Ujjain astronomers (history) | 17 March **78 CE** | the Indian Śaka era; still India's official civil era |
| **Cula Sakaraj (CS)** | King Popphausawraḥan of Pagan abolishes MS at year 560 | 22 March **638 CE** | THE era of this document; 78 + 560 = 638 |
| Mohnyin era | Mohnyin thado minsaw | 18 March **1436** | regional, short-lived |
| Magi-San | same epoch as CS | 22 March 638 | name used in Chittagong |

The chronicle chain (Sao Saimong Mangrai, JSS 1981): Buddha Śāsanā era → abolished at
621/622 by "Tricakkhu" → **Mahāsakaraj** (= Śaka 78 CE) → abolished at year 559/560 by
Anuruddha/Popphausawraḥan → **Cula Sakaraj**, 638 CE. Arakan founded its identical era
the same year under Thareyarenu of Dinyawadi. Some scholars suspected a later back-dating;
radiocarbon dating of Śrī Kṣetra (first millennium CE habitation) restored plausibility.

**Counting convention:** CS counts **elapsed years** — the epoch year itself is year 0.
Thus April 1999 – April 2000 = CS 1361.

---

## 2. The astronomical engine

Myanmar calendar calculation is a **mean** lunisolar system built on
Sūrya Siddhānta stock. Related Sakkaraj calendars in other regions can use different
month numbering, leap-day placement, and year boundaries.

### 2.1 Constants

| Constant | Value | Meaning |
|---|---|---|
| `SY` (modern/Thandeikta) | 1577917828 / 4320000 = **365.2587564815 d** | mean **sidereal** year (6h 12m 36.56s) |
| `SY₀` (old Makaranta) | 292207 / 800 = **365.25875 d** | the abbreviated form (see Lak-Jeng README: the 1350/193 correction restores exactly the modern figure over a mahāyuga) |
| `LM` | 1577917828 / 53433336 = **29.53058795 d** | mean synodic month |
| tithi ratio | **703 tithis : 692 solar days** | ⇒ month = 30×692/703 = 29.530583 d |
| `MO` (Myanmar era 0) | JD **1954168.050623** | fitted start of Myanmar year 0 |
| excess/year | SY − 12·LM = **10.8917011 d** | drives all intercalation logic |

The 703:692 tithi law gives the Metonic bundle automatically:
19 years × 235 months × 30 tithis = 7050 tithis = 6939.687055 solar days
→ mean "lunar" year 365.24667 d — Hipparchus' tropical year. This mismatch between the
*tropical-flavored* lunar wheel and the *sidereal* solar wheel (~12 days drift by ME 1100)
is the central drama of Sakkaraj history.

### 2.2 Five implemented Myanmar calculation regimes

| Regime | Span | `WO` | `NM` | Watat rule |
|---|---:|---:|---:|---|
| Makaranta 1 | ME <= 797 | -1.1 plus exceptions | -1 | 19-year Metonic |
| Makaranta 2 | ME 798-1099 | -1.1 plus exceptions | -1 | 19-year Metonic |
| Thandeikta | ME 1100-1216 | -0.85 plus exceptions | -1 | 19-year Metonic plus exceptions |
| Colonial | ME 1217-1311 | -1 plus exceptions | 4 | excess-day threshold plus exceptions |
| Post-independence | ME >= 1312 | -0.5 plus exceptions | 8 | excess-day threshold plus exceptions |

The full-moon and watat exception tables are part of the algorithm, not optional
corrections. Omitting them reverses ME 1263/1264 and 1344/1345 and puts the Second Waso
full moon of ME 1377 one day early.

Fixed insertion points (unique to Burma, unlike India): the leap-month **First Waso**
(30 days, always immediately before Waso), and the leap-day always as a **second day of
Nayon** (Nayon 29→30), only ever in a watat year.

### 2.3 Current-era watat algorithm (Yan Naing Aye / cool-emerald)

```
ja          = SY·my + MO                          # JD of year start (atat time)
jk          = ja − 2.169918982                    # akya time (Thingyan starts)
ed          = (SY·(my + 3739)) mod LM             # excess days at year start
TA          = (12 − NM)·(SY/12 − LM)              # NM = 8 in current era
if ed < TA: ed += LM
TW          = LM − NM·(SY/12 − LM)                # = 22.2694539
watat       ⇔  ed ≥ TW                            # leap-month year
```

For watat years, the **full moon of Second Waso** fixes everything downstream:

```
w  = round(SY·my + MO − ed + 4.5·LM + WO)         # WO = −0.5 (current era)
diff vs previous watat year's w, taken mod 354:
      remainder 30 → little watat (384-day year)
      remainder 31 → big watat    (385-day year, Nayon gets 30 days)
```

Year lengths: common **354**, little watat **384**, big watat **385**.
Months alternate 29/30 (Tagu 29, Kason 30, Nayon 29(+b), First Waso 30, Waso 30, …).
Day-within-month uses the closed-form `mm`, `md`, `fd`, `mp` equations (cool-emerald §7),
already summarized in this repo's README §6.

**Thingyan:** New Year = Sun's entry into Aries (Mesha saṁkrānti) = `ja`. The festival
runs akya (ja − 2.1699…d) → atat (ja); only the day *after* atat is "New Year's Day".
Before ME 1312 the festival length was 2.1675 d.

### 2.4 No canonical future

Because each reform moved the Metonic pattern ad hoc (and Irwin proposed de Cheseaux's
1040-year cycle without adoption), **future Myanmar dates beyond published tables have no
binding authority** — the Myanmar Calendar Advisory Board declares them year by year.
Algorithms reproduce official practice, not legislate it.

---

## 3. Regional variants — same era, different machines

Adopted from Burma: Lan Na (13th c.), Siam (16th c.), Lan Xang, Cambodia, Kengtung,
Sipsongpanna. Each kept local machinery:

### 3.1 Month numbering chaos (inscription hazard)

| Region | First numbered month |
|---|---|
| Kengtung | Tazaungmon (Karttika) |
| Lan Na (Chiengmai) | Thadingyut (Āśvina) — "Month One" |
| Western Shan / Central Thailand | Thadingyut counted as "Month Eleven" |
| Lan Xang, Sukhothai | Nadaw (Mārgaśīrṣa) |

Same night can be "Month Twelve waning 1" (Kengtung), "Month Eleven waning 1"
(Bangkok), or "Month One waning 1" (Chiengmai). Reading old inscriptions requires
region-aware translation, not just era math.

### 3.2 Siam: leap-DAY in ordinary years

Where Burma appends the extra day inside big-watat years (385), **Siamese practice moves
it into an ordinary year** (355), so the type set is {354, 355, 384} instead of
{354, 384, 385}. Totals over 19 years agree. Extra day likewise inserted after
Jyeṣṭha/Nayon.

### 3.3 The La Loubère / avoman method (Thai line, 1688 → Faraut → Eade)

Working purely in integers from the old-SY fraction:

```
q, R = divmod(292207·CS_year + 373, 800)
ahargana    h₀ = q + 1                       # days to New Year's Eve
kammacabala k  = 800 − R                     # age-of-year fraction (≤207 → solar leap)
avoman      a₀ = (h₀·11 + 650) mod 692       # tithi accumulator (703:692 inverted)
```

- **solar leap year** ⇔ kammacabala ≤ 207
- **leap day needed** ⇔ a₀ ≤ 137 (normal year) or a₀ ≤ 126 (solar leap year);
  complex adjacency rules then push it out of any year holding a leap month
- each civil day advances a₀ by 11 (mod 692); month boundaries where the tithi counter
  jumps — the classic "missing day"

Worked (Gislén): CS **1238** → h₀ = 452,191; kammacabala 161 → solar leap; a₀ = 655.

### 3.4 Era arithmetic cheat-sheet

```
CS  = AD − 638        after the computed New Year day following atat
    = AD − 639        before that year's computed boundary
BE  = CS + 1182       (Burma/Ceylon); Thailand BE = CS + 1181
MS/Śaka = AD − 78     (after mid-March)
Anjana  = AD + 691
AD year begins ≈ 3.5 months BEFORE the CS year of that number
```

---

## 4. Sakkaraj among the Tai peoples

- Ahom Buranjis double-date events with **Lak-Ni name + Sakkaraj year**; `lak_ni.py`
  prints CS for every query (`1388 CS` for 2026).
- Shan/Khün sources date precisely as Sao Saimong quotes: *"Year Ko-san CS 1342,
  Month Twelve, Waning 1st night"* (Oct 1980, Kengtung) — animal-name + CS + month +
  fortnight + day, i.e., the exact field set our tools compute.
- The Great-Dai/Shan calendar of Sipsongpanna (epoch 95 BCE) is a *different* era again;
  its Small-Dai variant coincides with CS (epoch 638) — see lak_jeng bridge notes.

---

## 5. Worked verification anchors (implemented in `sakkaraj.py --test`)

| Fact | Source | Status |
|---|---|---|
| ME 1375 begins JD 2456398.8408 = 2013-04-16 08:10 | cool-emerald ex. | pass |
| ME 1374 excess days = 24.1094385; watat | cool-emerald ex. | pass |
| Full moon 2nd Waso ME 1374 = JDN 2456142 = 2012-08-02 | cool-emerald ex. | pass |
| ME 1374 is **little** watat (Δw mod 354 = 30) | cool-emerald §5 | pass |
| CS 1238: h₀ = 452191, kammacabala 161 (solar leap), a₀ = 655 | Gislén 2015 | pass |
| CS 1341 still running 1980-03-31; CS 1342 from ~Apr 15 1980 | Sao Saimong 1981 | pass |
| Thingyan length switch 2.169918982 d at ME ≥ 1312 | cool-emerald | pass |

## 6. References

1. Y. N. Aye, *Algorithm, Program and Calculation of Myanmar Calendar* (2013) — current-era constants; http://cool-emerald.blogspot.com/2013/06/algorithm-program-and-calculation-of.html
2. J. C. Eade / L. Gislén, *The Calendars of Southeast Asia* (2 vols.) & Gislén, "Burmese Eclipse Calculations", JAHH 18 (2015) — avoman/kammacabala line, La Loubère reconstruction.
3. A. M. B. Irwin, *The Burmese & Arakanese Calendars* (1909) — Makaranta vs Thandeikta history; https://en.wikisource.org/wiki/The_Burmese_%26_Arakanese_Calendars
4. Sao Saimong Mangrai, "Cula Sakaraja and the Sixty Cyclical Year Names", JSS 69 (1981) — era-succession chronicles; https://thesiamsociety.org/wp-content/uploads/1981/03/JSS_069_0d_SaoSaimong_CulaSakarajaAndSixtyCyclicalYearNames.pdf
5. *Burmese calendar*, Wikipedia — era table, regional month-numbering, Thai/Burmese leap-type contrast.
6. Burgess (trans.), *Sūrya Siddhānta*, ch. I vv. 34–37 — sunrise-to-sunrise civil day; see README ref [7].
