# Semantic Search

## What is Semantic Search?

Semantic search goes beyond traditional keyword search. Instead of matching exact words, it tries to understand the meaning, context, and intent behind a user's query.

### Key Benefits

* Understands the intent behind search queries.
* Analyzes the contextual meaning of words and phrases.
* Returns more accurate and relevant results.
* Adapts to user behavior and preferences.
* Improves overall search experience and user satisfaction.

---

# How Semantic Search Works (Simple Version)

Think of semantic search as a smart assistant that understands what you mean, not just what you type.

## Step 1: Getting the Gist

The search engine reads your query and tries to understand its meaning.

### Example

Query:

```text
How can I recover my account?
```

Instead of looking only for the words "recover" and "account", it understands that you may be asking about:

```text
Password reset
Account recovery
Login issues
```

---

## Step 2: Making Connections

The search engine understands relationships between words.

### Example

```text
Doctor = Physician
Car = Automobile
Laptop = Notebook
```

Even if different words are used, semantic search understands they may have the same meaning.

---

## Step 3: Picking the Best Results

The search engine searches through available information and finds content that best matches the meaning of your query.

### Example

Query:

```text
How do I fix my login problem?
```

Returned Result:

```text
Steps to reset your password and recover account access.
```

Even though the exact words do not match.

---

# The Technical Side of Semantic Search

Semantic search works using vectors.

## What is a Vector?

A vector is a list of numbers that represents the meaning of a word, sentence, or document.

### Example

Sentence:

```text
I love machine learning.
```

Vector Representation:

```text
[0.23, 0.89, 0.45, 0.12, ...]
```

Every sentence gets its own numerical representation.

---

# Why Vectors are Important

Imagine every sentence as a point in space.

### Example

```text
Doctor
Physician
```

Their vectors will be very close together because they have similar meanings.

```text
Doctor ●
        ● Physician
```

### Another Example

```text
Doctor
Pizza
```

Their vectors will be far apart because their meanings are very different.

```text
Doctor ●

                    ● Pizza
```

The closer the vectors, the more similar the meaning.

---

# Creating Vectors

We use embedding models such as:

* Universal Sentence Encoder (USE)
* OpenAI Embeddings
* Sentence Transformers

These models convert text into vectors.

### Example

Input:

```text
Artificial Intelligence is transforming industries.
```

Output:

```text
[0.67, 0.21, 0.54, 0.91, ...]
```

This vector acts like a unique numerical fingerprint for the sentence.

---

# Calculating Similarity

Once vectors are created, we compare them to measure similarity.

A common method is:

## Cosine Similarity

Cosine similarity measures how close two vectors are.

### Example

Query:

```text
How do I scale Kubernetes?
```

Document:

```text
Kubernetes Horizontal Pod Autoscaler Guide
```

The vectors will be very similar.

```text
Cosine Similarity = 0.95
```

High similarity means highly relevant.

---

# Using Vectors for Search

When a user enters a query:

1. Convert query into a vector.
2. Compare it with stored document vectors.
3. Find the closest vectors.
4. Return the most relevant results.

### Example

Query:

```text
How can I recover my account?
```

Stored Documents:

```text
Password Reset Guide
Leave Application Process
Payroll Policy
```

Closest Vector:

```text
Password Reset Guide
```

Returned as the result.

---

# How Vectors Power Semantic Search

Semantic search uses vectors in three major steps.

## 1. Vectorization

Convert the user's query into a vector.

### Example

```text
User Query
      ↓
Vector
```

---

## 2. Indexing

Store document vectors inside an index for fast searching.

### Example

```text
Document A → Vector A
Document B → Vector B
Document C → Vector C
```

---

## 3. Retrieval

Find vectors closest to the query vector.

### Example

```text
Query Vector
      ↓
Search Index
      ↓
Closest Vectors
      ↓
Relevant Results
```

---

# Understanding Vectorization and Indexing

Vectorization and indexing are key components of a semantic search engine.

Two important tools are:

* Universal Sentence Encoder (USE)
* FAISS

---

# Universal Sentence Encoder (USE)

## What Does USE Do?

The Universal Sentence Encoder converts text into vectors.

These vectors capture the semantic meaning of the text.

