# Lak Ni လႄႈ Lak Jeng — ပိူင်ၼပ်ႉသွၼ်ႇပၵ်းယဵမ်ႈတႆး လူၺ်ႈ Python

ၶိူင်ႈမိုဝ်းၶူၼ်ႉၶႂႃႉလႄႈလွင်းတူၺ်း တႃႇ **ပၵ်းယဵမ်ႈ 60 ၸိုဝ်ႈ** ဢၼ်ၸၢဝ်းတႆးၸႂ်ႉတိုဝ်း — ပႃးတင်း **တႆးဢႃႇႁူမ်** မိူင်းဢႃႇသမ်ႇ၊ ဢိၼ်းတီးယႃး (ႁွင်ႉဝႃႈ *Lak Ni* / *Lakni*) လႄႈ **တႆး** မိူင်းမၢၼ်ႈ (ပိူင်ၼပ်ႉသွၼ်ႇတင်းမိုဝ်း ႁွင်ႉဝႃႈ *Lak Jeng*)။

မီးပိူင်သၢင်ႈ 2 ပိူင် ဢၼ်လွတ်ႈလႅဝ်းၵၼ်၊ ၸွမ်းၸိူဝ်းၶိူဝ်းတႅမ်ႈမၢႆဝႆႉမၢင်ပိူင်။ မီးၸုမ်းတူၺ်းသွပ်ႇ ဢၼ်ယိုၼ်ယၼ်ဝႃႈ တင်း 2 ပိူင် ပၼ်ၶေႃႈတွပ်ႇမိူၼ်ၵၼ် လႄႈတူၵ်းမႅၼ်ႈၶေႃႈမုၼ်းဢိင်ဢၢင်ႈ ဢၼ်ပိုၼ်ၽႄႈဝႆႉ။

| Script | ၸိူဝ်းၶိူဝ်းဢၼ်ၸွမ်း | ပိူင် |
|---|---|---|
| `lak_ni.py` | တႆးဢႃႇႁူမ် *Lak Ni* (ဢႃႇသမ်ႇ) | ၵၢၼ်ၼပ်ႉသွၼ်ႇ modular ပေါ် Julian Day Numbers |
| `lak_jeng.py` | တႆး *Lak Jeng* (မိူင်းမၢၼ်ႈ/ယူႇၼၢၼ်ႇ) | ၼပ်ႉဝၼ်းပဵၼ်ၵွၼ်ႈ (*ahargaṇa*) ၸွမ်း Sūrya Siddhānta |
| `sakkaraj.py` | ပိူင်သၵ်ႉၵရဵတ်ႈ Chula Sakarat / Thet Kayit | ၵฎ watat မၢၼ်ႈ + လၵ်းၼပ်ႉ avoman ထႆး |

မၢႆတွင်းၶူၼ်ႉၶႂႃႉၵိုၵ်းၵၼ်: **`SAKKARAJ_SHN.md`** — ၶူၼ်ႉလူင်းလိုၵ်ႉလွင်ႈၸုမ်းပီသၵ်ႉၵရဵတ်ႈ (Anjana 691 BCE → Buddha 544 BCE → Śaka/Mahā 78 CE → **Cula Sakarat 22 March 638 CE**), ယူၵ်ႉၵၢပ်ႈၼပ်ႉသွၼ်ႇ Makaranta→Thandeikta→Advisory-Board, ၵฎထႅမ်လိူၼ် watat, ပၼ်ႁႃမၢႆလိူၼ်တၢမ်တူင်ႇတီႈ လႄႈတီႈဝၢင်းဝၼ်းထႅမ် ဢၼ်ထႆး/မၢၼ်ႈပႅၵ်ႇပိူင်ႈၵၼ်။

ဢမ်ႇလူဝ်ႇ dependency ၽၢႆႇၼွၵ်ႈ — ၸႂ်ႉ Python 3 standard library ၵူၺ်း။

---

## သဵၼ်ႈမၢႆႁူဝ်ၶေႃႈ

