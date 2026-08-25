from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.embedding_service import create_embeddings
from app.services.qdrant_service import (
    create_collection_if_not_exists,
    search_chunks,
)


# --------------------------------------------------
# Router
# --------------------------------------------------

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class SearchRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to search in uploaded data.",
    )

    user_id: str = Field(
        default="default",
        min_length=1,
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
    )


# --------------------------------------------------
# Search endpoint
# --------------------------------------------------

@router.post("/")
def search_documents(
    request: SearchRequest,
):
    """
    Convert the user's question into an embedding
    and retrieve the most relevant chunks from Qdrant.
    """

    # -----------------------------------------
    # 1. Clean question
    # -----------------------------------------

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    # -----------------------------------------
    # 2. Make sure collection exists
    # -----------------------------------------

    create_collection_if_not_exists()

    # -----------------------------------------
    # 3. Create embedding for question
    # -----------------------------------------

    try:

        embeddings = create_embeddings(
            [question]
        )

        if not embeddings:
            raise HTTPException(
                status_code=500,
                detail="Failed to create question embedding.",
            )

        query_embedding = embeddings[0]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to create question embedding: {str(e)}"
            ),
        )

    # -----------------------------------------
    # 4. Search Qdrant
    # -----------------------------------------

    try:

        results = search_chunks(
            query_embedding=query_embedding,
            user_id=request.user_id,
            limit=request.limit,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Qdrant search failed: {str(e)}"
            ),
        )

    # -----------------------------------------
    # 5. Format results
    # -----------------------------------------

    documents = []

    for result in results:

        payload = result.payload or {}

        documents.append(
            {
                "score": result.score,
                "text": payload.get(
                    "text",
                    "",
                ),
                "source_name": payload.get(
                    "source_name",
                ),
                "source_type": payload.get(
                    "source_type",
                ),
                "document_id": payload.get(
                    "document_id",
                ),
                "chunk_id": payload.get(
                    "chunk_id",
                ),
            }
        )

    # -----------------------------------------
    # 6. Return response
    # -----------------------------------------

    return {
        "success": True,
        "question": question,
        "results_count": len(documents),
        "results": documents,
    }