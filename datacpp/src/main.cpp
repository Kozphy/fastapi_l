// std
#include <cmath>
// #include <cstdlib>
#include <iostream>
#include <string>
// boost
#include <boost/smart_ptr/shared_ptr.hpp>
#include <boost/smart_ptr/make_shared.hpp>
#include <boost/filesystem.hpp>
// Demo
#include "BasicConfig.h"
#include "Demo/Logger.h"
#include "Demo/Configure.h"
// #include "datacpp/configuration/config.pb.h"
// Poco
#include "Poco/Data/Session.h"
#include "Poco/Data/PostgreSQL/Connector.h"
#include "Poco/Data/DataException.h"
// yaml
#include "yaml-cpp/yaml.h"

//TODO: wait for stable cmake with gcc c++ 20 modules support.
// import Example;

// std
using std::cout;
using std::cerr;
using std::endl;
using std::vector;
using std::string;
// poco
namespace poco_data_keywords = Poco::Data::Keywords;
using Poco::Data::Session;
using Poco::Data::Statement;
using Poco::Data::DataException;
// demo
using Demo::logger_setting;
using Demo::Configure;
// boost
using boost::shared_ptr;
using boost::make_shared;
using namespace boost::filesystem;



int main(int argc, const char* argv[])
{
    // GOOGLE_PROTOBUF_VERIFY_VERSION;



    // Optional:  Delete all global objects allocated by libprotobuf.
    // google::protobuf::ShutdownProtobufLibrary();

////////////////////////////////////////////////////////////////////////////

    if (argc < 2) {
        // report version
        std::cout << argv[0] << " Version " << Demo_VERSION_MAJOR << "."
                    << Demo_VERSION_MINOR << std::endl;
        std::cout << "Usage: " << argv[0] << " number" << std::endl;
        return 1;
    }

    try 
    {
        auto pLogger1 = boost::make_shared<logger_setting>("test", Demo::Level::INFO);
        pLogger1 -> set_level(Demo::Level::DEBUG);

        SPDLOG_INFO("start search config file");
        auto p_config = boost::make_shared<Configure>();
        // path config_path();
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

        // SPDLOG_INFO("start session");
        // if(exists(config_path)){
        //     YAML::Node config = YAML::LoadFile(config_path.string());
        //     if(config["persistence"]["db"]){
        //         std::cout << "db: " << config["persistence"]["db"].as<string>() << std::endl;;
        //     }
        // }
        // string db_setting = "host=localhost;port=5432;db=test;user=zixas";
        // Poco::Data::PostgreSQL::Connector::registerConnector();
        // Session session(db_setting);
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