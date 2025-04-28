# Resets development database
# Usage: ./db/reset.sh
#
# This script will drop the database, create a new one, and run migrations
# It will also seed the database with initial data

# ref: https://stackoverflow.com/a/4774063/3211029
SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
CALLER_PATH="${pwd}"

SCHEMA_SCRIPT="schema.sql"
SEED_SCRIPT="dev_data.sql"

# Prepare environment variables
cd "${SCRIPT_PATH}/.."
source .env
PG_IMAGE="postgres:14.6-alpine"
DB_HOST="host.docker.internal"


error_exit() {
  echo "Error: $1" >&2
  exit 1
}

# Check if Docker is installed
command -v docker >/dev/null 2>&1 || {
  echo "Docker is required, but not installed." >&2
  exit 1
}

# Check if psql is installed in the docker image
docker run --rm $PG_IMAGE psql --version >/dev/null 2>&1 || {
  echo "psql is required in the docker image ($PG_IMAGE), but not available." >&2
  exit 1
}

# Drop the database (if it exists)
echo "Dropping database: $DB_NAME"
docker run --rm -i \
  -e PGPASSWORD="$DB_PASSWORD" \
  $PG_IMAGE \
  psql -v ON_ERROR_STOP=1 \
       -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d "postgres" \
       -c "DROP DATABASE IF EXISTS $DB_NAME;" || error_exit "Failed to drop database."

# Create the database
echo "Creating database: $DB_NAME"
docker run --rm -i \
  -e PGPASSWORD="$DB_PASSWORD" \
  $PG_IMAGE \
  psql -v ON_ERROR_STOP=1 \
       -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d "postgres" \
       -c "CREATE DATABASE $DB_NAME;" || error_exit "Failed to create database."

# Run the schema script
echo "Running schema script: $SCHEMA_SCRIPT"
docker run --rm -i \
  -v "$(pwd)/db:/scripts" \
  -e PGPASSWORD="$DB_PASSWORD" \
  $PG_IMAGE \
  psql -v ON_ERROR_STOP=1 \
       -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d "$DB_NAME" \
       -f "/scripts/$SCHEMA_SCRIPT" || error_exit "Failed to run schema script."

# Run the seed data script
echo "Running seed data script: $SEED_SCRIPT"
docker run --rm -i \
  -v "$(pwd)/db:/scripts" \
  -e PGPASSWORD="$DB_PASSWORD" \
  $PG_IMAGE \
  psql -v ON_ERROR_STOP=1 \
       -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d "$DB_NAME" \
       -f "/scripts/$SEED_SCRIPT" || error_exit "Failed to run seed data script."


cd "${CALLER_PATH}"
echo "Database setup complete."
exit 0
