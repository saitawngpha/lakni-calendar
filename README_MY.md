# Lak Ni နှင့် Lak Jeng — Python ဖြင့် တိုင်ပြက္ခဒိန် တွက်ချက်နည်းများ

တိုင်လူမျိုးများ အသုံးပြုသည့် **အမည် 60 ပြက္ခဒိန်စက်ဝန်း** ကို လက်တွေ့လေ့လာနိုင်သော သုတေသနကိရိယာစုဖြစ်သည်။ အိန္ဒိယနိုင်ငံ အာသံပြည်နယ်ရှိ **Tai Ahom** များက ၎င်းကို *Lak Ni* / *Lakni* ဟုခေါ်ပြီး၊ မြန်မာနိုင်ငံရှိ **ရှမ်း** များ၏ လက်တွက်နည်းကို *Lak Jeng* ဟုခေါ်သည်။

မှတ်တမ်းတင်ထားသော အစဉ်အလာ 2 မျိုးကို လိုက်နာသည့် သီးခြား implementation 2 ခုနှင့်၊ ထိုနည်း 2 ခု အချင်းချင်းနှင့် ထုတ်ဝေထားသည့် ကိုးကားဒေတာတို့ တူညီကြောင်း သက်သေပြသော test suite ပါရှိသည်။

| Script | လိုက်နာသည့်အစဉ်အလာ | နည်းလမ်း |
|---|---|---|
| `lak_ni.py` | Tai Ahom *Lak Ni* (Assam) | Julian Day Number ပေါ် modular arithmetic |
| `lak_jeng.py` | ရှမ်း *Lak Jeng* (Myanmar/Yunnan) | Sūrya Siddhānta ၏ ကိန်းပြည့်ရက်ရေတွက်မှု (*ahargaṇa*) |
| `sakkaraj.py` | Chula Sakarat / သက္ကရာဇ်ခေတ်စနစ် | မြန်မာဝါထပ်စည်းမျဉ်း + ထိုင်း avoman ကိန်းပြည့်များ |

ပူးတွဲသုတေသနမှတ်စု **`SAKKARAJ_MY.md`** တွင် Anjana 691 BCE → Buddha 544 BCE → Śaka/Mahā 78 CE → **Cula Sakarat 22 March 638 CE** ဟူသော သက္ကရာဇ်မိသားစု၊ Makaranta→Thandeikta→Advisory-Board တွက်ချက်ခေတ်များ၊ ဝါထပ်တွက်နည်း၊ ဒေသအလိုက် လနံပါတ်ပြဿနာနှင့် ထိုင်း/မြန်မာ ရက်ငင်ထားပုံကွာခြားချက်တို့ကို အသေးစိတ်ဖော်ပြထားသည်။

ပြင်ပ dependency မလိုပါ — Python 3 standard library သာ အသုံးပြုသည်။

---

## မာတိကာ

