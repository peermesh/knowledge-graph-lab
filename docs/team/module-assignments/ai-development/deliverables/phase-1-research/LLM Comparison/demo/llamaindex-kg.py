# kg_demo.py
import os, re, json
from collections import defaultdict, Counter

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data-dir")
DOC_EXTS = {".txt", ".md"}

CONCEPTS = {
    # cooking & flavor
    "cooking", "flavor", "flavors", "umami", "sweet", "salty", "sour", "bitter",
    "recipe", "grilling", "baking", "boiling", "frying", "heat",
    # food chemistry
    "protein", "proteins", "sugar", "sugars", "acid", "acids", "ph", "caramelization",
    "maillard reaction", "denature", "denaturation", "tenderize", "browning",
    # general science
    "chemistry", "physics", "quantum", "relativity", "neural networks", "ai",
    "artificial intelligence", "renaissance", "humanism",
}

# Helpers
def iter_docs(data_dir):
    for name in os.listdir(data_dir):
        p = os.path.join(data_dir, name)
        if os.path.isfile(p) and os.path.splitext(name)[1].lower() in DOC_EXTS:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                yield name, f.read()

def sentences(text):
    # simple splitter; good enough for short demo docs
    return [s.strip() for s in re.split(r'[.!?]\s+', text) if s.strip()]

def normalize(term):
    return re.sub(r'\s+', ' ', term.lower()).strip()

def extract_concepts(text):
    txt = normalize(text)
    found = set()
    for c in CONCEPTS:
        if c in txt:
            found.add(normalize(c))
    return found

# --- Build graph ---
doc_to_concepts = defaultdict(set)
concept_to_docs = defaultdict(set)
concept_cooccur = Counter()  # (concept_a, concept_b) -> weight

for fname, content in iter_docs(DATA_DIR):
    cons = extract_concepts(content)
    doc_to_concepts[fname] |= cons
    for c in cons:
        concept_to_docs[c].add(fname)

    # concept–concept co-occurrence within same sentence
    for sent in sentences(content):
        scons = extract_concepts(sent)
        scons = sorted(scons)
        for i in range(len(scons)):
            for j in range(i + 1, len(scons)):
                a, b = scons[i], scons[j]
                concept_cooccur[(a, b)] += 1

# --- Show connections from cooking.txt to chemistry_of_food.txt ---
a_doc = "cooking.txt"
b_doc = "chemistry_of_food.txt"

a_cons = doc_to_concepts.get(a_doc, set())
b_cons = doc_to_concepts.get(b_doc, set())
shared = sorted(a_cons & b_cons)

print(f"\nConcepts in {a_doc}: {sorted(a_cons)}")
print(f"Concepts in {b_doc}: {sorted(b_cons)}")
print(f"\nShared concepts (direct link): {shared or '∅'}")

# If no direct overlap, try 2-hop via concept→concept cooccurrence
if not shared:
    # find concepts in A that co-occur with concepts in B
    bridges = []
    for ca in a_cons:
        for cb in b_cons:
            pair = tuple(sorted([ca, cb]))
            w = concept_cooccur.get(pair, 0)
            if w > 0:
                bridges.append((ca, cb, w))
    bridges.sort(key=lambda x: -x[2])
    print("\n2-hop bridges via co-occurrence:")
    for ca, cb, w in bridges[:10]:
        print(f"  {a_doc} —[{ca}]⇄({w})⇄[{cb}]— {b_doc}")

# --- Save graph as JSON (documents, concepts, edges) ---
graph = {
    "documents": sorted(doc_to_concepts.keys()),
    "concepts": sorted(concept_to_docs.keys()),
    "doc_concept_edges": [
        {"doc": d, "concept": c} for d, cs in doc_to_concepts.items() for c in cs
    ],
    "concept_concept_edges": [
        {"a": a, "b": b, "weight": w} for (a, b), w in concept_cooccur.items()
    ],
}

out_path = os.path.join(BASE_DIR, "graph.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(graph, f, indent=2, ensure_ascii=False)

print(f"\nSaved knowledge graph to: {out_path}")

# --- Optional: visualize if networkx+matplotlib are available ---
try:
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    # add document nodes
    for d in doc_to_concepts.keys():
        G.add_node(d, type="doc")
    # add concept nodes
    for c in concept_to_docs.keys():
        G.add_node(c, type="concept")
    # bipartite edges
    for d, cs in doc_to_concepts.items():
        for c in cs:
            G.add_edge(d, c, kind="mentions")
    # concept–concept edges (only heavier ones to keep it tidy)
    for (a, b), w in concept_cooccur.items():
        if w >= 1:
            G.add_edge(a, b, weight=w, kind="cooccurs")

    pos = nx.spring_layout(G, seed=7)
    node_colors = ["#1f77b4" if G.nodes[n]["type"] == "doc" else "#2ca02c" for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_size=600, font_size=8, node_color=node_colors)
    plt.title("Mini Knowledge Graph (Documents ↔ Concepts)")
    plt.show()
except Exception as e:
    print("\n(Visualization skipped — install `networkx` and `matplotlib` to draw the graph.)")