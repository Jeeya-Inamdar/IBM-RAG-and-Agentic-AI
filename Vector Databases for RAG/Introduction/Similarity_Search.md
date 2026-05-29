# Similarity Search


Similarity search is the process of finding items in a dataset that are most similar to a given query item.

It is widely used in:

- Recommendation systems
- Image retrieval
- Natural Language Processing (NLP)
- Face recognition systems

---

# 🔍 What is Cosine of an Angle?

The cosine of an angle is defined as:

$$\cos(\alpha)=\frac{\text{Adjacent}}{\text{Hypotenuse}}$$


![Cosine Triangle](../assets/image.png)


![Cosine Triangle](../assets/image%20copy.png)
# ➡️ What is a Vector?

A vector is a mathematical object that has:

- Magnitude (length)
- Direction

Example:

$$a = [4,8]$$

Vectors are represented on a Cartesian plane.

## Vector Representation

![Vector Diagram](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/Nt-qZvink5-7N2Y5AeLooA/Screenshot%202025-05-23%20at%203-26-13%E2%80%AFPM.png)

---

# 📏 Magnitude of a Vector


The magnitude of a vector is calculated using the L2 norm:

$$\|a\| = \sqrt{\sum_{k=1}^{n} a_k^2}$$

For a 2D vector:

$$\|a\| = \sqrt{x^2 + y^2}$$

Example:

$$a=[4,8]$$

$$\|a\| = \sqrt{4^2 + 8^2}$$

$$\|a\| \approx 8.94$$

---

# Multiple Vectors

Example vectors:

$$a=[4,8]$$

$$b=[11.5,5]$$

## Multiple Vector Visualization

![Multiple Vectors](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/qylHMInquwU-3NCCfA_QcA/Screenshot%202025-05-23%20at%201-31-08%E2%80%AFPM.png)

---

# 1️⃣ L2 Distance (Euclidean Distance)

## Definition

L2 distance measures the straight-line distance between two vectors.

$$L2(a,b)=\sqrt{\sum_{i=1}^{n}(a_i-b_i)^2}$$

---

## Example

$$a=[4,8]$$

$$b=[11.5,5]$$

$$L2(a,b)=\sqrt{(4-11.5)^2+(8-5)^2}$$

$$L2(a,b)\approx 8.08$$

---

## Euclidean Distance Diagram

![Euclidean Distance](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/OoUVTamIXV0S0GcuM3CVrg/Screenshot%202025-05-26%20at%203-49-12%E2%80%AFPM.png)

---

# 2️⃣ Dot Product Similarity

## Definition

The dot product of two vectors is:

$$a \cdot b = \sum_{i=1}^{n} a_i b_i$$

---

## Example

$$a=[4,8]$$

$$b=[11.5,5]$$

$$a \cdot b = 4 \times 11.5 + 8 \times 5$$

$$a \cdot b = 86$$

---

# Dot Product Using Angle

$$a \cdot b = \|a\|\|b\|\cos(\alpha)$$

---

## Dot Product Projection Visualization

![Dot Product Projection](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/e6c8ODQW0sPz95E00mTPHg/Screenshot%202025-05-23%20at%201-30-07%E2%80%AFPM.png)

It turns out that we can calculate the dot product $a \cdot b$ by multiplying the length of vector $b$ ($\|b\|$) by the length of the projection of $a$ onto $b$ ($\|c\|$):

$$a \cdot b = \|b\| \ \|c\|$$

Now, let $\alpha$ represent the angle between vectors $a$ and $b$ as shown in the above diagram. Note that the projection of $a$ onto $b$ forms a right-angle triangle with length $\|c\|$ forming an adjacent side for angle $\alpha$ and the length $\|a\|$ forming the hypotenuse. This allows us to use the following equation for the cosine of an angle:

$$\cos(\alpha) = \frac{\text{adjacent}}{\text{hypotenuse}}$$

$$\cos(\alpha) = \frac{\|c\|}{\|a\|}$$

Rearranging the above, we can solve for $\|c\|$:

$$\|c\| = \|a\| \cos(\alpha)$$

Finally, replacing $\|c\|$ with $\|a\| \cos(\alpha)$ in the calculation of the dot product:

$$a \cdot b = \|b\| \ \|c\|$$

$$a \cdot b = \|b\| \ \|a\| \cos(\alpha)$$

$$a \cdot b = \|a\| \ \|b\| \cos(\alpha)$$

![DOT product](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/8FsuIcqlyyZujKm7FURTzQ/Screenshot%202025-05-23%20at%201-29-48%E2%80%AFPM.png)

In the above image, the length of the projection of $a$ onto $b$ is depicted as $\|a\|\cos(\alpha)$, and the length of vector $b$ is indicated as $\|b\|$. The dot product $a \cdot b$ is just the product of the lengths $\|b\|$ and $\|a\| \cos(\alpha)$, or, when rearranged, $\|a\| \ \|b\| \cos(\alpha)$.

---

# 3️⃣ Cosine Similarity

## Definition

Cosine similarity measures the cosine of the angle between two vectors.

$$\text{cosine similarity}(a,b)=\frac{a \cdot b}{\|a\|\|b\|}$$

---

## Cosine Similarity Diagram

![Cosine Similarity](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Inner-product-angle.svg/512px-Inner-product-angle.svg.png)

---

# Cosine Distance

$$\text{cosine distance}(a,b)=1-\text{cosine similarity}(a,b)$$

---

# 🔄 Vector Normalization

To normalize a vector:

$$\text{norm}(a)=\frac{a}{\|a\|}$$

Example:

$$a=[4,8]$$

Normalized vector:

$$\text{norm}(a)\approx[0.448,0.895]$$

---

# 🧠 Choosing the Right Metric

| Metric | Sensitive to Magnitude | Best For |
|---|---|---|
| L2 Distance | ✅ Yes | Spatial data |
| Cosine Similarity | ❌ No | NLP, embeddings |
| Dot Product | ✅ Yes | Recommendations |

---

# 🧪 Practical Considerations

## L2 Distance
- Good for geometric data
- Sensitive to magnitude

## Cosine Similarity
- Excellent for text embeddings
- Works well in high-dimensional data

## Dot Product
- Computationally efficient
- Used heavily in neural networks

---

# ✅ Conclusion

Choosing the correct similarity metric is very important in machine learning and vector databases.

- Use **L2 Distance** when actual distance matters.
- Use **Cosine Similarity** for semantic similarity.
- Use **Dot Product** when both magnitude and direction matter.

---

# Author

**Wojciech "Victor" Fulmyk**