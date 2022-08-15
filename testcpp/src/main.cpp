// A simple program that computes the square root of a number
#include <cmath>
// #include <cstdlib>
#include <iostream>
#include <string>
#include "TutorialConfig.h"
#include "Poco/Data/Session.h"
#include "Poco/Data/PostgreSQL/Connector.h"
#include "spdlog/spdlog.h"
#include <boost/lambda/lambda.hpp>


using namespace Poco::Data::Keywords;
using Poco::Data::Session;

// Test cppcheck 
void foo(int x)
{
    int buf[10];
    if (x == 1000)
        buf[x] = 0; // <- ERROR
}

void foo2(int x)
{
    int buf[10];
    buf[x] = 0; // <- ERROR
    if (x == 1000) {}
}

int main(int argc, char* argv[])
{
    // test boost
    // using namespace boost::lambda;
    // typedef std::istream_iterator<int> in;

    // std::for_each(
    //     in(std::cin), in(), std::cout << (_1 * 3) << " " );

    // test cppcheck
    char a[10];
    a[10]=0;

    // test Poco
    // Session session("PostgreSQL", "sample.db");
    foo(10);
    foo2(10);
    spdlog::info("Welcome to spdlog!");
    std::cout << "Hello" << std::endl;
    if (argc < 2) {
        // report version
        std::cout << argv[0] << " Version " << Tutorial_VERSION_MAJOR << "."
                    << Tutorial_VERSION_MINOR << std::endl;
        std::cout << "Usage: " << argv[0] << " number" << std::endl;
        return 1;
    }

    return 0;
}