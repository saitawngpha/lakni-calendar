#include "lakni/sakkaraj.hpp"

#include "detail.hpp"

namespace lakni::sakkaraj {

int csYearFor(int year, int month, int day) {
    (void)gregorianToJdn(year, month, day);
    return lakni_cs_year_for(year, month, day);
}

Thingyan thingyan(int myanmarYear) {
    lakni_thingyan_dates raw{};
    detail::require(lakni_thingyan(myanmarYear, &raw), "Thingyan calculation");
    return {
        raw.myanmar_year, raw.ja_jd, raw.jk_jd, raw.akyo_day,
        raw.akya_day, raw.atat_day, raw.new_year_day
    };
}

Watat watatType(int myanmarYear) {
    lakni_watat_result raw{};
    detail::require(lakni_watat_type(myanmarYear, &raw), "watat calculation");
    Watat result;
    result.era = raw.era;
    result.excessDaysRaw = raw.excess_days_raw;
    result.excessDays = raw.excess_days;
    result.watat = raw.watat;
    if (raw.has_threshold) result.threshold = raw.threshold;
    if (raw.has_waso_full_moon) result.wasoFullMoon = raw.waso_full_moon;
    if (raw.watat) result.previousWatatYear = raw.previous_watat_year;
    result.yearLength = raw.year_length;
    result.type = detail::string(raw.type);
    return result;
}

MyanmarDate fromJdn(std::int64_t jdn) {
    lakni_myanmar_date raw{};
    detail::require(lakni_myanmar_from_jdn(jdn, &raw), "JDN to Myanmar conversion");
    return {
        raw.myanmar_year, raw.year_type, raw.month, detail::string(raw.month_name),
        raw.month_day, raw.month_length, detail::string(raw.phase), raw.fortnight_day
    };
}

std::int64_t toJdn(int myanmarYear, int month, int monthDay) {
    lakni_myanmar_date raw{};
    raw.myanmar_year = myanmarYear;
    raw.month = month;
    raw.month_day = monthDay;
    std::int64_t jdn{};
    detail::require(lakni_myanmar_to_jdn(&raw, &jdn), "Myanmar to JDN conversion");
    return jdn;
}

std::int64_t taiLunarNewYearJdn(int gregorianYear) {
    const auto jdn = lakni_tai_lunar_new_year_jdn(gregorianYear);
    if (jdn == 0) throw CalendarError("Tai lunar New Year calculation failed");
    return jdn;
}

ThaiIntegers thaiNewYearIntegers(int csYear) {
    lakni_thai_integers raw{};
    detail::require(lakni_thai_new_year_integers(csYear, &raw),
                    "Thai New Year integer calculation");
    return {
        raw.ahargana, raw.remainder, raw.kammacabala,
        raw.solar_leap, raw.avoman
    };
}

}  // namespace lakni::sakkaraj
