#include "lakni/calendar.h"

#include <math.h>
#include <stddef.h>
#include <string.h>

static const double SY = 1577917828.0 / 4320000.0;
static const double LM = 1577917828.0 / 53433336.0;
static const double MO = 1954168.050623;

static const char *const MYANMAR_MONTHS[] = {
    "First Waso", "Tagu", "Kason", "Nayon", "Waso", "Wagaung",
    "Tawthalin", "Thadingyut", "Tazaungmon", "Nadaw", "Pyatho",
    "Tabodwe", "Tabaung", "Late Tagu", "Late Kason"
};

typedef struct {
    double era;
    double wo;
    int nm;
    bool watat_exception;
} year_constants;

typedef struct {
    double era;
    double ed_raw;
    double ed;
    bool watat;
    bool has_threshold;
    double threshold;
    int64_t waso_full_moon;
} watat_info;

typedef struct {
    int year_type;
    int64_t tagu_1;
    int64_t waso_full_moon;
    bool discrepancy;
} myanmar_year_info;

static bool contains(const int *values, size_t count, int value) {
    size_t i;
    for (i = 0; i < count; i++) {
        if (values[i] == value) {
            return true;
        }
    }
    return false;
}

static int exception_delta(const int (*values)[2], size_t count, int year) {
    size_t i;
    for (i = 0; i < count; i++) {
        if (values[i][0] == year) {
            return values[i][1];
        }
    }
    return 0;
}

static year_constants constants_for(int my) {
    static const int fm3[][2] = {{1377, 1}};
    static const int we3[] = {1344, 1345};
    static const int fm2[][2] = {{1234, 1}, {1261, -1}};
    static const int we2[] = {1263, 1264};
    static const int fm13[][2] = {
        {1120, 1}, {1126, -1}, {1150, 1}, {1172, -1}, {1207, 1}
    };
    static const int we13[] = {1201, 1202};
    static const int fm12[][2] = {
        {813, -1}, {849, -1}, {851, -1}, {854, -1}, {927, -1},
        {933, -1}, {936, -1}, {938, -1}, {949, -1}, {952, -1},
        {963, -1}, {968, -1}, {1039, -1}
    };
    static const int fm11[][2] = {
        {205, 1}, {246, 1}, {471, 1}, {572, -1}, {651, 1},
        {653, 2}, {656, 1}, {672, 1}, {729, 1}, {767, -1}
    };
    year_constants c;
    if (my >= 1312) {
        c = (year_constants){3.0, -0.5, 8, contains(we3, 2, my)};
        c.wo += exception_delta(fm3, 1, my);
    } else if (my >= 1217) {
        c = (year_constants){2.0, -1.0, 4, contains(we2, 2, my)};
        c.wo += exception_delta(fm2, 2, my);
    } else if (my >= 1100) {
        c = (year_constants){1.3, -0.85, -1, contains(we13, 2, my)};
        c.wo += exception_delta(fm13, 5, my);
    } else if (my >= 798) {
        c = (year_constants){1.2, -1.1, -1, false};
        c.wo += exception_delta(fm12, 13, my);
    } else {
        c = (year_constants){1.1, -1.1, -1, false};
        c.wo += exception_delta(fm11, 10, my);
    }
    return c;
}

static double positive_fmod(double value, double divisor) {
    double result = fmod(value, divisor);
    return result < 0.0 ? result + divisor : result;
}

