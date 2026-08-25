#include "lakni/calendar.h"

#include <string.h>

static const char *const MOTHERS[] = {
    "Kap", "Lap", "Hai", "Mong", "Pok", "Kat", "Khut", "Hung", "Tao", "Ka"
};
static const char *const CHILDREN[] = {
    "Jai", "Pao", "Yi", "Mao", "Si", "Sai", "Singa", "Mot", "San", "Hao", "Met", "Kwai"
};
static const char *const MOTHERS_SHAN[] = {
    "ၵၢပ်ႇ", "လပ်း", "ႁၢႆး", "မိူင်း", "ပိုၵ်း", "ၵတ်း", "ၶုတ်း", "ႁုင်ႉ", "တဝ်ႇ", "ၵႃႇ"
};
static const char *const CHILDREN_SHAN[] = {
    "ၸႂ်ႉ", "ပဝ်ႉ", "ယီး", "မဝ်ႉ", "သီ", "သႂ်ႉ", "သီင", "မူတ်ႉ", "သၼ်", "ႁဝ်ႉ", "မဵတ်ႉ", "ၵႂ်ႉ"
};
static const char *const WEEKDAYS[] = {
    "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
};

enum {
    YEAR_BASE_DAYS = 292207,
    YEAR_DENOM = 800,
    CORR_PERIOD = 1350,
    CORR_UNITS = 7,
    CORR_STEP = 193,
    EPOCH_OFFSET_N = 6869,
    MISSING_MULT = 11,
    MISSING_SUB_DIV = 25,
    MISSING_ADD = 420,
    MISSING_DIV = 692
};

static const int64_t BRIDGE_JDN = 2459554;
static const int64_t BRIDGE_A = 772521;

static int64_t correction(int64_t year) {
    int64_t quotient = lakni_floor_div(year, CORR_PERIOD);
    int64_t remainder = lakni_floor_mod(year, CORR_PERIOD);
    return CORR_UNITS * quotient + lakni_floor_div(remainder, CORR_STEP);
}

static int cycle_index_from_a(int64_t elapsed_days) {
    return (int)lakni_floor_mod(elapsed_days + 2, 60);
}

lakni_status lakni_lak_jeng_calculate(int tai_year, lakni_lak_jeng_result *result) {
    int64_t y;
    int64_t remainder;
    int index;
    int year_mother;
    int year_child;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    memset(result, 0, sizeof(*result));
    y = (int64_t)tai_year - 1;
    result->tai_year = tai_year;
    result->calculation_year = tai_year - 1;
    result->correction = correction(y);
    result->numerator = YEAR_BASE_DAYS * y + result->correction + EPOCH_OFFSET_N;
    result->quotient = lakni_floor_div(result->numerator, YEAR_DENOM);
    remainder = lakni_floor_mod(result->numerator, YEAR_DENOM);
    result->old_position = remainder;
    result->new_position = YEAR_DENOM - remainder;
    result->elapsed_days = result->quotient + (remainder > 0 ? 1 : 0);
    result->missing = MISSING_MULT * result->elapsed_days
        - lakni_floor_div(y, MISSING_SUB_DIV) + MISSING_ADD;
    result->missing_days = lakni_floor_div(result->missing, MISSING_DIV);
    result->missing_position = lakni_floor_mod(result->missing, MISSING_DIV);
    result->lunar_months = lakni_floor_div(result->elapsed_days + result->missing_days, 30);
    result->lunar_month_position = (int)lakni_floor_mod(
        result->elapsed_days + result->missing_days, 30);
    index = cycle_index_from_a(result->elapsed_days);
    result->cycle_index = index;
    result->weekday = WEEKDAYS[lakni_floor_mod(result->elapsed_days, 7)];
    result->mother = MOTHERS[index % 10];
    result->child = CHILDREN[index % 12];
    result->mother_shan = MOTHERS_SHAN[index % 10];
    result->child_shan = CHILDREN_SHAN[index % 12];
    year_mother = (int)lakni_floor_mod(y + 3, 10);
    year_child = (int)lakni_floor_mod(y - 1, 12);
    result->year_mother = MOTHERS[year_mother];
    result->year_child = CHILDREN[year_child];
    return LAKNI_OK;
}

lakni_status lakni_lak_jeng_for_date(int year, int month, int day,
                                     lakni_lak_jeng_date *result) {
    int64_t jdn;
    int64_t this_new_year;
    int index;
    if (result == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    if (lakni_gregorian_to_jdn(year, month, day, &jdn) != LAKNI_OK) {
        return LAKNI_INVALID_DATE;
    }
    memset(result, 0, sizeof(*result));
    result->jdn = jdn;
    result->elapsed_days = BRIDGE_A + jdn - BRIDGE_JDN;
    index = cycle_index_from_a(result->elapsed_days);
    result->cycle_index = index;
    result->weekday = WEEKDAYS[lakni_floor_mod(result->elapsed_days, 7)];
    result->mother = MOTHERS[index % 10];
    result->child = CHILDREN[index % 12];
    result->mother_shan = MOTHERS_SHAN[index % 10];
    result->child_shan = CHILDREN_SHAN[index % 12];
    result->market_day = index % 10 == 2 || index % 10 == 7;
    this_new_year = lakni_tai_lunar_new_year_jdn(year);
    result->tai_year = jdn >= this_new_year ? year + 95 : year + 94;
    if (jdn >= this_new_year) {
        result->previous_new_year_jdn = this_new_year;
        result->next_new_year_jdn = lakni_tai_lunar_new_year_jdn(year + 1);
    } else {
        result->previous_new_year_jdn = lakni_tai_lunar_new_year_jdn(year - 1);
        result->next_new_year_jdn = this_new_year;
    }
    return LAKNI_OK;
}

int lakni_lak_jeng_self_test(void) {
    lakni_lak_jeng_result calculation;
    lakni_lak_jeng_date date;
    int64_t jdn;
    if (lakni_lak_jeng_calculate(2115, &calculation) != LAKNI_OK) return 1;
    if (calculation.calculation_year != 2114 || calculation.correction != 10
            || calculation.numerator != 617732477) return 2;
    if (calculation.quotient != 772165 || calculation.old_position != 477
            || calculation.new_position != 323 || calculation.elapsed_days != 772166) return 3;
    if (calculation.missing != 8494162 || calculation.missing_days != 12274
            || calculation.missing_position != 554) return 4;
    if (calculation.lunar_months != 26148 || calculation.lunar_month_position != 0
            || strcmp(calculation.weekday, "Tuesday") != 0) return 5;
    if (calculation.cycle_index != 28 || strcmp(calculation.mother, "Tao") != 0
            || strcmp(calculation.child, "Si") != 0) return 6;
    if (lakni_lak_jeng_calculate(2116, &calculation) != LAKNI_OK
            || calculation.elapsed_days != 772531) return 7;
    if (lakni_lak_jeng_for_date(2026, 8, 23, &date) != LAKNI_OK
            || date.tai_year != 2120 || date.cycle_index != 5
            || strcmp(date.mother, "Kat") != 0 || strcmp(date.child, "Sai") != 0) return 8;
    if (lakni_gregorian_to_jdn(2025, 11, 20, &jdn) != LAKNI_OK
            || lakni_tai_lunar_new_year_jdn(2025) != jdn) return 9;
    if (lakni_lak_jeng_for_date(2021, 12, 3, &date) != LAKNI_OK || date.tai_year != 2115) return 10;
    if (lakni_lak_jeng_for_date(2021, 12, 4, &date) != LAKNI_OK || date.tai_year != 2116) return 11;
    return 0;
}
