FROM alpine:3.9

LABEL maintainer="ilanbowen@gmail.com"

RUN apk update && \
apk add --no-cache python3 py-pip && \
pip3 install Flask==1.0 && \
pip3 install Click==7.0 && \
pip3 install itsdangerous==1.1.0 && \
pip3 install Jinja2==2.10 && \
pip3 install MarkupSafe==1.1.1 && \
pip3 install Werkzeug==0.14.1

COPY . /src

WORKDIR /src

CMD ["python3", "./app.py"]