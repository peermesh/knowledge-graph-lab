# Meta-Schema (Stable)
Records: **entity**, **edge**, **claim**, **evidence**, **topic**, **facets**.
- Claims carry predicate, value (typed), confidence, timestamps; link to ≥1 evidence record.
- Evidence holds URL, publisher, published_at, excerpt hash.
- Entities/Edges are canonical; **facets** store domain-specific fields.
This meta-schema is stable; domain Packs extend via facets and predicates.