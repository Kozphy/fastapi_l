#ifndef Demo_Logger_INCLUDE
#define Demo_Logger_INCLUDE

#include <iostream>
#include <string_view>
#include <map>
// #include <variant>
#include <fmt/core.h>
#include <boost/foreach.hpp>
#include "boost/variant.hpp"
#include "spdlog/spdlog.h"
#include "spdlog/fmt/ostr.h"
#include "spdlog/sinks/basic_file_sink.h"
#include "spdlog/sinks/rotating_file_sink.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/dist_sink.h"



namespace Demo {
    using std::string;
    using std::string_view;
    using std::ostream;
    using std::shared_ptr;
    using std::cout;
    using std::endl;
    using std::make_shared;
    using std::map;
    using boost::variant;
    using boost::get;
    class logger_setting 
    {
            friend ostream &operator<<(ostream &os, const logger_setting &c);
            public:
                explicit logger_setting(string logger_name, 
                                        unsigned int max_size = 1024 * 1024 * 5, 
                                        unsigned int max_files = 3);
                ~logger_setting();


                // setter
                inline void set_pattern(const string_view &pattern){
                    this -> format_pattern = pattern; 
                    set_spdlog_pattern();
                };
                inline void set_max_size(unsigned int size){
                   max_size = size; 
                };
                inline void set_max_files(unsigned int nums){
                    max_files = nums;
                }

                // getter
                inline string get_logger_name() const{
                    return logger_name;
                };

                inline string get_err_logger_name() const{
                    return err_logger_name;
                };
                inline string get_pattern() const{
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
            private:
                shared_ptr<spdlog::logger> _logger;
                shared_ptr<spdlog::logger> _logger_file;
                shared_ptr<spdlog::logger> _logger_err;
                shared_ptr<spdlog::logger> _logger_err_file;
                string logger_name;
                string logger_file_name;
                string err_logger_name;
                string format_pattern = "%^ %@";
                string logger_dir_dsn = "logs";
                string logger_dsn;
                unsigned int max_size;
                unsigned int max_files;
    };
}

#endif // Demo_Logger_INCLUDE