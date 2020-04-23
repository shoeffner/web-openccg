FROM openjdk:11-jdk-slim

LABEL maintainer="Sebastian Höffner <shoeffner@tzi.de>"
LABEL description="A small webapp to parse sentences using the DiaSpace grammar (University of Bremen) with OpenCCG."
LABEL version="2.2"

ARG GRAMMAR_VERSION=master
ARG OPENCCG_LIB_VERSION=0.9.5
ARG OPENCCG_REPOSITORY=https://github.com/OpenCCG/openccg
ARG OPENCCG_VERSION=master
ARG WCCG_POOL_SIZE=3

EXPOSE 5000 8080

ENV OPENCCG_HOME=/openccg
ENV PATH="${OPENCCG_HOME}/bin:$PATH" \
    LD_LIBRARY_PATH="${OPENCCG_HOME}/lib:/usr/local/lib:${LD_LIBRARY_PATH}" \
    LDFLAGS="-L/usr/local/lib/python3.7/config-3.7m-x86_64-linux-gnu" \
    WCCG_POOL_SIZE=${WCCG_POOL_SIZE}

# Install libraries etc.
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        curl \
        graphviz \
        libc-dev \
        libgraphviz-dev \
        python \
        unzip \
    && apt-get clean \
# Download and extract OpenCCG -- first for libraries, then the requested source-code version
    && curl -o openccg-${OPENCCG_LIB_VERSION}.tgz https://iweb.dl.sourceforge.net/project/openccg/openccg/openccg%20v${OPENCCG_LIB_VERSION}%20-%20deplen%2C%20kenlm%2C%20disjunctivizer/openccg-${OPENCCG_LIB_VERSION}.tgz \
    && tar zxf openccg-${OPENCCG_LIB_VERSION}.tgz \
    && rm openccg-${OPENCCG_LIB_VERSION}.tgz \
# Source code overwrites
    && curl -o openccg.zip -L ${OPENCCG_REPOSITORY}/archive/${OPENCCG_VERSION}.zip \
    && unzip openccg.zip \
    && rm openccg.zip \
    && cp -r openccg-*/* /openccg/ \
    && rm -r openccg-* \
# Download and extract grammar
    && curl -o grammar.zip -L https://github.com/shoeffner/openccg-gum-cooking/archive/${GRAMMAR_VERSION}.zip \
    && unzip -d /tmp grammar.zip \
    && mv /tmp/openccg-gum-cooking-*/english-cooking /grammar \
    && rm grammar.zip \
    && rm -rf /tmp/openccg-gum-cooking-* \
# Download viz.js
    && mkdir -p /app/webopenccg/static \
    && curl -L -o /app/webopenccg/static/viz.js https://github.com/mdaines/viz.js/releases/download/v2.0.0/viz.js \
    && curl -L -o /app/webopenccg/static/lite.render.js https://github.com/mdaines/viz.js/releases/download/v2.0.0/lite.render.js \
# Build OpenCCG
    && (cd /openccg && ccg-build)

# "Install" Python 3, replacing Python 2
COPY --from=python:3.7-slim \
     /usr/local/bin/python \
     /usr/local/bin/python3 \
     /usr/local/bin/python3.7 \
     /usr/local/bin/pip \
     /usr/local/bin/pip3 \
     /usr/local/bin/pip3.7 \
     /usr/local/bin/
COPY --from=python:3.7-slim \
     /usr/local/include/python3.7m \
     /usr/local/include/python3.7m
COPY --from=python:3.7-slim \
     /usr/local/lib/libpython3.7m.so.1.0 \
     /usr/local/lib/
COPY --from=python:3.7-slim \
     /usr/local/lib/python3.7 \
     /usr/local/lib/python3.7
ENV PYTHONHOME=/usr/local

COPY setup.py requirements.txt README.md /app/
COPY webopenccg /app/webopenccg/
COPY tests /tests

# Install app dependencies
RUN pip3 install -r /app/requirements.txt \
    && pip3 install uwsgi \
    && pip3 install -e /app

CMD uwsgi --http :8080 \
          --uid www-data \
          --manage-script-name \
          --module webopenccg.webapp \
          --callable app \
          --master
