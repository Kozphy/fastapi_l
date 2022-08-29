#include "Demo/Logger.h"


namespace Demo {
    using std::string;
    using std::string_view;
    using std::ostream;
    using std::shared_ptr;
    using std::cout;
    using std::endl;
    using std::make_shared;
    using std::function;
    using std::map;
    using std::vector;
    using spdlog::set_pattern;
    
    ostream &operator<<(ostream &os, const logger_setting &c)
    {
        os << "{\n" << "\tlogger name: " << c.get_logger_name() << "," << "\n"
        << "\tlogger level: " << static_cast<int>(c.get_logger_level()) << "," << "\n"
        <<"\tlogger pattern: " << c.get_pattern()<< "," << "\n"
        << "\tlogger file size: " << c.get_max_size() << "," << "\n"
        << "\tlogger max files: " << c.get_max_files() << "\n}";

        return os;
    }
    
    logger_setting::logger_setting(string logger_name, Level logger_level, unsigned int max_size , unsigned int max_files)
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
            this -> logger_level = logger_level;
            this -> logger_name = logger_name;
            this -> logger_file_name = fmt::format("{0}.txt", logger_name);
            this -> logger_file_dsn = fmt::format("{0}/{1}", logger_dir_dsn, logger_file_name);

            
            vector<spdlog::sink_ptr> sinks{
                make_shared<spdlog::sinks::stdout_color_sink_mt>(),
                make_shared<spdlog::sinks::rotating_file_sink_mt>(logger_file_dsn, max_size, max_files)
            };

            auto combined_logger = make_shared<spdlog::logger>(logger_name, begin(sinks), end(sinks));
            // Note:: if manually created logger, have to register_logger, otherwise will be segement fault.
            spdlog::register_logger(combined_logger);
            spdlog::set_default_logger(combined_logger);

            // if use spdlog::get you need to be careful segement fault here.
            // _logger = spdlog::get(logger_name);
            this -> _logger = combined_logger;
            set_spdlog_pattern();
            set_spdlog_level();
        }
        catch(const spdlog::spdlog_ex& ex)
        {
            cout << "Log init failed: " << ex.what() << endl;
        }
    }

    void logger_setting::set_spdlog_level()
    {
        auto spdlog_level = spdlog::level::info;
        /* In spdlog/common.h spdlog::level
            #define SPDLOG_LEVEL_TRACE 0
            #define SPDLOG_LEVEL_DEBUG 1
            #define SPDLOG_LEVEL_INFO 2
            #define SPDLOG_LEVEL_WARN 3
            #define SPDLOG_LEVEL_ERROR 4
            #define SPDLOG_LEVEL_CRITICAL 5
            #define SPDLOG_LEVEL_OFF 6
        */
        switch(this -> logger_level){
            case Level::INFO:
                SPDLOG_INFO("verbose level set to info");
                break;
            case Level::DEBUG:
                spdlog_level = spdlog::level::debug;
                SPDLOG_INFO("verbose level set to debug");
                break;
            case Level::TRACE:
                spdlog_level = spdlog::level::trace;
                SPDLOG_INFO("verbose level set to trace");
                break;
        }
        _logger.lock() -> set_level(spdlog_level);
    }
    void logger_setting::set_spdlog_pattern()
    {
        _logger.lock() -> set_pattern(this -> format_pattern);
    }

    // logger_setting::~logger_setting()
    // {
    // }
}
