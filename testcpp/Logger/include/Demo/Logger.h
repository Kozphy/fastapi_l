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
    class logger_setting 
    {
            friend ostream &operator<<(ostream &os, const logger_setting &c);
            public:
                explicit logger_setting();
                ~logger_setting();

                // setter
                void set_format();
                void set_pattern(string pattern){
                    format_pattern = pattern; 
                };
                void set_max_size(unsigned int size){
                   max_size = size; 
                };
                void set_max_files(unsigned int nums){
                    max_files = nums;
                }

                // getter
                string get_logger_name() const{
                    return logger_name;
                };
                string get_pattern() const{
                    return format_pattern;
                };

                unsigned int get_max_size() const {
                    return max_size;
                };

                unsigned int get_max_files() const {
                    return max_files;
                };

            // protected:
            private:
                string logger_name;
                string format_pattern;
                shared_ptr<spdlog::logger> _logger;
                unsigned int max_size = 1024 * 1024 * 5;
                unsigned int max_files = 3;
    }; 
}

#endif // Demo_Logger_INCLUDE