#!/bin/bash
# test_flow.sh: End-to-end test for local BeeAI stack
set -euo pipefail

# Wait for health endpoints
wait_for_health() {
  local name="$1"; local port="$2"
  echo "Waiting for $name on port $port..."
  for i in {1..30}; do
    if curl -sf http://localhost:$port/healthz > /dev/null; then
      echo "$name is healthy."
      return 0
    fi
    sleep 2
done
  echo "$name failed to become healthy!" >&2
  exit 1
}

wait_for_health contextagent 8081
wait_for_health validator 8082

# Start a RabbitMQ consumer to check for validation.completed event
RECEIVED=$(docker run --rm --network host --entrypoint sh rabbitmq:3-management -c '
  rabbitmqadmin -u beeai -p beeai_pass get queue=beeai_validator_events requeue=false | grep validation.completed || true
')

if [[ "$RECEIVED" == *validation.completed* ]]; then
  echo "✅ End-to-end flow succeeded: validation.completed event received."
  exit 0
else
  echo "❌ End-to-end flow failed: validation.completed event not found."
  exit 1
fi
