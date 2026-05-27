import re
from typing import Dict, List, Any
from openai import OpenAI
from config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ATSAnalyzer:
    def __init__(self):
        self.common_ats_issues = [
            "Tables or graphics detected",
            "Special characters or unusual formatting",
            "Image-based content",
            "Multiple columns",
            "Complex formatting"
        ]
        
        self.action_verbs = [
            "Achieved", "Accelerated", "Accomplished", "Automated", "Built",
            "Collaborated", "Created", "Delivered", "Developed", "Enhanced",
            "Established", "Evaluated", "Implemented", "Improved", "Increased",
            "Initiated", "Launched", "Led", "Managed", "Optimized",
            "Organized", "Pioneered", "Reduced", "Redesigned", "Restructured",
            "Scaled", "Spearheaded", "Streamlined", "Strengthened", "Transformed"
        ]

    def extract_keywords(self, job_description: str) -> List[str]:
        """Extract important keywords from job description"""
        # Convert to lowercase for processing
        text = job_description.lower()
        
        # Remove common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "is", "are"}
        
        # Extract words and filter
        words = re.findall(r'\b[a-z]+\b', text)
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        
        # Get unique keywords and return most common
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, _ in keyword_counts.most_common(20)]

    def check_formatting_issues(self, resume_text: str) -> List[str]:
        """Check for common ATS formatting issues"""
        issues = []
        
        # Check for multiple spaces
        if "  " in resume_text:
            issues.append("Multiple spaces detected - may cause parsing issues")
        
        # Check for special characters
        if any(char in resume_text for char in ["©", "®", "™", "→", "←"]):
            issues.append("Special characters detected - remove for ATS safety")
        
        # Check for common section headers
        headers = ["EXPERIENCE", "EDUCATION", "SKILLS", "SUMMARY"]
        found_headers = sum(1 for header in headers if header in resume_text.upper())
        if found_headers < 2:
            issues.append("Missing standard section headers")
        
        return issues

    def calculate_ats_score(self, resume_text: str, job_keywords: List[str]) -> float:
        """Calculate ATS compatibility score"""
        score = 100.0
        
        # Check formatting issues
        formatting_issues = self.check_formatting_issues(resume_text)
        score -= len(formatting_issues) * 5
        
        # Check keyword matching
        resume_lower = resume_text.lower()
        keyword_matches = sum(1 for keyword in job_keywords if keyword.lower() in resume_lower)
        keyword_coverage = (keyword_matches / max(len(job_keywords), 1)) * 30
        score = (score / 100 * 70) + keyword_coverage
        
        # Check for action verbs
        action_verb_count = sum(1 for verb in self.action_verbs if verb.lower() in resume_lower)
        verb_score = min((action_verb_count / 15) * 10, 10)
        score += verb_score
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))

    async def optimize_with_ai(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Use OpenAI to optimize resume for ATS and job match"""
        try:
            prompt = f"""
You are an ATS (Applicant Tracking System) optimization expert. Analyze the following resume against the job description and optimize it for ATS compatibility (90+ score).

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Please provide:
1. ATS Score (0-100)
2. Missing Keywords (list 5-10 important keywords not in resume)
3. Formatting Issues (if any)
4. Optimization Suggestions (3-5 specific improvements)
5. Optimized Resume Section (rewritten to include keywords naturally)

Respond in JSON format with keys: ats_score, missing_keywords, formatting_issues, suggestions, optimized_content
"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer specializing in ATS optimization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"AI optimization error: {e}")
            raise

    def generate_occupation_template(self, occupation: str) -> Dict[str, Any]:
        """Generate a default resume template for an occupation"""
        templates = {
            "Software Engineer": {
                "summary": "Results-driven Software Engineer with expertise in full-stack development...",
                "skills": ["Python", "JavaScript", "React", "PostgreSQL", "AWS", "Docker", "Git"],
                "experience_bullets": [
                    "Developed and deployed microservices architecture using",
                    "Optimized database queries resulting in 40% performance improvement",
                    "Led team of 3 developers in agile environment"
                ]
            },
            "Data Analyst": {
                "summary": "Data-driven professional with strong analytical and visualization skills...",
                "skills": ["Python", "SQL", "Tableau", "Excel", "Power BI", "Statistics"],
                "experience_bullets": [
                    "Created interactive dashboards for stakeholder reporting",
                    "Analyzed large datasets to identify business trends",
                    "Automated data collection process saving 10 hours weekly"
                ]
            },
            "Product Manager": {
                "summary": "Strategic Product Manager with proven track record of launching successful products...",
                "skills": ["Product Strategy", "Market Analysis", "Leadership", "Agile", "Analytics"],
                "experience_bullets": [
                    "Launched product feature that increased revenue by 25%",
                    "Managed cross-functional teams across engineering and marketing",
                    "Conducted user research to inform product roadmap"
                ]
            }
        }
        
        return templates.get(occupation, {
            "summary": f"Experienced {occupation} professional with proven expertise...",
            "skills": ["Skill 1", "Skill 2", "Skill 3"],
            "experience_bullets": ["Achievement 1", "Achievement 2", "Achievement 3"]
        })

ats_analyzer = ATSAnalyzer()
