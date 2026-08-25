from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, HttpUrl

from app.services.document_service import (
    extract_text,
    extract_url,
)
from app.services.chunking_service import chunk_text
from app.services.embedding_service import create_embeddings

from app.services.qdrant_service import (
    create_collection_if_not_exists,
    insert_chunks,
    get_documents,
    delete_document,
)


# ==================================================
# Router
# ==================================================

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# ==================================================
# Supported document formats
# ==================================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}


# ==================================================
# Default user
# ==================================================

DEFAULT_USER_ID = "default"


# ==================================================
# URL request model
# ==================================================

class URLRequest(BaseModel):
    url: HttpUrl


# ==================================================
# Upload PDF / DOCX
# ==================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload a PDF or DOCX document.

    Pipeline:

    File
      ↓
    Text extraction
      ↓
    Chunking
      ↓
    Embeddings
      ↓
    Qdrant
    """

    # ----------------------------------------------
    # 1. Validate filename
    # ----------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported types: PDF and DOCX."
            ),
        )

    # ----------------------------------------------
    # 2. Create temporary file path
    # ----------------------------------------------

    temp_path = Path(
        f"temp_{uuid4()}{extension}"
    )

    try:

        # ------------------------------------------
        # 3. Read uploaded file
        # ------------------------------------------

        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        temp_path.write_bytes(
            file_content
        )

        # ------------------------------------------
        # 4. Extract text
        # ------------------------------------------

        text = extract_text(
            str(temp_path)
        )

        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found "
                    "in document."
                ),
            )

        # ------------------------------------------
        # 5. Create chunks
        # ------------------------------------------

        chunks = chunk_text(
            text
        )

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Document could not be "
                    "divided into chunks."
                ),
            )

        # ------------------------------------------
        # 6. Create embeddings
        # ------------------------------------------

        embeddings = create_embeddings(
            chunks
        )

        if not embeddings:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Unable to create document "
                    "embeddings."
                ),
            )

        # ------------------------------------------
        # 7. Make sure Qdrant collection exists
        # ------------------------------------------

        create_collection_if_not_exists()

        # ------------------------------------------
        # 8. Create document ID
        # ------------------------------------------

        document_id = str(
            uuid4()
        )

        # ------------------------------------------
        # 9. Store chunks in Qdrant
        # ------------------------------------------

        source_type = extension.replace(
            ".",
            "",
        )

        vectors_stored = insert_chunks(
            chunks=chunks,
            embeddings=embeddings,
            source_name=file.filename,
            source_type=source_type,
            document_id=document_id,
            user_id=DEFAULT_USER_ID,
        )

        # ------------------------------------------
        # 10. Return response
        # ------------------------------------------

        return {
            "success": True,
            "message": (
                "Document processed successfully."
            ),
            "document_id": document_id,
            "source_name": file.filename,
            "source_type": source_type,
            "characters": len(text),
            "chunks": len(chunks),
            "vectors_stored": vectors_stored,
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Document processing failed: {str(e)}"
            ),
        )

    finally:

        # ------------------------------------------
        # 11. Delete temporary file
        # ------------------------------------------

        if temp_path.exists():

            try:
                temp_path.unlink()
            except Exception:
                pass


# ==================================================
# Upload Website URL
# ==================================================

@router.post("/url")
def upload_url(
    request: URLRequest,
):
    """
    Extract website text and store it in Qdrant.

    Pipeline:

    URL
      ↓
    Web extraction
      ↓
    Chunking
      ↓
    Embeddings
      ↓
    Qdrant
    """

    url = str(
        request.url
    )

    # ----------------------------------------------
    # 1. Extract website text
    # ----------------------------------------------

    try:

        text = extract_url(
            url
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unable to extract website: {str(e)}"
            ),
        )

    # ----------------------------------------------
    # 2. Validate extracted text
    # ----------------------------------------------

    if not text or not text.strip():

        raise HTTPException(
            status_code=400,
            detail=(
                "No readable text found "
                "on the website."
            ),
        )

    # ----------------------------------------------
    # 3. Create chunks
    # ----------------------------------------------

    chunks = chunk_text(
        text
    )

    if not chunks:

        raise HTTPException(
            status_code=400,
            detail=(
                "Website text could not be "
                "divided into chunks."
            ),
        )

    # ----------------------------------------------
    # 4. Create embeddings
    # ----------------------------------------------

    embeddings = create_embeddings(
        chunks
    )

    if not embeddings:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to create website "
                "embeddings."
            ),
        )

    # ----------------------------------------------
    # 5. Make sure Qdrant collection exists
    # ----------------------------------------------

    create_collection_if_not_exists()

    # ----------------------------------------------
    # 6. Create document ID
    # ----------------------------------------------

    document_id = str(
        uuid4()
    )

    # ----------------------------------------------
    # 7. Store vectors in Qdrant
    # ----------------------------------------------

    vectors_stored = insert_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source_name=url,
        source_type="url",
        document_id=document_id,
        user_id=DEFAULT_USER_ID,
    )

    # ----------------------------------------------
    # 8. Return response
    # ----------------------------------------------

    return {
        "success": True,
        "message": (
            "Website processed successfully."
        ),
        "document_id": document_id,
        "source_name": url,
        "source_type": "url",
        "characters": len(text),
        "chunks": len(chunks),
        "vectors_stored": vectors_stored,
    }


# ==================================================
# Get all documents
# ==================================================

@router.get("/")
def list_documents():
    """
    Return all documents stored in Qdrant
    for the default user.
    """

    try:

        documents = get_documents(
            user_id=DEFAULT_USER_ID
        )

        return {
            "success": True,
            "documents": documents,
            "count": len(documents),
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Unable to get documents: {str(e)}"
            ),
        )


# ==================================================
# Delete document
# ==================================================

@router.delete("/{document_id}")
def remove_document(
    document_id: str,
):
    """
    Delete a complete document from Qdrant.

    All chunks/vectors belonging to the
    document will be deleted.
    """

    if not document_id.strip():

        raise HTTPException(
            status_code=400,
            detail="Document ID cannot be empty.",
        )

    try:

        deleted_count = delete_document(
            document_id=document_id,
            user_id=DEFAULT_USER_ID,
        )

        if deleted_count == 0:

            raise HTTPException(
                status_code=404,
                detail=(
                    "Document not found."
                ),
            )

        return {
            "success": True,
            "message": (
                "Document deleted successfully."
            ),
            "document_id": document_id,
            "vectors_deleted": deleted_count,
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Unable to delete document: {str(e)}"
            ),
        )