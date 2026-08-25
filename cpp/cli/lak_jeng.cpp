#include "lakni/lak_jeng.hpp"
#include "lakni/calendar.h"

#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc == 2 && std::string{argv[1]} == "--test") {
        const int result = lakni_lak_jeng_self_test();
        if (result != 0) {
            std::cerr << "Lak Jeng self-test failed at check " << result << '\n';
            return 1;
        }
        std::cout << "all self-tests passed (C++ Lak Jeng API)\n";
        return 0;
    }
    try {
        if (argc == 5 && std::string{argv[1]} == "--date") {
            const int year = std::stoi(argv[2]);
            const int month = std::stoi(argv[3]);
            const int day = std::stoi(argv[4]);
            const auto date = lakni::jeng::forDate(year, month, day);
            std::cout << "Gregorian       : " << year << '-' << month << '-' << day
                      << " (" << date.weekday << ")\n"
                      << "Tai (Shan) year : " << date.taiYear << '\n'
                      << "elapsed days A  : " << date.elapsedDays << '\n'
                      << "day cycle       : " << date.mother << ' ' << date.child << " / "
                      << date.motherShan << date.childShan << " (index "
                      << date.cycleIndex << "/60)\n"
                      << "market day      : " << (date.marketDay ? "yes" : "no") << '\n';
            return 0;
        }
        if (argc == 2) {
            const auto value = lakni::jeng::calculate(std::stoi(argv[1]));
            std::cout << "Lak Jeng calculation for Tai Year " << value.taiYear << '\n'
                      << "  calculation year Y   : " << value.calculationYear << '\n'
                      << "  correction C         : " << value.correction << '\n'
                      << "  numerator N          : " << value.numerator << '\n'
                      << "  elapsed days A       : " << value.elapsedDays << '\n'
                      << "  missing M            : " << value.missing << " -> D="
                      << value.missingDays << " P=" << value.missingPosition << '\n'
                      << "  day cycle            : " << value.mother << ' ' << value.child
                      << " / " << value.motherShan << value.childShan << " (index "
                      << value.cycleIndex << "/60)\n";
            return 0;
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
    std::cerr << "usage: " << argv[0] << " TAI_YEAR | --date YYYY MM DD | --test\n";
    return 2;
}
