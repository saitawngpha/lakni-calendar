# Songkran and Thingyan at the Sakkaraj New Year

## Short answer

**They belong to the same historical calendar family, but they are not one identical
calendar.** Myanmar Thingyan, Thai Songkran, Lao Pi Mai, and Khmer Moha Sangkran all
mark the seasonal passage associated with the Sun entering Aries. The older scholarly
calendars also share the Cula Sakaraj epoch of 638 CE. That common origin does **not**
make their lunar dates, leap years, day labels, or modern public holidays identical.

For a date converter, the safe rule is:

> Never apply the Myanmar `thingyan()` result or Myanmar watat table to Thailand, Laos,
> or Cambodia merely because the record uses a Sakkaraj year.

The record's community, year-boundary convention, month numbering, and intercalation
tradition must also be known.

## 1. What is genuinely shared?

### A common solar idea

*Songkran*, *Sangkran*, and Burmese *Thingyan* are regional descendants of Sanskrit
*saṅkrānti*, a solar passage. In this New Year context the intended event is
Meṣa-saṅkrānti: the Sun's entry into Aries. The festivals therefore cluster in the
same mid-April season.

This is a **solar** boundary. The lunar date on which it falls is a consequence of the
regional lunisolar calendar; the Moon does not determine the ingress itself.

### A common era family

The older Burmese and Thai systems use the Cula Sakaraj epoch in 638 CE. Gislén's
comparison states explicitly that the two calendars use the same epoch and the same
traditional mean sidereal-year value in their older forms. Sakkaraj is principally the
numbering of years from that epoch, not a guarantee that all regions use one calendar
table.

Consequently, two records may display the same CS number while assigning a different
month number or lunar day to the same civil date. Near New Year, even the CS year number
is unsafe unless the local boundary rule is known.

## 2. What differs?

| Question | Myanmar | Older Thai line; broadly related Lao/Khmer line |
|---|---|---|
| Solar-year model | Current code uses `SY = 1577917828 / 4320000` and fitted Myanmar epoch `MO` | Classical Thai calculation uses `292207 / 800` with its own epoch constants and integer `kammacabala` |
| Leap month | Myanmar watat rules changed through five historical regimes and include exception years | Thai intercalation is driven by the solar New Year position in Caitra/Vaisakha; it is not the Myanmar exception table |
| Leap day | Added to Nayon inside a big-watat year, producing 385 days | Not allowed in a leap-month year; normally moved to an adjacent ordinary year, producing a 355-day year |
| Possible year lengths | 354, 384, 385 days | 354, 355, 384 days |
| Month number | Myanmar month names/order | Numbering varies among Central Thai, Lan Na, Lao, Khmer, Khün, and Lü traditions |
| New Year civil label | Atat day is partly old and new; the following civil day is Myanmar New Year's Day | Songkran/Sangkran traditions have their own first, intervening, and rising/new-year labels |
| Present public practice | Calculated Thingyan sequence remains part of the Myanmar calendar | Thailand now fixes the civil Songkran holiday at 13–15 April; Lao and Cambodian public observances use their national conventions |

The scholarly result is stronger than "minor regional variation." Gislén concludes
that Thai and Burmese calendars look similar but have **fundamentally different
intercalation schemes**. Thailand, Laos, and Cambodia are close enough to be studied as
one comparative branch, but local implementation and terminology still matter.

## 3. How Thailand, Laos, and Cambodia calculate or assign the days

### Thailand: two calculated solar instants, three fixed holidays

The traditional Thai **Sūriyayātra** line distinguishes two solar events:

1. **Mahā Songkran**: the traditional **true Sun** reaches sidereal longitude 0°
   (enters Aries).
2. **Thaloeng Sok**: the traditional **mean Sun** reaches sidereal longitude 0°;
   the CS year changes. Gislén and Eade place this about two days after Songkran.

The integer foundation for CS year `y` is:

```text
q, R = divmod(292207*y + 373, 800)
h0   = q + 1                         # New Year ahargana
k    = 800 - R                       # kammacabala
a0   = (11*h0 + 650) mod 692         # New Year avoman; replace 0 by 692

solar leap year iff k <= 207
```

`h0` counts elapsed solar days; `k` is the remaining fraction of the New Year day in
units of 1/800 day; and `a0` tracks the excess tithi fraction. The calculation of the
**true** Sun requires the additional traditional longitude corrections described by
Faraut/Wisandarunkorn; `h0`, `k`, and `a0` alone do not produce the exact Mahā Songkran
clock time.

For CS 1388, the implementation in `sakkaraj.py` gives:

```text
h0 = 506980
R  = 489
k  = 311        -> normal 365-day solar year
a0 = 602
```

