#ifndef Demo_Logger_INCLUDE
#define Demo_Logger_INCLUDE

#include <iostream>
#include <fmt/core.h>
#include "spdlog/spdlog.h"
#include "spdlog/fmt/ostr.h"
#include "spdlog/sinks/basic_file_sink.h"
#include "spdlog/sinks/rotating_file_sink.h"
#include "spdlog/sinks/stdout_color_sinks.h"

using std::string;
using std::ostream;
using std::shared_ptr;
using std::cout;
using std::endl;

namespace Demo {
    template<typename log_size, typename log_file>
    class logger_setting 
    {
            friend ostream &operator<<(ostream &os, const logger_setting<log_size, log_file> &c);
            public:
                logger_setting();
                void set_format();
                void set_pattern(string pattern){
                    format_pattern = pattern; 
                };

                string get_logger_name() const{
                    return logger_name;
                };
                string get_pattern() const{
                    return format_pattern;
                };

                log_size get_max_size() const {
                    return max_size;
                };

                log_file get_max_files() const {
                    return max_files;
                };

            protected:
                ~logger_setting();
            private:
                string logger_name;
                string format_pattern;
                shared_ptr<spdlog::logger> _logger;
                log_size max_size;
                log_file max_files;
    }; 
}

#endif // Demo_Logger_INCLUDE