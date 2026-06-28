# Introduction to RAG

## What is RAG

Retrieval-Augmented Generation (RAG) is a machine-learning technique that integrates information retrieval with generative AI to produce accurate and context-aware responses. By equipping generative models, such as large language models (LLMs), with access to external data sources, RAG enhances the model's ability to provide relevant and helpful answers to user prompts or queries.

---

# Why RAG?

To understand the value of RAG, we need to consider the limitations of generative models that aren't part of a RAG system. The following image describes the response generation process of an LLM that is not part of a RAG pipeline:

![Traditional LLM Pipeline](assets/LLM%20based%20RG%20Process.png)   

LLMs embedded in such pipelines cannot access external sources and are limited to the information provided by the user in a prompt and the information the LLM was trained on. Consequently, these LLMs are prone to generating responses that may be:

- Inaccurate
- Outdated
- Fabricated ("hallucinations")

Additionally, such responses often lack valid sources, making it difficult to trace their origin or verify their accuracy.

Now, consider a generative model integrated into an RAG system. The diagram below outlines the response generation component of such a system:

![RAG Pipeline](assets/RAG%20based%20RG%20Process.png)

In an RAG system, retrieved text from an external data store is combined with the user's prompt to create an **augmented prompt**. This approach provides several key benefits:

- **Enhanced Quality:** Incorporates relevant facts for more accurate and detailed responses.
- **Up-to-Date Info:** Accesses current data beyond the model's static training set.
- **Source Verification:** Allows users to verify accuracy by citing specific external sources.

---

# Why RAG over Long Context Models?

While modern models support context lengths up to 128,000+ tokens, RAG remains essential due to several key limitations of long-context reliance:

- **Input Dependency:** Users don't need to manually possess or provide source info; the system retrieves it automatically.
- **Unlimited Capacity:** RAG handles massive datasets (e.g., libraries exceeding 500k+ words) that still surpass context limits.
- **Reduced Redundancy:** Prevents "needle in a haystack" issues by only passing relevant info, avoiding focus dilution.
- **Faster Processing:** Smaller prompts significantly reduce the time needed for the LLM to analyze tokens.
- **Lower Costs:** Using fewer tokens in prompts reduces both computational and financial expenses.

---

# How does RAG work?

The following diagram illustrates the RAG process for a basic RAG system. Note that this is just one possible representation, and alternative diagrams may result from various modifications or adaptations of the RAG system. However, this diagram captures the core concept, as all variations build on the common themes presented here.

![RAG Process Diagram](assets/RAG%20based%20RG%20Process.png)

## RAG Process

The steps in the RAG process are as follows:

1. **Gather Sources**  
   Start with sources like office documents, company policies, or any other relevant information that may provide context for the user's future prompt.

2. **Embed Sources**  
   Pass the gathered information through an embedding model. The embedding model converts each chunk of text into a vector representation, which is essentially a fixed-length column of numbers.

3. **Store Vectors**  
   Store the embedded source vectors in a vector store — a specialized database optimized for storing and manipulating vector data.

4. **Obtain a User's Prompt**  
   Receive a prompt from the user.

5. **Embed the User's Prompt**  
   Embed the user's prompt using the same embedding model used for the source documents. This produces a prompt embedding, which is a vector of numbers equal in length to the vectors representing the source embeddings.

6. **Retrieve Relevant Data**  
   Pass the prompt embedding to the retriever. The retriever also accesses the vector store to find and pull relevant source embeddings (vectors) that match the prompt embedding. The retriever's output is the retrieved text.

7. **Create an Augmented Prompt**  
   Combine the retrieved text with the user's original prompt to form an augmented prompt.

8. **Obtain a Response**  
   Feed the augmented prompt into a large language model (LLM), which processes it and produces a response.

---

# RAG Details

There are many nuances to each of the RAG steps highlighted above. Some of these details are elaborated on below.

---

## Gather Sources

Gathering sources often involves preprocessing the data before moving to the next step.

Preprocessing may include:

- Converting source files into more machine-friendly formats (for example, turning PDFs into plain text)
- Utilizing dynamic preprocessing libraries before passing documents to the next phase

---

## Embed Sources

### Steps involved in embedding documents

#### Chunking

Large documents are split into smaller, manageable chunks to enable efficient retrieval.

#### Embedding

Text chunks are processed by an embedding model, distinct from the LLM used for response generation. This embedding model transforms text chunks into fixed-length numeric vectors that capture their semantic meaning.

### How embedding works

#### Tokenization

Text is split into tokens (for example, words, parts of words, punctuation). Each token is assigned (encoded with) a unique numerical ID with no intrinsic meaning — IDs are consistent for the same token.

#### Neural Network Processing

Token IDs are input into the embedding model's neural network, producing fixed-length vectors that encapsulate the text's semantic meaning.

---

## Store Vectors

Embedding vectors are stored for future retrieval.

Simple systems use matrices, but most utilize specialized vector databases like:

- ChromaDB
- FAISS
- Milvus

Each database offers unique features and limitations.

---

## Obtain a User's Prompt

A user's prompt can either be standalone or incorporate prior conversation history.

If a discussion history is included, conversation memory tools (for example, LangChain, LlamaIndex) help augment the current prompt with the relevant context.

---

## Embed the User's Prompt

The user's prompt is embedded using the same embedding model as the source documents, ensuring compatibility.

---

## Retrieve Relevant Data

Various retrieval strategies exist, such as:

- Retrieving the most relevant text chunk
- Fetching the entire document containing the relevant chunk
- Retrieving multiple relevant documents

---

## Create an Augmented Prompt

Augmented prompts merge the user's original query with retrieved data.

Common methods include:

- Simple concatenation of the user's prompt with retrieved text
- Using structured templates where different components (for example, user input, retrieved text) are placed alongside additional instructions for the LLM to follow

---

## Obtain a Response

Responses can be further refined using predefined templates, ensuring a consistent presentation style tailored to the use case.

The many intricacies of each RAG step contribute to a wide range of implementation possibilities, enabling customization to suit various applications and needs.