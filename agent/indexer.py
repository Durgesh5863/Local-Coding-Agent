import os
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from embeddings.embedder import embed
from utils.repo_utils import scan_repo
from config.settings import QDRANT_HOST, QDRANT_PORT


def get_collection_name(repo_path):
    return hashlib.md5(repo_path.encode()).hexdigest()


def index_repo(repo_path):

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    collection = get_collection_name(repo_path)

    client.recreate_collection(
        collection_name=collection,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    files = scan_repo(repo_path)

    points = []

    for i, file in enumerate(files):

        vector = embed(file["content"])

        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={
                    "path": file["path"],
                    "content": file["content"]
                }
            )
        )

    client.upsert(collection_name=collection, points=points)

    print("Repo indexed:", repo_path)