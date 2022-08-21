#ifndef Demo_Logger_INCLUDE
#define Demo_Logger_INCLUDE

#include "spdlog/spdlog.h"
#include "spdlog/fmt/ostr.h"
#include "spdlog/sinks/basic_file_sink.h"
#include "spdlog/sinks/rotating_file_sink.h"

using std::string;
using std::ostream;

namespace Demo {
   class logger_setting 
   {
        friend ostream &operator<<(ostream &os, const logger_setting &c);
        public:
            logger_setting();
            void set_format();
            void set_pattern(string pattern){
                format_pattern = pattern; 
            };
            string get_pattern() const{
                return format_pattern;
            };
        protected:
            ~logger_setting();
        private:
            string format_pattern;
   }; 
}

#endif // Demo_Logger_INCLUDE