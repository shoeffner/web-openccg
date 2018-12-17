FROM openjdk:11-jdk

LABEL maintainer="Sebastian Höffner <shoeffner@tzi.de>"
LABEL description="A small webapp to parse sentences using the DiaSpace grammar (University of Bremen) with OpenCCG."
LABEL version="2.1"

ARG GRAMMAR_VERSION=master
ARG OPENCCG_LIB_VERSION=0.9.5
ARG OPENCCG_REPOSITORY=https://github.com/OpenCCG/openccg
ARG OPENCCG_VERSION=master
ARG WCCG_POOL_SIZE=3

EXPOSE 5000 8080

ENV OPENCCG_HOME /openccg
ENV PATH "${OPENCCG_HOME}/bin:$PATH"
ENV LD_LIBRARY_PATH "${OPENCCG_HOME}/lib:${LD_LIBRARY_PATH}"
ENV WCCG_POOL_SIZE=${WCCG_POOL_SIZE}

# Download and extract OpenCCG -- first for libraries, then the requested source-code version
RUN curl -o openccg-${OPENCCG_LIB_VERSION}.tgz https://datapacket.dl.sourceforge.net/project/openccg/openccg/openccg%20v${OPENCCG_LIB_VERSION}%20-%20deplen%2C%20kenlm%2C%20disjunctivizer/openccg-${OPENCCG_LIB_VERSION}.tgz \
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
# Install libraries etc.
    && apt-get update \
    && apt-get install -y python3 python3-pip graphviz libgraphviz-dev python-tk \
    && pip3 install flask \
                    uwsgi \
                    tatsu \
                    pygraphviz \
                    pexpect \
# Build OpenCCG
    && (cd /openccg && ccg-build)

COPY setup.py requirements.txt README.md /app/
COPY webopenccg /app/webopenccg/
COPY tests /tests

RUN pip3 install -e /app

CMD uwsgi --http :8080 \
          --uid www-data \
          --manage-script-name \
          --module webopenccg.webapp \
          --callable app \
          --master
