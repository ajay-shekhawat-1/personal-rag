from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.embedding_service import create_embeddings
from app.services.qdrant_service import search_chunks
from app.services.llm_service import generate_answer


# --------------------------------------------------
# Router
# --------------------------------------------------

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# --------------------------------------------------
# Conversation message
# --------------------------------------------------

class ChatMessage(BaseModel):
    role: str
    content: str


# --------------------------------------------------
# Request model
# --------------------------------------------------

class ChatRequest(BaseModel):
    question: str
    user_id: str = "default"

    history: list[ChatMessage] = Field(
        default_factory=list
    )


# --------------------------------------------------
# Chat endpoint
# --------------------------------------------------

@router.post("/")
def chat(request: ChatRequest):
    """
    Answer a user's question using the RAG pipeline
    and previous conversation history.

    Flow:

        Question
            ↓
        Conversation History
            ↓
        Embedding
            ↓
        Qdrant Retrieval
            ↓
        Relevant Context
            ↓
        Groq LLM
            ↓
        Final Answer
    """

    # -----------------------------------------
    # 1. Validate question
    # -----------------------------------------

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )


    # -----------------------------------------
    # 2. Validate user ID
    # -----------------------------------------

    user_id = request.user_id.strip()

    if not user_id:
        user_id = "default"


    # -----------------------------------------
    # 3. Clean conversation history
    # -----------------------------------------

    history = []

    for message in request.history:

        role = message.role.strip().lower()
        content = message.content.strip()

        if role not in {"user", "assistant"}:
            continue

        if not content:
            continue

        history.append(
            {
                "role": role,
                "content": content,
            }
        )


    # -----------------------------------------
    # 4. Limit history
    # -----------------------------------------

    # Keep only the latest 10 messages.
    # This prevents the prompt from growing
    # indefinitely.

    history = history[-10:]


    # -----------------------------------------
    # 5. Create question embedding
    # -----------------------------------------

    try:

        query_embeddings = create_embeddings(
            [question]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to create question embedding: "
                f"{str(e)}"
            ),
        )


    if not query_embeddings:

        raise HTTPException(
            status_code=500,
            detail="Unable to create question embedding.",
        )


    query_embedding = query_embeddings[0]


    # -----------------------------------------
    # 6. Search Qdrant
    # -----------------------------------------

    try:

        results = search_chunks(
            query_embedding=query_embedding,
            user_id=user_id,
            limit=5,
            score_threshold=0.35,
        )

    except Exception as e:

        raise HTTPException(
            status_code=503,
            detail=(
                f"Unable to search Qdrant: {str(e)}"
            ),
        )


    # -----------------------------------------
    # 7. Check retrieved context
    # -----------------------------------------

    if not results:

        return {
            "success": True,
            "question": question,
            "answer": (
                "I could not find relevant information "
                "in your uploaded documents."
            ),
            "sources": [],
        }


    # -----------------------------------------
    # 8. Build context and sources
    # -----------------------------------------

    context_parts = []
    sources = []

    for result in results:

        payload = result.payload or {}

        text = payload.get(
            "text",
            "",
        )

        # -----------------------------------------
        # Add non-empty chunk
        # -----------------------------------------

        if text and text.strip():

            context_parts.append(
                text.strip()
            )


        # -----------------------------------------
        # Source information
        # -----------------------------------------

        sources.append(
            {
                "source_name": payload.get(
                    "source_name"
                ),
                "source_type": payload.get(
                    "source_type"
                ),
                "document_id": payload.get(
                    "document_id"
                ),
                "chunk_id": payload.get(
                    "chunk_id"
                ),
                "score": result.score,
            }
        )


    # -----------------------------------------
    # 9. Build final context
    # -----------------------------------------

    context = "\n\n".join(
        context_parts
    )


    if not context.strip():

        return {
            "success": True,
            "question": question,
            "answer": (
                "I could not find readable information "
                "in the retrieved documents."
            ),
            "sources": sources,
        }


    # -----------------------------------------
    # 10. Generate answer using Groq
    # -----------------------------------------

    try:

        answer = generate_answer(
            question=question,
            context=context,
            history=history,
        )

    except Exception as e:

        raise HTTPException(
            status_code=503,
            detail=(
                f"Unable to generate answer: {str(e)}"
            ),
        )


    # -----------------------------------------
    # 11. Validate LLM response
    # -----------------------------------------

    if not answer or not answer.strip():

        raise HTTPException(
            status_code=500,
            detail="The LLM returned an empty answer.",
        )


    # -----------------------------------------
    # 12. Return final response
    # -----------------------------------------

    return {
        "success": True,
        "question": question,
        "answer": answer.strip(),
        "sources": sources,
    }