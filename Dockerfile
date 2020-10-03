# Version: 0.0.1
FROM heroku/heroku:18-build

# INSTALL ALL
RUN apt-get update  \
&& apt-get install -y  \
    build-essential \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config  \
    libavcodec-dev \ 
    libavformat-dev  \
    libswscale-dev \
    libtbb2  \
    libtbb-dev \ 
    libjpeg-dev \
    libpng-dev  \
    libtiff-dev  \
    libdc1394-22-dev \
    python-dev  \
    python-numpy



# DOWNLOAD opencv. since 3.4.2 still contains opencv_contrib modules
# we don't need to download any extra more
ENV OPENCV_VER 3.4.2

RUN git clone https://github.com/opencv/opencv.git \
    && cd opencv \
    && git checkout ${OPENCV_VER} \
    && mkdir build

WORKDIR "opencv/build"

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D PYTHON_EXECUTABLE=/usr/bin/python \
    -D BUILD_EXAMPLES=ON ..

RUN make
RUN make install
ENV LD_LIBRARY_PATH /usr/local/lib


# INSTALL PIP and python libraries for opencv
RUN apt -y install python-pip \
    && pip install opencv-python==3.4.2.17 \
    && pip install opencv-contrib-python==3.4.2.17


# Construct buildpack for heroku
ENV HOME /root
WORKDIR $HOME

RUN mkdir .heroku \
    && mkdir .heroku/vendor \
    && cp -r /usr/local/bin .heroku/vendor/ \
    && cp -r /usr/local/include .heroku/vendor/ \
    && cp -r /usr/local/man .heroku/vendor/ \
    && cp -r /usr/local/share .heroku/vendor/ \
    && cp -r /usr/local/lib .heroku/vendor/ \
    && cp -r /usr/lib/lib* .heroku/vendor/lib/ \
    && cp -r /usr/lib/x86_64-linux-gnu/lib* .heroku/vendor/lib/

# Clean buildpack
# RUN rm -rf .heroku/vendor/lib/python*
RUN rm .heroku/vendor/lib/libicudata* 
RUN rm .heroku/vendor/lib/libLLVM*

RUN tar -czvf "heroku18-buildpack-opencv${OPENCV_VER}.tar.gz" .heroku

CMD ["true"]
