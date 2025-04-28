import asyncio
import aio_pika
import redis
from neo4j import GraphDatabase
from fastapi import FastAPI
import uvicorn
import threading

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

latest_insight = None

import json
from datetime import datetime

async def receive_agent_events():
    global latest_insight
    connection = await aio_pika.connect_robust("amqp://beeai:beeai_pass@rabbitmq/")
    channel = await connection.channel()
    queue = await channel.declare_queue("beeai_agent_events", durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print("[Agent] Received event:", message.body)
                event = json.loads(message.body)
                if event.get("event") == "score.insight":
                    typ = event["payload"].get("type")
                    data = event["payload"].get("insight", {})
                    scored = {"event": "insight.scored", "payload": {"type": typ, "insight": data}}
                    # Add scoring/enrichment
                    if typ == "health":
                        # Example: risk score based on stress and recovery
                        risk = 0
                        if data.get("stress_level") in ["elevated", "high"]:
                            risk += 10
                        if data.get("recovery_score", 100) < 60:
                            risk += 10
                        scored["payload"]["risk_score"] = risk
                    elif typ == "workout":
                        # Example: effort score pass-through
                        scored["payload"]["effort_score"] = data.get("effort_score", 0)
                    elif typ == "sleep":
                        # Example: sleep quality assessment
                        quality = "good" if data.get("sleep_quality_percent", 0) > 80 else "poor"
                        scored["payload"]["sleep_quality"] = quality
                    # Optionally: persist to Neo4j (stub)
                    # TODO: Implement Neo4j persistence
                    latest_insight = scored["payload"]
                    await channel.default_exchange.publish(
                        aio_pika.Message(body=json.dumps(scored).encode()),
                        routing_key="beeai_api_events"
                    )
                    print(f"[Agent] Published insight.scored event: {typ}")

async def main():
    # Connect to Redis
    r = redis.Redis(host='redis', port=6379, db=0)
    # Connect to Neo4j
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "beeai_graph"))
    await receive_agent_events()

def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8083)

if __name__ == "__main__":
    threading.Thread(target=start_fastapi, daemon=True).start()
    asyncio.run(main())
