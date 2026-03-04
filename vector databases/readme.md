## What is a Vector DB
Vector databases are specialized data structures designed for storing and retrieving high-dimensional data efficiently. They are particularly useful when dealing with large datasets that require complex queries or need to handle high-dimensional data. They encode information as vectors in a multi-dimensional space, allowing you to perform efficient and accurate searches based on the similarity of these vectors.

```
           Vector DB Pipeline

  Raw Data          Embedding Model         Vector DB
 ┌─────────┐       ┌──────────────┐       ┌──────────────┐
 │  Text    │       │              │       │  [0.2, 0.8]  │
 │  Images  │ ───►  │  Transform   │ ───►  │  [0.5, 0.1]  │
 │  Audio   │       │  to Vectors  │       │  [0.9, 0.3]  │
 └─────────┘       └──────────────┘       └──────────────┘
                                                 │
                                                 ▼
                                           ┌──────────┐
                                    Query  │ Similar  │
                                    ───►   │ Results  │
                                           └──────────┘
```

### Components of a Vector DB
1. Vector
2. Dimensionality
3. Similarity Search

### What is a Vector?
A vector is a mathematical representation of data that consists of multiple components or dimensions. It has a direction and magnitude. In mathematics, it can be represented as an ordered list of numbers.

Example:
```
camp 1 --------> camp 2
```
Magnitude = 1 KM (Distance between camp1 and camp2)
Direction = To camp 2

Databases that hold vectors are called Vector Databases.

```python
import numpy as np

# Create two simple vectors
vector_a = np.array([1.0, 2.0, 3.0])
vector_b = np.array([4.0, 5.0, 6.0])

# Calculate Euclidean distance between them
distance = np.linalg.norm(vector_a - vector_b)
print(f"Distance: {distance:.2f}")  # 5.20
```

### Why do we need a vector database? Why not relational databases?
80% or more data in the world is unstructured. For example we have a lot of text documents, images, videos, audio files etc. These need to be saved somewhere and searched later on. If we save unstructured data like an image in a relational or non-relational database, it needs to be tagged. This makes it difficult to search the data and perform similarity searches.

Vector databases are designed to handle high-dimensional data efficiently, mainly for unstructured data such as text documents, images, videos, audio files etc. They can store and retrieve information based on semantic similarity rather than exact matches. Relational databases are good for storing structured data, but they struggle with unstructured or high-dimensional data.

### What makes vector databases efficient?
Vector databases convert unstructured data into a numerical format called vectors. These vectors can be used to perform similarity searches and can be stored in a database. This allows us to search for similar documents, images, videos, audio files etc. efficiently.

### Why are vectors used in a Vector Database?

Each unstructured data can have multiple features. For example, a campsite can be close to the pool, whereas another can be close to the entrance.

Example:
```
# here each number represents a feature of the campsite.
camp 1(close to pool) --------> camp 2(close to entrance)
[-0.1, -0.3, -0.5]                    [-0.4,-0.6,-0.7]
```

Now two campsites can have similarities — for example, both of them are close to a water body (lake, pool). These kinds of similarities are inferences that we can use to search for similar documents. Using vectors, these similarities can be stored and used efficiently. There are specialised algorithms (e.g. nearest neighbor search) that can be used to find the similarity between vectors. This makes providing recommendations based on past choices made by the user possible.

```
        Similarity Search in 2D Space

    ▲ Feature 2
    │
  5 │              ○ Doc C
    │
  4 │    ● Query
    │          ○ Doc A     (nearest neighbor)
  3 │
    │                          ○ Doc D
  2 │  ○ Doc B
    │
  1 │
    └──────────────────────────────► Feature 1
    0    1    2    3    4    5    6

    ● = Query vector
    ○ = Stored vectors
    Doc A is closest to the query → most similar result
```

### Dimensionality

A vector is a mathematical object that has length or magnitude, which is the number of elements in the vector. The number of elements in a vector is called its dimensionality. The dimensionality of a vector determines how many features it can represent. For example, a vector with two elements is called a 2-dimensional vector, and a vector with three elements is called a 3-dimensional vector.

| Embedding Model     | Dimensions | Use Case                    |
|---------------------|------------|-----------------------------|
| Word2Vec            | 300        | Word embeddings             |
| BERT                | 768        | Sentence/document embeddings|
| OpenAI text-embedding-3-small | 1536 | General-purpose embeddings |
| OpenAI text-embedding-3-large | 3072 | High-accuracy embeddings   |

