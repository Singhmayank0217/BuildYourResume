import ScoreBreakdown from "./ScoreBreakdown";

interface ATSComparisonProps {
  before?: {
    ats_score: number;
    breakdown: any;
  };
  after: {
    ats_score: number;
    breakdown: any;
  };
}

const ATSComparison = ({ before, after }: ATSComparisonProps) => {
  return (
    <div style={{ marginTop: 32 }}>
      <h3>ATS Score Comparison</h3>

      <div style={{ display: "flex", gap: 40 }}>
        {/* BEFORE */}
        {before && (
          <div style={{ flex: 1 }}>
            <h4>Before</h4>
            <strong>{before.ats_score} / 100</strong>
            <ScoreBreakdown breakdown={before.breakdown} />
          </div>
        )}

        {/* AFTER */}
        <div style={{ flex: 1 }}>
          <h4>After (Optimized)</h4>
          <strong style={{ color: "#16a34a" }}>
            {after.ats_score} / 100
          </strong>
          <ScoreBreakdown breakdown={after.breakdown} />
        </div>
      </div>
    </div>
  );
};

export default ATSComparison;
