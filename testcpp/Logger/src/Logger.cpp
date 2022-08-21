#include "Demo/Logger.h"


namespace Demo {
    using spdlog::set_pattern;
    
    ostream &operator<<(ostream &os, const logger_setting &c)
    {
        os << "logger pattern: " << c.get_pattern();
        return os;
    }
    logger_setting::~logger_setting()
    {
    }
    void set_format(){
       set_pattern("%n %v");
    }
}
