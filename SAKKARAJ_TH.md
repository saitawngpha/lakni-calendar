# ศักราช — บันทึกการวิจัยเชิงลึก

เอกสารประกอบ `lak_ni.py` / `lak_jeng.py` ว่าด้วย **จุลศักราช (Chula Sakarat)** ซึ่งเป็นระบบเวลาหลักของเอเชียตะวันออกเฉียงใต้ภาคพื้นทวีป implementation อยู่ใน **`sakkaraj.py`**

## 1. ตระกูลศักราช

| ศักราช | Epoch | วันเริ่ม 0 | หมายเหตุ |
|---|---|---|---|
| **Anjanasakaraj** | King Anjana | 10 March **691 BCE** | ใช้กับวันก่อนพุทธกาล |
| **Buddha Sakaraj** | Parinibbāna | 11–13 May **544 BCE** | BE = CS + 1182; ไทยน้อยกว่า 1 |
| **Mahāsakaraj / Śaka** | Kaṇiṣka/Ujjain | 17 March **78 CE** | ศก Śaka ของอินเดีย |
| **Cula Sakarat (CS)** | Popphausawraḥan | 22 March **638 CE** | 78 + 560 = 638 |
| Mohnyin era | Mohnyin thado minsaw | 18 March **1436** | ใช้ในภูมิภาคช่วงสั้น |
| Magi-San | epoch เดียวกับ CS | 22 March 638 | ชื่อที่ใช้ใน Chittagong |

ลำดับพงศาวดารคือ Buddha Śāsanā → ยกเลิกใน 621/622 → **Mahāsakaraj** → ยกเลิกเมื่อปี 559/560 → **Cula Sakarat**, 638 CE อาระกันเริ่มศักราชเดียวกันในปีนั้น CS นับ **จำนวนปีที่ผ่านไปแล้ว** ดังนั้นปี epoch คือ 0 และ April 1999 – April 2000 = CS 1361

## 2. กลไกดาราศาสตร์

ปฏิทิน Sakkaraj เป็นระบบสุริยจันทรคติแบบค่าเฉลี่ยที่อิง Sūrya Siddhānta

### 2.1 ค่าคงที่

| Constant | ค่า | ความหมาย |
|---|---|---|
| `SY` | 1577917828 / 4320000 = **365.2587564815 d** | mean sidereal year |
| `SY₀` | 292207 / 800 = **365.25875 d** | รูปย่อแบบ Makaranta |
| `LM` | 1577917828 / 53433336 = **29.53058795 d** | mean synodic month |
| tithi ratio | **703 : 692** | month = 30×692/703 |
| `MO` | JD **1954168.050623** | จุดเริ่มปีเมียนมา 0 |
| excess/year | **10.8917011 d** | ขับตรรกะอธิกมาส |

19 ปี × 235 เดือน × 30 tithis = 7050 tithis = 6939.687055 solar days ความต่างระหว่างวงล้อจันทรคติแบบ tropical กับวงล้อสุริยคติแบบ sidereal ซึ่งสะสมราว 12 วันเมื่อ ME 1100 เป็นปัญหาหลักในประวัติศาสตร์ Sakkaraj

### 2.2 ยุคคำนวณเมียนมา 3 ยุค

| ยุค | ช่วง | กฎวาตัด |
|---|---|---|
| **Makaranta** | ถึง 1853 CE (ME < 1215) | ตำแหน่ง **2, 5, 7, 10, 13, 15, 18** ในรอบ 19 ปี |
| **Thandeikta** | 1853–1950 | threshold ของ excess day, หน้าต่าง 4 เดือน |
| **Current** | 1950– | หน้าต่าง 8 เดือน |

เดือนอธิกมาสคือ **First Waso** 30 วันก่อน Waso เสมอ วันอธิกวารเป็น **วันที่ 2 ของ Nayon** และมีเฉพาะปีวาตัด

### 2.3 อัลกอริทึมวาตัดปัจจุบัน

```
ja = SY·my + MO
jk = ja − 2.169918982
ed = (SY·(my + 3739)) mod LM
TA = (12 − NM)·(SY/12 − LM)          # NM = 8
if ed < TA: ed += LM
TW = LM − NM·(SY/12 − LM)            # 22.2694539
watat ⇔ ed ≥ TW
```

