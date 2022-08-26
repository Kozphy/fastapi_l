// A simple program that computes the square root of a number
#include <cmath>
// #include <cstdlib>
#include <iostream>
#include <string>
#include <boost/smart_ptr/shared_ptr.hpp>
#include <boost/smart_ptr/make_shared.hpp>
#include <boost/filesystem.hpp>
#include "BasicConfig.h"
#include "Poco/Data/Session.h"
#include "Poco/Data/PostgreSQL/Connector.h"
#include "Poco/Data/DataException.h"
#include "Demo/Logger.h"
// #include "config.pb.h"
#include "yaml-cpp/yaml.h"

//TODO: wait for stable cmake with gcc c++ 20 modules support.
// import Example;

using std::cout;
using std::cerr;
using std::endl;
using std::vector;
using std::string;
namespace poco_data_keywords = Poco::Data::Keywords;
using Poco::Data::Session;
using Poco::Data::Statement;
using Poco::Data::DataException;
using Demo::logger_setting;
using boost::shared_ptr;
using boost::make_shared;
using namespace boost::filesystem;




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
        auto pLogger1 = make_shared<logger_setting>("test", 0);
        // std::cout << *pLogger1 << std::endl;

        SPDLOG_INFO("start search config file");
        path config_path("/workspace/testcpp/configuration/config.yaml");
        path p;
        // if(exists(config_path)){
        //     if(is_regular_file(config_path))
        //         cout << config_path << " size is: " << file_size(config_path) << "\n";
        //     else if(is_directory(config_path))
        //     {
        //         cout << config_path << " is a directory containing:\n";
        //         vector<path> v;
        //         for (auto&& x : directory_iterator(config_path)){
        //             v.push_back(x.path());
        //         }

        //         // std::sort(v.begin(), v.end());
        //         for(auto&& x : v){
        //             cout << "   " << x.filename() << "\n";
        //             cout << "   " << x << "\n";
        //         }
        //         // for (directory_entry& x : directory_iterator(config_path))
        //         //     cout << "   " << x.path() << "\n";
        //     }
        //     else
        //         cout << config_path << " exists, but is not a regular file or directory\n";
        // }
        // else
        // {
        //     cout << config_path << " does not exist\n";
        // }
        cout << "current path: " << current_path() << endl;

        SPDLOG_INFO("start session");
        if(exists(config_path)){
            YAML::Node config = YAML::LoadFile(config_path.string());
            if(config["persistence"]["db"]){
                std::cout << "db: " << config["persistence"]["db"].as<string>() << std::endl;;
            }
        }
        string db_setting = "host=localhost;port=5432;db=test;user=zixas";
        Poco::Data::PostgreSQL::Connector::registerConnector();
        Session session(db_setting);
    }

    catch(DataException &e)
    {
        SPDLOG_ERROR("error");
        cerr << e.message() << endl;
        return 1;
    }

    catch (const filesystem_error& ex)
    {
        SPDLOG_ERROR("error");
        cout << ex.what() << '\n';
    }



    return 0;
}