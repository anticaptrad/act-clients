#!/usr/bin/env sh
set -eu
base=${ACT_BASE_URL:?set ACT_BASE_URL}
path=${1:-/health}
curl --fail --silent --show-error --location-trusted "${base%/}/${path#/}" -H 'accept: application/json'