```
w = round(SY·my + MO − ed + 4.5·LM + WO)  # WO = −0.5
ส่วนต่างจากปีวาตัดก่อนหน้า mod 354:
30 → little watat (384 วัน)
31 → big watat (385 วัน, Nayon 30 วัน)
```

ความยาวปีคือ 354, 384 หรือ 385 วัน เดือนสลับ 29/30 วัน **Thingyan:** `ja` คือ atat และ `ja − 2.1699…d` คือ akya เฉพาะวันหลัง atat จึงเป็นวันปีใหม่

### 2.4 ไม่มีข้อกำหนดตายตัวสำหรับอนาคต

การปฏิรูปแต่ละครั้งเลื่อนรูปแบบ Metonic แบบเฉพาะกิจ ดังนั้นวันเมียนมาในอนาคตที่เกินตารางประกาศไม่มีอำนาจผูกพัน Advisory Board ประกาศเป็นรายปี อัลกอริทึมทำซ้ำแนวปฏิบัติทางการ ไม่ได้บัญญัติกฎใหม่

## 3. ความแตกต่างตามภูมิภาค

| ภูมิภาค | เดือนหมายเลข 1 |
|---|---|
| Kengtung | Tazaungmon |
| Lan Na | Thadingyut = เดือน 1 |
| Western Shan / Central Thailand | Thadingyut = เดือน 11 |
| Lan Xang, Sukhothai | Nadaw |

คืนเดียวกันอาจเป็น “เดือน 12 แรม 1” ใน Kengtung, “เดือน 11 แรม 1” ใน Bangkok หรือ “เดือน 1 แรม 1” ใน Chiengmai การอ่านจารึกจึงต้องรู้ภูมิภาค

### Siam: วันอธิกวารในปีปกติ

เมียนมาใส่วันพิเศษใน big-watat 385 วัน แต่สยามย้ายไปไว้ในปีปกติ 355 วัน จึงมีชุด {354, 355, 384} แทน {354, 384, 385} ผลรวมตลอด 19 ปีเท่ากัน

### วิธี La Loubère / avoman

```
q, R = divmod(292207·CS_year + 373, 800)
h₀ = q + 1
k  = 800 − R
a₀ = (h₀·11 + 650) mod 692
```

- solar leap ⇔ k ≤ 207
- ต้องมี leap day ⇔ a₀ ≤ 137 หรือ a₀ ≤ 126 ใน solar leap
- แต่ละ civil day เพิ่ม a₀ ทีละ 11 (mod 692)

ตัวอย่าง CS **1238** → h₀ = 452,191; k = 161; a₀ = 655

```
CS = AD − 638
BE = CS + 1182; Thailand = CS + 1181
MS/Śaka = AD − 78
Anjana = AD + 691
```

## 4. Sakkaraj ในหมู่ชนชาติไท

- พงศาวดาร Ahom ลงวันที่แบบ **ชื่อ Lak-Ni + ปี Sakkaraj**
- แหล่ง Shan/Khün ใช้ ชื่อสัตว์ + CS + เดือน + ข้างขึ้น/ข้างแรม + วัน
- Great-Dai/Shan ของ Sipsongpanna ใช้ epoch 95 BCE แยกต่างหาก ส่วน Small-Dai ตรงกับ CS epoch 638

## 5. จุดยืนยันที่ทดสอบใน `sakkaraj.py --test`

| ข้อเท็จจริง | ผล |
|---|---|
| ME 1375 = JD 2456398.8408 = 2013-04-16 08:10 | pass |
| ME 1374 excess = 24.1094385; watat | pass |
| 2nd Waso ME 1374 = 2012-08-02 | pass |
| ME 1374 เป็น little watat | pass |
| CS 1238: h₀=452191, k=161, a₀=655 | pass |
| CS 1341 ยังใช้ 1980-03-31; CS 1342 ราว Apr 15 | pass |
| Thingyan 2.169918982 d เมื่อ ME ≥ 1312 | pass |

## 6. เอกสารอ้างอิง

1. Y. N. Aye, *Algorithm, Program and Calculation of Myanmar Calendar* (2013)
2. J. C. Eade / L. Gislén, *The Calendars of Southeast Asia*
3. A. M. B. Irwin, *The Burmese & Arakanese Calendars* (1909)
4. Sao Saimong Mangrai, “Cula Sakaraja and the Sixty Cyclical Year Names” (1981)
5. *Burmese calendar*, Wikipedia
6. Burgess (trans.), *Sūrya Siddhānta*, ch. I vv. 34–37
