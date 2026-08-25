#ifndef LAKNI_CPP_SAKKARAJ_HPP
#define LAKNI_CPP_SAKKARAJ_HPP

#include "lakni/common.hpp"

#include <cstdint>
#include <optional>
#include <string>

namespace lakni::sakkaraj {

struct Thingyan {
    int myanmarYear{};
    double jaJd{};
    double jkJd{};
    std::int64_t akyoDay{};
    std::int64_t akyaDay{};
    std::int64_t atatDay{};
    std::int64_t newYearDay{};
};

struct Watat {
    double era{};
    double excessDaysRaw{};
    double excessDays{};
    bool watat{};
    std::optional<double> threshold;
    std::optional<std::int64_t> wasoFullMoon;
    std::optional<int> previousWatatYear;
    int yearLength{};
    std::string type;
};

struct MyanmarDate {
    int myanmarYear{};
    int yearType{};
    int month{};
    std::string monthName;
    int monthDay{};
    int monthLength{};
    std::string phase;
    int fortnightDay{};
};

struct ThaiIntegers {
    std::int64_t ahargana{};
    int remainder{};
    int kammacabala{};
    bool solarLeap{};
    int avoman{};
};

int csYearFor(int year, int month, int day);
Thingyan thingyan(int myanmarYear);
Watat watatType(int myanmarYear);
MyanmarDate fromJdn(std::int64_t jdn);
std::int64_t toJdn(int myanmarYear, int month, int monthDay);
std::int64_t taiLunarNewYearJdn(int gregorianYear);
ThaiIntegers thaiNewYearIntegers(int csYear);

}  // namespace lakni::sakkaraj

#endif
