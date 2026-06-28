# LLAMAIndex Indexes and Retrievers

## Core Index Types Available in LLAMAIndex

LLAMAIndex provides three core index types:

* **VectorStoreIndex** – Used for semantic search based on meaning.
* **DocumentSummaryIndex** – Uses generated summaries to identify relevant documents.
* **KeywordTableIndex** – Enables exact keyword matching for rule-based or hybrid search.

---

# 1. VectorStoreIndex

## What is VectorStoreIndex?

* Stores vector embeddings for each document chunk.
* Best suited for semantic retrieval.
* Commonly used in pipelines that involve large language models.

## How it Works

### Document

```
"Users can reset their password from Account Settings."
```

### Stored Embedding

```
[0.23, 0.78, 0.11, 0.56, ...]
```

### User Query

```
"How do I change my login credentials?"
```

Even though the exact phrase "reset password" does not exist in the query, semantic similarity allows retrieval of the correct document chunk.

## Example

### Stored Document

```
Node.js application deployment guide
```

### Query

```
How can I deploy my backend application?
```

### Result

The retriever finds the deployment guide because the meaning is similar.

## Best Use Cases

* Chatbots
* RAG applications
* Enterprise search
* Knowledge assistants
* Customer support systems

---

# 2. DocumentSummaryIndex

## What is DocumentSummaryIndex?

* Generates and stores summaries of documents at indexing time.
* These summaries are used to filter documents before retrieving the full content.

## Example

### Original Document

```
100-page Annual Financial Report
```

### Generated Summary

```
Revenue increased by 20%, operating costs decreased by 10%, and international expansion contributed significantly to growth.
```

### User Query

```
What were the major financial improvements this year?
```

Instead of searching all 100 pages, LLAMAIndex first searches the summary and identifies the document as relevant.

### Returned Result

Original document pages, not the summary.

## Benefits

* Useful when working with large and diverse document sets.
* Helps manage document collections that cannot fit in the context window of an LLM.
* Reduces the search space before retrieving original content.

---

# 3. KeywordTableIndex

## What is KeywordTableIndex?

* Extracts keywords from documents.
* Maps those keywords to specific content chunks.
* Ideal for exact keyword matching.
* Useful for hybrid or rule-based search scenarios.

## Example

### Document

```
Docker is a containerization platform.
Kubernetes is used for orchestration.
Redis is used for caching.
```

### Generated Keyword Table

| Keyword    | Content Chunk |
| ---------- | ------------- |
| Docker     | Chunk 1       |
| Kubernetes | Chunk 2       |
| Redis      | Chunk 3       |

### Query

```
Redis
```

### Result

Returns the Redis chunk immediately through exact keyword matching.

## Best Use Cases

* Technical documentation
* Legal systems
* Compliance search
* Product catalogs

---

# Retrievers in LLAMAIndex

Retrievers are responsible for finding relevant content from indexes.

---

## 1. Vector Index Retriever - The Foundation

The Vector Index Retriever uses vector embeddings to find semantically related content, making it ideal for general-purpose search and widely used in retrieval-augmented generation (RAG) pipelines.

**How it works**: 
- Documents are split into nodes and embedded using the configured embedding model
- Query is converted to an embedding vector
- Returns nodes ranked by cosine similarity to the query embedding
- Generates embeddings in batches of 2048 nodes by default

**When to use:**
- General-purpose semantic search (most common use case)
- Finding conceptually related content based on meaning rather than exact keywords
- RAG pipelines where semantic understanding is crucial
- When exact keyword matching isn't the primary requirement

**Key characteristics from authoritative source:**
- **Stores embeddings for each document chunk** (VectorStoreIndex foundation)
- **Best for semantic retrieval** based on meaning and context
- **Commonly used in LLM pipelines** for retrieval-augmented generation

**Strengths**: 
- Excellent semantic understanding and context awareness
- Handles synonyms and related concepts effectively
- Works well with natural language queries

**Limitations**: 
- May miss exact keyword matches when specific terms are crucial
- Requires a good embedding model for optimal performance
- Can be computationally intensive for large document collections


## Example

