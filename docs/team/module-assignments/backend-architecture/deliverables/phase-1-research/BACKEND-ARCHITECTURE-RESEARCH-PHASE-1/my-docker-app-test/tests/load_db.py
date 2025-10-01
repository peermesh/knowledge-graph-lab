import psycopg2, time

conn = psycopg2.connect("dbname=appdb user=app password=app host=localhost port=5432")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS items;")
cur.execute("CREATE TABLE items (id SERIAL PRIMARY KEY, name TEXT, value INT);")
conn.commit()

# Insert 10K
t0 = time.time()
cur.executemany("INSERT INTO items (name, value) VALUES (%s, %s);",
                [(f"item{i}", i) for i in range(10000)])
conn.commit()
print("Inserted 10K in", time.time()-t0, "s")

# Query speed test
import random
for _ in range(5):
    v = random.randint(0, 9999)
    t1 = time.time()
    cur.execute("SELECT * FROM items WHERE value=%s;", (v,))
    _ = cur.fetchone()
    print("Query latency:", (time.time()-t1)*1000, "ms")
