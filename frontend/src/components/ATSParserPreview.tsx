type Props = {
  data: any;
};

const ATSParserPreview = ({ data }: Props) => {
  return (
    <div className="border p-4 rounded bg-gray-50">
      <h3 className="font-bold mb-2">What the ATS Sees</h3>

      <p><strong>Name:</strong> {data.parsed_name || "Not detected"}</p>
      <p><strong>Email:</strong> {data.parsed_email || "Not detected"}</p>
      <p><strong>Phone:</strong> {data.parsed_phone || "Not detected"}</p>

      <p className="mt-2"><strong>Skills:</strong></p>
      <ul>
        {data.parsed_skills?.map((s: string) => (
          <li key={s}>• {s}</li>
        ))}
      </ul>

      <p className="mt-2">
        <strong>Experience:</strong>{" "}
        {data.estimated_experience_years} years
      </p>

      <p className="mt-2">
        <strong>Sections Detected:</strong>{" "}
        {data.sections_detected?.join(", ")}
      </p>
    </div>
  );
};

export default ATSParserPreview;
