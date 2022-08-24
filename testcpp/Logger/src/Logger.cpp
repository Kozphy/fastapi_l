#include "Demo/Logger.h"


namespace Demo {
    using spdlog::set_pattern;
    
    ostream &operator<<(ostream &os, const logger_setting &c)
    {
        os << "logger name: " << c.get_logger_name()
        << ",err logger name: " <<  c.get_err_logger_name()
        <<",logger pattern: " << c.get_pattern()
        << ",logger file size: " << c.get_max_size()
        << ",logger max files: " << c.get_max_files();

        return os;
    }
    
    logger_setting::logger_setting(string logger_name, unsigned int max_size , unsigned int max_files)
    {
        try
        {
            // map<variant<unsigned int, string>, variant<unsigned int, string>> logger_setting_member{
            //     {this -> max_size, max_size},
            //     {"max_files", max_files},
            //     {"logger_name", logger_name},
            //     {"logger_file_name", fmt::format("{0}_file", logger_name)},
            //     {"err_logger_name", fmt::format("{0}_stderr", logger_name)},
            //     {"logger_dsn", fmt::format("{0}/{1}", this -> logger_dir_dsn, logger_name)},
            //     {"err_logger_dsn", fmt::format("{0}/{1}", this -> logger_dir_dsn, this -> err_logger_name)}
            // };

            // for (const auto& [k, v]: logger_setting_member)
            // {
            //     this -> k = get<>(v)
            // }
            // TODO: need refactor
            this -> max_size = max_size;
            this -> max_files = max_files;
            this -> logger_name = logger_name;
            this -> err_logger_name = fmt::format("{0}_stderr", logger_name);
            this -> logger_dsn = fmt::format("{0}/{1}", this -> logger_dir_dsn, logger_name);
            this -> logger_file_name = fmt::format("{0}.txt", logger_name);

            // destribute log message
            // TODO: complete
            auto dist_sink = make_shared<spdlog::sinks::dist_sink_st>();
            auto console = make_shared<spdlog::sinks::stdout_color_sink_mt>(logger_name);
            auto err_console = make_shared<spdlog::sinks::stderr_color_sink_mt>(err_logger_name);
            auto file_console = make_shared<spdlog::sinks::rotating_file_sink_mt>(logger_file_name, max_size, max_files);
            dist_sink -> add_sink(console);
            dist_sink -> add_sink(err_console);
            dist_sink -> add_sink(file_console);

            // console logger
            // auto console = spdlog::stdout_color_mt(logger_name);
            // auto err_console = spdlog::stderr_color_mt(err_logger_name);

            // file logger
            // auto console_file = spdlog::rotating_logger_mt(logger_name, logger_dsn, max_size, max_files);
            _logger = spdlog::get(logger_name);
            _logger_err = spdlog::get(this -> err_logger_name);
            set_spdlog_pattern();
        }
        catch(const spdlog::spdlog_ex& ex)
        {
            cout << "Log init failed: " << ex.what() << endl;
        }
    }

    void logger_setting::set_spdlog_pattern()
    {
        _logger -> set_pattern(this -> format_pattern);
        _logger_err -> set_pattern(this -> format_pattern);
        
    }

    logger_setting::~logger_setting()
    {
    }
}
