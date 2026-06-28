# Chroma DB - Interview Notes & Key Concepts

## What is Chroma DB?

Chroma DB is a vector database specifically designed to support various retrieval tasks.

It offers the following capabilities:

* Storage of embeddings and their metadata to efficiently store and manage vector representations of data.
* Vector search compares vector embeddings to find text based on semantic similarity using distance metrics such as cosine distance.
* Full text search to find relevant documents based on lexical or spelling similarity.
* Data storage to store entire documents, not just their embeddings.
* Metadata filtering can be used to narrow down search results based on metadata to improve the accuracy of the data retrieval process.
* Multi-modal retrieval to retrieve and manage multi-modal data such as images, audio and text in a unified manner.

---

# Chroma DB Deployment Options

## 1. Client-Server Architecture

Chroma DB typically operates using a client-server architecture, where the Chroma client connects to a Chroma server running in a separate process.

The server can be launched either via the Chroma command-line interface, including the core Chroma package, or by using a Docker image.

The clients, whether local or remote, connect to the server using the HTTP protocol.

---

## 2. Standalone Mode

For Python, Chroma can run in a standalone mode instead of the typical client-server setup.

In standalone mode, both the server and client functionalities are run within a single process.

This mode is useful for quickly testing Chroma's features or when the server is expected to always run on the same machine as the client.

---

# Chroma DB Architecture & Workflow

The Chroma vector database architecture works in multiple phases.

## Architecture Diagram

```text
┌──────────────────────────────┐
│ Phase 1 (Optional)           │
│ Obtain Embeddings            │
│ Text/Image/Data → Vectors    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 2                      │
│ Create Collections           │
│ Similar to tables in SQL     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 3                      │
│ Store Data                   │
│ Documents + Metadata         │
│ + Embeddings                 │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 4                      │
│ Collection Operations        │
│ Update/Delete/Rename         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 5                      │
│ Query & Group Data           │
│ Semantic Search              │
│ Metadata Filtering           │
│ Document Filtering           │
└──────────────────────────────┘
```

---

## Phase 1: Obtain Embeddings (Optional)

During the first phase, which is optional, you'll obtain embeddings.

During this phase, you'll convert text, images, or data into their vector representations using an embedding model.

This step is optional because you can offload the embedding step to Chroma DB if you want.

---

## Phase 2: Create Collections

Similar to tables in a relational database, Chroma DB uses collections to store all of its data.

---

## Phase 3: Store Data

This is where you store data within the collections.

If you created embeddings outside of Chroma DB, you would have to pass the embeddings to Chroma DB at this step.

Otherwise, if you allow Chroma DB to handle embedding, then Chroma DB will calculate and store the embeddings from the documents in the background.

---

## Phase 4: Collection Operations

Chroma DB lets you perform various database operations including deleting, updating, or renaming your collections, giving you more options for organizing your data.

---

## Phase 5: Query and Group Data

Chroma DB lets users use text or vector queries to find information in groups based on semantic meaning or textual similarity.

Moreover, Chroma DB allows users to filter documents on their metadata and document contents.

---

# Supported Clients & Integrations

## Officially Supported Clients

* Python
* JavaScript

These are maintained by the ChromaCore team.

---

## Community Supported Clients

* Ruby
* Java
* Go
* C#
* Rust
* PHP

---

## Framework Integrations

Chroma DB can also be integrated with popular frameworks and tools such as:

* LangChain
* LlamaIndex
* Ollama

It also provides native integration with embedding models from:

* Hugging Face
* Google
* OpenAI

---

# Typical Chroma DB Workflow

## Step 1: Create a Collection

The first step is to create a collection, which involves giving it a logical name.

## Step 2: Add Documents

The next step is to add chunks of text and associated metadata to the collection.

When you do this, Chroma DB automatically stores the text and handles the embedding process.

Alternatively, if you precomputed the embeddings before this step, you would supply those embeddings here along with the text.

## Step 3: Query the Collection

Lastly, you query the collection, and Chroma DB returns a list of the most similar results.

Again, Chroma DB handles the embedding of your query automatically, so you don't need to embed the query text before running your query.

---

# Distance Metrics

By default, Chroma uses Euclidean distance to identify the most similar chunks within a collection.

It also supports:

* Cosine Distance
* Dot Product Calculation

---

# Performance Features

## Approximate Nearest Neighbor Search

Chroma DB offers efficient similarity search capabilities, as it is optimized for approximate nearest neighbor search, allowing users to find similar vectors quickly.

## HNSW Algorithm

Internally, Chroma uses an advanced algorithm called the Hierarchical Navigable Small World (HNSW) for efficiently finding the approximate nearest neighbor according to the chosen distance metric.

## Rust Core

The core of Chroma DB was written in Rust, which allows for 3 to 5 times speed improvements in querying and writing operations when compared to a core written in Python.

---

# Common Use Cases

* Building personalized recommender systems based on user preferences.
* Implementing efficient document search engines using vector or full-text search capabilities.
* Retrieving images based on text queries using multi-modal retrieval.
* Providing chatbots with semantic search and retrieval capabilities for context augmentation.

---

