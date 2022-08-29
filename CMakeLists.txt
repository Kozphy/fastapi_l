cmake_minimum_required(VERSION 3.2.24)

# set the project name
project(fastapi_demo_with_cmake VERSION 0.01
        DESCRIPTION "test"
        LANGUAGES CXX
)

# Default build type
set(default_build_type "Debug")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")

#################################################################################
# Setup C/C++ compiler options
#################################################################################
# set(CMAKE_VERBOSE_MAKEFILE TRUE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
# message("List of compile features: ${CMAKE_CXX_COMPILE_FEATURES}")
# target_compile_options(${PROJECT_NAME} PRIVATE -fmodules-ts)

# where is conan install folder
include(${CMAKE_BINARY_DIR}/cmake-build-release/conan_paths.cmake)

# third party library
find_package(Boost REQUIRED)
find_package(Poco REQUIRED)
find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)
find_package(cppcheck)
find_package("yaml-cpp")
find_package(Protobuf REQUIRED)

configure_file(datacpp/BasicConfig.h.in BasicConfig.h)
include_directories(${CMAKE_CURRENT_BINARY_DIR})


# Allow enabling and disabling components
option(ENABLE_PROTOBUF_CONFIG "Enable Protobuf for configuration" OFF)

# add subdirectories
add_subdirectory(${PROJECT_SOURCE_DIR}/datacpp)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/datacpp/Logger)
# if(ENABLE_PROTOBUF_CONFIG)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/datacpp/configuration)
# endif()


if(SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()