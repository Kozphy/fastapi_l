# Sources
file(GLOB SRCS_G "src/*.cpp")

# Headers
file(GLOB_RECURSE HDRS_G "include/*.h")

add_library(Logger HDRS_G SRCS_G)
target_include_directories()