The Thai Palace Brahmin/Royal Ceremonies announcement for 2026 gives **Mahā Songkran
at 14 April 10:34:35** and the **change to CS 1388 at 16 April 14:40:12**. It also calls
the lunar year *adhikamāsa* (a leap-month year) and the solar year normal. These are
calculated almanac results. Separately, Thailand's civil holidays are administratively
set to **13–15 April**. The first holiday is therefore not necessarily the calculated
ingress day, and the holiday period can end before Thaloeng Sok.

### Laos: related arithmetic, locally assigned ritual days

The historical Lao lunisolar engine belongs to the same broad computational branch as
Thai and Khmer. The published comparison by Gislén and Eade treats Thailand, Laos, and
Cambodia as virtually the same lunisolar family and uses the Thai formulas as its worked
representative. That is evidence for shared arithmetic structure, not proof that every
Lao locality used Bangkok's longitude, exact ingress time, or names.

Modern Lao public sources present the result primarily as a civil ritual sequence:

1. **Sangkhan Luang/Long** — departure or last day of the old year;
2. **Mü Nao / Sangkhan Nao** — neutral day between years;
3. **Sangkhan Khuen** — rising/returning Sangkhan and the first day of the new year.

Some years historically have **two Nao days**, determined by the calendrical/astrological
calculation, so the festival can span four rather than three ritual days. For 2026, Lao
official sources assign 14 April to Sangkhan Luang and 16 April to Sangkhan Khuen; the
government holiday closure is **14–16 April**.

No primary Lao source found for this review publishes a complete, executable 2026
longitude calculation or an exact ingress clock time. Therefore this repository should
not label the Thai 10:34:35 time, the Khmer 10:48 time, or the Myanmar Akya time as a
computed Lao instant. A Lao calculator needs a Lao calendrical source or dated almanac
that specifies its epoch constants, longitude/time standard, true-Sun correction, and
civil-day rule.

### Cambodia: Faraut/Khmer Hora calculation plus a three-day civil festival

The classical Khmer calculation documented by Faraut uses the same early solar constants
and Thai/Khmer branch of intercalation, while retaining Khmer month names and local
astronomical practice. Gislén and Eade explicitly say the Faraut (Cambodian) and
Wisandarunkorn (Thai) solar calculations arrive at identical canonical results, although
the conversion to a local clock time and later civil observance must still be stated.

Cambodia's three labels are commonly:

1. **Moha Sankranta** — arrival/entry of the new-year deity;
2. **Vanapata / Vănabot** — intervening day;
3. **Loeung Sak** — rising of the era/new year.

For 2026, Cambodia's state news agency announced the Year of the Horse beginning on
**14 April at 10:48** and the official holiday period as **14–16 April**. The announced
clock time is 13 minutes 25 seconds later than Thailand's published Mahā Songkran time.
That observed difference is exactly why a converter must retain country, authority,
time standard, longitude, and rounding metadata instead of returning one universal
"Sakkaraj ingress."

### What the shared lunar arithmetic does

The Thai/Lao/Khmer branch uses alternating 29/30-day lunar months and:

- a 30-day intercalary Āṣāḍha month when the next solar New Year would fall too
  late in Caitra/Vaiśākha;
- an intercalary day in Jyeṣṭha, but never in the same lunar year as the intercalary
  month;
- year lengths 354, 355, or 384 days;
- the New Year avoman thresholds `a0 <= 137` in a normal solar year or `a0 <= 126`
  in a solar leap year, followed by adjacency rules that move a conflicting leap day.

This lunar machinery decides the lunar date under the solar New Year and keeps the lunar
calendar aligned with the sidereal solar calendar. It does **not** explain why a modern
government chooses a three-day public-holiday block; that is a separate civil decision.

## 4. The 2026 comparison

The overlap is easy to see, as is the reason not to call the observances identical.

| Tradition | Official or computed 2026 sequence |
|---|---|
| Myanmar | 13 Apr Akyo; 14 Apr Akya; 15 Apr Akyat; 16 Apr Atat; **17 Apr Myanmar New Year's Day** |
| Thailand | **13–15 Apr** public holidays; calculated Mahā Songkran 14 Apr 10:34:35; CS changes 16 Apr 14:40:12 |
| Laos | **14–16 Apr** Lao New Year holidays; official reporting calls 14 Apr Sangkhan Luang and 16 Apr Sangkhan Khuen/new-year renewal |
| Cambodia | **14–16 Apr** holidays; announced New Year arrival 14 Apr 10:48 |

For Myanmar year 1388, this repository calculates:

```text
akya time = 2026-04-14 about 12:50 Myanmar Standard Time
atat time = 2026-04-16 about 16:55 Myanmar Standard Time
New Year's Day = 2026-04-17
```

