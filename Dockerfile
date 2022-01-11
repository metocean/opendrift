FROM python:3.8-buster

RUN apt update && \
    apt install -y libeccodes-dev libeccodes0 libproj-dev proj-bin libgeos-dev && \
    apt -y upgrade && \
    apt clean

RUN pip install -U pip Cython numpy
        # upgrade pip to reduce warnings
RUN pip install \
        # OilLibrary requires
        zope.sqlalchemy\<1.1\
        sqlalchemy\<1.4\
        # opendrift-landmask-data requires
        future\
        # opendrift requires
        cfgrib \
        cartopy \
        coloredlogs \
        Cython\
        dask\<2021.03 \
        eccodes \
        ffmpeg \
        pysolar \
        geojson \
        motuclient \
        nc_time_axis \
        pytest-benchmark\
        toolz\
        xarray\<0.20.0\
        xhistogram==0.1.2 \
        shapely\
        --no-binary shapely \
        --no-binary cartopy\
        &&\
    # We do this because we don't trust setup.py install_requires
    pip install -r https://raw.githubusercontent.com/OpenDrift/OilLibrary/master/requirements.txt &&\
    pip install -r https://raw.githubusercontent.com/OpenDrift/opendrift-landmask-data/master/requirements.txt

ADD . /source/opendrift

RUN pip install -r /source/opendrift/requirements.txt &&\
    pip install /source/opendrift/
