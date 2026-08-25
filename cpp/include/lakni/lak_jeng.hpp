#ifndef LAKNI_CPP_LAK_JENG_HPP
#define LAKNI_CPP_LAK_JENG_HPP

#include "lakni/common.hpp"

#include <cstdint>
#include <string>

namespace lakni::jeng {

struct Calculation {
    int taiYear{};
    int calculationYear{};
    std::int64_t correction{};
    std::int64_t numerator{};
    std::int64_t quotient{};
    std::int64_t oldPosition{};
    std::int64_t newPosition{};
    std::int64_t elapsedDays{};
    std::int64_t missing{};
    std::int64_t missingDays{};
    std::int64_t missingPosition{};
    std::int64_t lunarMonths{};
    int lunarMonthPosition{};
    int cycleIndex{};
    std::string weekday;
    std::string mother;
    std::string child;
    std::string motherShan;
    std::string childShan;
    std::string yearMother;
    std::string yearChild;
};

struct Date {
    int taiYear{};
    std::int64_t jdn{};
    std::int64_t elapsedDays{};
    int cycleIndex{};
    std::string weekday;
    std::string mother;
    std::string child;
    std::string motherShan;
    std::string childShan;
    bool marketDay{};
    std::int64_t previousNewYearJdn{};
    std::int64_t nextNewYearJdn{};
};

Calculation calculate(int taiYear);
Date forDate(int year, int month, int day);

}  // namespace lakni::jeng

#endif
