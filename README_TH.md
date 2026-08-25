# Lak Ni และ Lak Jeng — อัลกอริทึมปฏิทินไทด้วย Python

> ⚠️ **สถานะคำแปล (2026-08-24):** แก้ไขอัลกอริทึมและ `README.md` ภาษาอังกฤษแล้ว
> แต่ฉบับแปลเก่านี้ยังต้องให้ชุมชนตรวจทาน และอาจกล่าวถึงสมมติฐานเดิมเรื่องขอบเขต
> เดือนเมษายนกับ folk cycle จึงยังไม่ควรใช้เป็นข้อกำหนดอ้างอิงหลัก

ชุดเครื่องมือวิจัยเชิงปฏิบัติสำหรับ **ปฏิทินรอบ 60 ชื่อ** ของชนชาติไท รวมทั้ง **ไทอาหม** ในรัฐอัสสัม ประเทศอินเดีย ซึ่งเรียกว่า *Lak Ni / Lakni* และ **ชาวไทใหญ่** ในเมียนมา ซึ่งมีวิธีคำนวณด้วยมือเรียกว่า *Lak Jeng* 

มี implementation อิสระ 2 แบบตามธรรมเนียมที่บันทึกไว้ต่างกัน พร้อม test suite ที่ยืนยันว่าทั้งสองแบบให้ผลตรงกันและตรงกับข้อมูลอ้างอิงที่ตีพิมพ์แล้ว

| สคริปต์ | ธรรมเนียม | วิธี |
|---|---|---|
| `lak_ni.py` | Tai Ahom *Lak Ni* | modular arithmetic บน Julian Day Number |
| `lak_jeng.py` | Shan *Lak Jeng* | จำนวนวันแบบจำนวนเต็ม (*ahargaṇa*) ของ Sūrya Siddhānta |
| `sakkaraj.py` | Chula Sakarat / Thet Kayit | กฎวาตัดเมียนมา + จำนวนเต็ม avoman ไทย |

เอกสารประกอบ **`SAKKARAJ_TH.md`** อธิบายตระกูลศักราช Anjana 691 BCE → Buddha 544 BCE → Śaka/Mahā 78 CE → **Cula Sakarat 22 March 638 CE** ตลอดจนยุคคำนวณ Makaranta→Thandeikta→Advisory-Board ตรรกะปีวาตัด ปัญหาการนับเดือนในแต่ละภูมิภาค และตำแหน่งวันอธิกวารที่ต่างกันระหว่างไทยกับเมียนมา

ไม่ต้องใช้ dependency ภายนอก ใช้เฉพาะ Python 3 standard library

## 1. พื้นหลัง — วงรอบเดียวที่ใช้ร่วมกัน

ปฏิทินตระกูลไทสืบจากระบบจีน **ganzhi (干支)** ซึ่งเลื่อนตัวนับยาว 10 (“แม่” / heavenly stems) และตัวนับยาว 12 (“ลูก” / earthly branches / สัตว์นักษัตร) ไปพร้อมกัน เพราะ lcm(10, 12) = **60** จึงมีคู่ชื่อ 60 คู่ก่อนเริ่มซ้ำ

```
Kra-Jai, Lup-Pao, Hai-Khan, Muang-Mao, Puek-Si, ...
... Tao-Hao, Ka-Set, Kra-Jai  ← ซ้ำหลัง 60 ขั้น
```

ชื่อทั้ง 60 ใช้กับ **ปี** **วัน** และในบางชุมชนใช้กับ **เดือน/ชั่วโมง** ด้วย วงรอบวันเป็นลำดับต่อเนื่องเดียวกันในจีน ไทใหญ่ Dai Lue Khün และ Ahom ไม่ได้มี alignment แยกตามกลุ่มชาติพันธุ์

สิ่งที่ต่างกันคือ epoch ขอบเขตปีใหม่ การสะกด และเลขคณิตจันทรคติที่ใช้สร้างเดือนจริง

## 2. แม่ 10 และลูก 12

