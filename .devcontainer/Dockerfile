FROM python:3.10

WORKDIR /workspace

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
       vim \
       nano \
       less \
       g++-arm-linux-gnueabihf \
       cmake

RUN conan profile new default --detect --force
RUN conan profile update settings.compiler.libcxx=libstdc++11 default
# RUN pip install --editable .
