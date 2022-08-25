// A simple program that computes the square root of a number
#include <cmath>
// #include <cstdlib>
#include <iostream>
#include <string>
#include "VersionConfig.h"
#include "Poco/Data/Session.h"
#include "Poco/Data/PostgreSQL/Connector.h"
#include "Poco/Data/DataException.h"
#include "Demo/Logger.h"
#include "boost/smart_ptr/shared_ptr.hpp"


//TODO: wait for stable cmake with gcc c++ 20 modules support.
// import Example;

using std::cerr;
using std::endl;
namespace poco_data_keywords = Poco::Data::Keywords;
using Poco::Data::Session;
using Poco::Data::Statement;
using Poco::Data::DataException;
using Demo::logger_setting;
using boost::shared_ptr;


int main(int argc, const char* argv[])
{

    if (argc < 2) {
        // report version
        std::cout << argv[0] << " Version " << Demo_VERSION_MAJOR << "."
                    << Demo_VERSION_MINOR << std::endl;
        std::cout << "Usage: " << argv[0] << " number" << std::endl;
        return 1;
    }

    try 
    {
        shared_ptr<logger_setting> pLogger1(new logger_setting("test", 0));
        std::cout << *pLogger1 << std::endl;
        SPDLOG_INFO("start session");
        Poco::Data::PostgreSQL::Connector::registerConnector();
        Session session("PostgreSQL", "sample.db");
    }

    catch(DataException &e)
    {
        SPDLOG_ERROR("error");
        cerr << e.message() << endl;
        return 1;
    }



    return 0;
}