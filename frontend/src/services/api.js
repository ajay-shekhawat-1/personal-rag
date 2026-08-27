import axios from "axios";

// ==================================================
// BACKEND CONFIGURATION
// ==================================================

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";


// ==================================================
// AXIOS CLIENT
// ==================================================

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
});


// ==================================================
// REQUEST LOGGER
// ==================================================

api.interceptors.request.use(
  (config) => {
    console.log(
      "API Request:",
      config.method?.toUpperCase(),
      `${config.baseURL}${config.url}`
    );

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


// ==================================================
// RESPONSE LOGGER
// ==================================================

api.interceptors.response.use(
  (response) => {
    console.log(
      "API Response:",
      response.status,
      response.config.url
    );

    return response;
  },
  (error) => {
    console.error("API Error:", error);

    if (error.response) {
      console.error(
        "Status:",
        error.response.status
      );

      console.error(
        "Response:",
        error.response.data
      );
    }

    return Promise.reject(error);
  }
);


// ==================================================
// UPLOAD DOCUMENT
// ==================================================

export const uploadDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/documents/upload",
    formData
  );

  return response.data;
};


// ==================================================
// UPLOAD WEBSITE
// ==================================================

export const uploadUrl = async (url) => {
  const response = await api.post(
    "/documents/url",
    {
      url: url,
    }
  );

  return response.data;
};


// ==================================================
// GET DOCUMENTS
// ==================================================

export const getDocuments = async () => {
  const response = await api.get(
    "/documents/"
  );

  return response.data;
};


// ==================================================
// DELETE DOCUMENT
// ==================================================

export const deleteDocument = async (documentId) => {
  const response = await api.delete(
    `/documents/${documentId}`
  );

  return response.data;
};


// ==================================================
// SEARCH DOCUMENTS
// ==================================================

export const searchDocuments = async (question) => {
  const response = await api.post(
    "/search/",
    {
      question: question,
      user_id: "default",
    }
  );

  return response.data;
};


// ==================================================
// RAG CHAT
// ==================================================

export const chatWithRag = async (question) => {
  const response = await api.post(
    "/chat/",
    {
      question: question,
      user_id: "default",
    }
  );

  return response.data;
};


// ==================================================
// HEALTH CHECK
// ==================================================

export const healthCheck = async () => {
  const response = await api.get(
    "/health"
  );

  return response.data;
};


// ==================================================
// DEFAULT EXPORT
// ==================================================

export default api;