static watat_info is_watat(int my) {
    year_constants c = constants_for(my);
    double ed_raw = positive_fmod(SY * (my + 3739), LM);
    double ta = (12 - c.nm) * (SY / 12.0 - LM);
    double ed = ed_raw < ta ? ed_raw + LM : ed_raw;
    double tw = LM - c.nm * (SY / 12.0 - LM);
    bool watat;
    watat_info result;
    if (c.era >= 2.0) {
        watat = ed >= tw;
    } else {
        watat = lakni_floor_div(lakni_floor_mod((int64_t)my * 7 + 2, 19), 12) == 1;
    }
    if (c.watat_exception) {
        watat = !watat;
    }
    result.era = c.era;
    result.ed_raw = ed_raw;
    result.ed = ed;
    result.watat = watat;
    result.has_threshold = c.era >= 2.0;
    result.threshold = tw;
    result.waso_full_moon = (int64_t)nearbyint(SY * my + MO - ed + 4.5 * LM + c.wo);
    return result;
}

static lakni_status get_year_info(int my, myanmar_year_info *result) {
    watat_info current;
    watat_info previous;
    int distance = 0;
    int64_t remainder;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    current = is_watat(my);
    do {
        distance++;
        previous = is_watat(my - distance);
        if (distance >= 3 && !previous.watat) {
            return LAKNI_CALCULATION_ERROR;
        }
    } while (!previous.watat);
    result->year_type = 0;
    result->waso_full_moon = previous.waso_full_moon + 354 * distance;
    result->discrepancy = false;
    if (current.watat) {
        remainder = lakni_floor_mod(current.waso_full_moon - previous.waso_full_moon, 354);
        result->year_type = (int)(remainder / 31) + 1;
        result->waso_full_moon = current.waso_full_moon;
        result->discrepancy = remainder != 30 && remainder != 31;
    }
    result->tagu_1 = previous.waso_full_moon + 354 * distance - 102;
    return LAKNI_OK;
}

lakni_status lakni_thingyan(int my, lakni_thingyan_dates *result) {
    double festival;
    double ja;
    double jk;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    ja = SY * my + MO;
    festival = my >= 1312 ? 2.169918982 : 2.1675;
    jk = ja - festival;
    result->myanmar_year = my;
    result->ja_jd = nearbyint(ja * 1000000.0) / 1000000.0;
    result->jk_jd = nearbyint(jk * 1000000.0) / 1000000.0;
    result->akya_day = (int64_t)nearbyint(jk);
    result->akyo_day = result->akya_day - 1;
    result->atat_day = (int64_t)nearbyint(ja);
    result->new_year_day = result->atat_day + 1;
    return LAKNI_OK;
}

int lakni_cs_year_for(int year, int month, int day) {
    int candidate = year - 638;
    int64_t jdn;
    lakni_thingyan_dates dates;
    if (lakni_gregorian_to_jdn(year, month, day, &jdn) != LAKNI_OK
            || lakni_thingyan(candidate, &dates) != LAKNI_OK) {
        return 0;
    }
    return jdn >= dates.new_year_day ? candidate : candidate - 1;
}

lakni_status lakni_watat_type(int my, lakni_watat_result *result) {
    watat_info current;
    watat_info previous;
    int prev;
    int64_t remainder;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    current = is_watat(my);
    memset(result, 0, sizeof(*result));
    result->era = current.era;
    result->excess_days_raw = current.ed_raw;
    result->excess_days = current.ed;
    result->watat = current.watat;
    result->has_threshold = current.has_threshold;
    result->threshold = current.threshold;
    if (!current.watat) {
        result->year_length = 354;
        result->type = "common (354)";
        return LAKNI_OK;
    }
    prev = my - 1;
    previous = is_watat(prev);
    while (!previous.watat) {
        prev--;
        previous = is_watat(prev);
    }
    remainder = lakni_floor_mod(current.waso_full_moon - previous.waso_full_moon, 354);
    if (remainder != 30 && remainder != 31) {
        return LAKNI_CALCULATION_ERROR;
    }
    result->has_waso_full_moon = true;
    result->waso_full_moon = current.waso_full_moon;
    result->previous_watat_year = prev;
    result->year_length = remainder == 31 ? 385 : 384;
    result->type = remainder == 31 ? "big watat (385)" : "little watat (384)";
    return LAKNI_OK;
}