1. [နောက်ခံ — စက်ဝန်းတစ်ခုတည်း၏ အခြေခံ](#1-နောက်ခံ--စက်ဝန်းတစ်ခုတည်း၏-အခြေခံ)
2. [မိခင် 10 ပါးနှင့် သားသမီး 12 ပါး](#2-မိခင်-10-ပါးနှင့်-သားသမီး-12-ပါး)
3. [အမြန်စတင်ရန်](#3-အမြန်စတင်ရန်)
4. [Algorithm A — Lak Ni နှစ်စက်ဝန်း](#4-algorithm-a--lak-ni-နှစ်စက်ဝန်း)
5. [Algorithm B — အားလုံးမျှဝေသည့် 60 ရက်စက်ဝန်း](#5-algorithm-b--အားလုံးမျှဝေသည့်-60-ရက်စက်ဝန်း)
6. [Algorithm C — မြန်မာနည်းဖြင့် လဆန်းလဆုတ်](#6-algorithm-c--မြန်မာနည်းဖြင့်-လဆန်းလဆုတ်)
7. [Algorithm D — Lak Jeng ahargaṇa အဆင့်ဆင့်](#7-algorithm-d--lak-jeng-ahargaṇa-အဆင့်ဆင့်)
8. [စစ်ဆေးအတည်ပြုပုံ](#8-စစ်ဆေးအတည်ပြုပုံ)
9. [သိထားသောကွာခြားချက်များနှင့် မဖြေရှင်းရသေးသည့်မေးခွန်းများ](#9-သိထားသောကွာခြားချက်များနှင့်-မဖြေရှင်းရသေးသည့်မေးခွန်းများ)
10. [ဝေါဟာရများ](#10-ဝေါဟာရများ)
11. [ကိုးကားချက်များ](#11-ကိုးကားချက်များ)

---

## 1. နောက်ခံ — စက်ဝန်းတစ်ခုတည်း၏ အခြေခံ

တိုင်ပြက္ခဒိန်မိသားစုသည် တရုတ် **ganzhi (干支)** စနစ်မှ ဆင်းသက်လာသည်။ အလျား 10 ရှိ counter (“မိခင်များ” / heavenly stems) နှင့် အလျား 12 ရှိ counter (“သားသမီးများ” / earthly branches / ရာသီခွင်တိရစ္ဆာန်များ) ကို တစ်ပြိုင်တည်း ရွှေ့သည်။ lcm(10, 12) = **60** ဖြစ်သောကြောင့် စက်ဝန်းပြန်မစမီ ထူးခြားသည့်အမည်တွဲ 60 ခု ရှိသည်။

```
Kra-Jai, Lup-Pao, Hai-Khan, Muang-Mao, Puek-Si, ...
... Tao-Hao, Ka-Set, Kra-Jai  ← 60 အဆင့်ပြီးနောက် ပြန်စသည်
```

ဤအမည် 60 ကို **နှစ်များ**၊ **ရက်များ** နှင့် အချို့အသိုင်းအဝိုင်းများတွင် **လ/နာရီများ** အတွက်ပါ ပြန်သုံးသည်။ အရေးကြီးသည်မှာ ရက်စက်ဝန်းသည် တရုတ်၊ ရှမ်း၊ Dai၊ Lue၊ Khün နှင့် Ahom အစဉ်အလာအားလုံးတွင် မပြတ်ဆက်နေသည့် ရေတွက်မှုတစ်ခုတည်းဖြစ်သည်။ လူမျိုးတစ်မျိုးစီအတွက် alignment တစ်ခုစီ မဟုတ်ပါ။

အသိုင်းအဝိုင်းအလိုက် ကွဲပြားနိုင်သည်များမှာ —

- **epoch** — မည်သည့်သမိုင်းနှစ်ကို “နှစ် 1” ဟုယူသနည်း၊
- **နှစ်သစ်နယ်နိမိတ်** — December အစောပိုင်း၊ April သင်္ကြန်၊ သို့မဟုတ် လနှစ်သစ်၊
- **စာလုံးပေါင်း** — Kut = Kud = Kat; Kwai = Kai; Möng = Muang စသည်၊
- လအစစ်များ တည်ဆောက်ရာတွင် အသုံးပြုသော **လဆိုင်ရာဂဏန်းသင်္ချာ** တို့ဖြစ်သည်။

ဤ repository သည် အစဉ်အလာ 2 မျိုးကို အကောင်အထည်ဖော်ပြီး ကွာခြားချက်များကို ရှင်းလင်းစွာပြထားသည်။

---

## 2. မိခင် 10 ပါးနှင့် သားသမီး 12 ပါး

အရင်းအမြစ်အလိုက် စာလုံးပေါင်းများစွာကွဲသော်လည်း စက်ဝန်းအတွင်း **နေရာမကွဲပါ**။

| # | မိခင် (ဓာတ်) | Ahom/Shan စာလုံးပေါင်းများ | | # | သားသမီး (တိရစ္ဆာန်) | စာလုံးပေါင်းများ |
|---|---|---|---|---|---|---|
| 0 | သစ် | Kra, Kap, Kha, Karp | | 0 | ကြွက် | Jai, Chai, Choad |
| 1 | မီး | Lup, Lap | | 1 | နွား | Pao, Ngok, Chalu |
| 2 | မြေ | Hut, Hot, Hai | | 2 | ကျား | Khan, Yee, Kharn |
| 3 | သတ္တု | Muang, Mong, Möng, Mvng | | 3 | ယုန် | Mao, Tho |
| 4 | ရေ | Puek, Pok, Pök | | 4 | နဂါး/နဂါးနတ် | Si |
| 5 | သစ် | Kut, Kud, Kat | | 5 | မြွေ | Sai |
| 6 | မီး | Koat, Kwat, Khot | | 6 | မြင်း | Singa, Nga, Si-nga |
| 7 | မြေ | Hong, Hung, Hvng, Hoong | | 7 | ဆိတ် | Met, Mot, Med |
| 8 | သတ္တု | Tao, Thao, Tv | | 8 | မျောက် | San, Saan, Wok |
| 9 | ရေ | Ka, Kap, Kaap | | 9 | ကြက် | Hao, Rao, Raga |
| | | | | 10 | ခွေး | Set, Sed, Jaw |
| | | | | 11 | ဝက် | Kai, Kwai, Goon |

> ဓာတ်အစီအစဉ်မှာ သစ်၊ မီး၊ မြေ၊ သတ္တု၊ ရေ ဖြစ်ပြီး ထပ်မံစတင်သည်။ ဆယ်စုနှစ်တစ်ခုတွင် ဓာတ်တစ်မျိုးစီ 2 ကြိမ် — အဖို 1 ကြိမ်၊ အမ 1 ကြိမ် — ပေါ်သည်။ ဤသည်မှာ **တိုင်** အစီအစဉ်ဖြစ်သည်။ တရုတ် stem–element အစီအစဉ်မှာ သစ်၊ သစ်၊ မီး၊ မီး… ဟူ၍ကွဲသဖြင့် index တူသော တိုင်ဓာတ်နှင့် တရုတ် stem သည် 1-to-1 မကိုက်ပါ။ တိရစ္ဆာန်မှာ အမြဲတူသည်။

### ယှဉ်ပြိုင်နေသော stem အမည်စာရင်း 2 မျိုး

| # | Shan/Lanna (`lak_jeng.py`) | Ahom/Buranji (`lak_ni.py` default) | တရုတ် stem |
|---|---|---|---|
| 0 | Kra/Kap | Kap | 甲 jiǎ (သစ် yang) |
| 1 | Lup/Lap | Dap | 乙 yǐ (သစ် yin) |
| 2 | Hut/Hai | Rai | 丙 bǐng (မီး yang) |
| 3 | Muang/Möng | Mueang | 丁 dīng (မီး yin) |
| 4 | Puek/Pök | Plaek | 戊 wù (မြေ yang) |
| 5 | Kut/Kud | Kat | 己 jǐ (မြေ yin) |
| 6 | Koat/Khot | Khut | 庚 gēng (သတ္တု yang) |
| 7 | Hong/Hung | Rung | 辛 xīn (သတ္တု yin) |
| 8 | Tao/Thao | Tao | 壬 rén (ရေ yang) |
| 9 | Ka | Ka | 癸 guǐ (ရေ yin) |

Ahom စာရင်းသည် တရုတ် stem များနှင့် ဓာတ်ချင်းတိုက်ရိုက်ကိုက်သည်။ Shan စာရင်းက ဒေသခံ ဓာတ် 5 မျိုး×2 အယူဝါဒကို သယ်ဆောင်သည်။ 0, 3, 5, 8, 9 နေရာများသည် စာရင်းနှစ်မျိုးစလုံးတွင် အလွန်နီးစပ်သဖြင့် ရှေးဟောင်းစကားလုံးစာရင်းတစ်ခု၏ ဒေသသံကွဲများ ဖြစ်နိုင်သည်။ `lak_ni.py` သည် Buranji အထောက်အထားအရ Ahom အမည်ကို အဓိကပြပြီး Shan ပုံစံကို ဘေးချင်းယှဉ်ပြသည်။

---

## 3. အမြန်စတင်ရန်

```bash
cd lak_ni_research

python3 lak_ni.py                     # ယနေ့အတွက် Lak-Ni အစီရင်ခံစာအပြည့်
python3 lak_ni.py 2026 08 23          # သတ်မှတ် Gregorian ရက်
python3 lak_ni.py --tz 5.5            # Myanmar အချိန်အစား Assam အချိန်
python3 lak_ni.py --test              # self-test များ

python3 lak_jeng.py 2115              # တိုင်နှစ် 2115 အတွက် Lak Jeng တွက်ချက်မှုအပြည့်
python3 lak_jeng.py --date 2026 8 23  # Gregorian bridge ဖြင့် ရက်စက်ဝန်း
python3 lak_jeng.py --test            # self-test + lak_ni နှင့် 1827 ရက် cross-check
```

နမူနာ output (`lak_ni.py 2026 08 23`):

```
Gregorian date : 2026-08-23 (Sun)
Tai year       : 2026 (turns songkran)
Lak-Ni year    : 54/60 "Khutchi" (folk Me-Pi count, anchored 1193 CE)
Year name      : Rai-Singa = fire horse  [Rai (bing 丙) x Singa/Nga (horse)]
Shan variant   : Hut/Hai-Singa
Sakkaraj era   : 1388 CS (sok 8 = atthasok)
Day name       : Kut-Sai  (5/60) [Kut x Sai (snake)]
Lunar phase    : waxing day 10  [UTC+6.5, Myanmar-style]
Julian Day No. : 2461276
```

---

## 4. Algorithm A — Lak Ni နှစ်စက်ဝန်း

### အဆင့် 1 — anchor ရွေးခြင်း

လူသိများသော Ahom အစဉ်အလာသည် Ahom နိုင်ငံတည်ထောင်သူ Sukaphaa မွေးဖွားသည့် **1193 CE = “Mungkeu”** မှ နှစ်များကို ရေတွက်သည်။

| ဖြစ်ရပ် | AD နှစ် | Lak-Ni နေရာ | အမည် |
|---|---|---|---|
| Sukaphaa မွေးဖွား | 1193 | 1 | Mungkeu |
| Assam သို့ ခရီးစ | 1215 | 23 | Katrau |
| နိုင်ငံတည်ထောင် (Charaideo) | 1253 | 61 ≡ 1 | Mungkeu ထပ်မံ ✓ |
| Sukaphaa ကွယ်လွန် | 1268 | 16 | Taoni |

### အဆင့် 2 — စက်ဝန်းအတွင်းနေရာ

```
n = ((AD_year − 1193) mod 60) + 1
name = ME_PI_60[n]
```

2026 → (2026−1193) = 833 → 833 mod 60 = 53 → n = 54 → **Khutchi**, စက်ဝန်း 14။ ဤလူထုသုံးရေတွက်မှုသည် Sukaphaa ကို anchor ထားသော Ahom သမိုင်းအစဉ်အလာဖြစ်ပြီး အောက်ပါ တရုတ်နှင့်ကိုက်ညီသည့် pan-Tai အမည်စနစ်နှင့် သီးခြားဖြစ်သည်။ မရောနှောရပါ။

### အဆင့် 3 — pan-Tai ဖွဲ့စည်းပုံ

pan-Tai အမည်တွဲသည် **4 CE = kap-chai (甲子)** ဟူသော ganzhi epoch ကိုသုံးသည်။ ထို့ကြောင့် `(Y − 4)` သည် တရုတ်တွက်နည်းနှင့် တူသည်။

```
stem_index   = (AD_year − 4) mod 10      # 2026 → 2 → Rai (丙 မီး)
animal_index = (AD_year − 4) mod 12      # 2026 → 6 → Singa/Nga (မြင်း)
cycle_index  = (AD_year − 4) mod 60      # 2026 → 42 (43rd term, bǐngwǔ 丙午)
```

ထို့ကြောင့် **2026 = Rai-Singa၊ မီးမြင်းနှစ်** ဖြစ်သည်။ 2025 = Dap-Sai / 乙巳 = သစ်မြွေနှစ်ဖြစ်ပြီး “ရေမြွေ” ဟုဖော်ပြထားသော နှိုင်းယှဉ်ဇယားတစ်ခုမှာ မှားသည်။

**နှစ်ပြောင်းစည်းမျဉ်း:** Tai/Ahom နှစ်သည် January 1 တွင်မဟုတ်ဘဲ **April လလယ်** Bohag Bihu / Sangken / Songkran ကာလတွင် ပြောင်းသည်။ ထို့ကြောင့် Jan 1–Apr 13, 2026 သည် သစ်မြွေနှစ်ထဲတွင် ရှိသေးသည်။ `lak_ni.py --boundary {songkran,lichun,jan1}` တွင် default သည် Apr 14 songkran ဖြစ်သည်။

### အဆင့် 3b — ထိုင်း *sok* offset

ထိုင်းအလယ်ပိုင်းသည် stem wheel အစား Chula Sakarat နှစ်၏ နောက်ဆုံးဂဏန်းဖြစ်သော ***sok*** ကိုသုံးသည်။ `CS = Y − 638`, `sok = (Y − 638) mod 10`။ 2026 → CS 1388 → digit 8 → *atthasok* → “မြင်းနှစ် atthasok”။ စက်တစ်ခုတည်းဖြစ်သော်လည်း ဆယ်စုနှစ်အမည်ဘီးကွဲခြားခြင်းသည် almanac များနှိုင်းယှဉ်ရာတွင် stem မကိုက်ခြင်း၏ အဓိကအကြောင်းဖြစ်သည်။

**ယဉ်ကျေးမှုအလိုက် တိရစ္ဆာန်အစားထိုးမှု:** နွား→ကျွဲ (Vietnam), ယုန်→ကြောင် (Vietnam), နဂါး→Naga/Nak (Lao/Thai), ဝက်→ဆင် (Lanna အချို့)။ Khmer အသိုင်းအဝိုင်းအချို့သည် Lao ရေတွက်မှုထက် တိရစ္ဆာန် 1 ကောင်ရှေ့ (+1 offset) ဖြစ်တတ်သည်။

### အဆင့် 4 — အခြားသက္ကရာဇ်များ

```
Sakkaraj (Chula Sakarat): CS = AD_year − 638
Buddhist Era (Thai):      BE = AD_year + 543   (Myanmar/Ceylon use +544)
Great Dai era:            T  ≈ AD_year + 95
```

---

## 5. Algorithm B — အားလုံးမျှဝေသည့် 60 ရက်စက်ဝန်း

script 2 ခုစလုံးသည် ဤနည်းကို တစ်ပုံစံတည်း အသုံးပြုပြီး 5 နှစ်စာ နေ့စဉ်စစ်ဆေးထားသည်။

### အဆင့် 1 — Julian Day Number

```
a  = floor((14 − month)/12);  y = year + 4800 − a;  m = month + 12a − 3
JDN = day + floor((153m+2)/5) + 365y + floor(y/4) − floor(y/100) + floor(y/400) − 32045
```

စစ်ဆေးချက်: 2000-01-01 → 2451545။

### အဆင့် 2 — မပြတ်ရေတွက်မှုနှင့် ချိတ်ခြင်း

အခိုင်အမာထုတ်ဝေထားသောအချက် **1949-10-01 သည် jiazi (甲子 / Kap-Jai / Kra-Jai) ရက်**၊ JDN 2433191 ဖြစ်သည်ကို anchor အဖြစ်ယူသည်။

```
index = (JDN − 2433191) mod 60
mother = MOTHERS[index mod 10]
child  = ANIMALS[index mod 12]
weekday = ပုံမှန် 7 ရက်သီတင်းပတ်
```

2026-08-23 → (2461276 − 2433191) mod 60 = **5** → Kut/Kat-Sai (မြွေရက်)။ ဒေသခံ almanac ကွဲလျှင် anchor ကိုပြင်မည့်အစား ၎င်း၏ offset ကို ရှာပါ။

```bash
python3 lak_ni.py --calibrate YYYY-MM-DD AnimalName
```

---

## 6. Algorithm C — မြန်မာနည်းဖြင့် လဆန်းလဆုတ်

`lak_ni.py` သည် စည်းမျဉ်း 3 ချက်ဖြင့် ရက်တိုင်းကို ရိုးရာ လဆန်း/လဆုတ်ရက် တပ်သည်။

**စည်းမျဉ်း 1 — ပျမ်းမျှ synodic month မဟုတ်ဘဲ လကွယ်အစစ်ကိုသုံးပါ။** Meeus ၏ low-precision series `true_new_moon_jde(k)` သည် 2000-01-06 18:14 UT conjunction ကို တိကျစွာပြန်ပေးပြီး ခေတ်သစ်ကာလတွင် ~±1 minute အတွင်း ရှိသည်။

**စည်းမျဉ်း 2 — conjunction ဖြစ်သောရက်သည် လဟောင်းကိုပိတ်သည်။** ထိုရက်သည် *လကွယ်ရက်* ဖြစ်ပြီး **လဆန်း 1 သည် နောက်ရက်** ဖြစ်သည်။

```
conj_local_JD = JDE_conjunction + tz_hours/24
conj_day      = floor(conj_local_JD + 0.5)
delta         = date_JDN − conj_day

delta = 0        → လကွယ်ရက်
1 ≤ delta ≤ 14   → လဆန်း delta
delta = 15       → လပြည့်
delta ≥ 16       → လဆုတ် (delta − 15)
```

**စည်းမျဉ်း 3 — timezone သည် အမှန်တကယ်အရေးပါသည်။** August 2026 conjunction သည် **Aug 12, 17:37 UT** တွင်ဖြစ်သည်။

| ဇုန် | ဒေသစံတော်ချိန် | conjunction ရက် | 2026-08-23 |
|---|---|---|---|
| UTC+6:30 (Myanmar) | Aug 13, 00:07 | Aug 13 | **လဆန်း 10** |
| UTC+5:30 (Assam) | Aug 12, 23:07 | Aug 12 | လဆန်း 11 |

ဖြစ်ချိန်သည် မြန်မာသန်းခေါင်ယံနှင့် ~35 minute သာကွာသဖြင့် အနီးစပ်ဆုံးဇုန် 2 ခုတွင် 1 ရက်ကွာခြင်းသည် အမှားမဟုတ်ပါ။ default `--tz 6.5`; Ahom/Assam အတွက် `--tz 5.5`။ စစ်ဆေး anchor: တိုင်နှစ်သစ် 2116 = Sunday **2021-12-05 = လဆန်း 1**။

---

## 7. Algorithm D — Lak Jeng ahargaṇa အဆင့်ဆင့်

`lak_jeng.py` သည် Süa Tai Möng (2021) ၏ ရှမ်းစာနည်းကို လိုက်နာပြီး Gregorian ဇယားမလိုဘဲ ကိန်းပြည့်များသာသုံးသည်။ constants များက **Sūrya Siddhānta** mean sidereal year ကို encode လုပ်ထားသည်။

```
1577917828 civil days / 4320000 years = 365.258756481481… d
≈ 292207/800 (= 365.25875) + 7/(1350·800)
```

**တိုင်နှစ် T** အတွက် —

```
Step 1  Y = T − 1
Step 2  q = floor(Y/1350); r = Y mod 1350
        C = 7q + floor(r/193)
        N = 292207·Y + C + 6869
Step 3  Q = floor(N/800); R = N mod 800
        A = Q + 1 if R > 0 else Q                 # ahargaṇa
Step 4  M = 11·A − floor(Y/25) + 420
        D = floor(M/692); P = M mod 692
Step 5  L = floor((A+D)/30); d = (A+D) mod 30
Step 6  weekday = A mod 7                         # 1=Sun … 0=Sat
Step 7  g = (A + 2) mod 60                        # 0 = Kap-Jai
Step 8  year mother = MOTHERS[(Y + 3) mod 10]
        year child  = CHILDREN[(Y − 1) mod 12]
```

### တိုင်နှစ် 2115 နမူနာ

```
Y = 2114
C = 7·1 + floor(764/193) = 10
N = 617,732,477
Q = 772,165, R = 477 → A = 772,166
M = 8,494,162 → D = 12,274, P = 554
A + D = 784,440 = 30 × 26,148 + 0
772,166 mod 7 = 3 → Tuesday
(A+2) mod 60 = 28 → Tao + Si → "Tao Si"
year: Hung + Pao → "Hung Pao"
```

Gregorian bridge ၏ anchor မှာ **တိုင်နှစ်သစ် 2116 = Sunday 2021-12-05, A = 772,521** ဖြစ်သည်။

```
A(date) = 772521 + (JDN(date) − 2459554)
```

`lak_jeng.py --date` သည် ယင်း bridge ကိုသုံးသည်။ Gregorian ရက်၏ တိုင်နှစ်ကို `T ≈ AD + 95` ဟုခန့်မှန်းပြီး December အစောပိုင်းတွင် ပြောင်းသည်။

---

## 8. စစ်ဆေးအတည်ပြုပုံ

```bash
python3 lak_ni.py --test && python3 lak_jeng.py --test
```

| စစ်ဆေးချက် | ကိုးကားချက် | ရလဒ် |
|---|---|---|
| Me-Pi anchors 1193/1215/1253/1268 | Ahom နှစ်စာရင်း | pass |
| Pan-Tai: 1984 = ကြွက် | တရုတ်ရာသီခွင် | pass |
| JDN | 2000-01-01 = 2451545 | pass |
| ရက်စက်ဝန်း | 1949-10-01 = jiazi | pass |
| လကွယ်အစစ် k=0 | 2000-01-06 18:14 UT | exact |
| Dec 2021 လကွယ် | 07:43 UT | ±1 min |
| တိုင်နှစ်သစ် 2116 | 2021-12-05, လဆန်း 1, Sunday, A=772,521 | pass |
| Lak Jeng T=2115 | အလယ်ကိန်းအားလုံး | pass |
| lak_ni ↔ lak_jeng | 1,827 ရက်ဆက်တိုက် (2023–2027) | pass |
| 2026-08-23 | မြန်မာပြက္ခဒိန် လဆန်း 10 | reproduced |
| ယနေ့အမည် | “Kut Sai” | reproduced |

---

## 9. သိထားသောကွာခြားချက်များနှင့် မဖြေရှင်းရသေးသည့်မေးခွန်းများ

1. **Lak Jeng မူရင်းသည် ကိုယ့်ဖော်မြူလာနှင့် 10 ရက်ကွာသည်။** T=2116 အတွက် formula က A = 772,531 ရသော်လည်း update စာသားက 772,521 ဟုဆိုသည်။ ဤ implementation သည် formula ကိုမပြောင်းဘဲ ရက်ပါသောအတွဲကို Gregorian bridge အဖြစ်သုံးသည်။ epoch offsets 6,869 နှင့် 420 ၏ မူလအကြောင်းပြချက် မသိရသေးပါ။
2. **`ME_PI_60` သည် လူသုံးများသော transliterated အရင်းအမြစ်များမှလာပြီး မညီမှုရှိသည်။** ပညာရပ်ဆိုင်ရာလုပ်ငန်းအတွက် Terwiel & Ranoo (1992), p. 91 ရှိ Me Pi ဇယားဖြင့် အစားထိုးသင့်သည်။
3. **နှစ်နယ်နိမိတ်များသည် ရည်ရွယ်ချက်ရှိရှိကွဲသည်။** Ahom Lak-Ni သည် သင်္ကြန်ဝန်းကျင်၊ Shan/Great-Dai သည် December အစောပိုင်း၊ မြန်မာလများသည် April ဝန်းကျင်တွင် ပြောင်းသည်။ ပြောင်းလဲတွက်ချက်ခြင်းမပြုဘဲ ခေတ်နံပါတ်များကို မနှိုင်းယှဉ်ရ။ ရက်အမည် 60 မှာ နေရာတိုင်း တူသည်။
4. **ΔT မထည့်ထားပါ။** 2026 တွင် ကမ္ဘာလည်ပတ်မှုနောက်ကျခြင်း ~69 s သာဖြစ်၍ conjunction သန်းခေါင်ယံအလွန်နီးမှသာ ရက်အဆင့်တွင် သက်ရောက်သည်။
5. **ဓာတ် mapping:** တိုင်ဓာတ် ≠ တရုတ် stem အညွှန်းတူ။ `lak_ni.py` သည် တိုင်ဓာတ်ကိုသာ ပြသည်။

---

## 10. ဝေါဟာရများ

| ဝေါဟာရ | အဓိပ္ပါယ် |
|---|---|
| **Lak Ni / Lakni** | “ပြက္ခဒိန်”; Tai Ahom ၏ 60 စက်ဝန်းစနစ် |
| **Lak Jeng** | ထိုစက်ဝန်းအတွက် ရှမ်းလက်တွက်နည်း |
| **Me-Pi / Mae-Pi** | “မိခင်နှစ်များ” — ဓာတ် 10 စက်ဝန်း |
| **Look-Pi / Son years** | တိရစ္ဆာန် 12 စက်ဝန်း |
| **ahargaṇa (A)** | epoch မှစ၍ လွန်ခဲ့သော civil day အရေအတွက် |
| **tithi** | synodic month ၏ 1/30 |
| **watat** | မြန်မာဝါထပ်နှစ်; big watat တွင် ရက်တစ်ရက်ပါထပ်သည် |
| **Sakkaraj / CS** | Chula Sakarat = AD − 638 |
| **JDN / JDE** | Julian Day Number / Julian Ephemeris Date |
| **Oo/Hnaung Tagu** | နှစ်သစ်ကိုဖြတ်သည့် တန်ခူးဦး/တန်ခူးနှောင်း |
| **Thingyan akya/atat** | မြန်မာနှစ်သစ်ပွဲ၏ အကြတ်/အတက် နယ်နိမိတ်အချိန်များ |

---

## 11. ကိုးကားချက်များ

1. Süa Tai Möng, “Method for Calculating the Lak Jeng Cycle” (Shan, 2021)။
2. Yan Naing Aye, *Algorithm, Program and Calculation of Myanmar Calendar* (2013)။ http://cool-emerald.blogspot.com/2013/06/algorithm-program-and-calculation-of.html
3. B. J. Terwiel & Ranoo Wichasin, *Tai Ahoms and the Stars* (1992)။
4. Stephen Morey et al., *Lakni (Calendar)*, The Language Archive။ https://archive.mpi.nl/tla/islandora/object/tla%3A1839_00_0000_0000_000D_F950_D
5. Monthip Sirithaikhongchuen, *Tai Name of the Year and Tai New Year* (2007)။
6. Jean Meeus, *Astronomical Algorithms*, 2nd ed., ch. 49။
7. Burgess (trans.), *Sūrya-Siddhānta*, Chapter I, verses 34–37။ https://en.wikisource.org/wiki/Page:English_translation_of_the_Surya_Siddhanta_and_the_Siddhanta_Siromani_by_Sastri,_1861.djvu/16
8. Sewell & Dikshit, *The Indian Calendar*; Irwin, *The Burmese and Arakanese Calendars*။
9. Lars Gislén, “Burmese Eclipse Calculations”, JAHH 18(1) 2015။
10. *Sexagenary Cycle — Tai comparative research* (Aug 2026)။

---

*သုတေသန build: August 2026။ တွက်ချက်မှုအားလုံးကို 2026-08-23 (Kut-Sai, လဆန်း 10) တွင် အတည်ပြုထားသည်။*
