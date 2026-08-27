import { useState } from "react";

import {
  uploadDocument,
  uploadUrl,
} from "../services/api";


function UploadDocument({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");


  // ==================================================
  // FILE SELECTION
  // ==================================================

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    setMessage("");
    setError("");

    if (!selectedFile) {
      setFile(null);
      return;
    }

    const fileName = selectedFile.name.toLowerCase();

    const isValidFile =
      fileName.endsWith(".pdf") ||
      fileName.endsWith(".docx");

    if (!isValidFile) {
      setFile(null);

      event.target.value = "";

      setError(
        "Unsupported file type. Please select a PDF or DOCX file."
      );

      return;
    }

    setFile(selectedFile);
  };


  // ==================================================
  // DOCUMENT UPLOAD
  // ==================================================

  const handleFileUpload = async () => {
    if (!file) {
      setError("Please select a PDF or DOCX file.");
      return;
    }

    setLoading(true);
    setMessage("");
    setError("");

    try {
      const data = await uploadDocument(file);

      setMessage(
        `${data.source_name || file.name} uploaded successfully. ` +
        `${data.chunks || 0} chunks stored in Qdrant.`
      );

      setFile(null);

      const input = document.getElementById(
        "document-file-input"
      );

      if (input) {
        input.value = "";
      }

      if (onUploadSuccess) {
        onUploadSuccess();
      }

    } catch (err) {
      console.error("Document upload error:", err);

      setError(
        err.response?.data?.detail ||
        "Unable to upload document."
      );

    } finally {
      setLoading(false);
    }
  };


  // ==================================================
  // WEBSITE URL
  // ==================================================

  const handleUrlUpload = async () => {
    const cleanUrl = url.trim();

    if (!cleanUrl) {
      setError("Please enter a website URL.");
      return;
    }

    setLoading(true);
    setMessage("");
    setError("");

    try {
      const data = await uploadUrl(cleanUrl);

      setMessage(
        `Website processed successfully. ` +
        `${data.chunks || 0} chunks stored in Qdrant.`
      );

      setUrl("");

      if (onUploadSuccess) {
        onUploadSuccess();
      }

    } catch (err) {
      console.error("Website processing error:", err);

      setError(
        err.response?.data?.detail ||
        "Unable to process website."
      );

    } finally {
      setLoading(false);
    }
  };


  // ==================================================
  // UI
  // ==================================================

  return (
    <section className="upload-section">

      {/* ==========================================
          FILE UPLOAD
      ========================================== */}

      <div className="upload-card">

        <div className="upload-card-icon">
          ↑
        </div>

        <div className="upload-card-content">

          <h3>
            Upload Document
          </h3>

          <p>
            PDF or DOCX files
          </p>

          <label
            htmlFor="document-file-input"
            className="file-picker"
          >
            {file
              ? file.name
              : "Choose a PDF or DOCX file"}
          </label>

          <input
            id="document-file-input"
            className="hidden-file-input"
            type="file"
            accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            onChange={handleFileChange}
            disabled={loading}
          />

          <button
            type="button"
            className="primary-button"
            onClick={handleFileUpload}
            disabled={loading || !file}
          >
            {loading
              ? "Processing..."
              : "Index Document"}
          </button>

        </div>

      </div>


      {/* ==========================================
          WEBSITE URL
      ========================================== */}

      <div className="upload-card">

        <div className="upload-card-icon">
          ↗
        </div>

        <div className="upload-card-content">

          <h3>
            Connect Website
          </h3>

          <p>
            Import searchable website content
          </p>

          <input
            className="url-input"
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(event) => {
              setUrl(event.target.value);
              setMessage("");
              setError("");
            }}
            disabled={loading}
          />

          <button
            type="button"
            className="secondary-button"
            onClick={handleUrlUpload}
            disabled={
              loading || !url.trim()
            }
          >
            {loading
              ? "Processing..."
              : "Index Website"}
          </button>

        </div>

      </div>


      {/* ==========================================
          SUCCESS MESSAGE
      ========================================== */}

      {message && (
        <div className="success-message">
          <span>✓</span>
          {message}
        </div>
      )}


      {/* ==========================================
          ERROR MESSAGE
      ========================================== */}

      {error && (
        <div className="error-message">
          <span>!</span>
          {error}
        </div>
      )}

    </section>
  );
}


export default UploadDocument;