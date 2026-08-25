from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    PayloadSchemaType,
    VectorParams,
)

from app.config import (
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
    QDRANT_URL,
)


# ==================================================
# Vector configuration
# ==================================================

VECTOR_SIZE = 384


# ==================================================
# Qdrant client
# ==================================================

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


# ==================================================
# Check Qdrant connection
# ==================================================

def check_qdrant_connection():
    """
    Check whether Qdrant Cloud is reachable.
    """

    return client.get_collections()


# ==================================================
# Create collection + payload indexes
# ==================================================

def create_collection_if_not_exists():
    """
    Create the Qdrant collection if it does not exist.

    Also creates payload indexes required for filtering
    documents by user_id and document_id.
    """

    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    # ----------------------------------------------
    # Create collection
    # ----------------------------------------------

    if QDRANT_COLLECTION not in collection_names:

        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    # ----------------------------------------------
    # Create user_id index
    # ----------------------------------------------

    client.create_payload_index(
        collection_name=QDRANT_COLLECTION,
        field_name="user_id",
        field_schema=PayloadSchemaType.KEYWORD,
    )

    # ----------------------------------------------
    # Create document_id index
    # ----------------------------------------------

    client.create_payload_index(
        collection_name=QDRANT_COLLECTION,
        field_name="document_id",
        field_schema=PayloadSchemaType.KEYWORD,
    )

    return {
        "created": QDRANT_COLLECTION not in collection_names,
        "collection": QDRANT_COLLECTION,
        "indexes": [
            "user_id",
            "document_id",
        ],
    }


# ==================================================
# Insert document chunks
# ==================================================

def insert_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    source_name: str,
    source_type: str,
    document_id: str,
    user_id: str = "default",
) -> int:
    """
    Store document chunks and embeddings in Qdrant.
    """

    if not chunks:
        return 0

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    points = []

    for chunk_index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        point = PointStruct(
            id=str(uuid4()),

            vector=embedding,

            payload={
                "user_id": user_id,
                "document_id": document_id,
                "chunk_id": chunk_index,
                "source_name": source_name,
                "source_type": source_type,
                "text": chunk,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=points,
    )

    return len(points)


# ==================================================
# Search document chunks
# ==================================================

def search_chunks(
    query_embedding: list[float],
    user_id: str = "default",
    limit: int = 5,
    score_threshold: float = 0.35,
):
    """
    Search Qdrant for relevant document chunks.
    """

    if not query_embedding:
        return []

    if limit < 1:
        limit = 1

    results = client.query_points(
        collection_name=QDRANT_COLLECTION,

        query=query_embedding,

        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(
                        value=user_id
                    ),
                )
            ]
        ),

        limit=limit,

        score_threshold=score_threshold,

        with_payload=True,
    )

    return results.points


# ==================================================
# Get documents
# ==================================================

def get_documents(
    user_id: str = "default",
):
    """
    Get a list of documents stored in Qdrant.
    """

    documents = {}

    offset = None

    while True:

        records, offset = client.scroll(
            collection_name=QDRANT_COLLECTION,

            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(
                            value=user_id
                        ),
                    )
                ]
            ),

            limit=100,

            offset=offset,

            with_payload=True,

            with_vectors=False,
        )

        for record in records:

            payload = record.payload or {}

            document_id = payload.get(
                "document_id"
            )

            if not document_id:
                continue

            if document_id not in documents:

                documents[document_id] = {
                    "document_id": document_id,
                    "source_name": payload.get(
                        "source_name"
                    ),
                    "source_type": payload.get(
                        "source_type"
                    ),
                    "user_id": payload.get(
                        "user_id"
                    ),
                    "chunks": 0,
                }

            documents[document_id]["chunks"] += 1

        if offset is None:
            break

    return list(
        documents.values()
    )


# ==================================================
# Delete document
# ==================================================

def delete_document(
    document_id: str,
    user_id: str = "default",
) -> int:
    """
    Delete all vectors belonging to a document.
    """

    # ----------------------------------------------
    # Find document chunks
    # ----------------------------------------------

    records, _ = client.scroll(
        collection_name=QDRANT_COLLECTION,

        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(
                        value=user_id
                    ),
                ),
                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id
                    ),
                ),
            ]
        ),

        limit=1000,

        with_payload=False,

        with_vectors=False,
    )

    if not records:
        return 0

    # ----------------------------------------------
    # Get point IDs
    # ----------------------------------------------

    point_ids = [
        record.id
        for record in records
    ]

    # ----------------------------------------------
    # Delete vectors
    # ----------------------------------------------

    client.delete(
        collection_name=QDRANT_COLLECTION,

        points_selector=point_ids,
    )

    return len(point_ids)