| # | แม่ (ธาตุ) | การสะกด | | # | ลูก (สัตว์) | การสะกด |
|---|---|---|---|---|---|---|
| 0 | ไม้ | Kra, Kap, Kha, Karp | | 0 | หนู | Jai, Chai, Choad |
| 1 | ไฟ | Lup, Lap | | 1 | วัว | Pao, Ngok, Chalu |
| 2 | ดิน | Hut, Hot, Hai | | 2 | เสือ | Khan, Yee, Kharn |
| 3 | โลหะ | Muang, Mong, Möng, Mvng | | 3 | กระต่าย | Mao, Tho |
| 4 | น้ำ | Puek, Pok, Pök | | 4 | มังกร/นาค | Si |
| 5 | ไม้ | Kut, Kud, Kat | | 5 | งู | Sai |
| 6 | ไฟ | Koat, Kwat, Khot | | 6 | ม้า | Singa, Nga, Si-nga |
| 7 | ดิน | Hong, Hung, Hvng, Hoong | | 7 | แพะ | Met, Mot, Med |
| 8 | โลหะ | Tao, Thao, Tv | | 8 | ลิง | San, Saan, Wok |
| 9 | น้ำ | Ka, Kap, Kaap | | 9 | ไก่ | Hao, Rao, Raga |
| | | | | 10 | สุนัข | Set, Sed, Jaw |
| | | | | 11 | หมู | Kai, Kwai, Goon |

ธาตุไทเรียง ไม้ ไฟ ดิน โลหะ น้ำ แล้วซ้ำ ธาตุละ 2 ครั้งต่อทศวรรษ แบบเพศผู้และเพศเมีย ส่วนจีนเรียงไม้ ไม้ ไฟ ไฟ… ดังนั้นธาตุไทกับ stem จีนที่ index เดียวกันไม่ตรงกันแบบ 1-to-1 แต่สัตว์ตรงกันเสมอ

### ตารางชื่อ stem 2 ชุด

| # | Shan/Lanna | Ahom/Buranji | stem จีน |
|---|---|---|---|
| 0 | Kra/Kap | Kap | 甲 jiǎ (ไม้ yang) |
| 1 | Lup/Lap | Dap | 乙 yǐ (ไม้ yin) |
| 2 | Hut/Hai | Rai | 丙 bǐng (ไฟ yang) |
| 3 | Muang/Möng | Mueang | 丁 dīng (ไฟ yin) |
| 4 | Puek/Pök | Plaek | 戊 wù (ดิน yang) |
| 5 | Kut/Kud | Kat | 己 jǐ (ดิน yin) |
| 6 | Koat/Khot | Khut | 庚 gēng (โลหะ yang) |
| 7 | Hong/Hung | Rung | 辛 xīn (โลหะ yin) |
| 8 | Tao/Thao | Tao | 壬 rén (น้ำ yang) |
| 9 | Ka | Ka | 癸 guǐ (น้ำ yin) |

ชุด Ahom ตรงกับธาตุของ stem จีน ส่วนชุด Shan รักษาหลักธาตุ 5×2 แบบพื้นเมือง ตำแหน่ง 0, 3, 5, 8, 9 ใกล้เคียงกันมาก จึงอาจเป็นสำเนียงต่างกันของรายการคำโบราณชุดเดียว `lak_ni.py` ใช้ชื่อ Ahom เป็นหลักตามหลักฐาน Buranji และแสดงรูป Shan ควบคู่กัน

## 3. เริ่มใช้งาน

```bash
cd python
python3 lak_ni.py
python3 lak_ni.py 2026 08 23
python3 lak_ni.py --tz 5.5
python3 lak_ni.py --test
python3 lak_jeng.py 2115
python3 lak_jeng.py --date 2026 8 23
python3 lak_jeng.py --test
```

ตัวอย่างผลลัพธ์ยังคงใช้ field ทางเทคนิคเดิม:

```
Gregorian date : 2026-08-23 (Sun)
Tai year       : 2026 (turns songkran)
Lak-Ni year    : 54/60 "Khutchi"
Year name      : Rai-Singa = fire horse
Shan variant   : Hut/Hai-Singa
Sakkaraj era   : 1388 CS (sok 8 = atthasok)
Day name       : Kut-Sai (5/60)
Lunar phase    : waxing day 10 [UTC+6.5]
Julian Day No. : 2461276
```

