#include "lakni/lak_jeng.hpp"
#include "lakni/lak_ni.hpp"
#include "lakni/sakkaraj.hpp"

#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

void expect(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

}  // namespace

int main() {
    try {
        const auto jdn = lakni::gregorianToJdn(2000, 1, 1);
        expect(jdn == 2451545, "Gregorian/JDN anchor");
        const auto gregorian = lakni::jdnToGregorian(jdn);
        expect(gregorian.year == 2000 && gregorian.month == 1 && gregorian.day == 1,
               "Gregorian/JDN round trip");

        const auto ahomYear = lakni::ahom::yearForCycle(2025);
        expect(ahomYear.position == 18 && ahomYear.name == "Rung Shiu", "Ahom year anchor");
        const auto ahomDate = lakni::ahom::forDate(2025, 11, 21);
        expect(ahomDate.year.cycleYear == 2025 && ahomDate.monthName == "Din Ching"
                   && ahomDate.monthDay == 1,
               "Dinching boundary");
        expect(lakni::ahom::forDate(2024, 11, 2).monthsInYear == 13,
               "Ahom leap lunation");
        expect(std::abs(lakni::ahom::trueNewMoonJde(0) - 2451550.25993) < 0.001,
               "new-moon anchor");

        const auto jengYear = lakni::jeng::calculate(2116);
        expect(jengYear.elapsedDays == 772531, "Lak Jeng worksheet anchor");
        const auto jengDate = lakni::jeng::forDate(2026, 8, 23);
        expect(jengDate.taiYear == 2120 && jengDate.mother == "Kat"
                   && jengDate.child == "Sai",
               "Lak Jeng Gregorian bridge");

        const auto watat = lakni::sakkaraj::watatType(1377);
        expect(watat.yearLength == 385 && watat.wasoFullMoon == 2457235,
               "Sakkaraj watat anchor");
        const auto myanmarJdn = lakni::sakkaraj::toJdn(1387, 9, 1);
        const auto myanmar = lakni::sakkaraj::fromJdn(myanmarJdn);
        expect(myanmar.myanmarYear == 1387 && myanmar.month == 9
                   && myanmar.monthDay == 1,
               "Myanmar calendar round trip");
        expect(lakni::sakkaraj::thaiNewYearIntegers(856).avoman == 692,
               "Thai avoman anchor");

        bool rejected = false;
        try {
            (void)lakni::gregorianToJdn(2026, 2, 30);
        } catch (const lakni::CalendarError&) {
            rejected = true;
        }
        expect(rejected, "invalid Gregorian date rejection");

        std::cout << "all C++ calendar tests passed\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "C++ calendar test failed: " << error.what() << '\n';
        return 1;
    }
}
