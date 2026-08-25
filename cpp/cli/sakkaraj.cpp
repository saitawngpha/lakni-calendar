#include "lakni/sakkaraj.hpp"
#include "lakni/calendar.h"

#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc == 2 && std::string{argv[1]} == "--test") {
        const int result = lakni_sakkaraj_self_test();
        if (result != 0) {
            std::cerr << "Sakkaraj self-test failed at check " << result << '\n';
            return 1;
        }
        std::cout << "all self-tests passed (C++ Sakkaraj API)\n";
        return 0;
    }
    try {
        if (argc == 3 && std::string{argv[1]} == "--year") {
            const int year = std::stoi(argv[2]);
            const auto festival = lakni::sakkaraj::thingyan(year);
            const auto watat = lakni::sakkaraj::watatType(year);
            const auto thai = lakni::sakkaraj::thaiNewYearIntegers(year);
            std::cout << "CS/Myanmar year : " << year << '\n'
                      << "New Year (atat) : JD " << festival.jaJd << '\n'
                      << "Akya (festival) : JD " << festival.jkJd << '\n'
                      << "Year type       : " << watat.type << '\n';
            if (watat.wasoFullMoon) {
                std::cout << "2nd Waso FM     : JDN " << *watat.wasoFullMoon << '\n';
            }
            std::cout << "Thai integers   : h0=" << thai.ahargana
                      << " kammacabala=" << thai.kammacabala
                      << " solar_leap=" << (thai.solarLeap ? "true" : "false")
                      << " avoman=" << thai.avoman << '\n';
            return 0;
        }
        if (argc == 4) {
            const int year = std::stoi(argv[1]);
            const int month = std::stoi(argv[2]);
            const int day = std::stoi(argv[3]);
            const auto jdn = lakni::gregorianToJdn(year, month, day);
            const auto myanmar = lakni::sakkaraj::fromJdn(jdn);
            std::cout << "Gregorian      : " << year << '-' << month << '-' << day << '\n'
                      << "Julian Day No. : " << jdn << '\n'
                      << "Sakkaraj (CS)  : " << lakni::sakkaraj::csYearFor(year, month, day) << '\n'
                      << "Myanmar date   : ME " << myanmar.myanmarYear << ' '
                      << myanmar.monthName << ' ' << myanmar.phase << ' '
                      << myanmar.fortnightDay << '\n';
            return 0;
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
    std::cerr << "usage: " << argv[0] << " YYYY MM DD | --year MY | --test\n";
    return 2;
}
