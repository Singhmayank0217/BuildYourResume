# ===============================
# AI SYSTEM PROMPTS
# ===============================

SYSTEM_PROMPT = """
You are an expert ATS Resume Architect and Hiring Manager.

Rules:
1. Every resume must score 90+ in ATS systems.
2. The job description is the primary authority.
3. No tables, columns, icons, or graphics.
4. Use standard section headings only.
5. Use quantified achievements where possible.
6. Never fabricate experience.
7. Optimize for ATS first, humans second.
8. Output clean structured JSON only.
"""

# ===============================
# KEYWORD EXTRACTION
# ===============================

KEYWORD_EXTRACTION_PROMPT = """
Extract the most important ATS keywords from the job description.

Return:
- Technical skills
- Soft skills
- Tools
- Certifications
- Action verbs

Job Description:
{job_description}

Return JSON:
{
  "technical_skills": [],
  "soft_skills": [],
  "tools": [],
  "certifications": [],
  "keywords": []
}
"""


# ===============================
# RESUME GENERATION (NO RESUME)
# ===============================

RESUME_GENERATION_PROMPT = """
Using the provided user information and job description,
generate an ATS-optimized resume with a guaranteed score of 90+.

User Info:
{user_data}

Job Description:
{job_description}

Rules:
- Prioritize job description keywords
- Do not invent experience
- Rewrite weak bullets
- Use strong action verbs
- Quantify impact where possible

Output JSON:
{
  "summary": "",
  "skills": [],
  "experience": [],
  "education": [],
  "certifications": []
}
"""


# ===============================
# RESUME OPTIMIZATION (UPLOAD)
# ===============================

RESUME_OPTIMIZATION_PROMPT = """
You are given an existing resume and a job description.

Tasks:
1. Identify ATS issues
2. Inject missing keywords naturally
3. Improve formatting
4. Rewrite bullets for impact
5. Guarantee ATS score of 90+

Resume:
{resume_text}

Job Description:
{job_description}

Return JSON:
{
  "ats_score": 90,
  "missing_keywords": [],
  "formatting_issues": [],
  "optimized_resume": {}
}
"""

# ===============================
# ATS ANALYSIS
# ===============================

ATS_ANALYSIS_PROMPT = """
Analyze the resume against the job description.

Return:
- ATS score (0–100)
- Missing keywords
- Formatting issues
- Suggestions

Resume:
{resume_text}

Job Description:
{job_description}

Return JSON:
{
  "ats_score": 0,
  "missing_keywords": [],
  "formatting_issues": [],
  "suggestions": []
}
"""
