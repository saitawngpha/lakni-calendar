#include "lakni/calendar.h"

#include <math.h>
#include <stdio.h>
#include <string.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

static const char *const MOTHERS_TAI[] = {
    "Kra (Kha)", "Lup", "Hut (Hot)", "Muang (Mvng)", "Puek",
    "Kut", "Koat (Kwat)", "Hong (Hvng)", "Tao (Thao)", "Ka (Kap)"
};
static const char *const MOTHERS_SHORT[] = {
    "Kra", "Lup", "Hut", "Muang", "Puek", "Kut", "Koat", "Hong", "Tao", "Ka"
};
static const char *const SONS_TAI[] = {
    "Jai (rat)", "Ngok/Pao (ox)", "Khan/Yee (tiger)", "Mao (hare)",
    "Si (naga/dragon)", "Sai (snake)", "Singa/Nga (horse)", "Met (goat)",
    "Saan (monkey)", "Rao/Hao (cock)", "Set/Sed (dog)", "Kai (pig)"
};
static const char *const SONS_SHORT[] = {
    "Jai", "Ngok", "Khan", "Mao", "Si", "Sai", "Singa", "Met", "Saan", "Rao", "Set", "Kai"
};
static const char *const MOTHERS_SHAN_SCRIPT[] = {
    "ၵၢပ်ႇ", "လပ်း", "ႁၢႆး", "မိူင်း", "ပိုၵ်း", "ၵတ်း", "ၶုတ်း", "ႁုင်ႉ", "တဝ်ႇ", "ၵႃႇ"
};
static const char *const CHILDREN_SHAN_SCRIPT[] = {
    "ၸႂ်ႉ", "ပဝ်ႉ", "ယီး", "မဝ်ႉ", "သီ", "သႂ်ႉ", "သီင", "မူတ်ႉ", "သၼ်", "ႁဝ်ႉ", "မဵတ်ႉ", "ၵႂ်ႉ"
};
static const char *const AHOM_LAKNI_MOTHERS[] = {
    "Kap", "Dap", "Rai", "Mung", "Plek", "Kat", "Khut", "Rung", "Tao", "Ka"
};
static const char *const AHOM_LAKNI_CHILDREN[] = {
    "Cheu", "Plao", "Ngi", "Mao", "Shi", "Shiu", "Shinga", "Mut", "San", "Rao", "Mit", "Keu"
};
static const char *const AHOM_MONTHS[] = {
    "Din Ching", "Din Kam", "Din Sham", "Din Shi", "Din Ha", "Din Ruk",
    "Din Chit", "Din Pet", "Din Kao", "Din Ship", "Din Shipit", "Din Shipshang"
};
static const char *const AHOM_STEMS[] = {
    "Kap", "Dap", "Rai", "Mueang", "Plaek", "Kat", "Khut", "Rung", "Tao", "Ka"
};
static const char *const AHOM_STEMS_CHINESE[] = {
    "jia 甲", "yi 乙", "bing 丙", "ding 丁", "wu 戊", "ji 己", "geng 庚", "xin 辛", "ren 壬", "gui 癸"
};
static const char *const ELEMENTS[] = {
    "wood", "wood", "fire", "fire", "earth", "earth", "metal", "metal", "water", "water"
};
static const char *const SHAN_STEMS[] = {
    "Kra/Kap", "Lup/Lap", "Hut/Hai", "Muang/Möng", "Puek/Pök",
    "Kut/Kud", "Koat/Khot", "Hong/Hung", "Tao/Thao", "Ka"
};

static const int64_t DAY_ANCHOR_JDN = 2433191;

static double radians(double degrees) {
    return degrees * M_PI / 180.0;
}

lakni_status lakni_ahom_year_for_cycle(int cycle_year, lakni_ahom_year *result) {
    int index;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    index = (int)lakni_floor_mod((int64_t)cycle_year - 2008, 60);
    result->position = index + 1;
    result->cycle_year = cycle_year;
    snprintf(result->name, sizeof(result->name), "%s %s",
             AHOM_LAKNI_MOTHERS[index % 10], AHOM_LAKNI_CHILDREN[index % 12]);
    return LAKNI_OK;
}

