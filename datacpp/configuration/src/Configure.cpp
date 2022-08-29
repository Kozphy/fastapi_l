#include "Demo/Configure.h"

namespace Demo{

    Configure::Configure()
    {
        set_yaml_dsn();
    }

    void Configure::set_yaml_dsn()
    {

        this -> yaml_dsn = fmt::format("{0}/{1}/{2}/{3}", WORKSPACE_DIR, PROJECT_DIR_NAME, Demo_DEFAULT_CONFIG_DIR_NAME,Demo_DEFAULT_YAML_NAME);
        // debug in future
        #ifdef BOOST_POSIX_API
            SPDLOG_DEBUG(fmt::format("yaml_dsn posix native(): {0}",yaml_dsn.native()));
            SPDLOG_DEBUG(fmt::format("yaml_dsn posix generic_string(): {0}",yaml_dsn.generic_string()));
            this -> os = "POSIX";
        #else 
            SPDLOG_DEBUG(fmt::format("yaml_dsn windows native(): {0}", yaml_dsn.native()));
            SPDLOG_DEBUG(fmt::format("yaml_dsn windows generic_string(): {0}", yaml_dsn.generic_string()));
            this -> os = "windows";
        #endif
        // if (BOOST_OS_UNIX)
        // {
        //     this -> yaml_dsn = fmt::vformat({0}/{1}/{2}/{3}, WORKSPACE_DIR, PROJECT_DIR_NAME, Demo_DEFAULT_CONFIG_DIR_NAME,Demo_DEFAULT_YAML_NAME)
        // }
        // else if(BOOST_OS_WINDOWS)
        // {

        // }
        // this -> yaml_dsn(fmt::vformat({0}/{1}));
    }

}