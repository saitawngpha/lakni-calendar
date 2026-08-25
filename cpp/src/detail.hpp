#ifndef LAKNI_CPP_DETAIL_HPP
#define LAKNI_CPP_DETAIL_HPP

#include "lakni/calendar.h"
#include "lakni/common.hpp"

#include <string>

namespace lakni::detail {

inline const char* statusText(lakni_status status) {
    switch (status) {
        case LAKNI_OK: return "success";
        case LAKNI_INVALID_ARGUMENT: return "invalid argument";
        case LAKNI_INVALID_DATE: return "invalid date";
        case LAKNI_CALCULATION_ERROR: return "calculation error";
    }
    return "unknown error";
}

inline void require(lakni_status status, const char* operation) {
    if (status != LAKNI_OK) {
        throw CalendarError(std::string(operation) + ": " + statusText(status));
    }
}

inline std::string string(const char* value) {
    return value == nullptr ? std::string{} : std::string{value};
}

}  // namespace lakni::detail

#endif
