# C++17 calendar API

This directory provides an idiomatic C++17 interface for the three reference
engines in [`../python`](../python):

- `src/lak_ni.cpp` — Ahom Lakni names, day cycle, new-moon estimate, and the
  reconstructed Dinching lunar calendar;
- `src/lak_jeng.cpp` — Lak Jeng worksheet, Gregorian bridge, and Tai New Year;
- `src/sakkaraj.cpp` — Thingyan, watat regimes, Myanmar date conversion, and
  Thai calendar integers.

The C++ layer uses owned `std::string` values, `std::optional`, namespaces, and
`lakni::CalendarError`. Calculations are delegated to the verified C11 core in
[`../c`](../c), preventing the Python, C, and C++ implementations from drifting
into different numeric results.

## Requirements

- A C++17 compiler such as Clang or GCC
- CMake 3.16 or newer

No third-party library is required.

## Build

Run from the repository root:

```bash
cmake -S cpp -B build/cpp
cmake --build build/cpp
ctest --test-dir build/cpp --output-on-failure
```

The build produces:

```text
build/cpp/lakni-cpp
build/cpp/lak-jeng-cpp
build/cpp/sakkaraj-cpp
build/cpp/liblakni_calendar_cpp.a
```

## Command-line usage

```bash
# Ahom Lakni calendar
build/cpp/lakni-cpp 2026 8 23
build/cpp/lakni-cpp --test

# Lak Jeng year worksheet or Gregorian bridge
build/cpp/lak-jeng-cpp 2115
build/cpp/lak-jeng-cpp --date 2026 8 23
build/cpp/lak-jeng-cpp --test

# Sakkaraj date or Myanmar-year report
build/cpp/sakkaraj-cpp 2015 7 31
build/cpp/sakkaraj-cpp --year 1377
build/cpp/sakkaraj-cpp --test
```

## Use the C++ library

Include the module needed by your program:

```cpp
#include "lakni/lak_ni.hpp"

#include <iostream>

int main() {
    try {
        const auto date = lakni::ahom::forDate(2026, 8, 23);
        std::cout << date.year.position << "/60 " << date.year.name
                  << ", " << date.monthName << " day " << date.monthDay
                  << '\n';
    } catch (const lakni::CalendarError& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
```

In another CMake project:

```cmake
add_subdirectory(path/to/lakni-calendar/cpp)
target_link_libraries(your_program PRIVATE lakni_calendar_cpp)
```

The public headers are:

```text
include/lakni/common.hpp
include/lakni/lak_ni.hpp
include/lakni/lak_jeng.hpp
include/lakni/sakkaraj.hpp
```

API conventions:

- functions return C++ value objects;
- invalid dates and failed calculations throw `lakni::CalendarError`;
- JDN and accumulated-day values use `std::int64_t`;
- absent calendar fields use `std::optional`;
- timezone offsets are signed hours from UTC, with `5.5` as the default Ahom
  reconstruction offset; and
- returned objects own their strings and can safely outlive the function call.

## Tests and sanitizers

Run the C++ regression executable directly or through CTest:

```bash
build/cpp/test-calendars-cpp
ctest --test-dir build/cpp --output-on-failure
```

Build both the C calculation core and C++ layer with AddressSanitizer and
UndefinedBehaviorSanitizer:

```bash
cmake -S cpp -B build/cpp-sanitize -DLAKNI_CPP_SANITIZE=ON
cmake --build build/cpp-sanitize
ctest --test-dir build/cpp-sanitize --output-on-failure
```

The Ahom result remains an explicitly labelled reconstruction. A C++ interface
does not strengthen the historical or cultural authority of the model.
