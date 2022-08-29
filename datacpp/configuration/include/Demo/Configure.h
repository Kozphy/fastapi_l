#ifndef CONFIGURE_H
#define CONFIGURE_H

#include <iostream>
#include <string>
#include "BasicConfig.h"
#include <fmt/core.h>
#include <boost/predef.h>
#include <boost/filesystem.hpp>
#include <Demo/Logger.h>

namespace Demo{

    class Configure
    {
        public:
            Configure();
            // getter
            boost::filesystem::path get_yaml_dsn(){
                return yaml_dsn.native();
            };
            // setter
            void set_yaml_dsn();
        private:
            constexpr auto os;
            boost::filesystem::path yaml_dsn;
            
       

    };

}

#endif // CONFIGURE_H