## 4. Algorithm A — รอบปี Lak Ni

ธรรมเนียม Ahom ที่แพร่หลายนับจาก **1193 CE = “Mungkeu”** ปีเกิดของ Sukaphaa

| เหตุการณ์ | AD | ตำแหน่ง | ชื่อ |
|---|---|---|---|
| Sukaphaa เกิด | 1193 | 1 | Mungkeu |
| เริ่มเดินทางสู่อัสสัม | 1215 | 23 | Katrau |
| สถาปนาอาณาจักร | 1253 | 61 ≡ 1 | Mungkeu อีกครั้ง |
| Sukaphaa เสียชีวิต | 1268 | 16 | Taoni |

```
n = ((AD_year − 1193) mod 60) + 1
name = ME_PI_60[n]
```

2026 → n = 54 → **Khutchi** รอบ 14 การนับพื้นบ้านนี้อิงประวัติศาสตร์ Ahom และแยกจากชื่อ pan-Tai ที่สอดคล้องกับจีน

```
stem_index   = (AD_year − 4) mod 10
animal_index = (AD_year − 4) mod 12
cycle_index  = (AD_year − 4) mod 60
```

ดังนั้น **2026 = Rai-Singa ปีม้าไฟ** ส่วน 2025 = Dap-Sai / 乙巳 ปีงูไม้

ปี Tai/Ahom เปลี่ยนราว **กลาง April** ไม่ใช่ January 1 ดังนั้น Jan 1–Apr 13, 2026 ยังเป็นปีงูไม้ ใช้ `--boundary {songkran,lichun,jan1}` โดยค่าเริ่มต้นคือ songkran, Apr 14

ไทยภาคกลางใช้ ***sok*** ซึ่งเป็นเลขท้ายของจุลศักราชแทน stem: `CS = Y − 638`, `sok = (Y − 638) mod 10` ดังนั้น 2026 → CS 1388 → *atthasok* สัตว์อาจเปลี่ยนตามวัฒนธรรม เช่น วัว→ควาย กระต่าย→แมว มังกร→นาค หมู→ช้าง

```
CS = AD_year − 638
BE = AD_year + 543
T ≈ AD_year + 95
```

## 5. Algorithm B — รอบวัน 60 ที่ใช้ร่วมกัน

```
a  = floor((14 − month)/12); y = year + 4800 − a; m = month + 12a − 3
JDN = day + floor((153m+2)/5) + 365y + floor(y/4) − floor(y/100) + floor(y/400) − 32045
```

anchor คือ **1949-10-01 = jiazi / Kap-Jai / Kra-Jai**, JDN 2433191

```
index = (JDN − 2433191) mod 60
mother = MOTHERS[index mod 10]
child = ANIMALS[index mod 12]
```

2026-08-23 ให้ index **5** = Kut/Kat-Sai วันงู หากปฏิทินท้องถิ่นไม่ตรง ให้หา offset ของปฏิทินนั้นแทนการแก้ anchor

```bash
python3 lak_ni.py --calibrate YYYY-MM-DD AnimalName
```

## 6. Algorithm C — ข้างขึ้นข้างแรมแบบเมียนมา

1. ใช้จันทร์ดับจริงจาก `true_new_moon_jde(k)` ไม่ใช้ mean synodic month
2. วันที่ conjunction เป็นวันสุดท้ายของเดือนเก่า และ **ขึ้น 1 ค่ำคือวันถัดไป**
3. timezone มีผลจริง

```
conj_local_JD = JDE_conjunction + tz_hours/24
conj_day = floor(conj_local_JD + 0.5)
delta = date_JDN − conj_day
delta = 0        → วันเดือนดับ
1 ≤ delta ≤ 14   → ขึ้น delta ค่ำ
delta = 15       → วันเพ็ญ
delta ≥ 16       → แรม (delta − 15) ค่ำ
```

conjunction เดือน August 2026 เกิด **Aug 12, 17:37 UT**: UTC+6:30 เป็น Aug 13, 00:07 ทำให้ 2026-08-23 = **ขึ้น 10 ค่ำ**; UTC+5:30 เป็น Aug 12, 23:07 ทำให้เป็นขึ้น 11 ค่ำ ค่าเริ่มต้น `--tz 6.5`; Assam ใช้ `--tz 5.5`

