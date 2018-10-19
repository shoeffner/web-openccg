FROM nginx:1.15.5-alpine

LABEL maintainer="Sebastian Höffner <shoeffner@tzi.de>"
LABEL description="nginx instance to serve OpenCCG and the OpenCCG.ebnf"
LABEL version="1.0"

EXPOSE 80

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY OpenCCG.ebnf /OpenCCG.ebnf
