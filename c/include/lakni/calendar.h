#ifndef LAKNI_CALENDAR_H
#define LAKNI_CALENDAR_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    LAKNI_OK = 0,
    LAKNI_INVALID_ARGUMENT = 1,
    LAKNI_INVALID_DATE = 2,
    LAKNI_CALCULATION_ERROR = 3
} lakni_status;

typedef struct {
    int year;
    int month;
    int day;
} lakni_gregorian_date;

typedef struct {
    int myanmar_year;
    double ja_jd;
    double jk_jd;
    int64_t akyo_day;
    int64_t akya_day;
    int64_t atat_day;
    int64_t new_year_day;
} lakni_thingyan_dates;

typedef struct {
    double era;
    double excess_days_raw;
    double excess_days;
    bool watat;
    bool has_threshold;
    double threshold;
    bool has_waso_full_moon;
    int64_t waso_full_moon;
    int previous_watat_year;
    int year_length;
    const char *type;
} lakni_watat_result;

typedef struct {
    int myanmar_year;
    int year_type;
    int month;
    const char *month_name;
    int month_day;
    int month_length;
    const char *phase;
    int fortnight_day;
} lakni_myanmar_date;

typedef struct {
    int64_t ahargana;
    int remainder;
    int kammacabala;
    bool solar_leap;
    int avoman;
} lakni_thai_integers;

typedef struct {
    int tai_year;
    int calculation_year;
    int64_t correction;
    int64_t numerator;
    int64_t quotient;
    int64_t old_position;
    int64_t new_position;
    int64_t elapsed_days;
    int64_t missing;
    int64_t missing_days;
    int64_t missing_position;
    int64_t lunar_months;
    int lunar_month_position;
    int cycle_index;
    const char *weekday;
    const char *mother;
    const char *child;
    const char *mother_shan;
    const char *child_shan;
    const char *year_mother;
    const char *year_child;
} lakni_lak_jeng_result;

typedef struct {
    int tai_year;
    int64_t jdn;
    int64_t elapsed_days;
    int cycle_index;
    const char *weekday;
    const char *mother;
    const char *child;
    const char *mother_shan;
    const char *child_shan;
    bool market_day;
    int64_t previous_new_year_jdn;
    int64_t next_new_year_jdn;
} lakni_lak_jeng_date;

typedef struct {
    int position;
    int cycle_year;
    char name[32];
} lakni_ahom_year;

typedef struct {
    int cycle_index;
    const char *stem;
    const char *stem_chinese;
    const char *element;
    const char *shan_stem;
    const char *son;
    char name[48];
} lakni_structural_year;

typedef struct {
    int index;
    const char *mother;
    const char *son;
    const char *mother_shan;
    const char *son_shan;
    char name[48];
    char shan[64];
} lakni_day_cycle;

typedef struct {
    const char *phase;
    int day;
    bool has_day;
    int64_t new_moon_jdn;
} lakni_lunar_phase;

typedef struct {
    lakni_ahom_year year;
    int64_t year_start_jdn;
    int64_t next_year_start_jdn;
    int month_number;
    const char *month_name;
    int month_day;
    int month_length;
    bool leap_month;
    int months_in_year;
} lakni_ahom_date;

int64_t lakni_floor_div(int64_t value, int64_t divisor);
int64_t lakni_floor_mod(int64_t value, int64_t divisor);
lakni_status lakni_gregorian_to_jdn(int year, int month, int day, int64_t *jdn);
lakni_status lakni_jdn_to_gregorian(int64_t jdn, lakni_gregorian_date *date);

int lakni_cs_year_for(int year, int month, int day);
lakni_status lakni_thingyan(int myanmar_year, lakni_thingyan_dates *result);
lakni_status lakni_watat_type(int myanmar_year, lakni_watat_result *result);
lakni_status lakni_myanmar_from_jdn(int64_t jdn, lakni_myanmar_date *result);
lakni_status lakni_myanmar_to_jdn(const lakni_myanmar_date *date, int64_t *jdn);
int64_t lakni_tai_lunar_new_year_jdn(int gregorian_year);
lakni_status lakni_thai_new_year_integers(int cs_year, lakni_thai_integers *result);

lakni_status lakni_lak_jeng_calculate(int tai_year, lakni_lak_jeng_result *result);
lakni_status lakni_lak_jeng_for_date(int year, int month, int day,
                                     lakni_lak_jeng_date *result);

lakni_status lakni_ahom_year_for_cycle(int cycle_year, lakni_ahom_year *result);
lakni_status lakni_structural_year_for(int ad_year, lakni_structural_year *result);
lakni_status lakni_day_cycle_for_jdn(int64_t jdn, lakni_day_cycle *result);
double lakni_true_new_moon_jde(int lunation);
lakni_status lakni_lunar_phase_for_jdn(int64_t jdn, double timezone_hours,
                                       lakni_lunar_phase *result);
lakni_status lakni_ahom_dinching_start(int gregorian_year, double timezone_hours,
                                       int64_t *jdn);
lakni_status lakni_ahom_for_date(int year, int month, int day, double timezone_hours,
                                 lakni_ahom_date *result);

int lakni_sakkaraj_self_test(void);
int lakni_lak_jeng_self_test(void);
int lakni_ahom_self_test(void);

#ifdef __cplusplus
}
#endif

#endif
