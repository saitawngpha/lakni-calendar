# သက္ကရာဇ်ခေတ် — အသေးစိတ်သုတေသနမှတ်စု

> ⚠️ ဘာသာပြန်ကို community review လုပ်ရန် လိုသေးသည်။ ပြင်ဆင်ထားသော Myanmar
> calculation era ငါးမျိုးနှင့် exception table များအတွက် အင်္ဂလိပ် `README.md`
> နှင့် Python tests ကို အဓိကကိုးကားပါ။

`lak_ni.py` / `lak_jeng.py` အတွက် ပူးတွဲမှတ်စု။ အရှေ့တောင်အာရှကုန်းမကြီး၏ အဓိကအချိန်စနစ်ဖြစ်သော **Chula Sakarat** (သက္ကရာဇ်၊ จุลศักราช) ကို ရှင်းပြသည်။ implementation မှာ **`sakkaraj.py`** ဖြစ်သည်။

## 1. သက္ကရာဇ်မိသားစု

| ခေတ် | epoch | သုညမှတ်ရက် | မှတ်ချက် |
|---|---|---|---|
| **Anjanasakaraj** | King Anjana | 10 March **691 BCE** | ဗုဒ္ဓမတိုင်မီရက်များအတွက် |
| **Buddha Sakaraj** | Parinibbāna | 11–13 May **544 BCE** | BE = CS + 1182; Thailand 1 လျော့ |
| **Mahāsakaraj / Śaka** | Kaṇiṣka/Ujjain | 17 March **78 CE** | အိန္ဒိယ Śaka ခေတ် |
| **Cula Sakarat (CS)** | Popphausawraḥan | 22 March **638 CE** | 78 + 560 = 638 |
| Mohnyin era | Mohnyin thado minsaw | 18 March **1436** | ဒေသသုံး၊ သက်တမ်းတို |
| Magi-San | CS နှင့် epoch တူ | 22 March 638 | Chittagong အမည် |

ရာဇဝင်စဉ်မှာ Buddha Śāsanā → 621/622 တွင်ဖျက် → **Mahāsakaraj** → 559/560 တွင်ဖျက် → **Cula Sakarat**, 638 CE ဖြစ်သည်။ CS သည် **လွန်ပြီးသောနှစ်များ** ကိုရေတွက်သောကြောင့် epoch နှစ်မှာ 0 ဖြစ်သည်။ April 1999 – April 2000 = CS 1361။

## 2. နက္ခတ္တဗေဒအင်ဂျင်

### 2.1 Constants

| Constant | တန်ဖိုး | အဓိပ္ပါယ် |
|---|---|---|
| `SY` | 1577917828 / 4320000 = **365.2587564815 d** | mean sidereal year |
| `SY₀` | 292207 / 800 = **365.25875 d** | Makaranta အတိုကောက် |
| `LM` | 1577917828 / 53433336 = **29.53058795 d** | mean synodic month |
| tithi ratio | **703 : 692** | month = 30×692/703 |
| `MO` | JD **1954168.050623** | မြန်မာနှစ် 0 အစ |
| excess/year | **10.8917011 d** | ဝါထပ်တွက်ချက်မှုကို မောင်းနှင်သည် |

19 နှစ် × 235 လ × 30 tithis = 7050 tithis = 6939.687055 solar days။ lunar wheel နှင့် sidereal solar wheel ကွာခြားမှု (~12 ရက် at ME 1100) သည် သက္ကရာဇ်သမိုင်း၏ အဓိကပြဿနာဖြစ်သည်။

### 2.2 မြန်မာတွက်ချက်ခေတ် 3 ခု

| ခေတ် | ကာလ | ဝါထပ်စည်းမျဉ်း |
|---|---|---|
| **Makaranta** | to 1853 CE (ME < 1215) | 19 နှစ်စက်ဝန်း၏ **2, 5, 7, 10, 13, 15, 18** |
| **Thandeikta** | 1853–1950 | excess-day threshold, 4 လ window |
| **Current** | 1950– | 8 လ window |

ဝါထပ်လမှာ အမြဲ Waso မတိုင်မီ **First Waso** 30 ရက်ဖြစ်သည်။ ရက်ငင်ကို ဝါထပ်နှစ်တွင်သာ Nayon ၏ **ဒုတိယရက်** အဖြစ်ထည့်သည်။

