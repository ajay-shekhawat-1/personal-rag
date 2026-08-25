import { useState } from "react";

import ChatPage from "./pages/ChatPage";
import KnowledgePage from "./pages/KnowledgePage";

function App() {
  const [currentPage, setCurrentPage] = useState("knowledge");
  const [refreshKey, setRefreshKey] = useState(0);

  const handleDocumentUploaded = () => {
    setRefreshKey((current) => current + 1);
  };

  const goToKnowledge = () => {
    setCurrentPage("knowledge");
  };

  const goToChat = () => {
    setCurrentPage("chat");
  };

  return (
    <div className="app-shell">

      {/* Background decoration */}
      <div className="ambient ambient-one"></div>
      <div className="ambient ambient-two"></div>

      {/* HEADER */}
      <header className="topbar">

        <div className="brand">

          <div className="brand-mark">
            R
          </div>

          <div className="brand-text">

            <div className="brand-name">
              Personal RAG
            </div>

            <div className="brand-subtitle">
              PRIVATE KNOWLEDGE INTELLIGENCE
            </div>

          </div>

        </div>

        {/* NAVIGATION */}
        <nav className="main-navigation">

          <button
            type="button"
            className={
              currentPage === "knowledge"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={goToKnowledge}
          >
            <span className="nav-number">01</span>
            Knowledge
          </button>

          <button
            type="button"
            className={
              currentPage === "chat"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={goToChat}
          >
            <span className="nav-number">02</span>
            Ask AI
          </button>

        </nav>

        {/* STATUS */}
        <div className="connection-status">
          <span className="status-dot"></span>
          Backend Connected
        </div>

      </header>


      {/* PAGE CONTENT */}

      {currentPage === "knowledge" && (
        <KnowledgePage
          refreshKey={refreshKey}
          onUploadSuccess={handleDocumentUploaded}
          onAskAI={goToChat}
        />
      )}

      {currentPage === "chat" && (
        <ChatPage
          onKnowledge={goToKnowledge}
        />
      )}


      {/* FOOTER */}
      <footer className="app-footer">

        <div>
          PERSONAL RAG
        </div>

        <div className="footer-line"></div>

        <div>
          QDRANT · GROQ · FASTAPI
        </div>

      </footer>

    </div>
  );
}

export default App;