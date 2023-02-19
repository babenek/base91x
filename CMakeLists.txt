cmake_minimum_required(VERSION 3.10)
project(base91x)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS " ${CMAKE_CXX_FLAGS} -pedantic -Wall -Wextra ")

# includes
INCLUDE_DIRECTORIES(./include/)

# main executable
add_executable(${PROJECT_NAME} src/base91x.cpp)

# unit tests
set(PROJECT_TEST_NAME test_${PROJECT_NAME})
add_executable(${PROJECT_TEST_NAME} tests/test_base91x.cpp)
add_test(NAME ${PROJECT_TEST_NAME} COMMAND ${PROJECT_TEST_NAME})
enable_testing()

# performance test - use make perf
set(PROJECT_PERF_NAME perf_${PROJECT_NAME})
add_executable(${PROJECT_PERF_NAME} perf/perf_base91x.cpp)
ADD_CUSTOM_TARGET(perf COMMAND ${PROJECT_PERF_NAME})

install(TARGETS ${PROJECT_NAME})
