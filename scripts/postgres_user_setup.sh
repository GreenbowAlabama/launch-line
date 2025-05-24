#!/bin/bash
# postgres_user_setup.sh
# Usage: ./postgres_user_setup.sh <PGPASSWORD>

set -e

# Required ENV VARS (set via Kubernetes Secret or manually passed)
DB_HOST="launch-lab-db.postgres.database.azure.com"
DB_PORT="5432"
DB_NAME="launch_lab"
DB_USER="launch_admin"
DB_PASSWORD="$1"
ADMIN_EMAIL="admin@launch-labs.io"

# Pre-generated valid bcrypt hash for password 'changeme'
ADMIN_PASSWORD_HASH='$2b$12$gB8uTWy0zCGHEW/Vw0R5c.tHKqKAgvW33I0loXjK9grydhzOFCpXK'

SQL_COMMANDS=$(cat <<EOF
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

INSERT INTO users (email, password_hash)
VALUES ('$ADMIN_EMAIL', '$ADMIN_PASSWORD_HASH')
ON CONFLICT (email) DO NOTHING;
EOF
)

# Run using a temporary Postgres client container
kubectl run psql-init --rm -i --tty --restart=Never \
  --env PGPASSWORD="$DB_PASSWORD" \
  --image=postgres \
  --command -- psql \
  -h "$DB_HOST" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  -p "$DB_PORT" \
  -c "$SQL_COMMANDS"