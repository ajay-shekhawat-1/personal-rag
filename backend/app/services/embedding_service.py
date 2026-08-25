from functools import lru_cache

from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"


@lru_cache
def get_embedding_model() -> TextEmbedding:
    """
    Load the embedding model once and reuse it.
    """
    return TextEmbedding(
        model_name=MODEL_NAME
    )


def create_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """
    Convert multiple text chunks into embeddings.
    """

    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.embed(texts)

    return [
        embedding.tolist()
        for embedding in embeddings
    ]