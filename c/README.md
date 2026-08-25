# C11 calendar port

This directory contains C ports of the three calendar engines in
[`../python`](../python). The Python implementation remains the research
reference; the C regression suite pins the same published anchors.

## Requirements

- A C11 compiler such as Clang or GCC
- CMake 3.16 or newer
- The standard math library (`libm`)

No third-party runtime package is required.

## Build

Run these commands from the repository root (`lakni-calendar/`):

```bash
cmake -S c -B build/c
cmake --build build/c
ctest --test-dir build/c --output-on-failure
```

The build produces:

```text
build/c/lakni              Ahom Lakni date converter
build/c/lak-jeng           Lak Jeng calculator
build/c/sakkaraj           Sakkaraj/Myanmar calendar converter
build/c/liblakni_calendar.a
```

## Command-line usage

### Lakni

Convert a Gregorian date to the reconstructed Ahom Lakni calendar:

```bash
build/c/lakni YYYY MM DD
build/c/lakni 2026 8 23
```

Example core result:

```text
Ahom Lakni*    : 18/60 Rung Shiu
Ahom month*    : 10 Din Ship day 11/30 [12 lunar months]
Day name       : Kut-Sai (5/60)
Myanmar date   : ME 1388 Wagaung waxing 10
```

Run the Lakni self-test:

```bash
build/c/lakni --test
```

The asterisk in the output is important: the Ahom lunar date is an explicit
seasonal/new-moon reconstruction, not a Myanmar Nadaw conversion.

### Lak Jeng

Run the source worksheet for a Tai year:

```bash
build/c/lak-jeng TAI_YEAR
build/c/lak-jeng 2115
```

Convert a Gregorian date through the documented Lak Jeng day-count bridge:

```bash
build/c/lak-jeng --date YYYY MM DD
build/c/lak-jeng --date 2026 8 23
```

Run the Lak Jeng self-test:

```bash
build/c/lak-jeng --test
```

The year worksheet and Gregorian bridge remain separate, matching the Python
reference. In particular, the published formula for Tai year 2116 gives an
elapsed-day value ten days different from the dated bridge anchor.

### Sakkaraj

Convert a Gregorian date to its Sakkaraj and Myanmar calendar values:

```bash
build/c/sakkaraj YYYY MM DD
build/c/sakkaraj 2015 7 31
```

Report Thingyan, watat type, Second Waso full moon, and Thai integers for a
CS/Myanmar year:

```bash
build/c/sakkaraj --year MYANMAR_YEAR
build/c/sakkaraj --year 1377
```

Run the Sakkaraj self-test:

```bash
build/c/sakkaraj --test
```

Commands return exit status `0` on success and a nonzero status for a failed
calculation, self-test, invalid Gregorian date, or usage error.

## Use as a C library

Include the public header and check every returned `lakni_status` value:

```c
#include <stdio.h>
#include "lakni/calendar.h"

int main(void) {
    lakni_ahom_date date;
    lakni_status status = lakni_ahom_for_date(2026, 8, 23, 5.5, &date);

    if (status != LAKNI_OK) {
        fprintf(stderr, "calendar calculation failed: %d\n", status);
        return 1;
    }

    printf("%d/60 %s, %s day %d\n",
           date.year.position,
           date.year.name,
           date.month_name,
           date.month_day);
    return 0;
}
```

Compile the example against the built static library:

```bash
cc example.c -Ic/include build/c/liblakni_calendar.a -lm -o example
./example
```

For another CMake project, include this directory and link the library target:

```cmake
add_subdirectory(path/to/lakni-calendar/c)
target_link_libraries(your_program PRIVATE lakni_calendar)
```

Important API conventions:

- Gregorian and Myanmar conversion functions return `lakni_status`.
- JDN and accumulated-day values use `int64_t`.
- `timezone_hours` is a signed UTC offset, such as `5.5` for Assam.
- String pointers inside result structs refer to static library data. Callers
  must not modify or free them.
- The caller owns every result struct and may allocate it on the stack.

## Tests

Run the combined regression suite:

```bash
ctest --test-dir build/c --output-on-failure
build/c/test-calendars
```

To run with AddressSanitizer and UndefinedBehaviorSanitizer:

```bash
cmake -S c -B build/c-sanitize -DLAKNI_SANITIZE=ON
cmake --build build/c-sanitize
ctest --test-dir build/c-sanitize --output-on-failure
```

## Quick examples

```bash

build/c/lakni 2026 8 23
build/c/lak-jeng --date 2026 8 23
build/c/sakkaraj 2015 7 31
```

