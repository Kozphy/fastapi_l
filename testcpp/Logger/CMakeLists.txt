add_library(Logger STATIC
    "src/Logger.cpp")

add_library(Demo::Logger ALIAS Logger)

target_link_libraries(Logger PRIVATE spdlog::spdlog fmt::fmt)

target_include_directories(Logger
    PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)