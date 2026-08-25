#ifndef LAKNI_CPP_COMMON_HPP
#define LAKNI_CPP_COMMON_HPP

#include <cstdint>
#include <stdexcept>
#include <string>

namespace lakni {

struct GregorianDate {
    int year{};
    int month{};
    int day{};
};

class CalendarError : public std::runtime_error {
public:
    explicit CalendarError(const std::string& message) : std::runtime_error(message) {}
};

std::int64_t gregorianToJdn(int year, int month, int day);
GregorianDate jdnToGregorian(std::int64_t jdn);

}  // namespace lakni

#endif
