interface ScoreBarProps {
  label: string;
  score: number;
  max: number;
}

const getColor = (percentage: number) => {
  if (percentage >= 75) return "#16a34a"; // green
  if (percentage >= 50) return "#f59e0b"; // yellow
  return "#dc2626"; // red
};

const ScoreBar = ({ label, score, max }: ScoreBarProps) => {
  const percentage = Math.round((score / max) * 100);
  const color = getColor(percentage);

  return (
    <div style={{ marginBottom: 12 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 4,
          fontSize: 14,
        }}
      >
        <strong>{label}</strong>
        <span>
          {score} / {max}
        </span>
      </div>

      <div
        style={{
          height: 10,
          background: "#e5e7eb",
          borderRadius: 6,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${percentage}%`,
            height: "100%",
            background: color,
            transition: "width 0.4s ease",
          }}
        />
      </div>
    </div>
  );
};

export default ScoreBar;
