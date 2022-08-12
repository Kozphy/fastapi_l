cmake_minimum_required(VERSION 3.2.24)

# set the project name
project(fastapi_demo_with_camke VERSION 0.01 
        DESCRIPTION "test"
        LANGUAGES CXX
)
# find_package(PythonExtensions REQUIRED)


set(CMAKE_VERBOSE_MAKEFILE TRUE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# control where the static and shared libraries are built so that on windows
# we don't need to tinker with the path to run the executable
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")

# option(BUILD_SHARED_LIBS "Build using shared libraries" ON)

configure_file(TutorialConfig.h.in TutorialConfig.h)

# add_subdirectory(MathFunctions)

# option(USE_MYMATH "Use tutorial provided math implementation" ON)
# if(USE_MYMATH)
#   add_subdirectory(MathFunctions)
#   list(APPEND EXTRA_LIBS MathFunctions)
#   # list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/MathFunctions")
# endif()

# add_subdirectory(MathFunctions)

# add the executable
add_executable(Test main.cpp)

# target_link_libraries(Test PUBLIC MathFunctions)

# target_include_directories(Test PUBLIC
#                            "${PROJECT_BINARY_DIR}"
#                           #  ${EXTRA_INCLUDES}
#                            )

# install(TARGETS Test DESTINATION bin)
# install(FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
#   DESTINATION include
#   )

# enable_testing()
# include(CTest)

# does the application run, segfault?
# add_test(NAME Runs COMMAND Test 25)

# does the usage message work?
# verifying that the usage message is printed when an incorrect number of arguments are provided.
# add_test(NAME Usage COMMAND Test)
# set_tests_properties(PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number")

# define a function to simplify adding tests
# function(do_test target arg result)
#   add_test(NAME Comp:${arg} COMMAND ${target} ${arg})
#   set_tests_properties(Comp:${arg}
#     PROPERTIES PASS_REGULAR_EXPRESSION ${result} 
#   )
# endfunction()

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