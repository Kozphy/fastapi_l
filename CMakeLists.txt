cmake_minimum_required(VERSION 3.2.24)

# set the project name
project(fastapi_demo_with_camke VERSION 0.01)
find_package(PythonExtensions REQUIRED)

# add the executable
add_executable(Tutorial tutorial.cxx)

if(SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()