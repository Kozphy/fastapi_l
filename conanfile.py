from conans import ConanFile, CMake


class Conan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = [
        "boost/1.79.0",
        "poco/1.12.2",
        "cppcheck/2.7.5",
        "spdlog/1.10.0",
        "fmt/9.0.0",
        "cli11/2.2.0",
        "yaml-cpp/0.7.0",
        "protobuf/3.21.4",  # comma-separated list of requirements
    ]
    generators = [
        "cmake_find_package",
        "cmake_paths",
        "CMakeDeps",
        "CMakeToolchain",
    ]
    default_options = {
        "poco:shared": False,
        "poco:shared": False,
        "fmt:shared": False,
        "spdlog:shared": False,
    }
    build_policy = "missing"

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")  # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib")  # From lib to bin

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
