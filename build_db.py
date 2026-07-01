import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load catalog
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Create Chroma database
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="shl_catalog"
)

print("Building vector database...")

for item in catalog:

    text = f"""
Name: {item.get("name","")}

Description:
{item.get("description","")}

Job Levels:
{item.get("job_levels_raw","")}

Assessment Length:
{item.get("assessment_length","")}

Remote Testing:
{item.get("remote_testing","")}

Test Types:
{item.get("test_types_raw","")}
"""

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[item["entity_id"]],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{
            "name": item["name"],
            "url": item["link"],
            "test_type": item.get("test_types_raw", "")
        }]
    )

print("Database created successfully!")
print("Total assessments:", collection.count())