Higher dimensionality captures more nuance but requires more storage and compute.

### Similarity Search

Similarity search finds vectors that are closest to a given query vector. Different distance metrics are used depending on the use case:

| Metric           | Formula                          | Best For                        |
|------------------|----------------------------------|---------------------------------|
| Euclidean (L2)   | √(Σ(aᵢ - bᵢ)²)                 | When magnitude matters          |
| Cosine Similarity| (A·B) / (‖A‖ × ‖B‖)            | Text similarity, NLP            |
| Dot Product      | Σ(aᵢ × bᵢ)                     | When vectors are normalized     |

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Two similar documents (vectors point in similar directions)
doc1 = np.array([0.9, 0.1, 0.8])
doc2 = np.array([0.85, 0.15, 0.75])

# A dissimilar document
doc3 = np.array([0.1, 0.9, 0.2])

print(f"doc1 vs doc2: {cosine_similarity(doc1, doc2):.4f}")  # ~0.9985 (very similar)
print(f"doc1 vs doc3: {cosine_similarity(doc1, doc3):.4f}")  # ~0.4741 (dissimilar)
```

### Uniformity
Vectors convert the unstructured data into structured data, which makes it easier to store and retrieve information. The uniformity of vectors is achieved by converting the data into a numeric format. This allows for easy comparison and analysis of the data.

### Algorithms for Vector Similarity Search

As datasets grow to millions or billions of vectors, brute-force comparison against every stored vector becomes impractical. Approximate Nearest Neighbor (ANN) algorithms trade a small amount of accuracy for massive speed improvements.

| Algorithm | Full Name                              | How It Works                                                    |
|-----------|----------------------------------------|-----------------------------------------------------------------|
| HNSW      | Hierarchical Navigable Small World     | Builds a multi-layer graph; navigates from coarse to fine layers to find neighbors quickly |
| IVF       | Inverted File Index                    | Partitions vectors into clusters; only searches the closest clusters at query time          |
| LSH       | Locality-Sensitive Hashing             | Hashes similar vectors into the same buckets; reduces search space via hash lookups         |

Most vector databases use HNSW as their default indexing algorithm due to its strong balance of speed and recall accuracy.

### Popular Vector Databases

| Database   | Open Source | Managed Cloud | Key Strength                          |
|------------|-------------|---------------|---------------------------------------|
| ChromaDB   | Yes         | No            | Simple API, great for prototyping     |
| Pinecone   | No          | Yes           | Fully managed, low operational burden |
| Weaviate   | Yes         | Yes           | Built-in vectorization modules        |
| Milvus     | Yes         | Yes (Zilliz)  | Scales to billions of vectors         |
| Qdrant     | Yes         | Yes           | Rust-based, high performance          |

This project uses **ChromaDB** for its simplicity and Python-native API:

```python
import chromadb

# Create a client and collection
client = chromadb.Client()
collection = client.create_collection("campsites")

# Add documents — ChromaDB handles embedding automatically
collection.add(
    documents=[
        "Campsite near a lake with hiking trails",
        "Beach resort with swimming pool",
        "Mountain cabin close to ski slopes",
        "Lakeside campsite with fishing spots",
    ],
    ids=["camp1", "camp2", "camp3", "camp4"],
)

# Query for similar campsites
results = collection.query(
    query_texts=["camping by the water"],
    n_results=2,
)

print(results["documents"])
# Returns the two most semantically similar: lake/lakeside campsites
```

### Use Cases
1. **Recommendation systems**: Use vector databases to provide personalized recommendations based on user behavior. For example, a movie streaming service stores each movie as a vector of features (genre, mood, actors). When a user watches a thriller, the system finds movies with similar vectors.

2. **Semantic search**: Go beyond keyword matching to understand meaning. For example, searching "how to fix a flat tire" also returns results about "changing a punctured tyre" because their vectors are similar.

3. **Image recognition**: Store image embeddings and find visually similar images. For example, an e-commerce site lets users upload a photo of a dress and finds similar products in inventory.

4. **Clustering**: Vector databases can be used to cluster data based on their similarity.

5. **Fraud detection**: Vector databases can be used to detect fraud by comparing transactions with known patterns.

6. **Natural language processing**: Vector databases can be used for natural language processing, allowing computers to understand and analyze text data.

### Bibliography
- https://www.youtube.com/watch?v=jbLa0KBW-jY
