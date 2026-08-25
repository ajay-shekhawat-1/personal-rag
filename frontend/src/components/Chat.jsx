import { useState } from "react";
import { chatWithRag } from "../services/api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const data = await chatWithRag(trimmedQuestion);

      console.log("Chat response:", data);

      // Handle common backend response formats
      const responseAnswer =
        data?.answer ??
        data?.response ??
        data?.result ??
        data?.message ??
        "No answer was returned by the backend.";

      setAnswer(responseAnswer);
    } catch (err) {
      console.error("Chat error:", err);

      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError("Unable to generate answer.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">

      {/* MESSAGES */}
      <div className="chat-messages">

        {!answer && !loading && !error && (
          <div className="chat-empty">
            <div className="chat-empty-icon">✦</div>

            <h3>Ask your knowledge base</h3>

            <p>
              Ask a question about the documents or websites
              you have added.
            </p>
          </div>
        )}

        {loading && (
          <div className="chat-message assistant-message">
            <div className="message-label">
              AI
            </div>

            <div className="loading-message">
              Searching your knowledge base...
            </div>
          </div>
        )}

        {error && (
          <div className="chat-error">
            <strong>Error</strong>
            <p>{error}</p>
          </div>
        )}

        {answer && !loading && (
          <div className="chat-message assistant-message">

            <div className="message-label">
              AI RESPONSE
            </div>

            <div className="answer-content">
              {answer}
            </div>

          </div>
        )}

      </div>

      {/* INPUT */}
      <form
        className="chat-input-area"
        onSubmit={handleSubmit}
      >

        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask something about your knowledge base..."
          rows={3}
          disabled={loading}
        />

        <div className="chat-input-footer">

          <span className="input-hint">
            Press Enter to ask
          </span>

          <button
            type="submit"
            disabled={loading || !question.trim()}
          >
            {loading ? "Thinking..." : "Ask AI →"}
          </button>

        </div>

      </form>

    </div>
  );
}

export default Chat;