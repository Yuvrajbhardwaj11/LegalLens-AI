import axios from "axios";

// In local dev, Vite proxies /api -> localhost:8000 (see vite.config.ts).
// In production, set VITE_API_BASE_URL to your deployed backend's URL,
// e.g. https://legallens-ai-backend.onrender.com/api
const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";
const api = axios.create({ baseURL });

export interface Citation {
  page: number;
  section: string;
  clause_title: string;
  excerpt: string;
}

export interface UploadResponse {
  document_id: string;
  filename: string;
  ocr_used: boolean;
  num_chunks: number;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
}

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post<UploadResponse>("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function askQuestion(documentId: string, question: string): Promise<QueryResponse> {
  const { data } = await api.post<QueryResponse>("/query", {
    document_id: documentId,
    question,
  });
  return data;
}
