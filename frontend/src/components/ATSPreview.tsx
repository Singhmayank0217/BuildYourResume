const ATSPreview = ({ resume }: any) => {
  return (
    <div style={{ marginTop: 20 }}>
      <h3>ATS Parsed Resume</h3>

      <p><b>Name:</b> {resume.full_name}</p>
      <p><b>Email:</b> {resume.email}</p>
      <p><b>Phone:</b> {resume.phone}</p>

      <h4>Skills</h4>
      <ul>{resume.skills.map((s: string) => <li key={s}>{s}</li>)}</ul>

      <h4>Experience</h4>
      {resume.experience.map((exp: any, i: number) => (
        <div key={i}>
          <b>{exp.title}</b>
          <ul>
            {exp.bullets.map((b: string, j: number) => <li key={j}>{b}</li>)}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default ATSPreview;