### Knowledge Base

```
Chunk 1: Password reset process
Chunk 2: Leave approval workflow
Chunk 3: Payroll processing
```

### Query

```
How do employees recover account access?
```

### Retrieved Chunk

```
Password reset process
```

The query never mentions "password reset" but semantic similarity finds the correct result.

---
# 2. BM25 Retriever - Advanced Keyword-Based Search

BM25 is a keyword-based retrieval method that improves on TF-IDF by addressing some of its key limitations. It's widely used in production search systems including Elasticsearch and Apache Lucene.

### Understanding TF-IDF: The Foundation

Before diving into BM25, let's understand **TF-IDF** (Term Frequency-Inverse Document Frequency), which BM25 builds upon:

**Term Frequency (TF)**: Measures how often a word appears in a document
- Example: If "neural" appears 3 times in a 100-word document, TF = 3/100 = 0.03

**Inverse Document Frequency (IDF)**: Measures how rare a word is across all documents
- Example: If "neural" appears in only 2 out of 1000 documents, IDF = log(1000/2) = 6.21
- Common words like "the" have low IDF; rare technical terms have high IDF

**TF-IDF Score**: TF × IDF
- Highlights words that are frequent in one document but rare across the collection
- Developed by Karen Spärck Jones, who pioneered the concept of term specificity

### How BM25 Improves Upon TF-IDF

**Key BM25 Improvements:**

1. **Term Frequency Saturation**: BM25 reduces the impact of repeated terms using term frequency saturation
   - Problem: In TF-IDF, if a word appears 100 times vs 10 times, the score increases linearly
   - Solution: BM25 uses a saturation function that plateaus after a certain frequency

2. **Document Length Normalization**: BM25 adjusts for document length, making it more effective for keyword-based search
   - Problem: In TF-IDF, longer documents have unfair advantages
   - Solution: BM25 normalizes scores based on document length relative to average

3. **Tunable Parameters**: Allows fine-tuning for different types of content
   - k1 ≈ 1.2: Controls term frequency saturation (how quickly scores plateau)
   - b ≈ 0.75: Controls document length normalization (0=none, 1=full)

### When to Use BM25

**Ideal for:**
- Technical documentation where exact terms matter
- Legal documents with specific terminology
- Product catalogs with precise specifications
- Academic papers with specialized vocabulary
- Applications requiring keyword-based retrieval rather than semantic similarity

**Advantages:**
- Excellent precision for exact term matches
- Fast computational performance
- Proven effectiveness in production systems
- No training required (unlike neural approaches)
- Interpretable scoring mechanism