## Scope

The C library and command-line programs provide:

- **Lakni:** Ahom 60-year names, Gregorian/JDN conversion, the reconstructed
  Dinching boundary and lunar months, and the continuous 60-day cycle.
- **Lak Jeng:** the integer source worksheet, Gregorian bridge, day and year
  names, and Tai lunar New Year lookup.
- **Sakkaraj:** Thingyan, all five watat regimes and exception years, Myanmar
  date conversion in both directions, Tai lunar New Year, and Thai avoman
  integers.

Output text and localization are secondary to numeric parity. No external
runtime library is required beyond the C standard library and `libm`.

## Layout

```text
c/
  CMakeLists.txt
  include/lakni/calendar.h    Public API and result/status types
  src/common.c                Gregorian/JDN conversion and floor arithmetic
  src/lak_ni.c                Ahom Lakni and reconstructed lunar calendar
  src/lak_jeng.c              Lak Jeng worksheet and Gregorian bridge
  src/sakkaraj.c              Myanmar/Chula Sakkaraj calculations
  cli/lak_ni.c                `lakni` command
  cli/lak_jeng.c              `lak-jeng` command
  cli/sakkaraj.c              `sakkaraj` command
  tests/test_calendars.c      C unit and regression tests
```

Use C11. Keep calendar calculations in the library; CLI files should only parse
arguments, call the library, and format results.

## API and representation decisions

- Use `int64_t` for JDNs, ahargana values, and intermediate integer products.
- Use `double` only where the Python algorithm uses astronomical Julian dates
  or fractional constants.
- Return calendar records through explicit structs such as `lakni_ahom_date`,
  `lakni_lak_jeng_result`, `lakni_watat_result`, and `lakni_myanmar_date`.
- Return a small status enum from functions that can reject invalid dates or
  unsupported ranges; do not use global error state.
- Store fixed month, stem, branch, and exception tables as `static const` data.
  UTF-8 labels are byte strings; calculations must not depend on byte length.
- Implement mathematical floor division/modulo helpers. Native C division
  truncates toward zero and must not silently replace Python's `//` and `%` for
  negative inputs.
- Reject invalid Gregorian dates and report calculation failures through the
  public status enum.

The public surface includes these operations:

```c
lakni_status lakni_gregorian_to_jdn(int year, int month, int day, int64_t *jdn);
lakni_status lakni_jdn_to_gregorian(int64_t jdn, lakni_gregorian_date *date);
lakni_status lakni_ahom_for_date(int year, int month, int day, double tz_hours,
                                 lakni_ahom_date *result);
lakni_status lakni_lak_jeng_calculate(int tai_year,
                                      lakni_lak_jeng_result *result);
lakni_status lakni_myanmar_from_jdn(int64_t jdn, lakni_myanmar_date *result);
lakni_status lakni_myanmar_to_jdn(const lakni_myanmar_date *date, int64_t *jdn);
lakni_status lakni_thingyan(int myanmar_year, lakni_thingyan_dates *result);
```

All exported symbols use the `lakni_` prefix to avoid collisions when embedded
in other programs.

## Implemented components

1. **Shared exact arithmetic**
   - Gregorian/JDN conversion and Python-compatible floor division/modulo.

2. **Lak Jeng**
   - Integer worksheet, Gregorian bridge, Tai year boundary, day names,
     weekdays, and market-day flags.

3. **Sakkaraj**
   - Era constants, all five regimes, exception tables, watat classification,
     Myanmar date conversion, Thingyan, Tai lunar New Year, and Thai integers.

4. **Lakni**
   - Historical 60-name table, deterministic year/day cycles, Meeus new-moon
     calculation, and the reconstructed Dinching/month model.

5. **CLIs and build**
   - Three command-line programs, a static library, CMake tests, strict
     warnings, and an optional sanitizer build.

## Verification

The checked-in regression executable verifies:

- Gregorian/JDN anchors and round trips;
- all Sakkaraj exception-year anchors from the Python suite;
- Myanmar date round trips across all five historical regimes;
- Lak Jeng worksheet, Gregorian bridge, year boundary, and day-cycle anchors;
- Ahom Lakni names, Dinching boundary, leap lunation, and day-cycle anchors;
- the Meeus new-moon reference with a `0.001` day tolerance; and
- clean execution under AddressSanitizer and UndefinedBehaviorSanitizer.

Integer anchors require exact equality. The Ahom CLI retains the reconstruction
warning because porting the implementation does not strengthen its historical
or cultural authority.