lakni_status lakni_structural_year_for(int ad_year, lakni_structural_year *result) {
    int stem;
    int son;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    stem = (int)lakni_floor_mod((int64_t)ad_year - 4, 10);
    son = (int)lakni_floor_mod((int64_t)ad_year - 4, 12);
    result->cycle_index = (int)lakni_floor_mod((int64_t)ad_year - 4, 60);
    result->stem = AHOM_STEMS[stem];
    result->stem_chinese = AHOM_STEMS_CHINESE[stem];
    result->element = ELEMENTS[stem];
    result->shan_stem = SHAN_STEMS[stem];
    result->son = SONS_TAI[son];
    snprintf(result->name, sizeof(result->name), "%s-%s", AHOM_STEMS[stem], SONS_SHORT[son]);
    return LAKNI_OK;
}

lakni_status lakni_day_cycle_for_jdn(int64_t jdn, lakni_day_cycle *result) {
    int index;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    index = (int)lakni_floor_mod(jdn - DAY_ANCHOR_JDN, 60);
    result->index = index;
    result->mother = MOTHERS_TAI[index % 10];
    result->son = SONS_TAI[index % 12];
    result->mother_shan = MOTHERS_SHAN_SCRIPT[index % 10];
    result->son_shan = CHILDREN_SHAN_SCRIPT[index % 12];
    snprintf(result->name, sizeof(result->name), "%s-%s",
             MOTHERS_SHORT[index % 10], SONS_SHORT[index % 12]);
    snprintf(result->shan, sizeof(result->shan), "%s%s",
             result->mother_shan, result->son_shan);
    return LAKNI_OK;
}

double lakni_true_new_moon_jde(int k) {
    double t = k / 1236.85;
    double t2 = t * t;
    double t3 = t2 * t;
    double t4 = t3 * t;
    double jde = 2451550.09766 + 29.530588861 * k + 0.00015437 * t2
        - 0.000000150 * t3 + 0.00000000073 * t4;
    double e = 1.0 - 0.002516 * t - 0.0000074 * t2;
    double m = radians(2.5534 + 29.10535670 * k - 0.0000014 * t2 - 0.00000011 * t3);
    double mp = radians(201.5643 + 385.81693528 * k + 0.0107582 * t2
                        + 0.00001238 * t3 - 0.000000058 * t4);
    double f = radians(160.7108 + 390.67050284 * k - 0.0016118 * t2
                       - 0.00000227 * t3 + 0.000000011 * t4);
    double o = radians(124.7746 - 1.56375588 * k + 0.0020672 * t2 + 0.00000215 * t3);
    double correction = -0.40720 * sin(mp) + 0.17241 * e * sin(m) + 0.01608 * sin(2 * mp)
        + 0.01039 * sin(2 * f) + 0.00739 * e * sin(mp - m)
        - 0.00514 * e * sin(mp + m) + 0.00208 * e * e * sin(2 * m)
        - 0.00111 * sin(mp - 2 * f) - 0.00057 * sin(mp + 2 * f)
        + 0.00056 * e * sin(2 * mp + m) - 0.00042 * sin(3 * mp)
        + 0.00042 * e * sin(m + 2 * f) + 0.00038 * e * sin(m - 2 * f)
        - 0.00024 * e * sin(2 * mp - m) - 0.00017 * sin(o)
        - 0.00007 * sin(mp + 2 * m) + 0.00004 * sin(2 * mp - 2 * f)
        + 0.00004 * sin(3 * m) + 0.00003 * sin(mp + m - 2 * f)
        + 0.00003 * sin(2 * mp + 2 * f) - 0.00003 * sin(mp + m + 2 * f)
        + 0.00003 * sin(mp - m + 2 * f) - 0.00002 * sin(mp - m - 2 * f)
        - 0.00002 * sin(3 * mp + m) + 0.00002 * sin(4 * mp);
    const double angles[] = {
        299.77 + 0.107408 * k - 0.009173 * t2, 251.88 + 0.016321 * k,
        251.83 + 26.651886 * k, 349.42 + 36.412478 * k,
        84.66 + 18.206239 * k, 141.74 + 53.303771 * k,
        207.14 + 2.453732 * k, 154.84 + 7.306860 * k,
        34.52 + 27.261239 * k, 207.19 + 0.121824 * k,
        291.34 + 1.844379 * k, 161.72 + 24.198154 * k,
        239.56 + 25.513099 * k, 331.55 + 3.592518 * k
    };
    const double coefficients[] = {
        0.000325, 0.000165, 0.000164, 0.000126, 0.000110, 0.000062,
        0.000060, 0.000056, 0.000047, 0.000042, 0.000040, 0.000037,
        0.000035, 0.000023
    };
    size_t i;
    for (i = 0; i < sizeof(angles) / sizeof(angles[0]); i++) {
        correction += coefficients[i] * sin(radians(angles[i]));
    }
    return jde + correction;
}

