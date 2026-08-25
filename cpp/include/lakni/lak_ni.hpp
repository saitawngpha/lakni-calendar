#ifndef LAKNI_CPP_LAK_NI_HPP
#define LAKNI_CPP_LAK_NI_HPP

#include "lakni/common.hpp"

#include <cstdint>
#include <optional>
#include <string>

namespace lakni::ahom {

struct Year {
    int position{};
    int cycleYear{};
    std::string name;
};

struct StructuralYear {
    int cycleIndex{};
    std::string stem;
    std::string stemChinese;
    std::string element;
    std::string shanStem;
    std::string son;
    std::string name;
};

struct DayCycle {
    int index{};
    std::string mother;
    std::string son;
    std::string motherShan;
    std::string sonShan;
    std::string name;
    std::string shan;
};

struct LunarPhase {
    std::string phase;
    std::optional<int> day;
    std::int64_t newMoonJdn{};
};

struct Date {
    Year year;
    std::int64_t yearStartJdn{};
    std::int64_t nextYearStartJdn{};
    int monthNumber{};
    std::string monthName;
    int monthDay{};
    int monthLength{};
    bool leapMonth{};
    int monthsInYear{};
};

Year yearForCycle(int cycleYear);
StructuralYear structuralYearFor(int adYear);
DayCycle dayCycleForJdn(std::int64_t jdn);
double trueNewMoonJde(int lunation);
LunarPhase lunarPhaseForJdn(std::int64_t jdn, double timezoneHours = 5.5);
std::int64_t dinchingStart(int gregorianYear, double timezoneHours = 5.5);
Date forDate(int year, int month, int day, double timezoneHours = 5.5);

}  // namespace lakni::ahom

#endif
