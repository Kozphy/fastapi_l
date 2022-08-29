#ifndef Demo_Logger_INCLUDE
#define Demo_Logger_INCLUDE
// if not define SPDLOG_LEVEL_DEBUG, all DEBUG/TRACE statements will be removed by the pre-processor.
// default SPDLOG_LEVEL is INFO.
#define SPDLOG_ACTIVE_LEVEL SPDLOG_LEVEL_DEBUG 

#include <iostream>
#include <string_view>
#include <map>
#include <vector>
#include <fmt/core.h>
#include "spdlog/spdlog.h"
#include "spdlog/fmt/ostr.h"
#include "spdlog/sinks/rotating_file_sink.h"
#include "spdlog/sinks/stdout_color_sinks.h"



namespace Demo {
    enum class Level {
        TRACE = 0,
        DEBUG = 1,
        INFO = 2,
        WARN = 3,
        ERROR = 4,
        CRITICAL = 5,
        OFF = 6
    };

    class logger_setting 
    {
            friend std::ostream &operator<<(std::ostream &os, const logger_setting &c);
            public:
                explicit logger_setting(std::string logger_name, 
                                        Level logger_level = Level::INFO,
                                        unsigned int max_size = 1024 * 1024 * 5, 
                                        unsigned int max_files = 3);
                // ~logger_setting();


                // setter
                inline void set_pattern(const std::string_view &pattern)
                {
                    this -> format_pattern = pattern; 
                    set_spdlog_pattern();
                };

                inline void set_level(const Level &level)
                {
                    this -> logger_level = level;
                    set_spdlog_level();
                }

                inline void set_max_size(const unsigned int &size){
                   max_size = size; 
                };

                inline void set_max_files(const unsigned int &nums){
                    max_files = nums;
                };

                // getter
                inline std::weak_ptr<spdlog::logger> get_logger() const {
                    return _logger;
                };

                inline std::string_view get_logger_name() const{
                    return logger_name;
                };

                inline Level get_logger_level() const {
                    return logger_level;
                }

                inline std::string_view get_pattern() const{
                    return format_pattern;
                };

                unsigned int get_max_size() const {
                    return max_size;
                };

                unsigned int get_max_files() const {
                    return max_files;
                };

            protected:
                void set_spdlog_pattern();
                void set_spdlog_level();
            private:
                std::weak_ptr<spdlog::logger> _logger;
                std::string logger_name;
                std::string logger_file_name;
                Level logger_level = Level::INFO;
                std::string format_pattern = "[%@] [%!] %^[%l]%$: %v";
                std::string logger_dir_dsn = "logs";
                std::string logger_file_dsn;
                unsigned int max_size;
                unsigned int max_files;
    };
}

#endif // Demo_Logger_INCLUDE