import pandas as pd
import random
from typing import Dict

class ScoringEngine:
    """AI-powered lead scoring engine"""
    
    def __init__(self):
        # Default scoring weights
        self.weights = {
            'job_title': 0.4,
            'tech_stack': 0.3,
            'buying_intent': 0.3
        }
        
        # Job title scoring matrix
        self.job_title_scores = {
            'decision_maker': (90, 100),
            'executive': (80, 95),
            'management': (70, 85),
            'technical': (60, 80),
            'other': (30, 60)
        }
        
        # Tech stack relevance keywords
        self.high_value_tech = [
            'react', 'node.js', 'python', 'kubernetes', 'docker',
            'aws', 'azure', 'microservices', 'api', 'cloud'
        ]
        
        # Company size multipliers
        self.size_multipliers = {
            'Enterprise': 1.2,
            'Large': 1.1,
            'Medium': 1.0,
            'Small': 0.9,
            'Startup': 0.8
        }
    
    def update_weights(self, new_weights: Dict[str, float]):
        """Update scoring weights"""
        total_weight = sum(new_weights.values())
        if total_weight > 0:
            # Normalize weights to sum to 1
            self.weights = {k: v/total_weight for k, v in new_weights.items()}
    
    def score_leads(self, df: pd.DataFrame) -> pd.DataFrame:
        """Score all leads in the dataframe"""
        scored_data = []
        
        for _, lead in df.iterrows():
            scored_lead = self._score_single_lead(lead)
            scored_data.append(scored_lead)
        
        return pd.DataFrame(scored_data)
    
    def _score_single_lead(self, lead: pd.Series) -> Dict:
        """Score a single lead"""
        # Calculate individual scores
        job_title_score = self._score_job_title(lead['job_category'], lead['seniority_level'])
        tech_stack_score = self._score_tech_stack(lead['tech_stack'])
        buying_intent_score = self._score_buying_intent(lead)
        
        # Apply company size multiplier
        size_multiplier = self.size_multipliers.get(lead['company_size'], 1.0)
        
        # Calculate weighted final score
        final_score = (
            job_title_score * self.weights['job_title'] +
            tech_stack_score * self.weights['tech_stack'] +
            buying_intent_score * self.weights['buying_intent']
        ) * size_multiplier
        
        # Ensure score is within bounds
        final_score = max(0, min(100, final_score))
        
        # Create scored lead dictionary
        scored_lead = lead.to_dict()
        scored_lead.update({
            'job_title_score': round(job_title_score, 1),
            'tech_stack_score': round(tech_stack_score, 1),
            'buying_intent_score': round(buying_intent_score, 1),
            'lead_score': round(final_score, 1),
            'score_explanation': self._generate_explanation(
                job_title_score, tech_stack_score, buying_intent_score, final_score
            )
        })
        
        return scored_lead
    
    def _score_job_title(self, job_category: str, seniority: str) -> float:
        """Score based on job title relevance"""
        base_range = self.job_title_scores.get(job_category, (30, 60))
        base_score = random.uniform(base_range[0], base_range[1])
        
        # Seniority bonus
        seniority_bonus = {
            'Executive': 10,
            'Senior': 5,
            'Mid-level': 0,
            'Junior': -10
        }.get(seniority, 0)
        
        return max(0, min(100, base_score + seniority_bonus))
    
    def _score_tech_stack(self, tech_stack: str) -> float:
        """Score based on technology stack alignment"""
        tech_lower = tech_stack.lower()
        
        # Count high-value technologies
        tech_matches = sum(1 for tech in self.high_value_tech if tech in tech_lower)
        
        # Base score calculation
        if tech_matches >= 3:
            base_score = random.uniform(85, 100)
        elif tech_matches >= 2:
            base_score = random.uniform(70, 90)
        elif tech_matches >= 1:
            base_score = random.uniform(55, 75)
        else:
            base_score = random.uniform(30, 60)
        
        return base_score
    
    def _score_buying_intent(self, lead: pd.Series) -> float:
        """Score based on buying intent signals"""
        # Simulate buying intent based on various factors
        intent_factors = []
        
        # Job category influence
        if lead['job_category'] in ['decision_maker', 'executive']:
            intent_factors.append(20)
        elif lead['job_category'] == 'management':
            intent_factors.append(10)
        else:
            intent_factors.append(0)
        
        # Company size influence
        size_bonus = {
            'Enterprise': 15,
            'Large': 10,
            'Medium': 5,
            'Small': 0,
            'Startup': 10  # Startups often have high buying intent
        }.get(lead['company_size'], 0)
        intent_factors.append(size_bonus)
        
        # Seniority influence
        seniority_bonus = {
            'Executive': 15,
            'Senior': 10,
            'Mid-level': 5,
            'Junior': 0
        }.get(lead['seniority_level'], 0)
        intent_factors.append(seniority_bonus)
        
        # Random market factors (simulating external signals)
        market_factor = random.uniform(0, 25)
        intent_factors.append(market_factor)
        
        # Calculate total intent score
        total_intent = sum(intent_factors)
        
        # Add some randomness and normalize
        final_intent = total_intent + random.uniform(-10, 10)
        return max(0, min(100, final_intent))
    
    def _generate_explanation(self, job_score: float, tech_score: float, 
                            intent_score: float, final_score: float) -> str:
        """Generate human-readable scoring explanation"""
        explanations = []
        
        # Job title explanation
        if job_score >= 85:
            explanations.append("High-value decision maker")
        elif job_score >= 70:
            explanations.append("Technical leader/manager")
        elif job_score >= 50:
            explanations.append("Technical professional")
        else:
            explanations.append("Lower relevance role")
        
        # Tech stack explanation
        if tech_score >= 80:
            explanations.append("excellent tech fit")
        elif tech_score >= 60:
            explanations.append("good tech alignment")
        else:
            explanations.append("limited tech relevance")
        
        # Buying intent explanation
        if intent_score >= 75:
            explanations.append("strong buying signals")
        elif intent_score >= 50:
            explanations.append("moderate buying intent")
        else:
            explanations.append("weak buying signals")
        
        return f"{', '.join(explanations)} (Score: {final_score})"