# Interview Questions & Answers

## Q1. What is Chroma DB?

Chroma DB is a vector database specifically designed to support various retrieval tasks.

---

## Q2. What capabilities does Chroma DB provide?

* Storage of embeddings and metadata
* Vector search
* Full text search
* Data storage
* Metadata filtering
* Multi-modal retrieval

---

## Q3. What deployment options are available in Chroma DB?

1. Client-Server Architecture
2. Standalone Mode

---

## Q4. What is a Collection in Chroma DB?

Similar to tables in a relational database, Chroma DB uses collections to store all of its data.

---

## Q5. Can Chroma DB generate embeddings automatically?

Yes.

If you allow Chroma DB to handle embedding, then Chroma DB will calculate and store the embeddings from the documents in the background.

---

## Q6. What distance metric does Chroma DB use by default?

By default, Chroma uses Euclidean distance to identify the most similar chunks within a collection.

---

## Q7. What other distance metrics are supported?

* Cosine Distance
* Dot Product

---

## Q8. What algorithm does Chroma DB use for similarity search?

Hierarchical Navigable Small World (HNSW).

---

## Q9. Why is Chroma DB fast?

The core of Chroma DB was written in Rust, which allows for 3 to 5 times speed improvements in querying and writing operations when compared to a core written in Python.

---

# Filtering in Chroma DB

Filtering in Chroma DB fundamentally differs from traditional SQL-based filtering due to its emphasis on vector similarity and flexible metadata querying.

While SQL databases rely on structured schemas and declarative logic to retrieve exact matches, Chroma DB is designed for unstructured data and semantic search, making it well-suited for AI-driven applications.

---

## Chroma DB Supports Two Primary Types of Filtering

### Metadata Filtering

Filters based on document metadata, such as:

```python
{"topic": "history"}
```

or

```python
{"date": "2023-01-15"}
```

Similar to SQL WHERE clauses, but more flexible and can be combined with vector search.

---

### Document Filtering

Filters based on document content using keyword presence.

Examples:

```python
$contains
```

```python
$not_contains
```

Comparable to SQL's CONTAINS or LIKE operators, but more powerful when integrated with vector search.

---

> Document filtering in Chroma DB is also referred to as full text search.

---

# Metadata Filtering in Chroma DB

Metadata filtering in Chroma DB can be performed by using the where parameter inside the .query(), .get(), or .delete() methods.

For basic metadata matches, where you want to find only equivalent matches, use the following syntax:

```python
where={"key": "value"}
```

---

## Supported Metadata Operators

* $eq - equal to (string, int, float)
* $ne - not equal to (string, int, float)
* $gt - greater than (int, float)
* $gte - greater than or equal to (int, float)
* $lt - less than (int, float)
* $lte - less than or equal to (int, float)

---

### Example

```python
where={"key": {"$eq": "value"}}
```

Note that the above is identical to:

```python
where={"key": "value"}
```

In other words, not providing an operator is equivalent to using the $eq operator.

---

## Logical Operators

Combining different filters can be achieved using:

* $and
* $or

Example:

```python
collection.get(
    where={
        "$and": [
            {"key": {"$eq": "value1"}},
            {"key": {"$ne": "value2"}}
        ]
    }
)
```

The above would get only the documents where key is equal to value1 and key is not equal to value2 from collection.

---

## List Operators

* $in
* $nin

Example:

```python
where={"key": {"$nin":["value1", "value2"]}}
```

The above code will find all documents where key is not equal to either value1 or value2.

---

# Document Filtering in Chroma DB

Document filtering in Chroma DB can be performed by supplying $contains or $not_contains to the where_document parameter inside the .query(), .get(), or .delete() methods.

Syntax:

```python
where_document={"$contains":"value"}
```

The above would find all documents that contain value in the text of the document.

---

Moreover, note that you can combine multiple document filters using the $and and $or document operators in an analogous way to the metadata filters.

---

## Important Interview Point

Document filtering is case-sensitive in Chroma DB.

Therefore, searching for:

```text
Pandas
```

will not find any documents if the stored word is:

```text
pandas
```

---

# Most Asked Interview Question

## Difference Between Metadata Filtering and Document Filtering

### Metadata Filtering

Filters based on document metadata.

Examples:

* source
* version
* topic
* date

Uses:

```python
where={}
```

---

### Document Filtering

Filters based on document content.

Uses:

```python
where_document={}
```

Supports:

* $contains
* $not_contains

Document filtering is also referred to as full text search.

---

# Quick Revision (30 Seconds)

* Chroma DB is a vector database.
* Stores embeddings, metadata and documents.
* Supports vector search, full text search and multi-modal retrieval.
* Collections are similar to SQL tables.
* Default distance metric = Euclidean Distance.
* Also supports Cosine Distance and Dot Product.
* Uses HNSW for Approximate Nearest Neighbor Search.
* Core is written in Rust.
* Supports metadata filtering and document filtering.
* Document filtering is also called full text search.
* Integrates with LangChain, LlamaIndex and Ollama.
* Official clients are Python and JavaScript.
* Can run in Client-Server mode or Standalone mode.

```
```
