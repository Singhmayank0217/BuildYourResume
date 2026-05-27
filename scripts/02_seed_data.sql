-- Seed Data for Smart Resume Builder

-- Insert Occupations
INSERT INTO occupations (title, summary_template, common_skills, experience_bullets) VALUES
('Software Engineer', 
 'Results-driven Software Engineer with expertise in full-stack development, cloud architecture, and agile methodologies. Proven track record of designing scalable solutions and leading high-performing teams.',
 '["Python", "JavaScript", "React", "PostgreSQL", "AWS", "Docker", "Git", "CI/CD", "Microservices", "REST APIs"]',
 '["Developed and deployed microservices architecture using Docker and Kubernetes, serving 100K+ daily users", "Optimized database queries resulting in 40% performance improvement and reduced cloud costs by $50K annually", "Led team of 3 developers in agile environment, delivering features 15% faster than planned", "Implemented automated testing increasing code coverage from 45% to 92%", "Mentored 2 junior developers, improving their technical skills and project contribution"]'),

('Data Analyst', 
 'Data-driven professional with strong analytical and visualization skills. Expert in extracting actionable insights from complex datasets to drive business decisions and strategic initiatives.',
 '["Python", "SQL", "Tableau", "Excel", "Power BI", "Statistics", "R", "Data Warehousing", "ETL", "Analytics"]',
 '["Created 15+ interactive dashboards for executive stakeholder reporting, reducing manual reporting time by 30 hours/week", "Analyzed customer behavior data identifying new market opportunity worth $2M in annual revenue", "Automated data collection process using Python and SQL, saving 10 hours weekly and improving data accuracy to 99.8%", "Conducted A/B testing on website features, increasing conversion rate by 23%", "Built predictive model achieving 87% accuracy in customer churn prediction"]'),

('Product Manager', 
 'Strategic Product Manager with proven track record of launching successful products and features. Skilled in market analysis, user research, and cross-functional leadership driving business growth.',
 '["Product Strategy", "Market Analysis", "Leadership", "Agile", "Analytics", "User Research", "Roadmapping", "Stakeholder Management", "Data Analysis"]',
 '["Launched product feature that increased subscription revenue by 25% and gained 50K new users in first quarter", "Managed cross-functional teams across engineering, design, and marketing, delivering products 20% faster", "Conducted user research with 100+ customers, informing product roadmap and reducing feature abandonment by 35%", "Optimized pricing strategy resulting in 18% increase in average revenue per user", "Built and mentored product team from 2 to 8 members while maintaining productivity"]'),

('UX/UI Designer', 
 'Creative and user-centric UX/UI Designer with expertise in creating beautiful, intuitive digital experiences. Specialized in design systems, user research, and translating business goals into engaging interfaces.',
 '["Figma", "Adobe XD", "Prototyping", "User Research", "Wireframing", "Design Systems", "CSS", "HTML", "Interaction Design", "A/B Testing"]',
 '["Designed and prototyped 40+ mobile and web interfaces used by 500K+ monthly active users", "Created comprehensive design system reducing design-to-development time by 35% and ensuring brand consistency", "Conducted user research with 200+ participants informing interface improvements that increased user engagement by 28%", "Led redesign of core product increasing user satisfaction score from 6.2 to 8.7 out of 10", "Collaborated with engineering team reducing design-to-implementation bugs by 42%"]'),

('DevOps Engineer', 
 'Infrastructure-focused DevOps Engineer with expertise in cloud platforms, containerization, and continuous integration/deployment. Experienced in building reliable, scalable systems serving millions of users.',
 '["Kubernetes", "Docker", "AWS", "CI/CD", "Terraform", "Linux", "Git", "Monitoring", "Security", "Automation"]',
 '["Designed and implemented Kubernetes infrastructure reducing deployment time from 2 hours to 5 minutes", "Built CI/CD pipeline with GitHub Actions reducing time-to-production by 60% and improving deployment frequency to 10x daily", "Managed AWS cloud infrastructure for 3 applications reducing operational costs by 45% through optimization", "Implemented comprehensive monitoring and alerting system reducing incident response time from 30 minutes to 5 minutes", "Led infrastructure security audit and implementation of best practices reducing vulnerabilities by 80%"]');

-- Insert Templates
INSERT INTO templates (name, category, description, structure, ats_safe, is_recommended) VALUES
('Professional Classic',
 'Professional',
 'Clean, professional template with traditional formatting. Perfect for traditional industries and conservative roles.',
 '{"header": "Name and contact info", "summary": "Professional summary or objective", "experience": "Work experience with dates and achievements", "education": "Educational background", "skills": "Technical and soft skills", "certifications": "Relevant certifications"}',
 true,
 true),

('Modern Minimal',
 'Modern',
 'Sleek, modern design emphasizing recent achievements and impact. Great for tech and creative industries.',
 '{"header": "Name with subtle styling", "summary": "Concise professional overview", "highlights": "Key achievements and metrics", "experience": "Recent roles with quantified results", "education": "Relevant degrees and certifications", "skills": "Technical skills with proficiency levels"}',
 true,
 true),

('Executive Summary',
 'Executive',
 'Executive-level resume highlighting leadership and strategic achievements. Ideal for senior roles.',
 '{"header": "Executive name and title", "executive_summary": "Detailed executive overview", "key_achievements": "Top 5 career accomplishments", "professional_experience": "Senior roles with business impact", "education": "Advanced degrees and executive training", "board_affiliations": "Directorships and board positions"}',
 true,
 false),

('Academic Researcher',
 'Academic',
 'Designed for researchers and academics highlighting publications and research contributions.',
 '{"header": "Name and academic credentials", "research_interests": "Primary research areas", "publications": "Recent publications and papers", "academic_experience": "Teaching and research positions", "education": "Advanced degrees and research specializations", "grants": "Research funding and grants received"}',
 true,
 false),

('Creative Professional',
 'Creative',
 'Portfolio-focused resume for designers and creative professionals.',
 '{"header": "Name with creative styling", "creative_summary": "Unique professional brand statement", "portfolio_highlights": "Featured projects and work", "experience": "Creative roles and projects", "skills": "Design tools and creative skills", "awards": "Design awards and recognition"}',
 true,
 false);

-- Insert Sample Skills
INSERT INTO skills_library (skill_name, category, industry_relevance) VALUES
('Python', 'Programming', '["Software Engineering", "Data Analysis", "DevOps"]'),
('JavaScript', 'Programming', '["Software Engineering", "Frontend Development"]'),
('React', 'Framework', '["Software Engineering", "Frontend Development"]'),
('PostgreSQL', 'Database', '["Software Engineering", "Data Analysis"]'),
('AWS', 'Cloud', '["Software Engineering", "DevOps", "Data Analysis"]'),
('Kubernetes', 'DevOps', '["DevOps", "Software Engineering"]'),
('Tableau', 'Analytics', '["Data Analysis", "Business Intelligence"]'),
('Figma', 'Design', '["UX/UI Design", "Product Management"]'),
('Leadership', 'Soft Skills', '["Product Manager", "Manager", "Executive"]'),
('Communication', 'Soft Skills', '["All"]');

-- Commit all changes
COMMIT;
