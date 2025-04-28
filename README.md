# BeeAI Infra

This directory contains the infrastructure and orchestration for the BeeAI platform using Podman Compose.

## 🚀 Quickstart

1. **Build and start all services:**
   ```sh
   podman-compose build
   podman-compose up -d
   ```

2. **Check health of core services:**
   ```sh
   curl -sf http://localhost:8081/healthz  # beeai_contextagent
   curl -sf http://localhost:8082/healthz  # validator
   # (Add others as you bring them online)
   ```

3. **Run end-to-end test:**
   ```sh
   chmod +x test_flow.sh
   ./test_flow.sh
   ```
   You should see: `✅ End-to-end flow succeeded: validation.completed event received.`

## 🩺 Troubleshooting
- If a health check fails, run `podman-compose logs <service>` to check for errors.
- Ensure ports 8081 and 8082 are not in use by other processes.
- Check RabbitMQ UI at [http://localhost:15672](http://localhost:15672) (user: beeai, pass: beeai_pass).
- If containers fail to build, try `podman-compose build --no-cache`.

## 🐇 Inspecting RabbitMQ Queues (Manual)
1. Go to [http://localhost:15672](http://localhost:15672) and log in.
2. Click on the `Queues` tab.
3. Select `beeai_validator_events` to see messages (e.g. `validation.completed`).
4. You can also use the CLI inside the RabbitMQ container:
   ```sh
   podman exec -it <rabbitmq_container_id> rabbitmqadmin -u beeai -p beeai_pass list queues
   podman exec -it <rabbitmq_container_id> rabbitmqadmin -u beeai -p beeai_pass get queue=beeai_validator_events requeue=false
   ```

## 📚 Docs
- See `/docs/C4_Context.puml` and `/docs/C4_Container.puml` for architecture diagrams.
- See `/adrs/` for architecture decisions.