### Benefits

#### Language Comprehension

USE understands sentence meaning by considering context.

#### Versatility

It is trained on multiple datasets and can handle many topics and sentence structures.

#### Speed

It quickly converts text into vectors after loading.

---

# How Universal Sentence Encoder Works

## Step 1: Analyze Words

USE looks at every word in a sentence.

### Example

```text
The bank approved the loan.
```

It understands the meaning of "bank" based on surrounding words.

---

## Step 2: Understand Context

USE analyzes:

* Word order
* Relationships between words
* Overall sentence meaning

### Example

```text
I deposited money in the bank.
```

Bank = Financial Institution

```text
I sat on the river bank.
```

Bank = River Edge

---

## Step 3: Create Vectors

The sentence is converted into a high-dimensional vector.

### Example

```text
Sentence
     ↓
USE Model
     ↓
Vector
```

---

# FAISS

## What is FAISS?

FAISS (Facebook AI Similarity Search) is a library used for efficient similarity search.

After USE generates vectors, FAISS helps search through them quickly.

---

# What Does FAISS Do?

### Efficient Searching

Quickly searches through millions of vectors.

### Scalability

Can handle very large vector databases.

### Accuracy

Uses advanced indexing techniques to find highly relevant results.

---

# How FAISS Works

## Step 1: Build an Index

FAISS organizes vectors so that similar vectors are stored close together.

### Example

```text
Vector A
Vector B
Vector C
```

Stored in an optimized search structure.

---

## Step 2: Search

When a query vector arrives:

```text
Query Vector
      ↓
FAISS Index
```

FAISS quickly identifies the nearest vectors.

---

## Step 3: Retrieve Results

FAISS returns the vectors most similar to the query.

### Example

Query:

```text
How do I reset my password?
```

Closest Vector:

```text
Password Recovery Guide
```

Returned as the result.

---

# Putting USE and FAISS Together

USE and FAISS work together to create a semantic search engine.

## Workflow

```text
Documents
    ↓
Preprocessing
    ↓
Universal Sentence Encoder (USE)
    ↓
Document Vectors
    ↓
FAISS Index
    ↓
User Query
    ↓
USE
    ↓
Query Vector
    ↓
FAISS Search
    ↓
Most Similar Documents
```

---

# Universal Sentence Encoder Implementation

After preprocessing the text data, the next step is to transform the cleaned text into numerical vectors using USE.

These vectors capture the semantic meaning of the text.

---

## Loading the USE Module

We use TensorFlow Hub to load the pre-trained Universal Sentence Encoder.

```python
import tensorflow_hub as hub

embed = hub.load(
    "https://tfhub.dev/google/universal-sentence-encoder/4"
)
```

This makes the USE model ready for vectorization.

---

## Defining the Embedding Function

The embedding function converts text into vectors.

```python
def embed_text(text):
    return embed(text).numpy()
```

### What Happens?

1. Input text is passed to USE.
2. USE generates a vector.
3. TensorFlow tensor is converted to a NumPy array.

---

## Vectorizing Documents

Apply the embedding function to every preprocessed document.

```python
X_use = np.vstack(
    [embed_text(doc) for doc in processed_documents]
)
```

### Result

```text
X_use
```

contains a 2D array where:

* Each row = One document
* Each column = One vector dimension

Example:

```text
Document 1 → [0.12, 0.45, 0.87, ...]
Document 2 → [0.76, 0.31, 0.19, ...]
Document 3 → [0.23, 0.98, 0.54, ...]
```

These vectors are now ready for indexing in FAISS and can be used for semantic search.

---

# Final Summary

## Universal Sentence Encoder (USE)

* Converts text into vectors.
* Captures semantic meaning.
* Understands context and sentence structure.
* Produces numerical representations of text.

## FAISS

* Stores vectors efficiently.
* Performs fast similarity search.
* Finds vectors closest to the query vector.
* Enables scalable semantic search.

## Semantic Search Workflow

```text
Text
 ↓
USE
 ↓
Vectors
 ↓
FAISS Index
 ↓
Similarity Search
 ↓
Relevant Results
```

Together, USE and FAISS create a semantic search engine that understands meaning rather than relying only on exact keyword matches.
