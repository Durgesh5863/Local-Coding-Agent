import hashlib
from qdrant_client import QdrantClient

from embeddings.embedder import embed
from config.settings import QDRANT_HOST, QDRANT_PORT, TOP_K_RESULTS


def get_collection_name(repo_path):
    return hashlib.md5(repo_path.encode()).hexdigest()


def retrieve_files(repo_path, query):

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    collection = get_collection_name(repo_path)

    query_vector = embed(query)

    results = client.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=TOP_K_RESULTS
    )

    files = []

    for r in results:
        files.append(r.payload)

    return files