FROM openjdk:11-jdk

LABEL maintainer="Sebastian Höffner <shoeffner@tzi.de>"
LABEL description="A small webapp to parse sentences using the DiaSpace grammar (University of Bremen) with OpenCCG."
LABEL version="2.0"

# EXPOSE 80

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
# Server software: python 3, uwsgi; TatSu to parse the OpenCCG output
    && apt-get update \
    && apt-get install -y python3 python3-pip \
    && pip3 install flask uwsgi tatsu

COPY app /app
COPY tests /tests

# Run Flask app behind nginx
WORKDIR /app
CMD uwsgi --http :8080 \
          --uid www-data \
          --manage-script-name \
          --module ccgapp \
          --callable app \
          --master
