import DocumentList from "../components/DocumentList";
import UploadDocument from "../components/UploadDocument";

function KnowledgePage({
  refreshKey,
  onUploadSuccess,
  onAskAI,
}) {
  return (
    <main className="workspace">

      {/* HERO */}
      <section className="hero-section">

        <div className="hero-copy">

          <div className="eyebrow">
            KNOWLEDGE INGESTION
          </div>

          <h1>
            Build your
            <br />
            <span>AI knowledge base.</span>
          </h1>

          <p>
            Upload your documents or connect a website.
            Your information will be processed, embedded,
            and stored in Qdrant for intelligent retrieval.
          </p>

        </div>

        <div className="hero-stat">

          <div className="stat-label">
            VECTOR ENGINE
          </div>

          <div className="stat-value">
            QDRANT
          </div>

          <div className="stat-footer">
            Semantic retrieval
          </div>

        </div>

      </section>


      {/* KNOWLEDGE WORKSPACE */}
      <section className="knowledge-page-grid">

        {/* UPLOAD */}
        <div className="panel">

          <div className="panel-heading">

            <div className="section-number">
              01
            </div>

            <div>

              <div className="panel-kicker">
                KNOWLEDGE INGESTION
              </div>

              <h2>
                Add Knowledge
              </h2>

            </div>

          </div>

          <p className="panel-description">
            Add PDF or DOCX documents and website URLs
            to your private AI knowledge base.
          </p>

          <UploadDocument
            onUploadSuccess={onUploadSuccess}
          />

        </div>


        {/* DOCUMENTS */}
        <div className="panel documents-panel">

          <div className="panel-heading">

            <div className="section-number">
              02
            </div>

            <div>

              <div className="panel-kicker">
                VECTOR MEMORY
              </div>

              <h2>
                Knowledge Base
              </h2>

            </div>

          </div>

          <p className="panel-description">
            Documents currently indexed in Qdrant.
            You can remove any source from your knowledge base.
          </p>

          <DocumentList
            refreshKey={refreshKey}
          />

        </div>

      </section>


      {/* NEXT STEP */}
      <section className="next-step-card">

        <div>

          <div className="next-step-kicker">
            KNOWLEDGE READY?
          </div>

          <h2>
            Ask questions about your data.
          </h2>

          <p>
            Your indexed documents can now be used
            by the RAG engine to generate answers.
          </p>

        </div>

        <button
          type="button"
          className="next-step-button"
          onClick={onAskAI}
        >
          Go to Ask AI →
        </button>

      </section>

    </main>
  );
}

export default KnowledgePage;