1. [ပိုၼ်ႉလင်: ဝူင်းလဵဝ် ဢုပ်ႉပိူင်တင်းမူတ်း](#1-ပိုၼ်ႉလင်-ဝူင်းလဵဝ်-ဢုပ်ႉပိူင်တင်းမူတ်း)
2. [မႄႈ 10 လႄႈ လုၵ်ႈ 12](#2-မႄႈ-10-လႄႈ-လုၵ်ႈ-12)
3. [တႄႇၸႂ်ႉလႅတ်းလႅဝ်း](#3-တႄႇၸႂ်ႉလႅတ်းလႅဝ်း)
4. [Algorithm A — ဝူင်းပီ Lak Ni](#4-algorithm-a--ဝူင်းပီ-lak-ni)
5. [Algorithm B — ဝူင်းဝၼ်း 60 ဢၼ်ႁူမ်ႈၵၼ်](#5-algorithm-b--ဝူင်းဝၼ်း-60-ဢၼ်ႁူမ်ႈၵၼ်)
6. [Algorithm C — လိူၼ်မႂ်ႇ/လိူၼ်မူၼ်း ပိူင်မၢၼ်ႈ](#6-algorithm-c--လိူၼ်မႂ်ႇလိူၼ်မူၼ်း-ပိူင်မၢၼ်ႈ)
7. [Algorithm D — Lak Jeng ahargaṇa တီႈလႂ်တီႈၼၼ်ႈ](#7-algorithm-d--lak-jeng-ahargaṇa-တီႈလႂ်တီႈၼၼ်ႈ)
8. [ပိူင်ယိုၼ်ယၼ်တင်းမူတ်း](#8-ပိူင်ယိုၼ်ယၼ်တင်းမူတ်း)
9. [ၶေႃႈပႅၵ်ႇပိူင်ႈလႄႈၶေႃႈထၢမ်ဢၼ်ပႆႇတွပ်ႇ](#9-ၶေႃႈပႅၵ်ႇပိူင်ႈလႄႈၶေႃႈထၢမ်ဢၼ်ပႆႇတွပ်ႇ)
10. [ၶေႃႈသပ်း](#10-ၶေႃႈသပ်း)
11. [ဢိင်ဢၢင်ႈ](#11-ဢိင်ဢၢင်ႈ)

---

## 1. ပိုၼ်ႉလင်: ဝူင်းလဵဝ် ဢုပ်ႉပိူင်တင်းမူတ်း

ၸုမ်းပၵ်းယဵမ်ႈတႆး သိုပ်ႇမႃးတီႈပိူင်ၶႄႇ **ganzhi (干支)**: တူဝ်ၼပ်ႉ 2 ဢၼ် — ဢၼ်ၼိုင်ႈယၢဝ်း 10 ("မႄႈ" / heavenly stems) လႄႈဢၼ်ၼိုင်ႈယၢဝ်း 12 ("လုၵ်ႈ" / earthly branches / တူဝ်သတ်းပီ) — ၶိုၼ်ႈၵိုၵ်းၵၼ်။ ယွၼ်ႉ lcm(10, 12) = **60** ၸင်ႇမီးၸိုဝ်ႈၵူႈ 60 ၵူႈ ဢၼ်ဢမ်ႇတူၵ်းၵၼ် ၵွၼ်ႇဝူင်းၼႆႉတေသမ်ႉၶိုၼ်း:

```
Kra-Jai, Lup-Pao, Hai-Khan, Muang-Mao, Puek-Si, ...
... Tao-Hao, Ka-Set, Kra-Jai  ← သမ်ႉၶိုၼ်းလင် 60 ၶၵ်ႉ
```

ၸိုဝ်ႈ 60 ဢၼ်ၼႆႉ ၸႂ်ႉၶိုၼ်းတႃႇ **ပီ**, **ဝၼ်း**, ထိုင်တီႈ **လိူၼ်/ၸူဝ်ႈမူင်း** တၢမ်ၸုမ်းၵူၼ်း။ ဢၼ်လမ်ႇလွင်ႈတႄႉ ဝူင်း *ဝၼ်း* ပဵၼ်ၵၢၼ်ၼပ်ႉသိုပ်ႇတေႃႇ ဢၼ်ၶႄႇ၊ တႆး၊ Dai၊ Lue၊ Khün လႄႈ Ahom ႁူမ်ႈၵၼ်။ မီးၵၢၼ်တူၵ်းမႅၼ်ႈဢၼ်ထုၵ်ႇတီႈသုတ်း 1 ပိူင်ၵူၺ်း၊ ဢမ်ႇၸႂ်ႈၸၢဝ်းလႂ်ၸၢဝ်းၼၼ်ႉ။

ဢၼ်ပႅၵ်ႇပိူင်ႈၵၼ်တႄႉ:

- **epoch** (ပီပိုၼ်းတီႈလႂ်ပဵၼ် "ပီ 1"),
- **ၶွပ်ႇပီမႂ်ႇ** (ႁူဝ် December? April Thingyan? ပီမႂ်ႇတၢမ်လိူၼ်?),
- **ပိူင်တႅမ်ႈ** (Kut = Kud = Kat; Kwai = Kai; Möng = Muang ...),
- **လၵ်းၼပ်ႉလိူၼ်** တႃႇသၢင်ႈလိူၼ်တႄႉ။

repository ၼႆႉသၢင်ႈဝႆႉ 2 ၸိူဝ်းၶိူဝ်း လႄႈၼႄၶေႃႈပႅၵ်ႇပိူင်ႈၸႅင်ႈလႅင်း။

---

## 2. မႄႈ 10 လႄႈ လုၵ်ႈ 12

ပိူင်တႅမ်ႈပႅၵ်ႇပိူင်ႈၵၼ်ၼမ်တၢမ်ငဝ်ႈၶေႃႈမုၼ်း၊ ၵူၺ်းၵႃႈတီႈယူႇ **ဢမ်ႇ** ပႅၵ်ႇ။ ၸိုဝ်ႈတင်းမူတ်းတီႈတႂ်ႈၼႆႉ ပဵၼ်တီႈယူႇလဵဝ်ၵၼ်ၼႂ်းဝူင်း:

| # | မႄႈ (ထၢတ်ႈ) | Ahom/Shan ပိူင်တႅမ်ႈ | | # | လုၵ်ႈ (တူဝ်သတ်း) | ပိူင်တႅမ်ႈ |
|---|---|---|---|---|---|---|
| 0 | မႆႉ | Kra, Kap, Kha, Karp | | 0 | ၼူ | Jai, Chai, Choad |
| 1 | ၾႆး | Lup, Lap | | 1 | ဝူဝ်း | Pao, Ngok, Chalu |
| 2 | လိၼ် | Hut, Hot, Hai | | 2 | သၢင်ႇသီႈ | Khan, Yee, Kharn |
| 3 | လဵၵ်း | Muang, Mong, Möng, Mvng | | 3 | ပၢင်ႇတၢႆး | Mao, Tho |
| 4 | ၼမ်ႉ | Puek, Pok, Pök | | 4 | လူင်/ၼႃးၵႃး | Si |
| 5 | မႆႉ | Kut, Kud, Kat | | 5 | ငူး | Sai |
| 6 | ၾႆး | Koat, Kwat, Khot | | 6 | မႃႉ | Singa, Nga, Si-nga |
| 7 | လိၼ် | Hong, Hung, Hvng, Hoong | | 7 | ပႄႉ | Met, Mot, Med |
| 8 | လဵၵ်း | Tao, Thao, Tv | | 8 | လိင်း | San, Saan, Wok |
| 9 | ၼမ်ႉ | Ka, Kap, Kaap | | 9 | ၵႆႇ | Hao, Rao, Raga |
| | | | | 10 | မႃ | Set, Sed, Jaw |
| | | | | 11 | မူ | Kai, Kwai, Goon |

> မၢႆတွင်းပိူင်ထၢတ်ႈ: မႆႉ၊ ၾႆး၊ လိၼ်၊ လဵၵ်း၊ ၼမ်ႉ သမ်ႉၶိုၼ်း —
> *ထၢတ်ႈၼိုင်ႈၸိူဝ်ႉ ပေႃႇ 2 ပွၵ်ႈၼႂ်း 10 ပီ*၊ ၸၢႆး 1 ပွၵ်ႈ ယိင်း 1 ပွၵ်ႈ။
> ၼႆႉပဵၼ်ပိူင် **တႆး**။ ပိူင် stem-element ၶႄႇဝၢင်းတၢင်ႇပိူင် (မႆႉ၊ မႆႉ၊ ၾႆး၊ ၾႆး...)၊ ၵွပ်ႈၼၼ် ထၢတ်ႈတႆးဢမ်ႇတူၵ်းမႅၼ်ႈ stem ၶႄႇ 1-to-1 တီႈ index လဵဝ်ၵၼ် — ၵူၺ်းၵႃႈတူဝ်သတ်းတူၵ်းမႅၼ်ႈတႃႇသေႇ။

### တႃႇၸိုဝ်ႈ stem 2 ၸုမ်း ဢၼ်ၶႄႉၶဵင်ႇၵၼ် (လမ်ႇလွင်ႈ!)

ၵၢၼ်ၶူၼ်ႉၶႂႃႉတႅၵ်ႈၼိူင်း Vietnam/Laos/Thailand/India ၼႄဝႃႈ မီး **2 ၸုမ်းၸိုဝ်ႈ ဢၼ်မီးလၵ်းထၢၼ်** တႃႇတီႈယူႇ 10 ဢၼ်လဵဝ်ၵၼ်:

| # | Shan/Lanna (`lak_jeng.py`, ယိုၼ်ယၼ်ယဝ်ႉ) | Ahom/Buranji (`lak_ni.py` default) | stem ၶႄႇ |
|---|---|---|---|
| 0 | Kra/Kap | Kap | 甲 jiǎ (မႆႉ yang) |
| 1 | Lup/Lap | Dap | 乙 yǐ (မႆႉ yin) |
| 2 | Hut/Hai | Rai | 丙 bǐng (ၾႆး yang) |
| 3 | Muang/Möng | Mueang | 丁 dīng (ၾႆး yin) |
| 4 | Puek/Pök | Plaek | 戊 wù (လိၼ် yang) |
| 5 | Kut/Kud | Kat | 己 jǐ (လိၼ် yin) |
| 6 | Koat/Khot | Khut | 庚 gēng (လဵၵ်း yang) |
| 7 | Hong/Hung | Rung | 辛 xīn (လဵၵ်း yin) |
| 8 | Tao/Thao | Tao | 壬 rén (ၼမ်ႉ yang) |
| 9 | Ka | Ka | 癸 guǐ (ၼမ်ႉ yin) |

ၸုမ်း Ahom တူၵ်းမႅၼ်ႈထၢတ်ႈတေႃႇထၢတ်ႈၵပ်း stem ၶႄႇ။ ၸုမ်း Shan သမ်ႉယိပ်းၵမ်ပိူင်ပႆႇထၢတ်ႈ×2 ပိူင်တႆး။ တီႈ 0, 3, 5, 8, 9 ၸမ်ၵၼ်ၼႃႇၼႂ်းတင်း 2 ၸုမ်း (Kap≈Kra, Mueang≈Muang, Kat≈Kut, Tao, Ka) — တေၸၢင်ႈပဵၼ်သဵင်ၵႂၢမ်းပႅၵ်ႇၵၼ်ၶွင်သဵၼ်ႈၶေႃႈၵႂၢမ်းၵဝ်ႇလဵဝ်ၵၼ်။ `lak_ni.py` ဢဝ်ၸိုဝ်ႈ Ahom ပဵၼ်လၵ်း (လၵ်းထၢၼ် Buranji: "Lakni Rung-rao" = 辛酉 လဵၵ်း-ၵႆႇ; သဵၼ်ႈပီဢၼ်ၵူၼ်းၸႂ်ႉၼမ် ဝူင်းၸွမ်း *dap, rai, khut, rung*) လႄႈၼႄပိူင် Shan ၵိုၵ်းၵၼ်။

---

## 3. တႄႇၸႂ်ႉလႅတ်းလႅဝ်း

```bash
cd lak_ni_research

python3 lak_ni.py                     # မိူဝ်ႈၼႆႉ: လၢႆးငၢၼ်း Lak-Ni တဵမ်ထူၼ်ႈ
python3 lak_ni.py 2026 08 23          # ဝၼ်း Gregorian တီႈၵျႃႉ
python3 lak_ni.py --tz 5.5            # ယၢမ်း Assam တႅၼ်းယၢမ်း Myanmar
python3 lak_ni.py --test              # ပွႆႇ self-tests

python3 lak_jeng.py 2115              # ၼပ်ႉ Lak Jeng တဵမ်ထူၼ်ႈ တႃႇပီတႆး 2115
python3 lak_jeng.py --date 2026 8 23  # ဝူင်းဝၼ်း လူၺ်ႈ Gregorian bridge
python3 lak_jeng.py --test            # self-tests + cross-check 1827 ဝၼ်း ၵပ်း lak_ni
```

တူဝ်ယၢင်ႇ output (`lak_ni.py 2026 08 23`):

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

## 4. Algorithm A — ဝူင်းပီ Lak Ni

### ၶၵ်ႉ 1 — လိူၵ်ႈမၢႆလၵ်း

ၸိူဝ်းၶိူဝ်း Ahom ဢၼ်ၵူၼ်းၸႂ်ႉၼမ် တႄႇၼပ်ႉပီတီႈ **1193 CE = "Mungkeu"**၊ ပီၵိူတ်ႇၸဝ်ႈ Sukaphaa ၽူႈတင်ႈမိူင်း Ahom။ မၢႆလၵ်းၼႆႉတူၺ်းသွပ်ႇလႆႈတီႈသဵၼ်ႈပီဢၼ်ပိုၼ်ၽႄႈဝႆႉ:

| လွင်ႈပဵၼ် | ပီ AD | တီႈ Lak-Ni | ၸိုဝ်ႈ |
|---|---|---|---|
| Sukaphaa ၵိူတ်ႇ | 1193 | 1 | Mungkeu |
| တႄႇၶၢဝ်းတၢင်းၵႂႃႇ Assam | 1215 | 23 | Katrau |
| တင်ႈမိူင်း (Charaideo) | 1253 | 61 ≡ 1 | Mungkeu ထႅင်ႈ ✓ |
| Sukaphaa သဵင်ႈၵၢမ်ႇ | 1268 | 16 | Taoni |

### ၶၵ်ႉ 2 — တီႈယူႇၼႂ်းဝူင်း

```
n = ((AD_year − 1193) mod 60) + 1        # တီႈယူႇ 1-based ၼႂ်းဝူင်း Me-Pi 60 ပီ
name = ME_PI_60[n]                       # မိူၼ် n=54 → "Khutchi"
```

တူဝ်ယၢင်ႇ: 2026 → (2026−1193) = 833 → 833 mod 60 = 53 → n = 54 → **Khutchi**, ဝူင်း 14။ ⚠️ မၢႆၼပ်ႉၵူၼ်းမိူင်းၼႆႉ ဢိင်ပိုၼ်း Ahom (Sukaphaa)။ မၼ်းပဵၼ်ၸိူဝ်းၶိူဝ်းၼပ်ႉဢၼ် **ၽၢတ်ႇ** တီႈၸိုဝ်ႈ pan-Tai ဢၼ်တူၵ်းမႅၼ်ႈၶႄႇတီႈတႂ်ႈ — ယႃႇဢဝ်ရူၼ်းၵၼ်။

### ၶၵ်ႉ 3 — ယႅၵ်ႈၶူင်သၢင်ႈ (pan-Tai alignment)

ၸိုဝ်ႈၵူႈ pan-Tai ၸႂ်ႉ epoch ganzhi ၵဝ်ႇ: **4 CE = kap-chai (甲子)**၊ ၵွပ်ႈၼၼ် `(Y − 4)` မိူၼ်ပိူင်ၶႄႇ။ constant 1984 ဢၼ်ၸႂ်ႉမႃးဢွၼ်တၢင်း ≡ 4 mod 10/12/60 ၸင်ႇပၼ် index မိူၼ်ၵၼ်:

```
stem_index   = (AD_year − 4) mod 10      # 2026 → 2 → Rai (丙 ၾႆး)
animal_index = (AD_year − 4) mod 12      # 2026 → 6 → Singa/Nga (မႃႉ)
cycle_index  = (AD_year − 4) mod 60      # 2026 → 42 (ၶေႃႈ 43, bǐngwǔ 丙午)
```

→ **2026 = Rai-Singa, ပီမႃႉၾႆး** (ၶႄႇ Bǐng-wǔ ✓)။
2025 = Dap-Sai / 乙巳 = မႆႉ-ငူး (တႃႇတႅၵ်ႈၼိူင်းဢၼ်ၽႄႈဝႆႉဢၼ်ၼိုင်ႈ တႅမ်ႈၽိတ်းဝႃႈ "ၼမ်ႉ-ငူး"; 乙 ပဵၼ် မႆႉ-yin)။

**ၵฎပိၼ်ႇပီ (လမ်ႇလွင်ႈတႃႇဝၼ်း!):** ပီ Tai/Ahom ပိၼ်ႇမွၵ်ႈ **ၵၢင် April** (Bohag Bihu / Sangken / Songkran)၊ ဢမ်ႇၸႂ်ႈ January 1။ ၵွပ်ႈၼၼ် Jan 1–Apr 13, 2026 ယင်းပဵၼ်ပီ *မႆႉ-ငူး*။ ပိူင်ၶႄႇပိၼ်ႇတီႈ Lìchūn (~Feb 4)။ `lak_ni.py --boundary {songkran,lichun,jan1}` (default songkran, Apr 14) ၸႂ်ႉၵฎၼႆႉၵွၼ်ႇၼပ်ႉပီတင်းမူတ်း။

### ၶၵ်ႉ 3b — ပၼ်ႁႃ offset *sok* ထႆး

ထႆးၵၢင် တၢင် stem wheel လူၺ်ႈ ***sok*** တီႈပဵၼ်တူဝ်လိၵ်ႈလိုၼ်းသုတ်းၶွင်ပီ Chula Sakarat, `CS = Y − 638`။ မၼ်းယူႇ −4 တီႈတၢႆတူဝ်တီႈ kap–ka index: `sok = (Y − 638) mod 10`။ 2026 → CS 1388 → digit 8 → *atthasok* → "ပီမႃႉ atthasok"။ ၶိူင်ႈၸၵ်းလဵဝ်ၵၼ်၊ ဝူင်းၸိုဝ်ႈ 10 ပီပႅၵ်ႇၵၼ် — ပဵၼ်ငဝ်ႈပၼ်ႁႃ #1 တီႈ "stem ၵဝ်ဢမ်ႇတူၵ်း" မိူဝ်ႈတႅၵ်ႈ almanac။

**တူဝ်သတ်းတၢင်တႅၼ်းတၢမ်ၸိူဝ်ႉၸၢတ်ႈ:** ဝူဝ်း→ၵႂၢႆး (Vietnam), ပၢင်ႇတၢႆး→မႅဝ်း (Vietnam), လူင်→ၼႃးၵႃး/Nak (Lao/Thai), မူ→ၸၢင်ႉ (Lanna မၢင်တီႈ); Khmer ၵႆႉၼပ်ႉတူဝ်သတ်းလူင်ႈၼႃႈ Lao 1 တူဝ် (+1 offset)။

### ၶၵ်ႉ 4 — ပီၵမ်ႉထႅမ်

```
Sakkaraj (Chula Sakarat): CS = AD_year − 638
Buddhist Era (Thai):      BE = AD_year + 543   (Myanmar/Ceylon ၸႂ်ႉ +544)
Great Dai era:            T  ≈ AD_year + 95    (epoch 95 BCE, တူၺ်း lak_jeng)
```

---

## 5. Algorithm B — ဝူင်းဝၼ်း 60 ဢၼ်ႁူမ်ႈၵၼ်

script တင်း 2 သၢင်ႈဝႆႉမိူၼ်ၵၼ် (တူၺ်းသွပ်ႇဝၼ်းတေႃႇဝၼ်းယဝ်ႉ 5 ပီ)။

### ၶၵ်ႉ 1 — Julian Day Number

```
a  = floor((14 − month)/12);  y = year + 4800 − a;  m = month + 12a − 3
JDN = day + floor((153m+2)/5) + 365y + floor(y/4) − floor(y/100) + floor(y/400) − 32045
```

တူၺ်းသွပ်ႇ: 2000-01-01 → 2451545။

### ၶၵ်ႉ 2 — ယိုတ်းၵပ်းၵၢၼ်ၼပ်ႉသိုပ်ႇတေႃႇ

ၵၢၼ်ၼပ်ႉၼႆႉတႅၵ်ႈတင်ႈလူၺ်ႈၶေႃႈတႄႉ ဢၼ်ပိုၼ်ၽႄႈယဝ်ႉလႄႈမၼ်ႈၵိုမ်း: **1949-10-01 ပဵၼ်ဝၼ်း jiazi (甲子 / Kap-Jai / Kra-Jai)**, JDN 2433191။

```
index = (JDN − 2433191) mod 60       # 0 = Kra-Jai / Kap-Jai
mother = MOTHERS[index mod 10]
child  = ANIMALS[index mod 12]
weekday = ဝူင်ႈ 7 ဝၼ်းထမ်ႇမတႃႇ (လွတ်ႈလႅဝ်းတီႈဝူင်းၼႆႉ)
```

တူဝ်ယၢင်ႇ: 2026-08-23 → (2461276 − 2433191) mod 60 = **5** → Kut/Kat-Sai (ဝၼ်းငူး)။

သင် almanac ၼႂ်းတူင်ႇၵူၼ်းသူ ပႅၵ်ႇၵၼ်ၸိုင် ၶႆႈၸႂ် private offset မၼ်း တႅၼ်းတေပြင်မၢႆလၵ်း:

```bash
python3 lak_ni.py --calibrate YYYY-MM-DD AnimalName   # ၼႄမၢႆလၵ်းတီႈပဵၼ်လႆႈ
```

---

## 6. Algorithm C — လိူၼ်မႂ်ႇ/လိူၼ်မူၼ်း ပိူင်မၢၼ်ႈ

`lak_ni.py` တိတ်းၸိုဝ်ႈဝၼ်းလိူၼ်မႂ်ႇ/လွင်ႈ လူၺ်ႈၵฎ 3 ဢၼ် (တူၺ်း §8, check 4):

**ၵฎ 1 — ၸႂ်ႉလိူၼ်မႂ်ႇတႄႉ၊ ဢမ်ႇၸႂ်ႉ mean synodic month။**
series လႅတ်းလႅဝ်း Meeus (`true_new_moon_jde(k)` ၼႂ်း code) ပၼ် conjunction 2000-01-06 18:14 UT တူၵ်းမႅၼ်ႈတႅတ်ႈတေႃး လႄႈၽိတ်းဢမ်ႇပူၼ်ႉ ~±1 မိၼိတ်ႉတႃႇၵၢပ်ႈယၢမ်းမႂ်ႇ။

**ၵฎ 2 — ဝၼ်း conjunction ပိၵ်ႉလိူၼ်ၵဝ်ႇ။**
ငဝ်ႈၶေႃႈမုၼ်းတင်း 2 ၸိူဝ်းၶိူဝ်းလၢတ်ႈဝႆႉၸႅင်ႈလႅင်း:

> *"ဝၼ်းလိူၼ်လပ်း ပဵၼ်ဝၼ်းလိုၼ်းသုတ်းၶွင်လိူၼ်"* — cool-emerald (Myanmar), §7.2

ၵွပ်ႈၼၼ် ဢဝ်ၶၢဝ်း conjunction သႂ်ႇၼႂ်းယၢမ်းတူင်ႇတီႈ၊ ဝၼ်းမိူင်းၼၼ်ႉပဵၼ် *ဝၼ်းလိူၼ်လပ်း*; **လိူၼ်မႂ်ႇ 1 ပဵၼ်ဝၼ်းထတ်းမႃး။**

```
conj_local_JD = JDE_conjunction + tz_hours/24
conj_day      = floor(conj_local_JD + 0.5)      # ဝၼ်းမိူင်းဢၼ်ပႃး conjunction
delta         = date_JDN − conj_day

delta = 0        → ဝၼ်းလိူၼ်လပ်း (ဝၼ်းလိုၼ်းလိူၼ်ၵဝ်ႇ)
1 ≤ delta ≤ 14   → ဝၼ်းလိူၼ်မႂ်ႇ delta
delta = 15       → ဝၼ်းလိူၼ်မူၼ်း
delta ≥ 16       → ဝၼ်းလိူၼ်လွင်ႈ (delta − 15)
```

**ၵฎ 3 — timezone မီးၽွၼ်းတႄႉ။**

တူဝ်ယၢင်ႇတႄႉ August 2026 — conjunction တီႈ **Aug 12, 17:37 UT**:

| ယၢမ်း | conjunction တူင်ႇတီႈ | ဝၼ်း conjunction | 2026-08-23 ပဵၼ် |
|---|---|---|---|
| UTC+6:30 (Myanmar) | Aug 13, 00:07 | Aug 13 | **လိူၼ်မႂ်ႇ 10** |
| UTC+5:30 (Assam)   | Aug 12, 23:07 | Aug 12 | လိူၼ်မႂ်ႇ 11 |

ၶၢဝ်းၼၼ်ႉတူၵ်းၼႂ်း ~35 မိၼိတ်ႉၸမ်ၵၢင်ၶိုၼ်းမၢၼ်ႈ၊ ၵွပ်ႈၼၼ် ပၵ်းယဵမ်ႈတီႈၸႂ်ႉယၢမ်းတိတ်းၵၼ် ပႅၵ်ႇၵၼ် 1 ဝၼ်းလူၺ်ႈပိူင်သၢင်ႈ၊ ဢမ်ႇၸႂ်ႈၶေႃႈၽိတ်း။ Default ပဵၼ် `--tz 6.5`; တႃႇ Ahom/Assam ၸႂ်ႉ `--tz 5.5`။

မၢႆလၵ်းတူၺ်းသွပ်ႇ: ပီမႂ်ႇတႆး 2116 = ဝၼ်းဢႃးတိတ်ႉ **2021-12-05 = လိူၼ်မႂ်ႇ 1** (conjunction Dec 4) — တူၵ်းၸွမ်းလိၵ်ႈ Shan လႄႈၵฎ Myanmar။

---

## 7. Algorithm D — Lak Jeng ahargaṇa တီႈလႂ်တီႈၼၼ်ႈ

`lak_jeng.py` ၸွမ်းပိူင်ၵႂၢမ်းတႆး ("Method for Calculating the Lak Jeng Cycle", Süa Tai Möng, 2021) ဢၼ်ဢမ်ႇလူဝ်ႇ table Gregorian — ၸႂ်ႉ integer ၵူၺ်း။ constants မၼ်းတၢင်ႇ mean sidereal year ၶွင် **Sūrya Siddhānta**:

```
1577917828 civil days / 4320000 years = 365.258756481481… d
≈ 292207/800 (= 365.25875)  +  7/(1350·800)  (ၵၢၼ်ပြင်ၶိုၼ်း 28 ဝၼ်း/mahāyuga)
```

မိူဝ်ႈပၼ် **ပီတႆး T**:

```
ၶၵ်ႉ 1  Y = T − 1                                   (ပီၼပ်ႉသွၼ်ႇ)

ၶၵ်ႉ 2  q = floor(Y/1350);  r = Y mod 1350
        C = 7q + floor(r/193)                       (တူဝ်ၼပ်ႉပြင်ၸိူင်း)
        N = 292207·Y + C + 6869                     (တူဝ်တင်ႈဝၼ်း, epoch 6869)

ၶၵ်ႉ 3  Q = floor(N/800);  R = N mod 800             (R = "တီႈဝၼ်းၵဝ်ႇ",
        A = Q + 1 if R > 0 else Q                     800−R = "တီႈဝၼ်းမႂ်ႇ")
                                                      A = ဝၼ်းပူၼ်ႉ = ahargaṇa

ၶၵ်ႉ 4  M = 11·A − floor(Y/25) + 420                 ("ဝၼ်းႁၢႆ", tithi drift)
        D = floor(M/692);  P = M mod 692

ၶၵ်ႉ 5  L = floor((A+D)/30);  d = (A+D) mod 30       (လိူၼ်ဢၼ်တဵမ်ယဝ်ႉ,
                                                      ဝၼ်းၼႂ်းလိူၼ်)

ၶၵ်ႉ 6  weekday = A mod 7                            (1=Sun … 6=Fri, 0=Sat)

ၶၵ်ႉ 7  day index g = (A + 2) mod 60                 (0 = Kap-Jai)
        day mother = MOTHERS[g mod 10];  day child = CHILDREN[g mod 12]

ၶၵ်ႉ 8  year mother = MOTHERS[(Y + 3) mod 10]        (≡ (Y+4) mod 10, 1-based)
        year child  = CHILDREN[(Y − 1) mod 12]       (≡ Y mod 12, 1-based)
```

### တူဝ်ယၢင်ႇ — ပီတႆး 2115 (`lak_jeng.py 2115` ပၼ်မိူၼ်ၵၼ်တႅတ်ႈတေႃး)

```
Y = 2114
C = 7·1 + floor(764/193) = 7 + 3 = 10
N = 292207·2114 + 10 + 6869 = 617,732,477
Q = 772,165, R = 477  →  A = 772,166
M = 11·772166 − 84 + 420 = 8,494,162  →  D = 12,274, P = 554
A + D = 784,440 = 30 × 26,148 + 0     →  26,148 လိူၼ်, တီႈ 0
772,166 mod 7 = 3                      →  ဝၼ်းဢင်းၵၢၼ်း
(A+2) mod 60 = 28 → Tao + Si           →  "Tao Si"
ပီ: Hung + Pao                          →  "Hung Pao"
```

### ယိုတ်းၵပ်းဝၼ်း Gregorian

ငဝ်ႈၶေႃႈမုၼ်းပၼ်ၵူႈဝၼ်းဢၼ်မီးဝၼ်းတီႈ: **ပီမႂ်ႇတႆး 2116 = ဝၼ်းဢႃးတိတ်ႉ 2021-12-05, A = 772,521**။ ယွၼ်ႉဝၼ်းမိူင်းတိတ်းၵၼ် ႁဵတ်းႁႂ်ႈ A ၶိုၼ်ႈ 1:

```
A(date) = 772521 + (JDN(date) − 2459554)
```

ၼႆႉပဵၼ် bridge ဢၼ် `lak_jeng.py --date` ၸႂ်ႉ လႄႈပဵၼ်ပိူင်တူၺ်းသွပ်ႇ script တင်း 2 (§8)။ တႃႇမၢႆပီ Tai ၶွင်ဝၼ်း Gregorian, script ၶၢတ်ႈ `T ≈ AD + 95` လႄႈပိၼ်ႇတီႈႁူဝ် December။

---

## 8. ပိူင်ယိုၼ်ယၼ်တင်းမူတ်း

ပွႆႇ test တင်း 2 လႆႈၵူႈၶၢဝ်း:

```bash
python3 lak_ni.py --test && python3 lak_jeng.py --test
```

| တူၺ်းသွပ်ႇ | ဢိင်ဢၢင်ႈ | ၽွၼ်း |
|---|---|---|
| မၢႆလၵ်း Me-Pi 1193/1215/1253/1268 | သဵၼ်ႈပီ Ahom ဢၼ်ပိုၼ်ၽႄႈ | pass |
| တူဝ်သတ်း Pan-Tai: 1984 = ၼူ | တူၵ်းမႅၼ်ႈတူဝ်သတ်းပီၶႄႇ | pass |
| Formula JDN | 2000-01-01 = 2451545 | pass |
| မၢႆလၵ်းဝူင်းဝၼ်း | 1949-10-01 = jiazi (Kap-Jai) | pass |
| လိူၼ်မႂ်ႇတႄႉ, k=0 | 2000-01-06 18:14 UT | တႅတ်ႈတေႃး |
| လိူၼ်မႂ်ႇတႄႉ, Dec 2021 | solar-eclipse conjunction 07:43 UT | ±1 min |
| ပီမႂ်ႇတႆး 2116 = 2021-12-05 | လိူၼ်မႂ်ႇ 1, ဝၼ်းဢႃးတိတ်ႉ, A=772,521 | pass |
| တူဝ်ယၢင်ႇ Lak Jeng T=2115 | integer ၵူႈၶၵ်ႉ | pass |
| lak_ni ↔ lak_jeng တူၵ်းၵၼ် | 1,827 ဝၼ်းတိတ်းၵၼ် (2023–2027), cycle index + weekday | pass |
| တိတ်းၸိုဝ်ႈလိူၼ် 2026-08-23 | ပၵ်းယဵမ်ႈ Myanmar ၼႄလိူၼ်မႂ်ႇ 10 | reproduced (UTC+6:30) |
| ၸိုဝ်ႈဝၼ်းမိူဝ်ႈၼႆႉ | almanac ၼႂ်းတူင်ႇၵူၼ်း "Kut Sai" | reproduced (index 5) |

---

## 9. ၶေႃႈပႅၵ်ႇပိူင်ႈလႄႈၶေႃႈထၢမ်ဢၼ်ပႆႇတွပ်ႇ

ၶေႃႈၵတ်ႉၶၢတ်ႇဢၼ်လူဝ်ႇႁူႉၵွၼ်ႇဢိင်ဢၢင်ႈ code ၼႆႉ:

1. **ငဝ်ႈ Lak Jeng ပႅၵ်ႇၵၼ်တင်းတူဝ်မၼ်း 10 ဝၼ်း။** မိူဝ်ႈဢဝ် formula မၼ်းၸႂ်ႉတီႈ T=2116 လႆႈ A = 772,531၊ ၵူၺ်းၵႃႈ update text မၼ်းဝႃႈ 772,521 တႃႇပီမႂ်ႇၼၼ်ႉ။ ႁဝ်းသၢင်ႈ formula တႅတ်ႈတေႃး လႄႈၸႂ်ႉၵူႈဝၼ်းၼၼ်ႉပဵၼ် Gregorian bridge။ README ၶွင်ငဝ်ႈယွမ်းႁပ်ႉဝႃႈ epoch offsets (6,869 လႄႈ 420) ဢမ်ႇမီးတီႈမႃး။

2. **`ME_PI_60` (ၸိုဝ်ႈပီ Ahom 60) မႃးတီႈငဝ်ႈ transliteration ဢၼ်ၵူၼ်းၸႂ်ႉၼမ်** လႄႈမီးၶေႃႈဢမ်ႇညီၵၼ် (မိူၼ် "Dapcheu" ပေႃႇ 2 ပွၵ်ႈ, မၢႆ `*`)။ တႃႇၵၢၼ်ပၢႆးပၺ်ႇၺႃႇ ၶိုၼ်းတၢင်မၼ်းလူၺ်ႈ table Me Pi ၼႂ်း Terwiel & Ranoo (1992), p. 91 (columns Lakni / Kham Mvng / Pi Han / Pi Pan)။

3. **ၶွပ်ႇပီပႅၵ်ႇၵၼ်လူၺ်ႈပိူင်သၢင်ႈ**: Ahom Lak-Ni ပိၼ်ႇတီႈပီမႂ်ႇၵပ်း Sakkaraj; Shan/Great-Dai ပိၼ်ႇႁူဝ် December; လိူၼ် Myanmar ပိၼ်ႇမွၵ်ႈ April (Thingyan)။ ယႃႇတႅၵ်ႈမၢႆ *ပီ* ၶၢမ်ႈပိူင် ဢမ်ႇပိၼ်ႇၵွၼ်ႇ — ၵူၺ်းၵႃႈၸိုဝ်ႈ 60 *ဝၼ်း* တူၵ်းမႅၼ်ႈၵူႈတီႈ (§5)။

4. **ဢမ်ႇၼပ်ႉ ΔT**: Meeus JDE ယူႇၼႂ်း Dynamical Time; လွင်ႈမုၼ်းလုမ်ႈၾႃႉၸိူင်း ~69 s ၼႂ်း 2026 — ဢမ်ႇမီးၽွၼ်းတီႈၸၼ်ႉဝၼ်း လိူဝ်သေ conjunction တူၵ်းၼႂ်းမိၼိတ်ႉၸမ်ၵၢင်ၶိုၼ်း။

5. **ၶေႃႈၾၢင်ႉ element mapping** (§2): ထၢတ်ႈတႆး ≠ stem ၶႄႇတီႈ index လဵဝ်ၵၼ်။ `lak_ni.py` လၢႆးငၢၼ်းထၢတ်ႈတႆးၵူၺ်း။

---

## 10. ၶေႃႈသပ်း

| ၶေႃႈ | ပွင်ႇဝႃႈ |
|---|---|
| **Lak Ni / Lakni** | "ပၵ်းယဵမ်ႈ"; ပိူင် 60 တႆးဢႃႇႁူမ် (ပီ လႄႈ ဝၼ်း) |
| **Lak Jeng** | ပိူင်ၼပ်ႉတင်းမိုဝ်းတႆး တႃႇဝူင်းလဵဝ်ၵၼ် (algorithm D ၼႂ်း repo ၼႆႉ) |
| **Me-Pi / Mae-Pi** | "ပီမႄႈ" — ဝူင်းထၢတ်ႈ 10 (stems) |
| **Look-Pi / Son years** | ဝူင်းတူဝ်သတ်း 12 (branches) |
| **ahargaṇa (A)** | ၼပ်ႉဝၼ်းမိူင်းဢၼ်ပူၼ်ႉမႃးတီႈ epoch (ၶေႃႈပၢႆးလၢဝ်ဢိၼ်းတီးယႃး) |
| **tithi** | 1/30 ၶွင် synodic month; ငဝ်ႈၵၢၼ်ပြင် "ဝၼ်းႁၢႆ" |
| **watat** | ပီထႅမ်လိူၼ်မၢၼ်ႈ; "big watat" ထႅမ်ဝၼ်းထႅင်ႈ |
| **Sakkaraj / CS** | ပီ Chula Sakarat = AD − 638, ၸႂ်ႉၼႂ်း Southeast Asia ပွတ်းလိၼ်လူင် |
| **jdn / JDE** | Julian Day Number (ဝၼ်း integer) / Julian Ephemeris Date (ပႃးယၢမ်း) |
| **Oo/Hnaung Tagu** | Tagu ႁူဝ်/လင် — လိူၼ် Myanmar ဢၼ်ၶၢမ်ႈပီမႂ်ႇ |
| **Thingyan akya/atat** | ယၢမ်းၶွပ်ႇပွႆးပီမႂ်ႇ ၼႂ်းပၵ်းယဵမ်ႈ Myanmar |

---

## 11. ဢိင်ဢၢင်ႈ

**ငဝ်ႈလၵ်းတႃႇ algorithms**

1. Süa Tai Möng, "Method for Calculating the Lak Jeng Cycle" (Shan, 2021) — ပိုၼ်ႉထၢၼ် `lak_jeng.py`; ၵၢၼ်ဝူၼ်ႉၼပ်ႉၼႂ်း README ၶွင် project။
2. Yan Naing Aye, *"Algorithm, Program and Calculation of Myanmar Calendar"*, Cool-Emerald blog (2013) — ၵฎလိူၼ်, constants SY/LM, ပိူင် watat။
   http://cool-emerald.blogspot.com/2013/06/algorithm-program-and-calculation-of.html
3. B. J. Terwiel & Ranoo Wichasin, *Tai Ahoms and the Stars: Three Ritual Texts to Ward off Danger*, Cornell SEAP (1992) — tables Me Pi (Table 4), လိၵ်ႈလၢဝ် Ahom။
4. Stephen Morey et al., *Lakni (Calendar)* manuscript transcription, The Language Archive (MPI Nijmegen) — ပပ်ႉ Ahom Lakni (copy Atul Borgohain)။
   https://archive.mpi.nl/tla/islandora/object/tla%3A1839_00_0000_0000_000D_F950_D
5. Monthip Sirithaikhongchuen, *"Tai Name of the Year and Tai New Year"* (SOAS, 2007) — သဵၼ်ႈ Mother/Son pan-Tai, ၵฎပီမႂ်ႇ။
6. Jean Meeus, *Astronomical Algorithms*, 2nd ed., ch. 49 — series လိူၼ်မႂ်ႇတႄႉ။

**ပိုၼ်း/ပၢႆးလၢဝ်ပိုၼ်ႉလင်**

7. Burgess (trans.), *Sūrya-Siddhānta* — 1,577,917,828 days : 4,320,000 years။ **Chapter I, verses 34–37** မၵ်းမၼ်ႈဝူင်းလၵ်း၊ ဝၼ်းလုမ်ႈၾႃႉ လႄႈပိူင်ဝၼ်းမိူင်း တီႈၵၢင်ဝၼ်းဢွၵ်ႇထိုင်ၵၢင်ဝၼ်းဢွၵ်ႇ:
   https://en.wikisource.org/wiki/Page:English_translation_of_the_Surya_Siddhanta_and_the_Siddhanta_Siromani_by_Sastri,_1861.djvu/16
   ၵွပ်ႈၼၼ် 1,350 လႄႈ 193 ဢမ်ႇမႃးတီႈယၢမ်းၵၢင်ဝၼ်းဢွၵ်ႇၵမ်းသိုဝ်ႈ။ မၼ်းပဵၼ်ပိူင်ပြင် ဢၼ်ႁဵတ်းႁႂ်ႈ `292,207/800` တူၵ်းမႅၼ်ႈတူဝ်တဵမ် Sūrya Siddhānta လီၶိုၼ်ႈ။ ဝၼ်းမိူင်းပိုၼ်ႉထၢၼ် ယင်းမၵ်းမၼ်ႈတီႈၵၢင်ဝၼ်းဢွၵ်ႇထိုင်ၵၢင်ဝၼ်းဢွၵ်ႇ။
8. Sewell & Dikshit, *The Indian Calendar*; Irwin, *The Burmese and Arakanese Calendars* — constants လၵ်း ဢၼ်ပၵ်းယဵမ်ႈ SE Asia ႁပ်ႉၸႂ်ႉ။
9. Lars Gislén, "Burmese Eclipse Calculations", JAHH 18(1) 2015 — ပိူင်တႅမ်ႈ 292207/800။
10. *Sexagenary Cycle — Tai comparative research* (Vietnam/Laos/Thailand/India/China, user-supplied document, Aug 2026) — table stem Ahom kap…ka ၵပ်း 甲乙丙丁…, epoch 4 CE = kap-chai, offset *sok* ထႆး, တႅၵ်ႈၼိူင်းတူဝ်သတ်းတၢင်တႅၼ်း, ၵฎပိၼ်ႇပီ April။ ပဵၼ်ပိုၼ်ႉထၢၼ်တႃႇ table stem 2 ၸုမ်း ၼႂ်း §2 လႄႈ §4 ၶၵ်ႉ 3။

---

*Research build: August 2026။ ၵၢၼ်ၼပ်ႉတင်းမူတ်း ယိုၼ်ယၼ်ယဝ်ႉတီႈ 2026-08-23 (Kut-Sai, လိူၼ်မႂ်ႇ 10)။*
