## What is a Vector DB
Vector databases are specialized data structures designed for storing and retrieving high-dimensional data efficiently. They are particularly useful when dealing with large datasets that require complex queries or need to handle high-dimensional data. They encode information as vectors in a multi-dimensional space, allowing you to perform efficient and accurate searches based on the similarity of these vectors.

### Components of a Vector DB
1. Vector
2. Dimensionality
3. Similarity Search

### What is a Vector?
A vector is a mathematical representation of data that consists of multiple components or dimensions. It has a direction and magnatitude. In mathematics, it can be represented as an ordered list of numbers.

Example:
```
camp 1 --------> camp 2
```
Magnitude = 1 KM (Distance between camp1 and camp2)
Direction = To camp 2

Databases that hold vectors are called Vector Databases.

### Why do we need a vector database? Why not relational databases?
Vector databases are designed to handle high-dimensional data efficiently. They can store and retrieve information. Relational databases are good for storing structured data, but they struggle with unstructured or high-dimensional data. Vector databases are ideal for handling large datasets that require complex queries or need to handle high-dimensional data.

80% or more data in the world is unstructured. For example we have a lot of text documents, images, videos, audio files etc. These needs to be saved somewhere and can be searched later on. If we save these unstructured data like an image in a relational or non-relational database it needs to be tagged. It makes it difficult for us to search the data and perform similarity searches.

Vector databases are designed to handle high-dimensional data efficiently, mainly for unstructured data such as text documents, images, videos, audio files etc. They can store and retrieve information. Relational databases are good for storing structured data, but they struggle with unstructured or high dimensional data. Vector databases are ideal for handling large datasets that require complex queries or need to handle high-dimensional data.

### What makes vector databases efficient?
Vector databases are able to convert the unstructured data into a numerical format called vectors. These vectors can be used to perform similarity searches and can be stored in a database. This allows us to search for similar documents, images, videos, audio files etc. efficiently.

### Why are vectors used in a Vector Database?

Each unstructured data can have multiple features. for example, a campsite can be close to the pool, where as another can be close to entrance.

Example:
```
# here each number represents a feature of the campsite.
camp 1(close to pool) --------> camp 2(close to entrnace)
[-0.1, -0.3, -0.5]                    [-0.4,-0.6,-0.7]
```

Now two campsites can have similarities for example both of them are close to a water body(lake, pool). These kind of similarities are inferences that we can use to search for similar documents. And using vectors these similarities can be stored and used efficiently. There are specialised algorithms(e.g. nearest neighbor search) that can be used to find the similarity between vectors. This makes providing recommendations based on past choices made by the user possible.

### Dimensionality

A vector is a mathematical object that has length or magnitude, which is the number of elements in the vector. The number of elements in a vector is called its dimensionality. The dimensionality of a vector determines how many features it has. For example, a vector with two elements is called a 2-dimensional vector, and a vector with three elements is called a 3-dimensional vector. The dimensionality of a vector determines how many features it has.

### Uniformity
Vectors convert the unstructured data into structured data, which makes it easier to store and retrieve information.The uniformity of vectors is achieved by converting the data into a numeric format. This allows for easy comparison and analysis of the data.


### Usecases
1. Recommendation systems: Recommendation systems use vector databases to provide personalized recommendations based on user behavior.
2. Content-based filtering: Content-based filtering uses vector databases to find similar content and recommend it to the user.
3. Clustering: Vector databases can be used to cluster data based on their similarity.
4. Image recognition: Vector databases can be used for image recognition, allowing computers to recognize objects in images.
5. Fraud detection: Vector databases can be used to detect fraud by comparing transactions with known patterns.
6. Natural language processing: Vector databases can be used for natural language processing, allowing computers to understand and analyze text data. 

### Bibliography
https://www.youtube.com/watch?v=jbLa0KBW-jY
