cmake_minimum_required(VERSION 3.2.24)

# set the project name
project(fastapi_demo_with_cmake VERSION 0.01
        DESCRIPTION "test"
        LANGUAGES CXX
)


# set(CMAKE_VERBOSE_MAKEFILE TRUE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "")
# set(DCMAKE_EXPORT_COMPILE_COMMANDS ON)

# Using the "cmake_find_package" generator
# set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})
# set(CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR} ${CMAKE_PREFIX_PATH})
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

# TODO: fix cppcheck not work
find_package(Boost REQUIRED)
find_package(Poco REQUIRED)
find_package(cppcheck)
find_package(spdlog)

configure_file(testcpp/TutorialConfig.h.in TutorialConfig.h)


add_executable(${PROJECT_NAME} testcpp/src/main.cpp)


target_include_directories(${PROJECT_NAME} PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
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

if(TARGET cppcheck::cppcheck)
  message("using cppcheck")
  find_program(CPPCHECK cppcheck)
  set(CPPCHECK_TEMPLATE "cppcheck:{file}:{line}: {severity}:{message}")
  set(CPPCHECK_BUILD_RESULT "${CMAKE_CURRENT_SOURCE_DIR}/testcpp/cppcheck_result")
  message("Path: ${CPPCHECK}")
  # message("Current source: ${CMAKE_CURRENT_SOURCE_DIR}")
  target_link_libraries(${PROJECT_NAME} cppcheck::cppcheck)
  # set(CMAKE_CXX_CPPCHECK ${CPPCHECK}
  #     --enable=all
  #     --inconclusive
  #     --force
  #     --inline-suppr
  #     --template=${CPPCHECK_TEMPLATE}
  #     --verbose
  #     -i ${CMAKE_CURRENT_SOURCE_DIR}/testcpp/
  # )

  add_custom_target(cppcheck ALL COMMAND ${CPPCHECK}
      --enable=all
      --inconclusive
      --force
      --inline-suppr
      --template=${CPPCHECK_TEMPLATE}
      --cppcheck-build-dir=${CPPCHECK_BUILD_RESULT}
      --verbose
      --check-config
      --project=compile_commands.json
      # unwant in release
      -i ${CMAKE_CURRENT_SOURCE_DIR}/testcpp/training
    ${CMAKE_CURRENT_SOURCE_DIR}/testcpp/
    COMMENT "Checking ..."
    VERBATIM
  )

  message("debug value: ${CMAKE_CXX_CPPCHECK}")
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