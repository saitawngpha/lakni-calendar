cmake_minimum_required(VERSION 3.16)
project(lakni_calendar C)

option(LAKNI_SANITIZE "Build with address and undefined-behavior sanitizers" OFF)
option(LAKNI_BUILD_CLI "Build the C command-line programs" ON)
option(LAKNI_BUILD_TESTS "Build the C regression tests" ON)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_library(lakni_calendar
    src/common.c
    src/lak_ni.c
    src/lak_jeng.c
    src/sakkaraj.c
)
target_include_directories(lakni_calendar PUBLIC include)
target_compile_options(lakni_calendar PRIVATE -Wall -Wextra -Wpedantic)
target_link_libraries(lakni_calendar PUBLIC m)

if(LAKNI_SANITIZE AND CMAKE_C_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(lakni_calendar PUBLIC -fsanitize=address,undefined -fno-omit-frame-pointer)
    target_link_options(lakni_calendar PUBLIC -fsanitize=address,undefined)
endif()

if(LAKNI_BUILD_CLI)
    add_executable(lakni cli/lak_ni.c)
    target_link_libraries(lakni PRIVATE lakni_calendar)

    add_executable(lak-jeng cli/lak_jeng.c)
    target_link_libraries(lak-jeng PRIVATE lakni_calendar)

    add_executable(sakkaraj cli/sakkaraj.c)
    target_link_libraries(sakkaraj PRIVATE lakni_calendar)
endif()

if(LAKNI_BUILD_TESTS)
    enable_testing()
    add_executable(test-calendars tests/test_calendars.c)
    target_link_libraries(test-calendars PRIVATE lakni_calendar)
    add_test(NAME calendar-regressions COMMAND test-calendars)
endif()