static lakni_status new_moon_before_or_on(int64_t jdn, double timezone_hours,
                                          int64_t *new_moon_jdn) {
    int k0;
    int k;
    bool found = false;
    int64_t conjunction = 0;
    if (new_moon_jdn == NULL || !isfinite(timezone_hours)) {
        return LAKNI_INVALID_ARGUMENT;
    }
    k0 = (int)nearbyint((jdn - 2451550.09766) / 29.530588861);
    for (k = k0 - 1; k <= k0 + 1; k++) {
        int64_t day = (int64_t)(lakni_true_new_moon_jde(k) + timezone_hours / 24.0 + 0.5);
        if (day <= jdn) {
            conjunction = day;
            found = true;
        }
    }
    if (!found) {
        return LAKNI_CALCULATION_ERROR;
    }
    *new_moon_jdn = conjunction;
    return LAKNI_OK;
}

lakni_status lakni_lunar_phase_for_jdn(int64_t jdn, double timezone_hours,
                                       lakni_lunar_phase *result) {
    int64_t new_moon;
    int64_t delta;
    lakni_status status;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    status = new_moon_before_or_on(jdn, timezone_hours, &new_moon);
    if (status != LAKNI_OK) {
        return status;
    }
    delta = jdn - new_moon;
    result->new_moon_jdn = new_moon;
    result->has_day = true;
    if (delta == 0) {
        result->phase = "new moon day (ends old month)";
        result->day = 0;
        result->has_day = false;
    } else if (delta <= 14) {
        result->phase = "waxing";
        result->day = (int)delta;
    } else if (delta == 15) {
        result->phase = "full moon";
        result->day = 15;
    } else {
        result->phase = "waning";
        result->day = (int)(delta - 15);
    }
    return LAKNI_OK;
}

lakni_status lakni_ahom_dinching_start(int gregorian_year, double timezone_hours,
                                       int64_t *jdn) {
    int64_t november_1;
    int64_t december_1;
    int64_t day;
    if (jdn == NULL || !isfinite(timezone_hours)) {
        return LAKNI_INVALID_ARGUMENT;
    }
    if (lakni_gregorian_to_jdn(gregorian_year, 11, 1, &november_1) != LAKNI_OK
            || lakni_gregorian_to_jdn(gregorian_year, 12, 1, &december_1) != LAKNI_OK) {
        return LAKNI_INVALID_DATE;
    }
    for (day = november_1; day < december_1; day++) {
        int64_t new_moon;
        if (new_moon_before_or_on(day, timezone_hours, &new_moon) == LAKNI_OK
                && new_moon == day) {
            *jdn = day + 1;
            return LAKNI_OK;
        }
    }
    return LAKNI_CALCULATION_ERROR;
}

