#include "lakni/lak_jeng.hpp"

#include "detail.hpp"

namespace lakni::jeng {

Calculation calculate(int taiYear) {
    lakni_lak_jeng_result raw{};
    detail::require(lakni_lak_jeng_calculate(taiYear, &raw),
                    "Lak Jeng year calculation");
    return {
        raw.tai_year,
        raw.calculation_year,
        raw.correction,
        raw.numerator,
        raw.quotient,
        raw.old_position,
        raw.new_position,
        raw.elapsed_days,
        raw.missing,
        raw.missing_days,
        raw.missing_position,
        raw.lunar_months,
        raw.lunar_month_position,
        raw.cycle_index,
        detail::string(raw.weekday),
        detail::string(raw.mother),
        detail::string(raw.child),
        detail::string(raw.mother_shan),
        detail::string(raw.child_shan),
        detail::string(raw.year_mother),
        detail::string(raw.year_child)
    };
}

Date forDate(int year, int month, int day) {
    lakni_lak_jeng_date raw{};
    detail::require(lakni_lak_jeng_for_date(year, month, day, &raw),
                    "Gregorian to Lak Jeng conversion");
    return {
        raw.tai_year,
        raw.jdn,
        raw.elapsed_days,
        raw.cycle_index,
        detail::string(raw.weekday),
        detail::string(raw.mother),
        detail::string(raw.child),
        detail::string(raw.mother_shan),
        detail::string(raw.child_shan),
        raw.market_day,
        raw.previous_new_year_jdn,
        raw.next_new_year_jdn
    };
}

}  // namespace lakni::jeng
