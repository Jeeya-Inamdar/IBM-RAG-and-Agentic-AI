# Similarity Search & HNSW in Chroma DB

## What is a Vector Index?

* Used for fast similarity and nearest neighbor searches.
* Stores and organizes high-dimensional embeddings efficiently.
* Avoids comparing a query against every vector in the database.
* Scales to millions or billions of vectors.
* Structures data based on vector-space geometry.
* Clusters similar vectors together or links them using proximity-based graphs.
* Allows search algorithms to focus only on the most promising regions.

---

# What is HNSW?

**HNSW = Hierarchical Navigable Small World**

* Fast and scalable graph-based vector index.
* Designed for Approximate Nearest Neighbor (ANN) search.
* Sole indexing method supported by Chroma DB.
* Widely adopted by modern vector databases.
* Provides excellent balance between speed and accuracy.

---

# HNSW Architecture

```text
                    Layer 3
                 Entry Point
                      │
                      ▼

                    Layer 2
             Sparse Connections
                      │
                      ▼

                    Layer 1
            More Dense Connections
                      │
                      ▼

                    Layer 0
                All Vectors
             Dense Graph Search
```

---

# How HNSW Works

* Builds a multi-layered graph structure.
* Upper layers contain sparse connections.
* Lower layers contain increasingly dense connections.
* Bottom layer stores all vectors.
* Each vector is connected to nearby neighbors.
* Creates a "small world" network.
* Most vectors can be reached in only a few hops.

---

# HNSW Search Process

```text
Query
  │
  ▼
Top Layer
  │
  ▼
Find Closest Node
  │
  ▼
Move Down Layer
  │
  ▼
Refine Search
  │
  ▼
Bottom Layer
  │
  ▼
Return Nearest Neighbors
```

---

# Why Use HNSW?

### Fast

* Avoids scanning the entire dataset.
* Searches only relevant portions of the graph.

### Accurate

* Produces near-exact nearest neighbor results.

### Scalable

* Supports millions to billions of vectors.

### Versatile

* Supports multiple distance metrics.

---

# HNSW Configuration

```python
"hnsw": {
    "space": "cosine",
    "ef_search": 100,
    "ef_construction": 100,
    "max_neighbors": 16
}
```

---

# HNSW Parameters

## space

Distance metric used for similarity search.

### Options

* `l2` → Squared Euclidean Distance (Default)
* `ip` → Inner Product (Dot Product)
* `cosine` → Cosine Distance
* `ef` → Expansion Factor
---

## ef_search

* Candidate list size during querying.
* Default: `100`
* Higher value = explores more nodes :

  * Better recall
  * Better accuracy
  * Slower search

### Interview Tip

**Most important query-time tuning parameter.**

---

## ef_construction

* Candidate list size during index construction.
* Default: `100`
* Higher value:

  * Better index quality
  * Better accuracy
  * Slower index creation
  * More memory usage

---

## max_neighbors

* Maximum connections per node.
* Default: `16`
* Higher value:

  * Denser graph
  * Better search performance
  * Higher memory usage
  * Longer build time

---

# Performance Tuning

## Query-Time Performance

Parameter:

```text
ef_search
```

* Directly affects recall and search speed.
* Higher value = Better results but slower queries.

---

## Index Quality

Parameters:

```text
ef_construction
max_neighbors
```

* Affect graph quality.
* Improve search accuracy.
* Increase build time and memory consumption.

---

# Similarity Search Example

## Documents

### Animals

* id1 → Giant pandas are a bear species that lives in mountainous areas.
* id3 → I think everyone agrees that pandas are some of the cutest animals on the planet.

### Data Analysis

* id2 → A pandas DataFrame stores two-dimensional, tabular data.
* id4 → A direct comparison between pandas and polars indicates that polars is a more efficient library than pandas.

---

# Query Example

```python
collection.query(
    query_texts=["cats"],
    n_results=10
)
```

### Returned Order

1. id3
2. id1
3. id2
4. id4

### Why?

* Query "cats" is semantically closer to animals.
* Animal-related documents ranked higher.
* Chroma understands context, not just keywords.

---

# Filtering Example

## Problem

Query:

```python
query_texts=["polar bear"]
```

Returned:

```text
id4
```

Why?

* "polar" was matched with "polars" Python library.
* Semantic search misunderstood the intent.

---

# Solution 1 - Metadata Filtering

```python
collection.query(
    query_texts=["polar bear"],
    where={"topic":"animals"}
)
```

### Result

```text
id1
```

* Restricts search to animal documents.
* Correct result returned.

---

# Solution 2 - Full Text Filtering

```python
collection.query(
    query_texts=["polar bear"],
    where_document={
        "$not_contains":"library"
    }
)
```

### Result

```text
id1
```

* Excludes programming-library documents.
* Correct result returned.

---

# Solution 3 - Combine Both Filters

```python
collection.query(
    query_texts=["polar bear"],
    where={"topic":"animals"},
    where_document={
        "$not_contains":"library"
    }
)
```

### Result

```text
id1
```

* Metadata filter + document filter together.
* Most precise search strategy.

---

# Most Asked Interview Questions

## What is a Vector Index?

* Data structure for fast similarity search.
* Avoids brute-force vector comparisons.

---

## What does HNSW stand for?

* Hierarchical Navigable Small World.

---

## Which indexing algorithm does Chroma DB use?

* HNSW.

---

## Why is HNSW fast?

* Uses a multi-layer graph.
* Skips most vectors during search.

---

## Which parameter controls search quality?

* ef_search.

---

## Which parameters improve index quality?

* ef_construction
* max_neighbors

---

## Which distance metrics does HNSW support?

* L2 (Euclidean)
* Cosine
* Inner Product (Dot Product)

---

## What is ANN?

* Approximate Nearest Neighbor Search.
* Returns highly similar vectors quickly without scanning the entire dataset.

---

# Quick Revision (15 Seconds)

* Chroma uses HNSW for vector indexing.
* HNSW = Hierarchical Navigable Small World.
* ANN = Approximate Nearest Neighbor Search.
* Top layers = Sparse graph.
* Bottom layer = All vectors.
* ef_search = Query quality.
* ef_construction = Index quality.
* max_neighbors = Graph density.
* Supports L2, Cosine and Inner Product.
* Metadata filtering improves relevance.
* Full-text filtering reduces semantic mistakes.
* HNSW is fast, accurate and scalable.

```
```
