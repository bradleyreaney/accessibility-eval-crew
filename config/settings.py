"""
Configuration settings for accessibility evaluation system
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Dict, Optional
import os


class EvaluationConfig(BaseSettings):
    """Configuration for accessibility plan evaluation."""
    
    # LLM Configuration
    default_model: str = Field(default="gpt-4-turbo-preview", env="DEFAULT_MODEL")
    fallback_model: str = Field(default="gpt-3.5-turbo", env="FALLBACK_MODEL")
    temperature: float = Field(default=0.1, env="TEMPERATURE")
    
    # API Keys
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    
    # Evaluation Weights
    strategic_weight: float = Field(default=0.4, env="STRATEGIC_WEIGHT")
    technical_weight: float = Field(default=0.3, env="TECHNICAL_WEIGHT") 
    comprehensive_weight: float = Field(default=0.2, env="COMPREHENSIVE_WEIGHT")
    longterm_weight: float = Field(default=0.1, env="LONGTERM_WEIGHT")
    
    # Output Configuration
    output_dir: str = Field(default="outputs", env="OUTPUT_DIR")
    verbose: bool = Field(default=True, env="VERBOSE")
    
    # File Processing
    max_file_size_mb: int = Field(default=50, env="MAX_FILE_SIZE_MB")
    supported_extensions: list = Field(default=[".pdf"], env="SUPPORTED_EXTENSIONS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def validate_weights(self) -> bool:
        """Validate that evaluation weights sum to 1.0."""
        total = self.strategic_weight + self.technical_weight + self.comprehensive_weight + self.longterm_weight
        return abs(total - 1.0) < 0.001
    
    def get_weighted_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate weighted scores for each evaluation dimension."""
        return {
            "strategic": scores.get("strategic", 0) * self.strategic_weight,
            "technical": scores.get("technical", 0) * self.technical_weight,
            "comprehensive": scores.get("comprehensive", 0) * self.comprehensive_weight,
            "longterm": scores.get("longterm", 0) * self.longterm_weight
        }
    
    def calculate_total_score(self, scores: Dict[str, float]) -> float:
        """Calculate total weighted score."""
        weighted = self.get_weighted_scores(scores)
        return sum(weighted.values())
    
    @property
    def evaluation_criteria(self) -> Dict[str, Dict[str, float]]:
        """Get evaluation criteria with weights."""
        return {
            "Strategic Prioritization": {
                "weight": self.strategic_weight,
                "description": "Logic and rationale behind task sequencing and prioritization"
            },
            "Technical Specificity": {
                "weight": self.technical_weight,
                "description": "Clarity, accuracy, and actionability of technical solutions"
            },
            "Comprehensiveness": {
                "weight": self.comprehensive_weight,
                "description": "Complete coverage and structural organization"
            },
            "Long-Term Vision": {
                "weight": self.longterm_weight,
                "description": "Sustainability and continuous improvement provisions"
            }
        }


# Global configuration instance
config = EvaluationConfig()
