import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("shl_catalog")

model = SentenceTransformer("all-MiniLM-L6-v2")


def search_catalog(query, top_k=5):
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    recommendations = []

    for metadata, document in zip(
        results["metadatas"][0],
        results["documents"][0]
    ):
        recommendations.append({
            "name": metadata["name"],
            "url": metadata["url"],
            "test_type": metadata.get("test_type", ""),
            "description": document
        })

    return recommendations