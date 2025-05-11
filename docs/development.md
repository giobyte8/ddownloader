# DDownloader development
1. [Local setup](#local-setup)
2. [Telemetry](#telemetry)
3. [Release process](#release-process)

## Local setup

### Python virtual env

DDownloader development is done on **Python >= 3.12**. Make sure you're using a valid virtual env.

```shell
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Virtual env management through mise

If you're using [mise](https://mise.jdx.dev), then, virtual env setup can be automated by navigating to project root.

TODO: Include instructions for mise usage

### Config files and env variables

Setup your env files and config

```shell
cp template.env .env
vim .env

cp config/gdl-base.template.json config/gdl-base.json
vim config/gdl-base.json
```

### Database setup

Use scripts under `db/` dir to create schema and seed some development data into `ddownloader` database. If connection params are present in `.env` file you can use the `reset.sh` script to create schema and seed dev data automatically.

```shell
./db/reset.sh
```

### Run unit tests

...

### Run service

From project root you can directly execute the main entry point

```shell
python ddownloader/main.py
```

> If you need to generate telemetry data in development see the instructions in [telemetry section](#telemetry)

## Telemetry

The service includes support to generate and export telemetry data (traces and metrics) by using [Open telemetry](https://opentelemetry.io). This is configurable and the application can run with or without telemetry enabled.

### Configure telemetry

Telemetry can be enabled/disabled and configured via`OTEL_*` prefixed variables in `.env` file

Some of the most relevant:

```shell
OTEL_ENABLED=true
OTEL_SERVICE_NAME=ddownloader
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=0.0.0.0:4317
```

Once otel is enabled via `OTEL_ENABLED=true`, make sure that you have a valid [collector](https://opentelemetry.io/docs/collector/) listening for telemetry data and use the right endpoint in `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` var

> See: [infra config](https://github.com/giobyte8/dotfiles/blob/master/apps/infra/docker-compose.yaml#L25) for preconfigured otel collector and jaeger containers for dev env

### Run service using otel wrapper script

Use the [otelw.sh]() script to start the service, it will take care of running with telemetry enabled or disabled based on the value of `OTEL_ENABLED` var

```shell
./otelw.sh
# Service will start with right configurations for telemetry
```

> Alternatively, you could start the application directly via `python ddownloader/main.py` and it will run without producing any telemetry.

## Release Process

When a new version is ready for release, follow below instructions to build and publish a new docker image.

> NOTE: Make sure to prepare docker builder to build [multi-arch images](https://giovanniaguirre.me/blog/docker_build_multiarch/) before building new image version

