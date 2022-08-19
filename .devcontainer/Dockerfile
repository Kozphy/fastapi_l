FROM ubuntu

WORKDIR /workspace
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa

#TODO: fix build too slow
RUN  apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        vim \
        nano \
        less \
        # g++-arm-linux-gnueabihf \
        cmake \
        git \
        libpq-dev \
        python3.10 \
        python3-dev \
        python3-pip


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN conan profile new default --detect --force
RUN conan profile update settings.compiler.libcxx=libstdc++11 default
# RUN pip install --editable .
