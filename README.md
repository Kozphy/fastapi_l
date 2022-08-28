
# build datacpp
```bash
mkdir build && cd build
conan install .. --install-folder cmake-build-release [--build=missing]
cmake ..
cmake --build .
```