lakni_status lakni_myanmar_from_jdn(int64_t jdn, lakni_myanmar_date *result) {
    int my;
    myanmar_year_info info;
    int64_t day_count;
    int big;
    int common;
    int year_length;
    int late;
    int threshold;
    int month;
    int e;
    int f;
    int month_day;
    int month_length;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    my = (int)floor((jdn - 0.5 - MO) / SY);
    if (get_year_info(my, &info) != LAKNI_OK) {
        return LAKNI_CALCULATION_ERROR;
    }
    day_count = jdn - info.tagu_1 + 1;
    big = info.year_type / 2;
    common = 1 / (info.year_type + 1);
    year_length = 354 + (1 - common) * 30 + big;
    late = (int)lakni_floor_div(day_count - 1, year_length);
    day_count -= (int64_t)late * year_length;
    threshold = (int)lakni_floor_div(day_count + 423, 512);
    month = (int)floor((day_count - big * threshold + common * threshold * 30 + 29.26) / 29.544);
    e = (month + 12) / 16;
    f = (month + 11) / 16;
    month_day = (int)day_count - (int)(29.544 * month - 29.26)
        - big * e + common * f * 30;
    month += f * 3 - e * 4 + 12 * late;
    if (month < 0 || month > 14) {
        return LAKNI_CALCULATION_ERROR;
    }
    month_length = 30 - month % 2 + (month == 3 ? info.year_type / 2 : 0);
    result->myanmar_year = my;
    result->year_type = info.year_type;
    result->month = month;
    result->month_name = MYANMAR_MONTHS[month];
    result->month_day = month_day;
    result->month_length = month_length;
    if (month_day == 15) {
        result->phase = "full moon";
        result->fortnight_day = 15;
    } else if (month_day == month_length) {
        result->phase = "new moon";
        result->fortnight_day = 15;
    } else if (month_day < 15) {
        result->phase = "waxing";
        result->fortnight_day = month_day;
    } else {
        result->phase = "waning";
        result->fortnight_day = month_day - 15;
    }
    return LAKNI_OK;
}