The calculation agrees at day level with Myanmar's published 13–16 April 2026 Thingyan
festival window. Thailand overlaps it but ends on 15 April; Laos and Cambodia use
14–16 April; Myanmar reserves 17 April as the civil New Year's Day after Atat. Thus
"same season and related solar event" is accurate; "same date and same calendar" is not.

Public-holiday dates are not themselves proof that the underlying historical algorithms
are equal. Modern governments can fix or standardize festival dates independently of an
older computed Sakkaraj boundary.

## 5. Consequences for `lakni-calendar`

The code already makes two useful separations:

1. `sakkaraj.thingyan(my)` is a **Myanmar** calculation. It supplies Myanmar Akyo,
   Akya, Atat, and New Year's Day and is used by `cs_year_for()`.
2. `sakkaraj.thai_new_year_integers(cs)` exposes the old Thai `ahargana`,
   `kammacabala`, and `avoman` values for research. It does not pretend to be a complete
   Thai/Lao/Khmer date converter.

The `lak_ni.py --boundary songkran` option is only a fixed 14 April boundary for its
**comparative ganzhi year label**. It is not used for Ahom Lakni, Myanmar Sakkaraj, or a
historical Thai calendar conversion. A future regional converter should implement and
test each tradition separately instead of adding a country switch to Myanmar `thingyan()`.

## 6. Historical-date checklist

Before translating a Sakkaraj inscription or manuscript date, record:

1. community and place (Myanmar, Central Thai, Lan Na, Lao, Khmer, Khün, Lü, Shan,
   Ahom, or another tradition);
2. historical period and calendar reform regime;
3. whether the year changes at ingress, a following/rising day, or another local rule;
4. local month name or numbering convention;
5. leap-month and leap-day rule used by that community;
6. civil-day boundary and, if an exact ingress time matters, longitude/time standard;
7. whether a modern public-holiday date has replaced the computed traditional date.

Without those fields, a conversion should be labelled a model or an estimate rather
than an exact historical date.

## 7. Sources and evidential weight

1. Lars Gislén, "On Lunisolar Calendars and Intercalation Schemes in Southeast Asia,"
   *Journal of Astronomical History and Heritage* 21(1), 2018, pp. 2–6. This is the
   clearest mathematical comparison of Thai and Burmese intercalation:
   https://doi.org/10.3724/SP.J.1440-2807.2018.01.01
2. Lars Gislén and J. C. Eade, "The Calendars of Southeast Asia 2: Burma, Thailand,
   Laos and Cambodia," *Journal of Astronomical History and Heritage* 22(3), 2019,
   pp. 417–430:
   https://old.narit.or.th/files/JAHH/2019JAHHvol22/2019JAHH...22..417G.pdf
3. Yan Naing Aye, "Algorithm, Program and Calculation of Myanmar Calendar," 2013.
   This gives the Myanmar `SY`, `MO`, Thingyan duration, midnight day boundary, and the
   rule that New Year's Day follows Atat:
   https://cool-emerald.blogspot.com/2013/06/algorithm-program-and-calculation-of.html
4. Sao Saimong Mangrai, "Cula Sakaraja and the Sixty Cyclical Year Names," *Journal of
   the Siam Society* 69, 1981. This documents regional use of CS and why cyclical names
   must be read with local calendar practice:
   https://thesiamsociety.org/wp-content/uploads/1981/03/JSS_069_0d_SaoSaimong_CulaSakarajaAndSixtyCyclicalYearNames.pdf
5. Official 2026 civil observances: Myanmar Ministry of Hotels and Tourism
   (13–16 April), Thai Ministry of Foreign Affairs (13–15 April), Lao Ministry of
   Finance/Foreign Affairs (14–16 April), and National Bank of Cambodia (14–16 April):
   https://tourism.gov.mm/en/upcoming-events/thingyan-water-festival
   https://image.mfa.go.th/mfa/0/mkKfL2iULZ/Dip_List_March_2026/March_2026.pdf
   https://laoevisa.gov.la/info
   https://nbc.gov.kh/english./news_and_events/official_holiday.php
6. Thailand Ministry of Culture, Palace Brahmin/Royal Ceremonies Songkran announcement
   for BE 2569/CS 1388 (calculated 2026 instants and year types):
   https://www.culture.go.th/culture_th/ewt_news.php?filename=index&nid=9131
7. Lao News Agency, 2026 Sangkhan Luang and Sangkhan Khuen reports:
   https://kpl.gov.la/En/detail.aspx/detail.aspx?id=97790
   https://kpl.gov.la/EN/detail.aspx?id=97812
8. Agence Kampuchea Presse, 2026 Khmer New Year arrival at 10:48 on 14 April:
   https://www.akp.gov.kh/fr/post/detail/367426

The first four sources support the historical and mathematical comparison. Sources 5–8
support the modern 2026 country results and official terminology; they do not by
themselves supply a complete historical calendar algorithm.