static lakni_status month_starts(int cycle_year, double timezone_hours,
                                 int64_t starts[13], int *count,
                                 int64_t *next_year_start) {
    int64_t start;
    int64_t end;
    int64_t day;
    int n = 1;
    if (starts == NULL || count == NULL || next_year_start == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    if (lakni_ahom_dinching_start(cycle_year, timezone_hours, &start) != LAKNI_OK
            || lakni_ahom_dinching_start(cycle_year + 1, timezone_hours, &end) != LAKNI_OK) {
        return LAKNI_CALCULATION_ERROR;
    }
    starts[0] = start;
    for (day = start; day < end; day++) {
        int64_t new_moon;
        if (new_moon_before_or_on(day, timezone_hours, &new_moon) == LAKNI_OK
                && new_moon == day && day + 1 < end) {
            if (n >= 13) {
                return LAKNI_CALCULATION_ERROR;
            }
            starts[n++] = day + 1;
        }
    }
    if (n != 12 && n != 13) {
        return LAKNI_CALCULATION_ERROR;
    }
    *count = n;
    *next_year_start = end;
    return LAKNI_OK;
}

lakni_status lakni_ahom_for_date(int year, int month, int day, double timezone_hours,
                                 lakni_ahom_date *result) {
    int64_t jdn;
    int64_t this_start;
    int64_t starts[13];
    int count;
    int cycle_year;
    int month_index = 0;
    int64_t next_start;
    int64_t month_end;
    bool has_leap;
    if (result == NULL || !isfinite(timezone_hours)) {
        return LAKNI_INVALID_ARGUMENT;
    }
    if (lakni_gregorian_to_jdn(year, month, day, &jdn) != LAKNI_OK) {
        return LAKNI_INVALID_DATE;
    }
    if (lakni_ahom_dinching_start(year, timezone_hours, &this_start) != LAKNI_OK) {
        return LAKNI_CALCULATION_ERROR;
    }
    cycle_year = jdn >= this_start ? year : year - 1;
    if (month_starts(cycle_year, timezone_hours, starts, &count, &next_start) != LAKNI_OK) {
        return LAKNI_CALCULATION_ERROR;
    }
    while (month_index + 1 < count && starts[month_index + 1] <= jdn) {
        month_index++;
    }
    has_leap = count == 13;
    result->year_start_jdn = starts[0];
    result->next_year_start_jdn = next_start;
    result->months_in_year = count;
    result->leap_month = has_leap && month_index == 8;
    if (result->leap_month) {
        result->month_number = 8;
        result->month_name = "Leap after Din Pet";
    } else {
        result->month_number = month_index + 1 - (has_leap && month_index > 8 ? 1 : 0);
        result->month_name = AHOM_MONTHS[result->month_number - 1];
    }
    month_end = month_index + 1 < count ? starts[month_index + 1] : next_start;
    result->month_day = (int)(jdn - starts[month_index] + 1);
    result->month_length = (int)(month_end - starts[month_index]);
    return lakni_ahom_year_for_cycle(cycle_year, &result->year);
}

int lakni_ahom_self_test(void) {
    lakni_ahom_year year;
    lakni_ahom_date before;
    lakni_ahom_date after;
    lakni_ahom_date leap;
    lakni_structural_year structural;
    lakni_day_cycle day;
    lakni_lunar_phase phase;
    int64_t jdn;
    int64_t dinching;
    if (lakni_ahom_year_for_cycle(2008, &year) != LAKNI_OK
            || year.position != 1 || strcmp(year.name, "Kap Cheu") != 0) return 1;
    if (lakni_ahom_year_for_cycle(2025, &year) != LAKNI_OK
            || year.position != 18 || strcmp(year.name, "Rung Shiu") != 0) return 2;
    if (lakni_ahom_dinching_start(2025, 5.5, &dinching) != LAKNI_OK
            || lakni_gregorian_to_jdn(2025, 11, 21, &jdn) != LAKNI_OK || dinching != jdn) return 3;
    if (lakni_ahom_for_date(2025, 11, 20, 5.5, &before) != LAKNI_OK
            || lakni_ahom_for_date(2025, 11, 21, 5.5, &after) != LAKNI_OK) return 4;
    if (before.year.cycle_year != 2024 || after.year.cycle_year != 2025
            || strcmp(after.year.name, "Rung Shiu") != 0
            || strcmp(after.month_name, "Din Ching") != 0 || after.month_day != 1) return 5;
    if (lakni_ahom_for_date(2024, 11, 2, 5.5, &leap) != LAKNI_OK
            || leap.months_in_year != 13) return 6;
    if (lakni_structural_year_for(2026, &structural) != LAKNI_OK
            || strcmp(structural.stem, "Rai") != 0 || strcmp(structural.element, "fire") != 0
            || structural.cycle_index != 42) return 7;
    if (lakni_gregorian_to_jdn(1949, 10, 1, &jdn) != LAKNI_OK
            || lakni_day_cycle_for_jdn(jdn, &day) != LAKNI_OK
            || strcmp(day.name, "Kra-Jai") != 0) return 8;
    if (lakni_gregorian_to_jdn(2026, 8, 23, &jdn) != LAKNI_OK
            || lakni_day_cycle_for_jdn(jdn, &day) != LAKNI_OK
            || strcmp(day.name, "Kut-Sai") != 0) return 9;
    if (fabs(lakni_true_new_moon_jde(0) - 2451550.25993) >= 0.001) return 10;
    if (lakni_lunar_phase_for_jdn(jdn, 5.5, &phase) != LAKNI_OK
            || strcmp(phase.phase, "waxing") != 0 || phase.day != 11) return 11;
    return 0;
}
