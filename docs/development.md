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