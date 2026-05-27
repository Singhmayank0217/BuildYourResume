import axios from "axios";


const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

// Attach token automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const generateResume = async (payload: {
  user_data: any;
  job_description: string;
}) => {
  const res = await api.post("/resumes/generate", payload);
  return res.data;
};

export const analyzeResume = async (payload: {
  resume_id: number;
  job_description_text: string;
}) => {
  const res = await api.post("/analyze", payload);
  return res.data;
};

export const getOccupations = async () => {
  const res = await api.get("/occupations");
  return res.data;
};

export const getResumes = async () => {
  const res = await api.get("/resumes");
  return res.data;
};

export const getTemplates = async () => {
  const res = await api.get("/templates");
  return res.data;
};

export const getOccupationResumeTemplate = async (occupation: string) => {
  const res = await api.get(`/occupations/${occupation}/resume-template`);
  return res.data;
};

export const analyzeAPI = {
  atsPreview: (resumeId: number) =>
    api.get(`/analyze/parser-preview/${resumeId}`),
};

export const previewATS = async (payload: {
  resume: any;
  job_description: string;
}) => {
  const res = await api.post("/analyze/preview", payload);
  return res.data;
};


export default api;
