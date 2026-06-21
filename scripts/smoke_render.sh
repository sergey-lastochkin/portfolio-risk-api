#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 https://your-service.onrender.com" >&2
    exit 2
fi

base_url=${1%/}

echo "Checking ${base_url}/health"
curl --fail --silent --show-error "${base_url}/health"
printf '\n'

echo "Checking ${base_url}/metadata"
curl --fail --silent --show-error "${base_url}/metadata"
printf '\n'
