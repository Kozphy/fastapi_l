add_library(Logger STATIC
    "src/Logger.cpp")

target_link_libraries(Logger STATIC spdlog::spdlog fmt::fmt)

target_include_directories(Logger
    PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)