#include "lakni/calendar.h"

#include <stdio.h>

int main(void) {
    int result;
    result = lakni_sakkaraj_self_test();
    if (result != 0) {
        fprintf(stderr, "Sakkaraj test failed at check %d\n", result);
        return 1;
    }
    result = lakni_lak_jeng_self_test();
    if (result != 0) {
        fprintf(stderr, "Lak Jeng test failed at check %d\n", result);
        return 1;
    }
    result = lakni_ahom_self_test();
    if (result != 0) {
        fprintf(stderr, "Lakni test failed at check %d\n", result);
        return 1;
    }
    puts("all C calendar tests passed");
    return 0;
}
