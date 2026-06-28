# LangChain Retrievers - Interview Notes

# What is a LangChain Retriever?

* A LangChain retriever is an interface that returns documents based on an unstructured query.
* More general than a vector store.
* Does not necessarily store documents.
* Purpose is to retrieve documents or document chunks.
* Accepts a string query as input.
* Returns a list of documents/chunks as output.

---

# Retriever Workflow

```text
User Query
    │
    ▼
 Retriever
    │
    ▼
Relevant Documents / Chunks
```

---

# Types of LangChain Retrievers

1. Vector Store Retriever
2. Multi-Query Retriever
3. Self-Query Retriever
4. Parent Document Retriever

---

# 1. Vector Store Retriever

## What is it?

* Simplest retriever type.
* Retrieves documents from a vector database.
* Uses an existing vector store.
* Does not require an LLM.

---

## How it Works

```text
Documents
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
Vector Store
    │
    ▼
Vector Store Retriever
    │
    ▼
Similarity Search / MMR
    │
    ▼
Relevant Chunks
```

---

## Retrieval Process

### Step 1

Embed user query.

### Step 2

Compare query embedding against stored embeddings.

### Step 3

Retrieve most relevant chunks.

---

## Search Methods

### Similarity Search

* Retrieves most similar chunks.
* Based purely on similarity score.

Example:

```text
Query: Email Policy

Chunk A → 95% Similar
Chunk B → 90% Similar
Chunk C → 85% Similar

Returns A, B, C
```

---

### MMR (Maximum Marginal Relevance)

* Balances relevance and diversity.
* Avoids redundant documents.
* Selects documents:

  * Highly relevant to query
  * Minimally similar to already selected documents

---

## MMR Example

### Without MMR

```text
Query: Email Policy

Result 1 → Email Security
Result 2 → Email Security
Result 3 → Email Security
```

Lots of redundancy.

---

### With MMR

```text
Query: Email Policy

Result 1 → Email Security
Result 2 → Email Retention
Result 3 → Email Access Rules
```

More diverse coverage.

---

# Interview Question

## What is MMR?

**Answer:**

MMR (Maximum Marginal Relevance) is a retrieval technique that balances relevance and diversity by selecting documents that are highly relevant to the query while minimizing redundancy among retrieved results.

---

# 2. Multi-Query Retriever

## What Problem Does it Solve?

Different wording can produce different search results.

Example:

```text
"What is the smoking policy?"
```

vs

```text
"Can employees smoke?"
```

vs

```text
"Rules about smoking"
```

All mean nearly the same thing.

---

## How it Works

* Uses an LLM.
* Generates multiple versions of the same query.
* Runs retrieval for each generated query.
* Combines results.
* Returns unique union of documents.

---

## Architecture

```text
User Query
     │
     ▼

LLM Generates
Multiple Queries

     │
     ▼

Query 1 ──► Retriever
Query 2 ──► Retriever
Query 3 ──► Retriever

     │
     ▼

Unique Union
of Results

     │
     ▼

Final Documents
```

---

## Example

### Original Query

```text
Benefits of remote work
```

### Generated Queries

```text
Advantages of working remotely

Positive effects of remote work

Remote work productivity benefits
```

### Result

Larger set of relevant documents.

---

## Advantages

* Better recall.
* Richer document retrieval.
* Reduces dependency on exact wording.
* Helps when embeddings do not capture semantics well.

---

# Interview Question

## Why use Multi-Query Retriever?

**Answer:**

The Multi-Query Retriever uses an LLM to generate alternative versions of the same query, improving retrieval quality and increasing the number of relevant documents retrieved.

---

# 3. Self-Query Retriever

## What Problem Does it Solve?

Traditional retrievers only use document text.

They cannot automatically understand metadata.

---

## Example Documents

```text
Movie A
Rating: 9.0
Year: 2020
Director: Nolan

Movie B
Rating: 7.5
Year: 2018
Director: Cameron
```

---

## User Query

```text
I want to watch a movie rated higher than 8.5
```

The query contains:

* Semantic meaning
* Metadata requirement

---

## How it Works

The Self-Query Retriever converts the query into:

### Semantic Query

```text
movie
```

### Metadata Filter

```text
rating > 8.5
```

---

## Architecture

```text
User Query
      │
      ▼

Self Query Retriever

      │
      ├─────────────► Semantic Search
      │
      └─────────────► Metadata Filter

      │
      ▼

Filtered Results
```

---

## Example

### Input

```text
I want a movie rated higher than 8.5
```

### Generated Filter

```text
rating > 8.5
```

### Output

```text
Movie A
Movie C
```

---

## Metadata Examples

```text
Year

Rating

Director

Category

Author
```

---

# Interview Question

## What is Self-Query Retriever?

**Answer:**

A Self-Query Retriever uses an LLM to convert a query into two components:

1. Semantic search query
2. Metadata filter

It enables retrieval based on both document content and metadata.

---

# 4. Parent Document Retriever

## Problem

Conflicting requirements exist when chunking documents.

### Small Chunks

Pros:

* Better embeddings
* Better semantic accuracy

Cons:

* Lose context

---

### Large Chunks

Pros:

* More context retained

Cons:

* Embeddings become less precise

---

# Solution

Parent Document Retriever

Uses two splitters.

---

## Child Splitter

Creates small chunks.

Purpose:

* Generate accurate embeddings.

---

## Parent Splitter

Creates larger chunks.

Purpose:

* Preserve context.

---

## Architecture

```text
Original Document

      │

      ▼

Parent Splitter
(Large Chunks)

      │

      ▼

Child Splitter
(Small Chunks)

      │

      ▼

Embeddings Stored
in Vector Store

      │

      ▼

Query Matches Child

      │

      ▼

Find Parent ID

      │

      ▼

Return Parent Chunk
```

---

## Example

### Query

```text
Smoking Policy
```

### Child Chunk Match

```text
"...employees are not allowed..."
```

### Returned Result

Entire parent section:

```text
Smoking Policy
------------------
Employees are not allowed...
Smoking areas...
Disciplinary actions...
```

---

## Advantages

* Better embeddings.
* Better context retention.
* More complete answers.
* Useful for RAG systems.

---

# Interview Question

## Why use Parent Document Retriever?

**Answer:**

It combines the advantages of small chunks for embedding quality and large chunks for contextual understanding by retrieving parent documents after matching smaller child chunks.

---

# Comparison Table

| Retriever                 | Uses LLM | Uses Metadata | Returns Larger Context |
| ------------------------- | -------- | ------------- | ---------------------- |
| Vector Store Retriever    | ❌ No     | ❌ No          | ❌ No                   |
| Multi-Query Retriever     | ✅ Yes    | ❌ No          | ❌ No                   |
| Self-Query Retriever      | ✅ Yes    | ✅ Yes         | ❌ No                   |
| Parent Document Retriever | ❌ No     | ❌ No          | ✅ Yes                  |

---

# Quick Revision (30 Seconds)

* Retriever = Interface that returns documents for an unstructured query.
* Vector Store Retriever → Similarity Search or MMR.
* Similarity Search → Most similar chunks.
* MMR → Relevance + Diversity.
* Multi-Query Retriever → Uses LLM to generate multiple query variations.
* Self-Query Retriever → Creates semantic query + metadata filter.
* Parent Document Retriever → Small chunks for embeddings, large chunks for retrieval.
* Parent Retriever solves context vs chunk-size tradeoff.
* Multi-Query improves recall.
* Self-Query enables metadata-aware retrieval.

```
```
