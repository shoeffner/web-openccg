FROM openjdk:11-jdk

LABEL maintainer="Sebastian Höffner <shoeffner@tzi.de>"
LABEL description="A small webapp to parse sentences using the DiaSpace grammar (University of Bremen) with OpenCCG."
LABEL version="2.1"

EXPOSE 5000 8080

ENV OPENCCG_HOME /openccg
ENV PATH "$OPENCCG_HOME/bin:$PATH"
ENV LD_LIBRARY_PATH "$OPENCCG_HOME/lib:$LD_LIBRARY_PATH"

# Download and extract OpenCCG
RUN curl -o openccg-0.9.5.tgz https://datapacket.dl.sourceforge.net/project/openccg/openccg/openccg%20v0.9.5%20-%20deplen%2C%20kenlm%2C%20disjunctivizer/openccg-0.9.5.tgz \
    && tar zxf openccg-0.9.5.tgz \
    && rm openccg-0.9.5.tgz \
# Download and extract grammar
    && curl -O http://www.diaspace.uni-bremen.de/twiki/pub/DiaSpace/ReSources/english.zip \
    && unzip -d /english english.zip \
    && rm english.zip \
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
