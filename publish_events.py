#!/usr/bin/env python3
"""
publish_events.py - Publish sample events to beeai_agent and beeai_api queues to verify event receivers.
"""
import aio_pika
import asyncio

async def publish(queue_name, body):
    connection = await aio_pika.connect_robust("amqp://beeai:beeai_pass@localhost/")
    channel = await connection.channel()
    await channel.default_exchange.publish(
        aio_pika.Message(body=body.encode()),
        routing_key=queue_name
    )
    print(f"Published to {queue_name}: {body}")
    await connection.close()

async def main():
    await publish("beeai_agent_events", '{"event": "agent.test", "payload": {"msg": "hello agent"}}')
    await publish("beeai_api_events", '{"event": "api.test", "payload": {"msg": "hello api"}}')

if __name__ == "__main__":
    asyncio.run(main())
