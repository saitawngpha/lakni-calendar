cmake_minimum_required(VERSION 3.16)
project(lakni_calendar_cpp LANGUAGES C CXX)

option(LAKNI_CPP_SANITIZE "Build C and C++ with address/undefined sanitizers" OFF)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(LAKNI_BUILD_CLI OFF CACHE BOOL "" FORCE)
set(LAKNI_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(LAKNI_SANITIZE ${LAKNI_CPP_SANITIZE} CACHE BOOL "" FORCE)
add_subdirectory(../c c-core)

add_library(lakni_calendar_cpp
    src/common.cpp
    src/lak_ni.cpp
    src/lak_jeng.cpp
    src/sakkaraj.cpp
)
target_include_directories(lakni_calendar_cpp PUBLIC include)
target_link_libraries(lakni_calendar_cpp PUBLIC lakni_calendar)
target_compile_options(lakni_calendar_cpp PRIVATE -Wall -Wextra -Wpedantic)

if(LAKNI_CPP_SANITIZE AND CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(lakni_calendar_cpp PUBLIC
        -fsanitize=address,undefined -fno-omit-frame-pointer)
    target_link_options(lakni_calendar_cpp PUBLIC -fsanitize=address,undefined)
endif()

add_executable(lakni-cpp cli/lak_ni.cpp)
target_link_libraries(lakni-cpp PRIVATE lakni_calendar_cpp)

add_executable(lak-jeng-cpp cli/lak_jeng.cpp)
target_link_libraries(lak-jeng-cpp PRIVATE lakni_calendar_cpp)

add_executable(sakkaraj-cpp cli/sakkaraj.cpp)
target_link_libraries(sakkaraj-cpp PRIVATE lakni_calendar_cpp)

enable_testing()
add_executable(test-calendars-cpp tests/test_calendars.cpp)
target_link_libraries(test-calendars-cpp PRIVATE lakni_calendar_cpp)
add_test(NAME cpp-calendar-regressions COMMAND test-calendars-cpp)