lakni_status lakni_myanmar_to_jdn(const lakni_myanmar_date *date, int64_t *jdn) {
    myanmar_year_info info;
    int late;
    int month;
    int big;
    int common;
    int64_t day_count;
    int year_length;
    if (date == NULL || jdn == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    if (date->month < 0 || date->month > 14 || date->month_day < 1 || date->month_day > 31) {
        return LAKNI_INVALID_DATE;
    }
    if (get_year_info(date->myanmar_year, &info) != LAKNI_OK) {
        return LAKNI_CALCULATION_ERROR;
    }
    late = date->month / 13;
    month = date->month % 13 + late;
    big = info.year_type / 2;
    common = 1 - (info.year_type + 1) / 2;
    month += 4 - ((month + 15) / 16) * 4 + (month + 12) / 16;
    day_count = date->month_day + (int)(29.544 * month - 29.26)
        - common * ((month + 11) / 16) * 30 + big * ((month + 12) / 16);
    year_length = 354 + (1 - common) * 30 + big;
    *jdn = day_count + (int64_t)late * year_length + info.tagu_1 - 1;
    return LAKNI_OK;
}

int64_t lakni_tai_lunar_new_year_jdn(int gregorian_year) {
    lakni_myanmar_date date;
    int64_t jdn = 0;
    memset(&date, 0, sizeof(date));
    date.myanmar_year = gregorian_year - 638;
    date.month = 9;
    date.month_day = 1;
    if (lakni_myanmar_to_jdn(&date, &jdn) != LAKNI_OK) {
        return 0;
    }
    return jdn;
}

lakni_status lakni_thai_new_year_integers(int cs, lakni_thai_integers *result) {
    int64_t value;
    int64_t quotient;
    int64_t remainder;
    int64_t avoman;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    value = (int64_t)cs * 292207 + 373;
    quotient = lakni_floor_div(value, 800);
    remainder = lakni_floor_mod(value, 800);
    result->ahargana = quotient + 1;
    result->remainder = (int)remainder;
    result->kammacabala = 800 - (int)remainder;
    result->solar_leap = result->kammacabala <= 207;
    avoman = lakni_floor_mod(result->ahargana * 11 + 650, 692);
    result->avoman = avoman == 0 ? 692 : (int)avoman;
    return LAKNI_OK;
}

int lakni_sakkaraj_self_test(void) {
    int64_t jdn;
    lakni_gregorian_date gregorian;
    lakni_thingyan_dates thingyan;
    lakni_watat_result watat;
    lakni_myanmar_date myanmar;
    lakni_thai_integers thai;
    static const int exception_years[][2] = {
        {1263, 385}, {1264, 354}, {1344, 384}, {1345, 354}, {1377, 385}
    };
    static const int round_trips[][3] = {
        {205, 4, 15}, {813, 9, 1}, {1120, 4, 15},
        {1263, 0, 1}, {1344, 9, 1}, {1387, 9, 1}
    };
    size_t i;
    if (lakni_gregorian_to_jdn(2000, 1, 1, &jdn) != LAKNI_OK || jdn != 2451545) return 1;
    if (lakni_jdn_to_gregorian(jdn, &gregorian) != LAKNI_OK
            || gregorian.year != 2000 || gregorian.month != 1 || gregorian.day != 1) return 2;
    if (lakni_thingyan(1375, &thingyan) != LAKNI_OK
            || fabs(thingyan.ja_jd - 2456398.8407875) >= 1e-4) return 3;
    if (lakni_watat_type(1374, &watat) != LAKNI_OK || !watat.watat
            || watat.waso_full_moon != 2456142 || watat.year_length != 384) return 4;
    if (lakni_watat_type(1377, &watat) != LAKNI_OK
            || watat.waso_full_moon != 2457235 || watat.year_length != 385) return 5;
    if (lakni_gregorian_to_jdn(2025, 11, 20, &jdn) != LAKNI_OK
            || lakni_myanmar_from_jdn(jdn, &myanmar) != LAKNI_OK
            || myanmar.myanmar_year != 1387 || myanmar.month != 9 || myanmar.month_day != 1) return 6;
    if (lakni_myanmar_to_jdn(&myanmar, &jdn) != LAKNI_OK || jdn != 2461000) return 7;
    if (lakni_thai_new_year_integers(1238, &thai) != LAKNI_OK
            || thai.ahargana != 452191 || thai.kammacabala != 161
            || !thai.solar_leap || thai.avoman != 655) return 8;
    if (lakni_thai_new_year_integers(856, &thai) != LAKNI_OK || thai.avoman != 692) return 9;
    if (lakni_cs_year_for(2015, 4, 16) != 1376 || lakni_cs_year_for(2015, 4, 17) != 1377) return 10;
    for (i = 0; i < sizeof(exception_years) / sizeof(exception_years[0]); i++) {
        if (lakni_watat_type(exception_years[i][0], &watat) != LAKNI_OK
                || watat.year_length != exception_years[i][1]) return 11;
    }
    for (i = 0; i < sizeof(round_trips) / sizeof(round_trips[0]); i++) {
        lakni_myanmar_date input;
        memset(&input, 0, sizeof(input));
        input.myanmar_year = round_trips[i][0];
        input.month = round_trips[i][1];
        input.month_day = round_trips[i][2];
        if (lakni_myanmar_to_jdn(&input, &jdn) != LAKNI_OK
                || lakni_myanmar_from_jdn(jdn, &myanmar) != LAKNI_OK
                || myanmar.myanmar_year != input.myanmar_year
                || myanmar.month != input.month
                || myanmar.month_day != input.month_day) return 12;
    }
    return 0;
}
