# BeeAI Agent

This microservice implements the core agent logic for the BeeAI platform.

## Features
- Listens for events from RabbitMQ
- Maintains short-term memory (Redis)
- Interacts with context graph (Neo4j)

## Development

```sh
podman build -t beeai_agent .
podman run --rm -it beeai_agent
```

## Docs
- See `/docs/` for C4 diagrams
- See `/adrs/` for architecture decisions
