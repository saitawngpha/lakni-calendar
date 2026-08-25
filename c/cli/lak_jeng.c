#include "lakni/calendar.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--test") == 0) {
        int result = lakni_lak_jeng_self_test();
        if (result != 0) {
            fprintf(stderr, "Lak Jeng self-test failed at check %d\n", result);
            return 1;
        }
        puts("all self-tests passed (C Lak Jeng port)");
        return 0;
    }
    if (argc == 5 && strcmp(argv[1], "--date") == 0) {
        lakni_lak_jeng_date date;
        int year = atoi(argv[2]);
        int month = atoi(argv[3]);
        int day = atoi(argv[4]);
        if (lakni_lak_jeng_for_date(year, month, day, &date) != LAKNI_OK) {
            fprintf(stderr, "invalid or unsupported date\n");
            return 2;
        }
        printf("Gregorian       : %04d-%02d-%02d (%s)\n", year, month, day, date.weekday);
        printf("Tai (Shan) year : %d\n", date.tai_year);
        printf("elapsed days A  : %lld\n", (long long)date.elapsed_days);
        printf("day cycle       : %s %s / %s%s (index %d/60)\n",
               date.mother, date.child, date.mother_shan, date.child_shan, date.cycle_index);
        printf("market day      : %s\n", date.market_day ? "yes" : "no");
        return 0;
    }
    if (argc == 2) {
        lakni_lak_jeng_result result;
        int tai_year = atoi(argv[1]);
        if (lakni_lak_jeng_calculate(tai_year, &result) != LAKNI_OK) {
            fprintf(stderr, "calculation failed\n");
            return 1;
        }
        printf("Lak Jeng calculation for Tai Year %d\n", result.tai_year);
        printf("  calculation year Y   : %d\n", result.calculation_year);
        printf("  correction C         : %lld\n", (long long)result.correction);
        printf("  numerator N          : %lld\n", (long long)result.numerator);
        printf("  elapsed days A       : %lld\n", (long long)result.elapsed_days);
        printf("  missing M            : %lld -> D=%lld P=%lld\n",
               (long long)result.missing, (long long)result.missing_days,
               (long long)result.missing_position);
        printf("  day cycle            : %s %s / %s%s (index %d/60)\n",
               result.mother, result.child, result.mother_shan,
               result.child_shan, result.cycle_index);
        return 0;
    }
    fprintf(stderr, "usage: %s TAI_YEAR | --date YYYY MM DD | --test\n", argv[0]);
    return 2;
}
