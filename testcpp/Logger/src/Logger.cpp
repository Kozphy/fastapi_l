#include "Demo/Logger.h"


namespace Demo {
    using spdlog::set_pattern;
    
    inline ostream &operator<<(ostream &os, const logger_setting &c)
    {
        os << "logger name: " << c.get_logger_name()
        <<",logger pattern: " << c.get_pattern()
        << ",logger file size: " << c.get_max_size()
        << ",logger max files: " << c.get_max_files(); 

        return os;
    }

    logger_setting::logger_setting()
    {
        try
        {
            auto console = spdlog::stdout_color_mt(logger_name);
            auto err_logger = spdlog::stderr_color_mt(fmt::format("{0} stderr", logger_name));
            auto file_logger = spdlog::rotating_logger_mt(logger_name, "logs/rotating.txt",max_size, max_files);
            _logger = spdlog::get(logger_name);
        }
        catch(const spdlog::spdlog_ex& ex)
        {
            cout << "Log init failed: " << ex.what() << endl;
        }
        
    }


    logger_setting::~logger_setting()
    {
    }

    inline void logger_setting::set_format(){
       set_pattern(format_pattern);
    }
}
