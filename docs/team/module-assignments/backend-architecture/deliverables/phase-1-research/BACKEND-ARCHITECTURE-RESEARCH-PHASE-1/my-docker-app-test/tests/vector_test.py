import os, time, random
import numpy as np
import psycopg2

DIM = 128
N = 1000
embs = [np.random.rand(DIM).tolist() for _ in range(N)]

# ---- Postgres + pgvector ----
pg = psycopg2.connect("dbname=appdb user=app password=app host=localhost port=5432")
cur = pg.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
cur.execute("DROP TABLE IF EXISTS vecs;")
cur.execute(f"CREATE TABLE vecs (id SERIAL, embedding vector({DIM}));")
pg.commit()

t0 = time.time()
cur.executemany("INSERT INTO vecs (embedding) VALUES (%s);",
                [("{"+",".join(map(str,e))+"}",) for e in embs])
pg.commit()
print("Inserted 1K vectors in", time.time()-t0, "s")

# Create index
cur.execute("CREATE INDEX ON vecs USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);")
pg.commit()

# Similarity search
query = np.random.rand(DIM).tolist()
t1 = time.time()
cur.execute("SELECT id FROM vecs ORDER BY embedding <-> %s LIMIT 5;",
            ("{"+",".join(map(str,query))+"}",))
print("pgvector search latency ms:", (time.time()-t1)*1000)

# ---- Pinecone (requires API key) ----
try:
    import pinecone
    pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "demo-index"
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=DIM)
    index = pinecone.Index(index_name)

    # upsert
    vecs = [(str(i), e) for i,e in enumerate(embs)]
    index.upsert(vecs)

    q = np.random.rand(DIM).tolist()
    t2 = time.time()
    res = index.query(vector=q, top_k=5)
    print("Pinecone search latency ms:", (time.time()-t2)*1000)
except Exception as e:
    print("Pinecone test skipped:", e)

# ---- Weaviate (requires endpoint + key) ----
try:
    import weaviate
    client = weaviate.Client(
        url=os.getenv("WEAVIATE_URL"),
        auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))
    )

    # Search
    q = np.random.rand(DIM).tolist()
    t3 = time.time()
    res = client.query.get("Vecs", ["_additional { distance }"]).with_near_vector({"vector": q}).with_limit(5).do()
    print("Weaviate search latency ms:", (time.time()-t3)*1000)
except Exception as e:
    print("Weaviate test skipped:", e)
