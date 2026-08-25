# Historical basis for the reconstructed Ahom Lakni New Year

This note records exactly which parts of `lak_ni.py` are supported by historical
evidence and which parts are computational assumptions. It must be read before treating
the program's Gregorian dates as historical Ahom dates.

## Evidence hierarchy

| Claim | Evidence | Confidence in this project |
|---|---|---|
| A new Lakni arrived with Dinching | R. C. Kapoor cites *Ahom Buranji* (G. C. Barua, 1930), p. 327: Lakni Khutshinga in 1774 came with Dinching | Strong |
| Dinching was the first Ahom month | Kapoor 2021, p. 668 and Appendix, p. 686 | Strong |
| Dinching began on the civil day following the new moon ending month 12 | Kapoor 2021, p. 668 | Strong as a published interpretation of the chronicle |
| Ahom used 10 Mother and 12 Child names to form 60 Lakni names | Kapoor 2021, Tables 7-9, pp. 686-687 | Strong |
| Kap Cheu began the 1228 reconstruction and the corresponding cycle returned in 2008 | Kapoor 2021, pp. 668 and 686 | Strong within Kapoor's chronology |
| A Lakni year occupied approximately November-November | Kapoor's astronomical comparisons and the Katplao 1673-1674 comparison with Terwiel and Wichasin | Strong at seasonal resolution |
| The first Assam-local new moon on or after 1 November selects Dinching | No historical source located | **Program assumption** |
| A thirteenth lunation is inserted after month 8 | Reported for the related Shan system by Terwiel and summarized by Kapoor, p. 668; not yet proven as the exact Ahom rule | **Comparative reconstruction** |
| New moons are calculated with the Meeus Chapter 49 equations at UTC+05:30 | Modern astronomical implementation | **Program assumption** |

## Strongest source

R. C. Kapoor, “Fixing the Chronology in Tai-Ahom Chronicles by Using Astronomical
References,” *Journal of Astronomical History and Heritage* 24(3), 2021, pp. 665-687.

- Institutional record: <https://prints.iiap.res.in/handle/2248/7856>
- Full paper: <https://prints.iiap.res.in/bitstream/handle/2248/7856/Fixing%20the%20chronology%20in%20tai-ahom%20chronicles%20by%20using%20astronomical%20references.pdf?sequence=1>
- Page 668: Dinching boundary and the cited 1774 Khutshinga New Year.
- Pages 686-687: Ahom time-keeping appendix and Tables 7-9.

This is the principal source used by the implementation because it combines chronicle
evidence with independently dateable eclipses and comets. Kapoor in turn cites the
parallel Ahom-English *Ahom Buranji* edited and translated by Golap Chandra Barua
(1930), especially page 327. A public scan is available through the
[National Virtual Library of India](https://ocrdigitalfile.nvli.in/cslrepository/4028/RB860-ocr.pdf).
The present project has not independently retranslated the Ahom passage.

## Manuscript and philological checks

1. B. J. Terwiel and Ranoo Wichasin, [*Tai Ahoms and the Stars: Three Ritual Texts to
   Ward Off Danger*](https://www.cornellpress.cornell.edu/book/9780877277095/tai-ahoms-and-the-stars/),
   Cornell Southeast Asia Program, 1992, especially Table 4, p. 91, and pp. 105-107.
   Their manuscript work supplies an independent Katplao chronological comparison and
   warns that older printed Ahom translations and dictionaries contain serious errors.

2. Stephen Morey, [*A Sketch of Tai Ahom, as Recorded in Original
   Manuscripts*](https://archive.mpi.nl/islandora/object/tla%3A1839_00_0000_0000_0018_CC35_B/datastream/OBJ/download),
   Table 1. Morey lists a dedicated `Lakni` manuscript held in photocopy by Atul
   Borgohain and describes its translation as unpublished.

3. The [SEALANG Assam manuscript catalogue](https://sealang.net/assam/texts.htm)
   identifies `Junaram_Phukon_Lakni`, formerly owned by Junaram Sangbun Phukon, as a
   calendrical manuscript from Parijat Village.

4. [British Library EAP373/14/5](https://searcharchives.bl.uk/catalog/040-003345135)
   demonstrates the principal conversion problem: Lakni names repeat every sixty years,
   and published Gregorian alignments can differ by one or two years.

5. The [Government of Assam Directorate of Historical and Antiquarian
   Studies](https://dhas.assam.gov.in/portlets/ahom-studies) reports more than 240 Ahom
   and other Tai manuscripts, including Lakni, divination, and traditional astrological
   works. These manuscripts are the appropriate authority for improving the current
   reconstruction.

## Astronomical implementation source

The true-new-moon approximation in `lak_ni.py` follows Jean Meeus,
*Astronomical Algorithms*, 2nd edition, 1998, Chapter 49. Meeus supplies a modern lunar
conjunction calculation; he is not a source for the Ahom month-selection or leap-month
rules.

## Required citation for generated results

Results should be described as:

> Reconstructed Ahom Lakni date using the source-supported Dinching boundary described
> by Kapoor (2021, p. 668), with a program-assumed first-new-moon-after-1-November
> seasonal anchor and a comparative leap-month rule.

Do not describe the output as an exact historical priestly calendar until an edited
Lakni manuscript publishes the missing month-selection, intercalation, and civil-day
rules.
