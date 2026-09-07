FROM python:3.12-alpine
WORKDIR /opt/ddownloader


# For ADD/COPY instructions below, let's assume build context
# is the app's root folder

COPY ddownloader /opt/ddownloader/ddownloader
COPY otelw.sh /opt/ddownloader/otelw.sh
COPY requirements.txt /opt/ddownloader/requirements.txt


# Install dependencies and run app
RUN apk add --no-cache tzdata ffmpeg && pip install -r requirements.txt
ENTRYPOINT ["/bin/sh",  "otelw.sh"]