## 7. Algorithm D — Lak Jeng ahargaṇa

```
1577917828 days / 4320000 years = 365.258756481481… d
≈ 292207/800 + 7/(1350·800)
```

สำหรับปีไท `T`:

```
Y = T − 1
q = floor(Y/1350); r = Y mod 1350
C = 7q + floor(r/193)
N = 292207·Y + C + 6869
Q = floor(N/800); R = N mod 800
A = Q + 1 if R > 0 else Q
M = 11·A − floor(Y/25) + 420
D = floor(M/692); P = M mod 692
L = floor((A+D)/30); d = (A+D) mod 30
weekday = A mod 7
g = (A + 2) mod 60
```

ตัวอย่าง `T=2115` ให้ A = 772,166, D = 12,274, วัน Tuesday, ชื่อวัน “Tao Si” และชื่อปี “Hung Pao”

Gregorian bridge ใช้ **ปีใหม่ไท 2116 = Sunday 2021-12-05, A = 772,521**:

```
A(date) = 772521 + (JDN(date) − 2459554)
```

## 8. การตรวจสอบ

```bash
python3 lak_ni.py --test && python3 lak_jeng.py --test
```

ตรวจผ่าน anchor Me-Pi 1193/1215/1253/1268, JDN 2000-01-01 = 2451545, jiazi 1949-10-01, จันทร์ดับ 2000-01-06 18:14 UT, ปีใหม่ไท 2116, ตัวอย่าง T=2115 และการเทียบ `lak_ni ↔ lak_jeng` ต่อเนื่อง 1,827 วันใน 2023–2027

## 9. ข้อจำกัด

1. แหล่ง Lak Jeng ขัดกับสูตรของตนเอง 10 วัน: T=2116 ให้ A=772,531 แต่ข้อความระบุ 772,521
2. `ME_PI_60` มาจากแหล่งถอดอักษรยอดนิยมและมีความไม่สอดคล้อง งานวิชาการควรใช้ Terwiel & Ranoo (1992), p. 91
3. ขอบเขตปีต่างกัน: Ahom ราวสงกรานต์, Shan/Great-Dai ต้น December, เดือนเมียนมาราว April
4. ไม่รวม ΔT ซึ่งราว 69 s ใน 2026
5. ธาตุไทไม่เท่ากับ stem จีนที่ index เดียวกัน

## 10. ศัพท์

| ศัพท์ | ความหมาย |
|---|---|
| Lak Ni | ปฏิทินรอบ 60 ของ Tai Ahom |
| Lak Jeng | วิธีคำนวณด้วยมือของไทใหญ่ |
| Me-Pi | รอบแม่/ธาตุ 10 |
| Look-Pi | รอบสัตว์ 12 |
| ahargaṇa | จำนวน civil day ที่ผ่านจาก epoch |
| tithi | 1/30 ของ synodic month |
| watat | ปีอธิกมาสเมียนมา |
| Sakkaraj / CS | จุลศักราช = AD − 638 |
| JDN / JDE | Julian Day Number / Julian Ephemeris Date |

## 11. เอกสารอ้างอิง

1. Süa Tai Möng, “Method for Calculating the Lak Jeng Cycle” (2021)
2. Yan Naing Aye, *Algorithm, Program and Calculation of Myanmar Calendar* (2013)
3. Terwiel & Ranoo Wichasin, *Tai Ahoms and the Stars* (1992)
4. Stephen Morey et al., *Lakni (Calendar)*
5. Monthip Sirithaikhongchuen, *Tai Name of the Year and Tai New Year* (2007)
6. Jean Meeus, *Astronomical Algorithms*, 2nd ed.
7. Burgess, *Sūrya-Siddhānta*
8. Sewell & Dikshit; Irwin
9. Lars Gislén, “Burmese Eclipse Calculations” (2015)
10. *Sexagenary Cycle — Tai comparative research* (Aug 2026)

*ฉบับวิจัย August 2026 ตรวจสอบการคำนวณทั้งหมด ณ 2026-08-23 (Kut-Sai, ขึ้น 10 ค่ำ)*
