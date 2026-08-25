#include "lakni/calendar.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    int year;
    int month;
    int day;
    int64_t jdn;
    lakni_ahom_date ahom;
    lakni_day_cycle cycle;
    lakni_structural_year structural;
    lakni_lunar_phase phase;
    lakni_myanmar_date myanmar;
    if (argc == 2 && strcmp(argv[1], "--test") == 0) {
        int result = lakni_ahom_self_test();
        if (result != 0) {
            fprintf(stderr, "Lakni self-test failed at check %d\n", result);
            return 1;
        }
        puts("all self-tests passed (C Lakni port)");
        return 0;
    }
    if (argc != 4) {
        fprintf(stderr, "usage: %s YYYY MM DD | --test\n", argv[0]);
        return 2;
    }
    year = atoi(argv[1]);
    month = atoi(argv[2]);
    day = atoi(argv[3]);
    if (lakni_gregorian_to_jdn(year, month, day, &jdn) != LAKNI_OK
            || lakni_ahom_for_date(year, month, day, 5.5, &ahom) != LAKNI_OK
            || lakni_day_cycle_for_jdn(jdn, &cycle) != LAKNI_OK
            || lakni_structural_year_for(year, &structural) != LAKNI_OK
            || lakni_lunar_phase_for_jdn(jdn, 5.5, &phase) != LAKNI_OK
            || lakni_myanmar_from_jdn(jdn, &myanmar) != LAKNI_OK) {
        fprintf(stderr, "invalid or unsupported date\n");
        return 2;
    }
    printf("Gregorian date : %04d-%02d-%02d\n", year, month, day);
    printf("Ahom Lakni*    : %d/60 %s\n", ahom.year.position, ahom.year.name);
    printf("Ahom month*    : %d %s day %d/%d [%d lunar months]\n",
           ahom.month_number, ahom.month_name, ahom.month_day,
           ahom.month_length, ahom.months_in_year);
    printf("Ganzhi compare : %s = %s %s\n", structural.name,
           structural.element, structural.son);
    printf("Day name       : %s (%d/60)\n", cycle.name, cycle.index);
    printf("Myanmar date   : ME %d %s %s %d\n", myanmar.myanmar_year,
           myanmar.month_name, myanmar.phase, myanmar.fortnight_day);
    printf("Moon estimate  : %s", phase.phase);
    if (phase.has_day) printf(" day %d", phase.day);
    printf("\nJulian Day No. : %lld\n", (long long)jdn);
    puts("* Ahom lunar date is an explicit seasonal/new-moon reconstruction; not a Nadaw conversion.");
    return 0;
}
