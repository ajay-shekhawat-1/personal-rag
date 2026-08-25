import { useEffect, useState } from "react";

import {
  deleteDocument,
  getDocuments,
} from "../services/api";


function DocumentList({ refreshKey }) {

  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);


  const loadDocuments = async () => {

    try {

      setLoading(true);
      setError("");

      const data = await getDocuments();

      if (Array.isArray(data)) {

        setDocuments(data);

      } else if (Array.isArray(data.documents)) {

        setDocuments(data.documents);

      } else {

        setDocuments([]);

      }

    } catch (err) {

      console.error(
        "Document loading error:",
        err
      );

      setError(
        err.response?.data?.detail ||
        "Unable to load documents."
      );

    } finally {

      setLoading(false);

    }
  };


  useEffect(() => {

    loadDocuments();

  }, [refreshKey]);


  const handleDelete = async (documentId) => {

    try {

      setDeletingId(documentId);
      setError("");

      await deleteDocument(documentId);

      setDocuments((currentDocuments) =>
        currentDocuments.filter(
          (document) =>
            (document.id || document.document_id) !== documentId
        )
      );

      setConfirmDeleteId(null);

    } catch (err) {

      console.error(
        "Delete error:",
        err
      );

      setError(
        err.response?.data?.detail ||
        "Unable to delete document."
      );

    } finally {

      setDeletingId(null);

    }
  };


  /* LOADING */

  if (loading) {

    return (
      <div className="documents-state">

        <div className="state-spinner"></div>

        <p>
          Loading knowledge base...
        </p>

      </div>
    );

  }


  /* ERROR */

  if (error) {

    return (
      <div className="documents-error">

        <div className="error-icon">
          !
        </div>

        <div>

          <strong>
            Unable to load knowledge base
          </strong>

          <p>
            {error}
          </p>

          <button
            type="button"
            onClick={loadDocuments}
            className="retry-button"
          >
            Try Again
          </button>

        </div>

      </div>
    );

  }


  /* EMPTY */

  if (documents.length === 0) {

    return (
      <div className="documents-empty">

        <div className="empty-icon">
          ◇
        </div>

        <h3>
          Knowledge base is empty
        </h3>

        <p>
          Upload a document or connect a website
          to start building your knowledge base.
        </p>

      </div>
    );

  }


  /* DOCUMENT LIST */

  return (
    <div className="document-list">

      <div className="document-list-header">

        <div>
          Indexed Sources
        </div>

        <div className="document-count">
          {documents.length}
          {" "}
          {documents.length === 1
            ? "source"
            : "sources"}
        </div>

      </div>


      {documents.map((document, index) => {

        const id =
          document.id ||
          document.document_id ||
          document.source_name ||
          `document-${index}`;


        const name =
          document.source_name ||
          document.filename ||
          document.name ||
          "Untitled document";


        const chunks =
          document.chunks ??
          document.chunk_count ??
          0;


        const source =
          document.source_type ||
          document.type ||
          "Document";


        const isDeleting =
          deletingId === id;


        const isConfirming =
          confirmDeleteId === id;


        return (
          <div
            className="document-card"
            key={id}
          >

            {/* DOCUMENT ICON */}

            <div className="document-icon">

              {source.toLowerCase().includes("url") ||
              source.toLowerCase().includes("web")
                ? "↗"
                : "▤"}

            </div>


            {/* DOCUMENT INFO */}

            <div className="document-info">

              <div className="document-name">
                {name}
              </div>

              <div className="document-details">

                <span className="document-type">
                  {source}
                </span>

                <span className="document-separator">
                  •
                </span>

                <span>
                  {chunks} chunks
                </span>

              </div>

            </div>


            {/* DELETE AREA */}

            <div className="document-actions">

              {!isConfirming && !isDeleting && (

                <button
                  type="button"
                  className="delete-document-button"
                  onClick={() =>
                    setConfirmDeleteId(id)
                  }
                >
                  <span>
                    ×
                  </span>

                  Delete
                </button>

              )}


              {isConfirming && !isDeleting && (

                <div className="delete-confirmation">

                  <span>
                    Delete?
                  </span>

                  <button
                    type="button"
                    className="confirm-delete-button"
                    onClick={() =>
                      handleDelete(id)
                    }
                  >
                    Yes
                  </button>

                  <button
                    type="button"
                    className="cancel-delete-button"
                    onClick={() =>
                      setConfirmDeleteId(null)
                    }
                  >
                    No
                  </button>

                </div>

              )}


              {isDeleting && (

                <div className="deleting-state">
                  Deleting...
                </div>

              )}

            </div>

          </div>
        );

      })}

    </div>
  );
}


export default DocumentList;