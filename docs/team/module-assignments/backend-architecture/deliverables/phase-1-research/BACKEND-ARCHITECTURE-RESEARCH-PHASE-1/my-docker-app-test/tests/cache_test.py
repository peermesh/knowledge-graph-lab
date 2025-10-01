import redis, time, random

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Simulate cache hits
hits, total = 0, 1000
for i in range(total):
    key = f"item:{random.randint(1,100)}"
    if r.get(key):
        hits += 1
    else:
        r.set(key, f"value-{i}", ex=60)

print("Cache hit rate:", hits/total)

# Simple job queue
queue = "jobs"
for i in range(100):
    r.lpush(queue, f"job-{i}")

processed = 0
start = time.time()
while time.time() - start < 60:  # 1 minute
    job = r.rpop(queue)
    if job:
        processed += 1
        time.sleep(0.01)  # simulate work
print("Processed jobs/min:", processed)
