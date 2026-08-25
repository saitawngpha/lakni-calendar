#include "lakni/calendar.h"

#include <limits.h>

int64_t lakni_floor_div(int64_t value, int64_t divisor) {
    int64_t quotient = value / divisor;
    int64_t remainder = value % divisor;
    if (remainder != 0 && ((remainder < 0) != (divisor < 0))) {
        quotient--;
    }
    return quotient;
}

int64_t lakni_floor_mod(int64_t value, int64_t divisor) {
    return value - lakni_floor_div(value, divisor) * divisor;
}

static bool is_leap_year(int year) {
    return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
}

static bool valid_date(int year, int month, int day) {
    static const int lengths[] = {0, 31, 28, 31, 30, 31, 30,
                                  31, 31, 30, 31, 30, 31};
    int limit;
    if (year < -4799 || month < 1 || month > 12) {
        return false;
    }
    limit = lengths[month] + (month == 2 && is_leap_year(year));
    return day >= 1 && day <= limit;
}

lakni_status lakni_gregorian_to_jdn(int year, int month, int day, int64_t *jdn) {
    int64_t a;
    int64_t y;
    int64_t m;
    if (jdn == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    if (!valid_date(year, month, day)) {
        return LAKNI_INVALID_DATE;
    }
    a = lakni_floor_div(14 - month, 12);
    y = (int64_t)year + 4800 - a;
    m = month + 12 * a - 3;
    *jdn = day + lakni_floor_div(153 * m + 2, 5) + 365 * y
        + lakni_floor_div(y, 4) - lakni_floor_div(y, 100)
        + lakni_floor_div(y, 400) - 32045;
    return LAKNI_OK;
}

lakni_status lakni_jdn_to_gregorian(int64_t jdn, lakni_gregorian_date *date) {
    int64_t j;
    int64_t y;
    int64_t d;
    int64_t m;
    if (date == NULL) {
        return LAKNI_INVALID_ARGUMENT;
    }
    j = jdn - 1721119;
    y = lakni_floor_div(4 * j - 1, 146097);
    j = 4 * j - 1 - 146097 * y;
    d = lakni_floor_div(j, 4);
    j = lakni_floor_div(4 * d + 3, 1461);
    d = 4 * d + 3 - 1461 * j;
    d = lakni_floor_div(d + 4, 4);
    m = lakni_floor_div(5 * d - 3, 153);
    d = 5 * d - 3 - 153 * m;
    d = lakni_floor_div(d + 5, 5);
    y = 100 * y + j;
    if (m < 10) {
        m += 3;
    } else {
        m -= 9;
        y += 1;
    }
    if (y < INT_MIN || y > INT_MAX) {
        return LAKNI_CALCULATION_ERROR;
    }
    date->year = (int)y;
    date->month = (int)m;
    date->day = (int)d;
    return LAKNI_OK;
}
