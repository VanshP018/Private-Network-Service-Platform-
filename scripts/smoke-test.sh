#!/bin/bash
# Run from any CLIENT Mac once Tasks A-D are done, to sanity-check the
# whole chain before moving on to TLS (Task E).
# Usage: ./smoke-test.sh teamX.test

DOMAIN="${1:-teamX.test}"

echo "== 1. DNS resolution =="
dig +short "app.$DOMAIN"

echo ""
echo "== 2. HTTP through the load balancer (5 requests) =="
for i in 1 2 3 4 5; do
  curl -s "http://app.$DOMAIN/api/status"
  echo ""
done

echo ""
echo "== 3. Response headers (Cache-Control, X-Backend) =="
curl -sI "http://app.$DOMAIN/api/status"
