"""
CrewAI Agents for Accessibility Plan Evaluation
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional
import os


class AccessibilityEvaluationAgents:
    """Factory class for creating specialized accessibility evaluation agents."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview", temperature: float = 0.1):
        """Initialize with LLM configuration."""
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self._create_llm()
    
    def _create_llm(self):
        """Create LLM instance based on model name."""
        if self.model_name.startswith("gpt"):
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif self.model_name.startswith("gemini"):
            return ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            # Default to OpenAI
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=self.temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def create_strategic_evaluator(self) -> Agent:
        """Create agent specialized in strategic prioritization assessment."""
        return Agent(
            role="Strategic Accessibility Evaluator",
            goal="Evaluate the strategic prioritization and sequencing logic of accessibility remediation plans",
            backstory="""You are a senior accessibility consultant with 15+ years of experience 
            leading large-scale remediation projects. You excel at analyzing the strategic coherence 
            of remediation plans, particularly their ability to synthesize multiple prioritization 
            models (user impact, architectural leverage, effort, risk) rather than following 
            simplistic approaches. You understand that effective accessibility remediation requires 
            sophisticated thinking about critical user paths, site-wide architectural fixes, and 
            the interdependencies between different types of barriers.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def create_technical_evaluator(self) -> Agent:
        """Create agent specialized in technical solution assessment."""
        return Agent(
            role="Technical Accessibility Evaluator", 
            goal="Assess the technical specificity, correctness, and actionability of proposed accessibility solutions",
            backstory="""You are a lead accessibility engineer with deep expertise in modern 
            web development, WCAG implementation, and assistive technologies. You have extensive 
            experience reviewing remediation plans for technical feasibility and completeness. 
            You excel at identifying whether proposed solutions are specific enough for developers 
            to implement without additional research, technically sound according to current web 
            standards, and aligned with modern development best practices. You can spot vague 
            recommendations and appreciate when plans include concrete code examples, specific 
            CSS values, and correct ARIA implementations.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def create_comprehensive_evaluator(self) -> Agent:
        """Create agent specialized in comprehensiveness and structure assessment."""
        return Agent(
            role="Comprehensive Accessibility Evaluator",
            goal="Evaluate the completeness, structure, and foundational understanding of accessibility remediation plans",
            backstory="""You are an accessibility program manager and WCAG expert who has 
            overseen hundreds of accessibility audits and remediation projects. You have a 
            exceptional ability to cross-reference remediation plans against original audit 
            findings to ensure nothing is missed. You deeply understand the POUR principles 
            (Perceivable, Operable, Understandable, Robust) and can assess whether proposed 
            solutions demonstrate genuine understanding of these foundational concepts rather 
            than just surface-level compliance. You also excel at evaluating whether plans 
            are structured in a way that's useful for multi-disciplinary teams including 
            developers, designers, and project managers.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def create_longterm_evaluator(self) -> Agent:
        """Create agent specialized in long-term vision and sustainability assessment."""
        return Agent(
            role="Long-term Accessibility Strategist",
            goal="Assess the long-term vision, sustainability, and continuous improvement aspects of accessibility plans",
            backstory="""You are a digital accessibility director who has built and scaled 
            accessibility programs at multiple organizations. You understand that true digital 
            inclusion requires treating accessibility as a continuous process, not a one-time 
            project. You excel at identifying whether remediation plans include provisions for 
            post-remediation verification, ongoing monitoring, team training, and cultural 
            integration. You can distinguish between plans that treat accessibility as a 
            compliance checkbox versus those that embed it as a core organizational value 
            throughout the entire product development lifecycle.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def create_synthesis_agent(self) -> Agent:
        """Create agent specialized in synthesizing evaluations and creating champion plans."""
        return Agent(
            role="Accessibility Plan Synthesis Expert",
            goal="Synthesize multiple evaluations to identify the best elements and create recommendations for an optimal remediation strategy",
            backstory="""You are a master accessibility consultant who has spent decades 
            analyzing and improving remediation strategies across industries. You have an 
            exceptional ability to identify the strongest elements from multiple plans and 
            synthesize them into a superior approach. You excel at gap analysis, identifying 
            what's missing from all provided plans that a world-class remediation strategy 
            would include. You understand the nuances of balancing strategic prioritization, 
            technical excellence, comprehensive coverage, and long-term sustainability. Your 
            recommendations have helped organizations build accessibility programs that are 
            both effective and sustainable.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=5,
            memory=True
        )
