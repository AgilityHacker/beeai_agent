#!/bin/bash
# test_integration.sh: Self-verifying BeeAI end-to-end test
set -euo pipefail

EXPECTED='{"score":42,"insight":"validated"}'

# 1. Spin up stack (if not running)
echo "[BeeAI Test] Bringing up stack..."
podman-compose up -d

# 2. Wait for API healthz
for i in {1..30}; do
  if curl -sf http://localhost:8084/healthz > /dev/null; then
    echo "[BeeAI Test] beeai_api healthy."
    break
  fi
  sleep 2
done

# 3. Wait for /latest_insight to appear
for i in {1..30}; do
  INSIGHT=$(curl -sf http://localhost:8084/latest_insight || true)
  if [[ "$INSIGHT" == "$EXPECTED" ]]; then
    echo "✅ BeeAI integration test PASSED: $INSIGHT"
    exit 0
  fi
  sleep 2
done

>&2 echo "❌ BeeAI integration test FAILED: Got '$INSIGHT', expected '$EXPECTED'"
exit 1
