cmake_minimum_required(VERSION 3.2.24)

# set the project name
project(fastapi_demo_with_cmake VERSION 0.01
        DESCRIPTION "test"
        LANGUAGES CXX
)


# set(CMAKE_VERBOSE_MAKEFILE TRUE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

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
  target_link_libraries(${PROJECT_NAME} cppcheck::cppcheck)
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