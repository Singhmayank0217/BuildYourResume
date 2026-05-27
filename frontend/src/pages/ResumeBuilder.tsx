import { useEffect, useState } from "react";
import { generateResume, previewATS } from "../services/api";
import ScoreBreakdown from "../components/ScoreBreakdown";

const ResumeBuilder = () => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [skills, setSkills] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState<any>(null);
  const [atsPreview, setAtsPreview] = useState<any>(null);

  // ----------------------------
  // LIVE ATS PREVIEW (debounced)
  // ----------------------------
  useEffect(() => {
    if (!jobDescription || !fullName) return;

    const timeout = setTimeout(async () => {
      try {
        const res = await previewATS({
          resume: {
            full_name: fullName,
            email,
            skills: skills.split(",").map(s => s.trim()),
            experience: [],
          },
          job_description: jobDescription,
        });

        setAtsPreview(res);
      } catch (err) {
        console.error("ATS preview failed");
      }
    }, 600);

    return () => clearTimeout(timeout);
  }, [fullName, email, skills, jobDescription]);

  // ----------------------------
  // FINAL GENERATE & SAVE
  // ----------------------------
  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await generateResume({
        resume: {
          full_name: fullName,
          email,
          skills: skills.split(",").map(s => s.trim()),
          experience: [],
        },
        job_description: jobDescription,
      });

      setGenerated(res);
    } catch (err) {
      console.error(err);
      alert("Failed to generate resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 800 }}>
      <h2>Resume Builder (Live ATS)</h2>

      <input
        placeholder="Full Name"
        value={fullName}
        onChange={(e) => setFullName(e.target.value)}
      />

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        placeholder="Skills (comma separated)"
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />

      <textarea
        placeholder="Paste Job Description"
        rows={8}
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      {/* LIVE ATS PREVIEW */}
      {atsPreview && (
        <div style={{ marginTop: 24 }}>
          <h3>Live ATS Score: {atsPreview.ats_score}</h3>
          <ScoreBreakdown breakdown={atsPreview.breakdown} />
        </div>
      )}

      <button onClick={handleGenerate} disabled={loading}>
        {loading ? "Generating..." : "Generate & Save Resume"}
      </button>

      {/* FINAL GENERATED RESULT */}
      {generated && (
        <div style={{ marginTop: 30 }}>
          <h3>Final ATS Score: {generated.ats_score}</h3>
          <ScoreBreakdown breakdown={generated.breakdown} />
        </div>
      )}
    </div>
  );
};

export default ResumeBuilder;
