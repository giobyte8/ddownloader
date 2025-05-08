#!/bin/bash
# OpenTelemetry Wrapper
# Runs the application using the zero-code instrumentation approach
# and sends telemetry data to the OpenTelemetry Collector.

# ref: https://stackoverflow.com/a/4774063/3211029
HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$HERE"
source ".env"


if [ "$OTEL_ENABLED" = "true" ]; then
  echo "Starting 'ddownloader' with otel instrumentation..."
  echo "  OTEL_SERVICE_NAME: $OTEL_SERVICE_NAME"
  echo "  OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: $OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"
  echo

  opentelemetry-instrument \
    --service_name $OTEL_SERVICE_NAME \
    python ddownloader/main.py
else
  echo "OpenTelemetry is disabled, Starting 'ddownloader' without instrumentation..."
  echo

  python ddownloader/main.py
fi
