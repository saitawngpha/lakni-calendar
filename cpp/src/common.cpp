#include "lakni/common.hpp"

#include "detail.hpp"

namespace lakni {

std::int64_t gregorianToJdn(int year, int month, int day) {
    std::int64_t jdn{};
    detail::require(lakni_gregorian_to_jdn(year, month, day, &jdn),
                    "Gregorian to JDN conversion");
    return jdn;
}

GregorianDate jdnToGregorian(std::int64_t jdn) {
    lakni_gregorian_date raw{};
    detail::require(lakni_jdn_to_gregorian(jdn, &raw),
                    "JDN to Gregorian conversion");
    return {raw.year, raw.month, raw.day};
}

}  // namespace lakni