**Limitations:**
- No semantic understanding (doesn't handle synonyms)
- Struggles with typos and variations
- Limited context understanding
- Requires careful parameter tuning for optimal performance


---

# 3. Document Summary Index Retriever

Document Summary Index Retrievers use document summaries instead of the actual documents to find relevant content, making them efficient for large collections. **They return the original documents, not their summaries.**

**How it works (from authoritative source)**:
- **Generates and stores summaries of documents** at indexing time
- **Uses summaries to filter documents** before retrieving full content
- **Two-stage Process**: First uses summaries to filter documents, then returns full document content
- **Especially useful for large, diverse corpora** that cannot fit in the context window of an LLM

**Two Retrieval Options**: 
1. **DocumentSummaryIndexLLMRetriever**: 
   - Uses a large language model to analyze the query against document summaries
   - Provides intelligent document selection but can be more time-consuming and expensive
   - Best for complex queries requiring nuanced understanding

2. **DocumentSummaryIndexEmbeddingRetriever**: 
   - Uses semantic similarity between the query and summary embeddings
   - Faster and more cost-effective than LLM-based approach
   - Good for straightforward similarity matching

**When to use (based on authoritative guidance):**
- Large document collections where documents cover different topics
- When you need efficient document-level filtering before detailed retrieval
- Multi-document QA where documents have distinct subject matters
- Large and diverse document sets that cannot fit in the context window of an LLM

**Configuration Parameters:**
- `choice_top_k` (LLM retriever): Number of documents to select
- `similarity_top_k` (Embedding retriever): Number of documents to select
- Default is 1, increase for multiple document retrieval

**Key Point**: **Returns original documents, not their summaries** - the summaries are only used for filtering

**Strengths**: 
- Efficient document selection and reduces search space
- Good for heterogeneous collections with diverse topics
- Returns original documents with full context intact

**Limitations**: 
- Requires LLM for summary generation during indexing
- May lose some detail present in original documents during summary creation
- LLM-based version can be slower and more expensive than other options

---
# 4. Auto Merging Retriever - Hierarchical Context Preservation

Auto Merging Retriever is designed to preserve context in long documents using a hierarchical structure. **It uses hierarchical chunking to break documents into parent and child nodes, and if enough child nodes from the same parent are retrieved, the retriever returns the parent node instead.**

**How it works (from authoritative source)**:
- **Uses hierarchical chunking** to break documents into parent and child nodes
- **Retrieves parent if enough children match** - intelligent merging logic
- **Preserves context in long documents** by consolidating related content
- **Dual Storage**: Smaller child chunks are indexed in the vector store for precise matching, while larger parent chunks are stored in the docstore

**Key behavior pattern**:
- Child chunks enable precise matching for specific queries
- When multiple child chunks from the same parent are retrieved, the system returns the parent chunk
- This **helps consolidate related content and preserve broader context**

**When to use (based on authoritative guidance):**
- Long documents where small chunks lose important surrounding context
- Legal documents, research papers, technical specifications that need context preservation
- When you need both precise matching and comprehensive context
- Documents with natural hierarchical structure (sections, subsections)

**Configuration:**
- `chunk_sizes`: List of chunk sizes from largest to smallest (e.g., [512, 256, 128])
- `chunk_overlap`: Overlap between chunks to maintain continuity
- Storage context manages both vector store (child nodes) and docstore (parent nodes)

**Strengths**: 
- Automatically preserves context without manual intervention
- Reduces information fragmentation in long documents
- Intelligent merging based on retrieval patterns
- Maintains granular search capability while providing broader context

**Limitations**: 
- More complex setup compared to basic retrievers
- Requires hierarchical document structure to be effective
- Higher storage overhead due to multiple chunk levels
- May not be suitable for very short documents

*Based on: https://docs.llamaindex.ai/en/stable/examples/retrievers/auto_merging_retriever/*

# 5. Recursive Retriever - Multi-Level Reference Following

The Recursive Retriever is **designed to follow relationships between nodes using references**. **It can follow references from one node to another, such as citations in academic papers or other metadata links**, allowing it to **retrieve related content across documents or layers of abstraction**.

**How it works (from authoritative source)**:
- **Follows node references** - traverses relationships to find referenced content
- **Supports chunk and metadata linking** - handles different types of references
- **Multi-Level Navigation**: Can execute sub-queries on referenced retrievers or query engines
- **Network Building**: Creates a network of interconnected retrievers that can reference each other

**Reference Types Supported**:
1. **Chunk References**: Smaller child chunks refer to larger parent chunks for additional context
2. **Metadata References**: Summaries or generated questions refer to larger content chunks, such as citations in academic papers

**When to use (based on authoritative guidance):**
- **Academic papers with citations** and extensive references
- **Research papers** where you need to retrieve relevant content from cited papers
- Documentation with cross-references and linked content
- Knowledge bases with interconnected information
- When nodes reference structured data (tables, databases, other documents)

**Configuration:**
- `retriever_dict`: Maps node IDs or keys to specific retrievers
- `query_engine_dict`: Maps keys to query engines for sub-queries
- Node metadata can contain references to other nodes or data structures

**Key capability**: **Retrieves related content across documents** by following reference chains

**Strengths**: 
- Follows complex relationships and enables multi-step reasoning
- Provides comprehensive coverage across related documents
- Excellent for handling interconnected information systems
- Can traverse multiple levels of references automatically

**Limitations**: 
- Requires careful setup of node relationships
- Can be computationally expensive for deep reference chains
- Complex debugging when reference chains are extensive
- May retrieve too much related content if not properly configured

*Based on: https://docs.llamaindex.ai/en/stable/examples/retrievers/recurisve_retriever_nodes_braintrust/*

# 6. Query Fusion Retriever - Multi-Query Enhancement with Advanced Fusion

The Query Fusion Retriever **combines results from different retrievers** (such as vector-based and keyword-based methods) and **optionally generates multiple variations of a query using an LLM to improve coverage**. **The results are merged using fusion strategies** to improve recall.

**How it works (from authoritative source)**:
- **Combines results from multiple retrievers** - e.g., vector-based and keyword-based methods
- **Supports multiple query variations** - generates different formulations of the same query
- **Uses fusion strategies to improve recall** - sophisticated merging techniques
- **Improved Coverage**: Reduces impact of query formulation on final results

**Core capabilities**:
1. **Multiple Retriever Support**: Combines results from different retrievers
2. **Query Variation Generation**: Optionally generates multiple variations of a query using an LLM
3. **Fusion Strategies**: Merges results using sophisticated fusion techniques

**Fusion Strategies Supported (from authoritative source)**:
1. **Reciprocal Rank Fusion (RRF)**: **Combines rankings across queries** - robust and doesn't rely on score magnitudes
2. **Relative Score Fusion**: **Normalizes scores within each result set** - preserves the relative confidence of each retriever
3. **Distribution-Based Fusion**: **Uses statistical normalization** - ideal for handling score variability

**When to use (based on authoritative guidance):**
- General Q&A where you want to combine semantic relevance with keyword matching
- Complex or ambiguous queries that may benefit from multiple formulations
- When query phrasing significantly impacts results
- Research and exploratory search scenarios
- When users provide under-specified or unclear queries

**Configuration:**
- `num_queries`: Number of query variations to generate (default: 4)
- `mode`: Fusion strategy ("reciprocal_rerank", "relative_score", "dist_based_score")
- `similarity_top_k`: Number of results to retrieve per query
- `use_async`: Enable async processing for better performance

**Key benefit**: **Uses fusion strategies such as reciprocal rank fusion or relative score fusion** to intelligently combine results

**Strengths**: 
- Improved recall through multiple query formulations
- Handles query variations effectively
- Reduces query sensitivity
- Combines strengths of different retrieval methods

**Limitations**: 
- Higher computational cost due to multiple retrievers/queries
- Requires LLM for query generation (additional cost)
- May introduce noise if fusion strategies are not well-tuned
- More complex setup and configuration

# Query Expansion Example

Original Query:

```
How do I scale Kubernetes?
```

Generated Variations:

```
Kubernetes scaling
Cluster autoscaling
Horizontal pod autoscaler
Scaling worker nodes
```

This improves coverage.

---

# Fusion Strategies Supported by Query Fusion Retriever

---

## 6.1 Reciprocal Rank Fusion (RRF) Mode

Reciprocal Rank Fusion (RRF) is a search-ranking algorithm used to combine multiple ranked lists of search results into a single, unified list without needing to normalize varying similarity scores. It is widely used in Retrieval-Augmented Generation (RAG) pipelines to merge keyword (BM25) and semantic (vector) search results.

**How it works within QueryFusionRetriever**:
- Generates multiple query variations (e.g., "machine learning approaches", "ML techniques", "learning algorithms")
- Retrieves results for each query variation
- Calculates reciprocal rank score: `1 / (rank + k)` where k is typically 60
- Sums reciprocal rank scores across all query variations for each document
- Re-ranks documents by combined RRF scores

**Mathematical formula**:
```
RRF_score(d) = Σ (1 / (rank_i(d) + k))
```
Where:
- `d` is a document
- `rank_i(d)` is the rank of document d in query variation i's results
- `k` is a constant (typically 60) that controls the fusion behavior

**Why RRF works well for query fusion**:
- **Scale-invariant**: Works regardless of individual query result score ranges
- **Robust to outliers**: Reciprocal function reduces impact of extreme rankings
- **Query-agnostic**: Doesn't depend on specific query formulations
- **Proven effectiveness**: Well-established in information retrieval research

**When to use RRF mode**:
- Default choice for most query fusion scenarios
- When query variations might have very different result qualities
- When you want stable, predictable fusion behavior
- For production systems requiring consistent performance

**Advantages**:
- Most stable fusion method across different query types
- No parameter tuning required beyond the standard k=60
- Handles varying numbers of results per query variation gracefully
- Computationally efficient

**Limitations**:
- Loses absolute score information from individual queries
- Treats all query variations equally (no weighting)
- May not leverage score magnitude differences effectively

*Based on: https://docs.llamaindex.ai/en/stable/examples/retrievers/reciprocal_rerank_fusion/*

## 6.2 Relative Score Fusion Mode

Relative Score Fusion (RSF) is a hybrid search algorithm that normalizes and combines scores from multiple search modalities (e.g., vector search and BM25) into a unified scale. It scales the highest score to 1 and the lowest to 0, allowing systems to perform a weighted sum of relevance

**How it works within QueryFusionRetriever**:
- Generates multiple query variations using LLM
- Retrieves results for each query variation
- Normalizes each query's scores by dividing by the maximum score in that query's results
- Creates scores in the range [0, 1] where 1 is the best result from each query variation
- Combines normalized scores using weighted average or sum

**Mathematical approach**:
```
normalized_score_i(d) = score_i(d) / max_score_i
combined_score(d) = Σ (weight_i × normalized_score_i(d))
```

**Why Relative Score Fusion is valuable for query variations**:
- **Preserves score magnitudes**: Unlike RRF, retains information about how confident each query was about its results
- **Fair combination**: Ensures no single query variation dominates due to different scoring scales
- **Interpretable results**: Final scores reflect the relative strength across query variations
- **Flexible weighting**: Can weight certain query formulations more heavily if desired

**When to use Relative Score mode**:
- When you trust the embedding model's confidence scores
- For queries where score magnitudes are meaningful
- When different query variations should contribute proportionally to their confidence
- In scenarios where you want to understand why certain results ranked highly

**Configuration within QueryFusionRetriever**:
- Automatically handles score normalization across query variations
- Equal weighting of all query variations by default
- Preserves relative differences in retriever confidence

**Advantages**:
- Preserves valuable score magnitude information
- Intuitive normalization approach
- Works well when retriever scores are reliable
- More interpretable than pure rank-based methods

**Limitations**:
- Sensitive to outlier scores within individual query results
- Assumes retriever scores are meaningful and comparable
- May not handle unreliable scoring mechanisms well

*Based on: https://docs.llamaindex.ai/en/stable/examples/retrievers/relative_score_dist_fusion/*

## 6.3 Distribution-Based Score Fusion Mode

Distribution-Based Score Fusion (DBSF) is an algorithm used in information retrieval and biometric identification to combine search results from multiple models. It resolves the issue of comparing raw similarity scores across different sources (e.g., Cosine Similarity vs. BM25) by normalizing their distribution tails to create a standardized scale.

**How it works within QueryFusionRetriever**:
- Generates multiple query variations using LLM
- Analyzes the statistical distribution of scores from each query variation
- Normalizes scores using distribution parameters (mean, standard deviation, percentiles)
- Applies statistical transformations like z-score normalization or percentile ranking
- Combines normalized scores with confidence weighting based on distribution characteristics

**Statistical approaches used**:
1. **Z-score normalization**: Centers scores around mean with unit variance
   - Formula: `z_score = (score - mean) / std_dev`
   - Converts to [0,1] range using sigmoid: `1 / (1 + exp(-z_score))`

2. **Percentile ranking**: Converts scores to percentile positions
   - Formula: `percentile = rank(score) / total_results`

3. **Distribution-aware normalization**: Considers score distribution shape
   - Uses IQR (Interquartile Range) to adjust for distribution spread
   - Handles multi-modal distributions from different query variations

**Why Distribution-Based Fusion excels for query variations**:
- **Statistical robustness**: Accounts for how scores are distributed within each query variation
- **Adaptive weighting**: Can weight query variations based on their score distribution confidence
- **Outlier handling**: Statistical methods naturally handle extreme scores
- **Multi-modal support**: Each query variation may have different score distribution characteristics

**When to use Distribution-Based mode**:
- When query variations produce very different score distributions
- For complex queries where some variations are much more reliable than others
- When you need statistically principled score combination
- In scenarios with noisy or unreliable retrieval scoring

**Advanced features in QueryFusionRetriever context**:
- Automatic distribution analysis for each query variation
- Confidence-based weighting of query variations
- Robust handling of varying result set sizes
- Statistical outlier detection within query results

**Advantages**:
- Most statistically principled approach to query fusion
- Handles complex score distributions effectively
- Adapts to different query variation characteristics
- Robust to various types of score variability and noise

**Limitations**:
- Most computationally intensive fusion method
- Requires sufficient results for reliable distribution estimation
- May over-normalize in some simple scenarios
- More complex to interpret than simpler fusion methods

*Based on: https://docs.llamaindex.ai/en/stable/examples/retrievers/relative_score_dist_fusion/*

# Recommended Retriever Selection

## General Q&A

Use:

* Vector Index Retriever
* BM25 Retriever

### Example

Query:

```
How can I reset my account password?
```

Vector search understands meaning.

BM25 catches exact terms.

---

## Technical Documents

Use:

* BM25 Retriever (Primary)
* Vector Index Retriever (Secondary)

### Example

Query:

```
Kubernetes HPA
```

Exact terminology matters, making BM25 more important.

---

## Long Documents

Use:

* Auto Merging Retriever

### Example

Books
Technical Manuals
Legal Contracts

Preserves parent-child context.

---

## Research Papers

Use:

* Recursive Retriever

### Example

Research papers with citations and references.

---

## Large Document Sets

Use:

### Step 1

Document Summary Index Retriever

### Step 2

Vector Search

### Example

100,000 research papers

Summary search narrows the candidate set before semantic retrieval.

---

# Production RAG Architecture Example

User Query
↓
Query Fusion Retriever
├── Vector Retriever
├── BM25 Retriever
↓
Merged Results
↓
Reranker (Optional)
↓
LLM
↓
Final Answer

## Benefits

* Better Recall
* Better Precision
* Semantic Understanding
* Exact Keyword Matching
* Scalable Retrieval Pipeline

| Retriever                              | Searches Using                  | Understands Meaning?      | Uses Keywords? | Uses LLM? | Best For                   | Example Query                        |
| -------------------------------------- | ------------------------------- | ------------------------- | -------------- | --------- | -------------------------- | ------------------------------------ |
| Vector Index Retriever                 | Embeddings (Vector Similarity)  | ✅ Yes                     | ❌ No           | ❌ No      | General RAG, Q&A           | "How do I recover my account?"       |
| BM25 Retriever                         | Exact Keywords                  | ❌ No                      | ✅ Yes          | ❌ No      | Technical Docs             | "Kubernetes HPA"                     |
| Document Summary Retriever (Embedding) | Document Summaries + Embeddings | ✅ Yes                     | ❌ No           | ❌ No      | Large Document Collections | "Revenue growth trends"              |
| Document Summary Retriever (LLM)       | Document Summaries              | ✅ Yes                     | Optional       | ✅ Yes     | High Accuracy Filtering    | "What does this document discuss?"   |
| Auto Merging Retriever                 | Retrieved Child Chunks          | Depends on Base Retriever | Depends        | ❌ No      | Long Documents             | "Explain microservices architecture" |
| Recursive Retriever                    | References/Citations            | Depends on Base Retriever | Depends        | ❌ No      | Research Papers            | "How do transformers work?"          |
| Query Fusion Retriever                 | Multiple Retrievers             | ✅ Yes                     | ✅ Yes          | Optional  | Production RAG             | Any Query                            |


| Situation                 | Retriever                    |
| ------------------------- | ---------------------------- |
| General Chatbot           | Vector Retriever             |
| Technical Documentation   | BM25 + Vector                |
| Large Document Repository | Summary Retriever            |
| Long PDFs / Books         | Auto Merging                 |
| Research Papers           | Recursive                    |
| Production RAG            | Query Fusion + Vector + BM25 |
