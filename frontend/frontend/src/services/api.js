import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const ingestRepo = (repo_url) => {
  return API.post("/ingest", { repo_url });
};

export const sendMessage = (query) => {
  return API.post("/chat", { query });
};