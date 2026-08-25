#include "lakni/lak_ni.hpp"

#include "detail.hpp"

namespace lakni::ahom {

Year yearForCycle(int cycleYear) {
    lakni_ahom_year raw{};
    detail::require(lakni_ahom_year_for_cycle(cycleYear, &raw),
                    "Ahom year calculation");
    return {raw.position, raw.cycle_year, raw.name};
}

StructuralYear structuralYearFor(int adYear) {
    lakni_structural_year raw{};
    detail::require(lakni_structural_year_for(adYear, &raw),
                    "structural year calculation");
    return {
        raw.cycle_index,
        detail::string(raw.stem),
        detail::string(raw.stem_chinese),
        detail::string(raw.element),
        detail::string(raw.shan_stem),
        detail::string(raw.son),
        raw.name
    };
}

DayCycle dayCycleForJdn(std::int64_t jdn) {
    lakni_day_cycle raw{};
    detail::require(lakni_day_cycle_for_jdn(jdn, &raw), "day-cycle calculation");
    return {
        raw.index,
        detail::string(raw.mother),
        detail::string(raw.son),
        detail::string(raw.mother_shan),
        detail::string(raw.son_shan),
        raw.name,
        raw.shan
    };
}

double trueNewMoonJde(int lunation) {
    return lakni_true_new_moon_jde(lunation);
}

LunarPhase lunarPhaseForJdn(std::int64_t jdn, double timezoneHours) {
    lakni_lunar_phase raw{};
    detail::require(lakni_lunar_phase_for_jdn(jdn, timezoneHours, &raw),
                    "lunar phase calculation");
    LunarPhase result;
    result.phase = detail::string(raw.phase);
    if (raw.has_day) result.day = raw.day;
    result.newMoonJdn = raw.new_moon_jdn;
    return result;
}

std::int64_t dinchingStart(int gregorianYear, double timezoneHours) {
    std::int64_t jdn{};
    detail::require(lakni_ahom_dinching_start(gregorianYear, timezoneHours, &jdn),
                    "Dinching boundary calculation");
    return jdn;
}

Date forDate(int year, int month, int day, double timezoneHours) {
    lakni_ahom_date raw{};
    detail::require(lakni_ahom_for_date(year, month, day, timezoneHours, &raw),
                    "Gregorian to Ahom conversion");
    return {
        {raw.year.position, raw.year.cycle_year, raw.year.name},
        raw.year_start_jdn,
        raw.next_year_start_jdn,
        raw.month_number,
        detail::string(raw.month_name),
        raw.month_day,
        raw.month_length,
        raw.leap_month,
        raw.months_in_year
    };
}

}  // namespace lakni::ahom
