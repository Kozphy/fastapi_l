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
#include "datacpp/configuration/config.pb.h"
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
// boost
using boost::shared_ptr;
using boost::make_shared;
using namespace boost::filesystem;

// This function fills in a Person message based on user input.
using namespace std;
void PromptForAddress(tutorial::Person* person) {
    cout << "Enter person ID number: ";
    int id;
    cin >> id;
    person->set_id(id);
    cin.ignore(256, '\n');

    cout << "Enter name: ";
    getline(cin, *person->mutable_name());

    cout << "Enter email address (blank for none): ";
    string email;
    getline(cin, email);
    if (!email.empty()) {
        person->set_email(email);
    }

    while (true) {
        cout << "Enter a phone number (or leave blank to finish): ";
        string number;
        getline(cin, number);
        if (number.empty()) {
        break;
        }

        tutorial::Person::PhoneNumber* phone_number = person->add_phones();
        phone_number->set_number(number);

        cout << "Is this a mobile, home, or work phone? ";
        string type;
        getline(cin, type);
        if (type == "mobile") {
        phone_number->set_type(tutorial::Person::MOBILE);
        } else if (type == "home") {
        phone_number->set_type(tutorial::Person::HOME);
        } else if (type == "work") {
        phone_number->set_type(tutorial::Person::WORK);
        } else {
        cout << "Unknown phone type.  Using default." << endl;
        }
    }
}





int main(int argc, const char* argv[])
{
    // Main function:  Reads the entire address book from a file,
    // adds one person based on user input, then writes it back out to the same
    // file.
    // Verify that the version of the library that we linked against is
    // compatible with the version of the headers we compiled against.
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    if (argc != 2) {
        cerr << "Usage:  " << argv[0] << " ADDRESS_BOOK_FILE" << endl;
        return -1;
    }

    tutorial::AddressBook address_book;

    {
        // Read the existing address book.
        fstream input(argv[1], ios::in | ios::binary);
        if (!input) {
        cout << argv[1] << ": File not found.  Creating a new file." << endl;
        } else if (!address_book.ParseFromIstream(&input)) {
        cerr << "Failed to parse address book." << endl;
        return -1;
        }
    }

    // Add an address.
    PromptForAddress(address_book.add_people());

    {
        // Write the new address book back to disk.
        fstream output(argv[1], ios::out | ios::trunc | ios::binary);
        if (!address_book.SerializeToOstream(&output)) {
        cerr << "Failed to write address book." << endl;
        return -1;
        }
    }

        // Optional:  Delete all global objects allocated by libprotobuf.
        google::protobuf::ShutdownProtobufLibrary();

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
        auto pLogger1 = boost::make_shared<logger_setting>("test", 0);
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