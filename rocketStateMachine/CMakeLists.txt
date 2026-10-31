cmake_minimum_required(VERSION 3.16)
project(RocketFlightSoftware CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_POLICY_VERSION_MINIMUM 3.5 CACHE STRING "" FORCE)

# Include CMake's FetchContent module to pull dependencies locally
include(FetchContent)

# 1. Fetch and build libzmq locally
FetchContent_Declare(
    libzmq
    GIT_REPOSITORY https://github.com/zeromq/libzmq.git
    GIT_TAG        v4.3.5  # Stable release version
)
# Disable unwanted options to speed up local compilation (tests, docs, etc.)
set(ZMQ_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(ZMQ_BUILD_DOCS OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(libzmq)

# 2. Fetch and build cppzmq (C++ bindings) locally
FetchContent_Declare(
    cppzmq
    GIT_REPOSITORY https://github.com/zeromq/cppzmq.git
    GIT_TAG        v4.10.0 # Stable release version
)
set(CPPZMQ_BUILD_TESTS OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(cppzmq)

# Include directories
include_directories(include)

# Define your flight software executable target
add_executable(rocket_fsw
    src/main.cpp
    src/state_machine.cpp
)

# Link ZeroMQ locally to your executable
target_link_libraries(rocket_fsw PRIVATE libzmq-static cppzmq)
