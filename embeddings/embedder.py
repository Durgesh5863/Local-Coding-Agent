from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def embed(text):
    return model.encode(text).tolist()