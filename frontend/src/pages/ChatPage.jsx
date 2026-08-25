import Chat from "../components/Chat";

function ChatPage({ onKnowledge }) {
  return (
    <main className="workspace">

      {/* HERO */}
      <section className="hero-section">

        <div className="hero-copy">

          <div className="eyebrow">
            RETRIEVAL + GENERATION
          </div>

          <h1>
            Ask your
            <br />
            <span>knowledge base.</span>
          </h1>

          <p>
            Ask questions about the documents and websites
            you have indexed. The RAG engine retrieves
            relevant information from Qdrant before
            generating the answer.
          </p>

        </div>

        <div className="hero-stat">

          <div className="stat-label">
            AI ENGINE
          </div>

          <div className="stat-value">
            GROQ
          </div>

          <div className="stat-footer">
            Retrieval augmented generation
          </div>

        </div>

      </section>


      {/* CHAT */}
      <section className="chat-page-wrapper">

        <div className="chat-panel">

          <div className="chat-header">

            <div>

              <div className="section-number">
                01
              </div>

              <div className="panel-kicker">
                PRIVATE AI
              </div>

              <h2>
                Ask Your Knowledge Base
              </h2>

            </div>

            <div className="ai-indicator">
              <span className="ai-pulse"></span>
              AI READY
            </div>

          </div>


          <div className="chat-description">
            Answers are generated using information
            retrieved from your indexed documents and websites.
          </div>


          <Chat />

        </div>

      </section>


      {/* BACK TO KNOWLEDGE */}
      <section className="back-to-knowledge">

        <div>

          <strong>
            Need to add more information?
          </strong>

          <span>
            Upload another document or connect a website.
          </span>

        </div>

        <button
          type="button"
          className="secondary-navigation-button"
          onClick={onKnowledge}
        >
          ← Manage Knowledge
        </button>

      </section>

    </main>
  );
}

export default ChatPage;