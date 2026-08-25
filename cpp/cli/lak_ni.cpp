#include "lakni/lak_ni.hpp"
#include "lakni/sakkaraj.hpp"
#include "lakni/calendar.h"

#include <cstdlib>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc == 2 && std::string{argv[1]} == "--test") {
        const int result = lakni_ahom_self_test();
        if (result != 0) {
            std::cerr << "Lakni self-test failed at check " << result << '\n';
            return 1;
        }
        std::cout << "all self-tests passed (C++ Lakni API)\n";
        return 0;
    }
    if (argc != 4) {
        std::cerr << "usage: " << argv[0] << " YYYY MM DD | --test\n";
        return 2;
    }
    try {
        const int year = std::stoi(argv[1]);
        const int month = std::stoi(argv[2]);
        const int day = std::stoi(argv[3]);
        const auto jdn = lakni::gregorianToJdn(year, month, day);
        const auto ahom = lakni::ahom::forDate(year, month, day);
        const auto cycle = lakni::ahom::dayCycleForJdn(jdn);
        const auto structural = lakni::ahom::structuralYearFor(year);
        const auto phase = lakni::ahom::lunarPhaseForJdn(jdn);
        const auto myanmar = lakni::sakkaraj::fromJdn(jdn);
        std::cout << "Gregorian date : " << year << '-' << month << '-' << day << '\n'
                  << "Ahom Lakni*    : " << ahom.year.position << "/60 " << ahom.year.name << '\n'
                  << "Ahom month*    : " << ahom.monthNumber << ' ' << ahom.monthName
                  << " day " << ahom.monthDay << '/' << ahom.monthLength
                  << " [" << ahom.monthsInYear << " lunar months]\n"
                  << "Ganzhi compare : " << structural.name << " = " << structural.element
                  << ' ' << structural.son << '\n'
                  << "Day name       : " << cycle.name << " (" << cycle.index << "/60)\n"
                  << "Myanmar date   : ME " << myanmar.myanmarYear << ' ' << myanmar.monthName
                  << ' ' << myanmar.phase << ' ' << myanmar.fortnightDay << '\n'
                  << "Moon estimate  : " << phase.phase;
        if (phase.day) std::cout << " day " << *phase.day;
        std::cout << "\nJulian Day No. : " << jdn << '\n'
                  << "* Ahom lunar date is an explicit seasonal/new-moon reconstruction; not a Nadaw conversion.\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