### 2.3 လက်ရှိ watat algorithm

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
previous watat နှင့် diff mod 354:
30 → little watat (384 ရက်)
31 → big watat (385 ရက်, Nayon 30)
```

နှစ်အရှည်များမှာ 354, 384, 385 ဖြစ်သည်။ **Thingyan** တွင် `ja` သည် အတက်၊ `ja − 2.1699…d` သည် အကြတ်စချိန်ဖြစ်ပြီး အတက်နောက်တစ်ရက်သာ နှစ်ဆန်း 1 ရက်ဖြစ်သည်။

### 2.4 အနာဂတ်အတွက် canonical မရှိခြင်း

ပြုပြင်မှုတိုင်းက Metonic pattern ကို ad hoc ရွှေ့ထားသဖြင့် ထုတ်ဝေဇယားများကျော်လွန်သော အနာဂတ်မြန်မာရက်များတွင် စည်းနှောင်သည့်အာဏာမရှိပါ။ Advisory Board က နှစ်စဉ်သတ်မှတ်သည်။

## 3. ဒေသကွဲများ

| ဒေသ | ပထမလနံပါတ် |
|---|---|
| Kengtung | Tazaungmon |
| Lan Na | Thadingyut = လ 1 |
| Western Shan / Central Thailand | Thadingyut = လ 11 |
| Lan Xang, Sukhothai | Nadaw |

ညတစ်ညတည်းကို Kengtung တွင် “လ 12 လဆုတ် 1”၊ Bangkok တွင် “လ 11 လဆုတ် 1”၊ Chiengmai တွင် “လ 1 လဆုတ် 1” ဟုခေါ်နိုင်သည်။

### Siam ရက်ငင်

မြန်မာသည် big-watat 385 ထဲတွင် ရက်ငင်ထည့်သော်လည်း Siam က ရိုးရိုးနှစ် 355 ထဲသို့ရွှေ့သည်။ ထို့ကြောင့် {354, 355, 384} နှင့် {354, 384, 385} ဟူ၍ကွဲသော်လည်း 19 နှစ်စုစုပေါင်းတူသည်။

### La Loubère / avoman နည်း

```
q, R = divmod(292207·CS_year + 373, 800)
h₀ = q + 1
k  = 800 − R
a₀ = (h₀·11 + 650) mod 692
```

- solar leap ⇔ k ≤ 207
- leap day ⇔ a₀ ≤ 137၊ solar leap တွင် a₀ ≤ 126
- civil day တစ်ရက်လျှင် a₀ ကို 11 (mod 692) တိုးသည်

CS **1238** → h₀ = 452,191; k = 161; a₀ = 655။

```
CS = AD − 638
BE = CS + 1182; Thailand = CS + 1181
MS/Śaka = AD − 78
Anjana = AD + 691
```

## 4. တိုင်လူမျိုးများနှင့် Sakkaraj

- Ahom Buranji များသည် **Lak-Ni အမည် + Sakkaraj နှစ်** ဖြင့် နှစ်ထပ်ရက်စွဲရေးသည်။
- Shan/Khün မှတ်တမ်းများသည် တိရစ္ဆာန်အမည် + CS + လ + လဆန်း/လဆုတ် + ရက် ကိုသုံးသည်။
- Sipsongpanna Great-Dai/Shan epoch 95 BCE သည် သီးခြားဖြစ်ပြီး Small-Dai သည် CS epoch 638 နှင့်တူသည်။

## 5. စစ်ဆေး anchor များ

| အချက် | ရလဒ် |
|---|---|
| ME 1375 = JD 2456398.8408 = 2013-04-16 08:10 | pass |
| ME 1374 excess = 24.1094385; watat | pass |
| 2nd Waso ME 1374 = 2012-08-02 | pass |
| ME 1374 little watat | pass |
| CS 1238: h₀=452191, k=161, a₀=655 | pass |
| CS 1341 at 1980-03-31; CS 1342 around Apr 15 | pass |
| Thingyan 2.169918982 d at ME ≥ 1312 | pass |

## 6. ကိုးကားချက်များ

1. Y. N. Aye, *Algorithm, Program and Calculation of Myanmar Calendar* (2013)။
2. J. C. Eade / L. Gislén, *The Calendars of Southeast Asia*။
3. A. M. B. Irwin, *The Burmese & Arakanese Calendars* (1909)။
4. Sao Saimong Mangrai, “Cula Sakaraja and the Sixty Cyclical Year Names” (1981)။
5. *Burmese calendar*, Wikipedia။
6. Burgess (trans.), *Sūrya Siddhānta*, ch. I vv. 34–37။
