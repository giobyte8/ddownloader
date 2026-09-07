FROM python:3.12-alpine
WORKDIR /opt/ddownloader

# NOTE> For ADD/COPY instructions below, let's assume build context
#   is the app's root folder

# Install dependencies and run app
COPY requirements.txt /opt/ddownloader/requirements.txt
RUN apk add --no-cache tzdata ffmpeg && pip install -r requirements.txt

COPY ddownloader /opt/ddownloader/ddownloader
COPY otelw.sh /opt/ddownloader/otelw.sh

ENTRYPOINT ["/bin/sh",  "otelw.sh"]
