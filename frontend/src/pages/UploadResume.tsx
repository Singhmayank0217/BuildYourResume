import { useState } from "react";
import { uploadResume } from "../services/api";
import ATSPreview from "../components/ATSPreview";

const UploadResume = () => {
  const [file, setFile] = useState<File | null>(null);
  const [parsed, setParsed] = useState<any>(null);

  const handleUpload = async () => {
    if (!file) return;

    const res = await uploadResume(file);
    setParsed(res.parsed_resume);
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Upload Resume</h2>

      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload}>Upload</button>

      {parsed && <ATSPreview resume={parsed} />}
    </div>
  );
};

export default UploadResume;
