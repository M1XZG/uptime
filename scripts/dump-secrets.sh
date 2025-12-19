#!/bin/bash
# dump-secrets.sh
# Dumps all GitHub Actions secrets (set as env vars) to a file in KEY=VALUE format
# Intended to be run in a GitHub Actions workflow step

set -euo pipefail

# List of secret names to dump (edit as needed)
SECRETS=(

)

OUTFILE="secrets_dump.txt"

> "$OUTFILE"
for key in "${SECRETS[@]}"; do
  value="${!key:-}"
  echo "$key=$value" >> "$OUTFILE"
done

echo "Secrets dumped to $OUTFILE"
