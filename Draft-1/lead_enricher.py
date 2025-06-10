import pandas as pd
import random
from typing import Dict, List
import re

class LeadEnricher:
    """Handles lead data enrichment with simulated realistic data"""
    
    def __init__(self):
        # Job title mappings based on email domains and patterns
        self.job_titles = {
            'technical': [
                'Software Engineer', 'Senior Software Engineer', 'Lead Developer',
                'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
                'DevOps Engineer', 'Site Reliability Engineer', 'Data Engineer',
                'Machine Learning Engineer', 'AI Engineer', 'Cloud Architect'
            ],
            'management': [
                'Engineering Manager', 'Technical Lead', 'Team Lead',
                'Principal Engineer', 'Staff Engineer', 'Senior Technical Lead'
            ],
            'executive': [
                'CTO', 'VP Engineering', 'Head of Engineering', 'Director of Technology',
                'Chief Technology Officer', 'VP of Product', 'Head of IT'
            ],
            'decision_maker': [
                'CEO', 'Founder', 'Co-Founder', 'President', 'VP Sales',
                'Chief Executive Officer', 'Managing Director'
            ],
            'other': [
                'Product Manager', 'Project Manager', 'Business Analyst',
                'Technical Writer', 'QA Engineer', 'Sales Engineer'
            ]
        }
        
        # Technology stacks
        self.tech_stacks = [
            'React, Node.js, MongoDB',
            'Python, Django, PostgreSQL',
            'Java, Spring Boot, MySQL',
            'Vue.js, Express, Redis',
            'Angular, .NET, SQL Server',
            'Ruby on Rails, PostgreSQL',
            'PHP, Laravel, MySQL',
            'Go, Kubernetes, Docker',
            'Scala, Spark, Cassandra',
            'Swift, iOS, Firebase',
            'Kotlin, Android, SQLite',
            'TypeScript, Next.js, Prisma'
        ]
        
        # Company size indicators
        self.company_sizes = ['Startup', 'Small', 'Medium', 'Large', 'Enterprise']
        
    def enrich_leads(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrich lead data with additional information"""
        enriched_data = []
        
        for _, row in df.iterrows():
            enriched_lead = self._enrich_single_lead(row)
            enriched_data.append(enriched_lead)
        
        return pd.DataFrame(enriched_data)
    
    def _enrich_single_lead(self, lead: pd.Series) -> Dict:
        """Enrich a single lead with additional data"""
        # Extract basic info
        name = lead['name']
        email = lead['email']
        company_domain = lead['company_domain']
        
        # Determine job category based on email and name patterns
        job_category = self._determine_job_category(email, name)
        job_title = random.choice(self.job_titles[job_category])
        
        # Generate seniority level
        seniority = self._determine_seniority(job_title, email)
        
        # Generate LinkedIn profile
        linkedin_url = self._generate_linkedin_url(name)
        
        # Assign tech stack
        tech_stack = random.choice(self.tech_stacks)
        
        # Determine company size
        company_size = self._determine_company_size(company_domain)
        
        # Generate phone number
        phone = self._generate_phone_number()
        
        return {
            'name': name,
            'email': email,
            'company_domain': company_domain,
            'job_title': job_title,
            'seniority_level': seniority,
            'linkedin_url': linkedin_url,
            'tech_stack': tech_stack,
            'company_size': company_size,
            'phone': phone,
            'job_category': job_category
        }
    
    def _determine_job_category(self, email: str, name: str) -> str:
        """Determine job category based on email patterns and name"""
        email_lower = email.lower()
        name_lower = name.lower()
        
        # Executive patterns
        if any(pattern in email_lower for pattern in ['ceo', 'founder', 'president', 'exec']):
            return 'decision_maker'
        
        if any(pattern in email_lower for pattern in ['cto', 'vp', 'head', 'director']):
            return 'executive'
        
        # Technical patterns
        if any(pattern in email_lower for pattern in ['dev', 'engineer', 'tech', 'code']):
            return 'technical'
        
        # Management patterns
        if any(pattern in email_lower for pattern in ['manager', 'lead', 'principal']):
            return 'management'
        
        # Name-based inference
        if any(title in name_lower for title in ['dr', 'prof', 'phd']):
            return 'technical'
        
        # Default distribution
        weights = [0.4, 0.25, 0.15, 0.1, 0.1]
        categories = ['technical', 'management', 'executive', 'decision_maker', 'other']
        return random.choices(categories, weights=weights)[0]
    
    def _determine_seniority(self, job_title: str, email: str) -> str:
        """Determine seniority level"""
        title_lower = job_title.lower()
        email_lower = email.lower()
        
        if any(word in title_lower for word in ['ceo', 'cto', 'vp', 'head', 'director', 'chief']):
            return 'Executive'
        elif any(word in title_lower for word in ['senior', 'lead', 'principal', 'staff', 'manager']):
            return 'Senior'
        elif any(word in title_lower for word in ['junior', 'associate', 'intern']):
            return 'Junior'
        else:
            return random.choice(['Mid-level', 'Senior'])
    
    def _generate_linkedin_url(self, name: str) -> str:
        """Generate LinkedIn profile URL"""
        # Clean and format name for URL
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name)
        url_name = clean_name.lower().replace(' ', '-')
        return f"https://linkedin.com/in/{url_name}"
    
    def _determine_company_size(self, domain: str) -> str:
        """Determine company size based on domain patterns"""
        # Well-known large companies
        large_domains = ['google', 'microsoft', 'apple', 'amazon', 'facebook', 'netflix']
        if any(large_domain in domain.lower() for large_domain in large_domains):
            return 'Enterprise'
        
        # Random distribution for others
        weights = [0.2, 0.3, 0.3, 0.15, 0.05]
        return random.choices(self.company_sizes, weights=weights)[0]
    
    def _generate_phone_number(self) -> str:
        """Generate a formatted phone number"""
        area_code = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"+1 ({area_code}) {exchange}-{number}"
