cmake_minimum_required(VERSION 3.2.24)

# set the project name
project(fastapi_demo_with_camke VERSION 0.01 
        DESCRIPTION "test"
        LANGUAGES CXX
)


set(CMAKE_VERBOSE_MAKEFILE TRUE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Using the "cmake_find_package" generator
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})
set(CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR} ${CMAKE_PREFIX_PATH})

find_package(Boost REQUIRED)
find_package(Poco REQUIRED)
find_package(cppcheck REQUIRED)

configure_file(TutorialConfig.h.in TutorialConfig.h)


add_executable(Test src/main.cpp)

target_link_libraries(Test Poco::Poco Boost::Boost cppcheck::cppcheck)



# enable_testing()
# include(CTest)

# does the application run, segfault?
# add_test(NAME Runs COMMAND Test 25)

# does the usage message work?
# verifying that the usage message is printed when an incorrect number of arguments are provided.
# add_test(NAME Usage COMMAND Test)
# set_tests_properties(PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number")



# do a bunch of result based tests
# do_test(Test 4 "4 is 2")
# do_test(Test 9 "9 is 3")
# do_test(Test 5 "5 is 2.236")
# do_test(Test -25 "-25 is (-nan|nan|0)")
# do_test(Test 0.0001 "0.0001 is 0.01")

# include(InstallRequiredSystemLibraries)
# set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/License.txt")
# set(CPACK_PACKAGE_VERSION_MAJOR "${Tutorial_VERSION_MAJOR}")
# set(CPACK_PACKAGE_VERSION_MINOR "${Tutorial_VERSION_MINOR}")
# set(CPACK_SOURCE_GENERATOR "TGZ")
# include(CPack)

if(SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()