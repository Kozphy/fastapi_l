add_library(MathFunctions 
            mathFunctions.cpp
)

# anybody linking to us needs to include the current source dir
# to find MathFunctions.h
target_include_directories(MathFunctions
INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
)
# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)
if(USE_MYMATH)
    target_compile_definitions(MathFunctions PRIVATE "USE_MYMATH")
    add_executable(makeTable makeTable.cpp)
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/Table.h
        COMMAND makeTable ${CMAKE_CURRENT_BINARY_DIR}/Table.h
        DEPENDS makeTable
    )

    add_library(SqrtLibrary STATIC
                mysqrt.cpp
                ${CMAKE_CURRENT_BINARY_DIR}/Table.h
    )

    # state that we depend on our binary dir to find Table.h
    target_include_directories(SqrtLibrary PRIVATE
        ${CMAKE_CURRENT_BINARY_DIR}
    )

    set_target_properties(SqrtLibrary PROPERTIES
        POSITION_INDEPENDENT_CODE ${BUILD_SHARED_LILBS}
    )

    target_link_libraries(MathFunctions PRIVATE SqrtLibrary)
endif()

# define the symbol stating we are using the declspec(sllexport) when
# building on windows
target_compile_definitions(MathFunctions PRIVATE "EXPORTING_MYMATH")

# does this system provide the log and exp functions?
# include(CheckCXXSourceCompiles)
# check_cxx_source_compiles("
#     #include <cmath>
#     int main(){
#         std::log(1.0);
#         return 0;
#     }
# " HAVE_LOG)

# check_cxx_source_compiles("
#     #include <cmath>
#     int main(){
#         std::exp(1.0);
#         return 0;
#     };
# " HAVE_EXP)

# if(HAVE_LOG AND HAVE_EXP)
#     target_compile_definitions(MathFunctions 
#     PRIVATE "HAVE_LOG" "HAVE_EXP")
# endif()

# install rule
set(installalbe_libs SqrtLibrary)
if(TARGET SqrtLibrary)
    list(APPEND installable_libs SqrtLibrary)
endif()

install(TARGETS ${installable_libs} DESTINATION lib)
install(FILES mathFunctions.h DESTINATION include)