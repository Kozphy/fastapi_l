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



include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(Boost REQUIRED)
find_package(Poco REQUIRED)
find_package(cppcheck)
find_package(spdlog)

configure_file(testcpp/VersionConfig.h.in VersionConfig.h)


add_executable(${PROJECT_NAME} testcpp/src/main.cpp)


target_include_directories(${PROJECT_NAME} PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
target_compile_options(${PROJECT_NAME} PRIVATE -fmodules-ts)

if(TARGET Boost::Boost)
  target_link_libraries(${PROJECT_NAME} Boost::Boost)
else()
  message(FATAL_ERROR "Boost not found")
endif()

if(TARGET Poco::Poco)
  target_link_libraries(${PROJECT_NAME} Poco::Poco)
else()
  message(FATAL_ERROR "Poco not found")
endif()

# TODO: fix cppcheck check-config not found header file error,
# load from build dir output with \0 is wrong format and
# output xml which convert to html report.
if(TARGET cppcheck::cppcheck)
  message("using cppcheck")
  find_program(CPPCHECK cppcheck)
  # set(CPPCHECK_TEMPLATE "cppcheck: {file}:{line}:{severity}, {id}, {message}\\n{code}")
  # set(CPPCHECK_TEMPLATE_LOCATION "{file}:{line}: note: {info}\\n{code}")
  set(CPPCHECK_CHECK_DSN "${CMAKE_CURRENT_SOURCE_DIR}/testcpp/")
  set(CPPCHECK_BUILD_RESULT "${CMAKE_CURRENT_SOURCE_DIR}/testcpp/cppcheck_result")
  list(
    APPEND CPPCHECK_CMD_OPTION
      "--enable=all"
      "--inconclusive"
      "--force"
      "--inline-suppr"
      "--verbose"
      # "--check-config"
      # "--xml"
      # "--output-file=${CPPCHECK_BUILD_RESULT}/output.xml"
      "--project=compile_commands.json"
      "--template=gcc"
      "--suppress=missingInclude"
      # "--check-library"
      # "--addon=cert.py"
      # "--template=${CPPCHECK_TEMPLATE}"
      # "--template-location=${CPPCHECK_TEMPLATE_LOCATION}"
      "--cppcheck-build-dir=${CPPCHECK_BUILD_RESULT}"
      # unwant in release
      "-i ${CMAKE_CURRENT_SOURCE_DIR}/testcpp/training"
  )

  message("Path: ${CPPCHECK}")
  message("Current source: ${CMAKE_CURRENT_SOURCE_DIR}")
  target_link_libraries(${PROJECT_NAME} cppcheck::cppcheck)

  add_custom_target(cppcheck ALL COMMAND ${CPPCHECK}
    ${CPPCHECK_CMD_OPTION}
    ${CPPCHECK_CHECK_DSN} 
    # "--xml 2> output.xml"
    # "htmlreport/cppcheck-html-htmlreport --file=output.xml --report-dir=${CPPCHECK_BUILD_RESULT} --source-dir=."
    COMMENT "Cppcheck Checking ..."
    VERBATIM
  )

  message("debug value: ${CPPCHECK_CMD_OPTION}")
  message("htmlreport: ${CPPCHECK_HTMLREPORT}")
  # message("bin path: ${CPPCHECK}")
else()
  message(FATAL_ERROR "cppcheck not found")
endif()

if(TARGET spdlog::spdlog)
  target_link_libraries(${PROJECT_NAME} spdlog::spdlog)
else()
  message(FATAL_ERROR "spdlog not found")
endif()




if(SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()