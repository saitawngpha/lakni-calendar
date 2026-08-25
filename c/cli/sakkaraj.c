#include "lakni/calendar.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int report_year(int year) {
    lakni_thingyan_dates thingyan;
    lakni_watat_result watat;
    lakni_thai_integers thai;
    if (lakni_thingyan(year, &thingyan) != LAKNI_OK
            || lakni_watat_type(year, &watat) != LAKNI_OK
            || lakni_thai_new_year_integers(year, &thai) != LAKNI_OK) {
        fprintf(stderr, "calculation failed\n");
        return 1;
    }
    printf("CS/Myanmar year : %d\n", year);
    printf("New Year (atat) : JD %.6f\n", thingyan.ja_jd);
    printf("Akya (festival) : JD %.6f\n", thingyan.jk_jd);
    printf("Year type       : %s\n", watat.type);
    if (watat.has_waso_full_moon) {
        printf("2nd Waso FM     : JDN %lld\n", (long long)watat.waso_full_moon);
    }
    printf("Thai integers   : h0=%lld kammacabala=%d solar_leap=%s avoman=%d\n",
           (long long)thai.ahargana, thai.kammacabala,
           thai.solar_leap ? "true" : "false", thai.avoman);
    return 0;
}

int main(int argc, char **argv) {
    int year;
    int month;
    int day;
    int64_t jdn;
    lakni_myanmar_date myanmar;
    if (argc == 2 && strcmp(argv[1], "--test") == 0) {
        int result = lakni_sakkaraj_self_test();
        if (result != 0) {
            fprintf(stderr, "Sakkaraj self-test failed at check %d\n", result);
            return 1;
        }
        puts("all self-tests passed (C Sakkaraj port)");
        return 0;
    }
    if (argc == 3 && strcmp(argv[1], "--year") == 0) {
        return report_year(atoi(argv[2]));
    }
    if (argc != 4) {
        fprintf(stderr, "usage: %s YYYY MM DD | --year MY | --test\n", argv[0]);
        return 2;
    }
    year = atoi(argv[1]);
    month = atoi(argv[2]);
    day = atoi(argv[3]);
    if (lakni_gregorian_to_jdn(year, month, day, &jdn) != LAKNI_OK
            || lakni_myanmar_from_jdn(jdn, &myanmar) != LAKNI_OK) {
        fprintf(stderr, "invalid or unsupported date\n");
        return 2;
    }
    printf("Gregorian      : %04d-%02d-%02d\n", year, month, day);
    printf("Julian Day No. : %lld\n", (long long)jdn);
    printf("Sakkaraj (CS)  : %d\n", lakni_cs_year_for(year, month, day));
    printf("Myanmar date   : ME %d %s %s %d\n", myanmar.myanmar_year,
           myanmar.month_name, myanmar.phase, myanmar.fortnight_day);
    return 0;
}
