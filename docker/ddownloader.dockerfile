FROM python:3.12-alpine
WORKDIR /opt/ddownloader


# For ADD/COPY instructions below, let's assume build context
# is the app's root folder

ADD ddownloader /opt/ddownloader/ddownloader
ADD otelw.sh /opt/ddownloader/otelw.sh
ADD requirements.txt /opt/ddownloader/requirements.txt


# Install dependencies and run app
RUN apk add --no-cache tzdata && pip install -r requirements.txt
ENTRYPOINT ["./otelw.sh"]
