import { useState } from "react";
import { analyzeResume } from "../services/api";
import ScoreBreakdown from "../components/ScoreBreakdown";

const ResumeAnalyzer = () => {
  const [resumeId, setResumeId] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const [baseline, setBaseline] = useState<any>(null);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const res = await analyzeResume({
        resume_id: Number(resumeId),
        job_description_text: jobDescription,
      });

      if (!baseline) {
        setBaseline(res);
      }
      setResult(res);
    } catch (err) {
      console.error(err);
      alert("Failed to analyze resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 900 }}>
      <h2>Resume Analyzer</h2>

      <input
        placeholder="Resume ID"
        value={resumeId}
        onChange={(e) => setResumeId(e.target.value)}
      />

      <textarea
        placeholder="Paste Job Description"
        rows={8}
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {/* BEFORE / AFTER */}
      {baseline && result && (
        <div style={{ marginTop: 30 }}>
          <h3>Before vs After</h3>

          <div style={{ display: "flex", gap: 40 }}>
            <div style={{ flex: 1 }}>
              <h4>Before</h4>
              <p>ATS Score: {baseline.ats_score}</p>
              <ScoreBreakdown breakdown={baseline.breakdown} />
            </div>

            <div style={{ flex: 1 }}>
              <h4>After</h4>
              <p>ATS Score: {result.ats_score}</p>
              <ScoreBreakdown breakdown={result.breakdown} />
            </div>
          </div>

          <h3 style={{ marginTop: 20 }}>
            Improvement: +{result.ats_score - baseline.ats_score}
          </h3>
        </div>
      )}
    </div>
  );
};

export default ResumeAnalyzer;
