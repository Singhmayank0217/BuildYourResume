import ScoreBar from "./ScoreBar";

interface BreakdownProps {
  breakdown: {
    keyword_relevance: number;
    skills_depth: number;
    experience_alignment: number;
    formatting: number;
  };
}

const ScoreBreakdown = ({ breakdown }: BreakdownProps) => {
  return (
    <div style={{ marginTop: 20 }}>
      <h4>ATS Score Breakdown</h4>

      <ScoreBar
        label="Keyword Relevance"
        score={breakdown.keyword_relevance}
        max={35}
      />

      <ScoreBar
        label="Skills Depth & Recency"
        score={breakdown.skills_depth}
        max={25}
      />

      <ScoreBar
        label="Experience Alignment"
        score={breakdown.experience_alignment}
        max={25}
      />

      <ScoreBar
        label="Formatting & ATS Parsing"
        score={breakdown.formatting}
        max={15}
      />
    </div>
  );
};

export default ScoreBreakdown;
