#!/bin/bash
# dump-secrets.sh
# Dumps all GitHub Actions secrets (set as env vars) to a file in KEY=VALUE format
# Intended to be run in a GitHub Actions workflow step

set -euo pipefail


# Read secret names from 'my-secrets' file (one per line)
SECRETS=()
if [[ -f "my-secrets" ]]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^# ]] && continue  # skip empty lines and comments
    SECRETS+=("$line")
  done < my-secrets
else
  echo "my-secrets file not found!" >&2
  exit 1
fi

OUTFILE="secrets_dump.txt"

> "$OUTFILE"
for key in "${SECRETS[@]}"; do
  value="${!key:-}"
  echo "$key=$value" >> "$OUTFILE"
done

echo "Secrets dumped to $OUTFILE"
