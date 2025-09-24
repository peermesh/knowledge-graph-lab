import os

os.environ["OPENAI_API_KEY"] = 

print("Current working dir:", os.getcwd())

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader(
    "docs/team/module-assignments/ai-development/deliverables/phase-1-research/data-dir"
).load_data()

# Simple vector storage

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

# Query Engine 

# response = query_engine.query("What is in ans.txt?")

# print(response)

# Example response
# The content of ans.txt includes statistical hypotheses related to treatment outcomes, 
# preferences for a soda brand, and a code snippet for calculating a p-value based on observed data.

response = query_engine.query("Why does meat turn brown when cooked?")
print(response)
