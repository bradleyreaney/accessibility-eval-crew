"""
CrewAI Tasks for Accessibility Plan Evaluation
"""

from crewai import Task
from typing import List, Dict, Any


class AccessibilityEvaluationTasks:
    """Factory class for creating specialized accessibility evaluation tasks."""
    
    @staticmethod
    def create_strategic_evaluation_task(agent, audit_report: str, plans: Dict[str, str]) -> Task:
        """Create task for strategic prioritization evaluation."""
        plans_text = "\n\n".join([f"#### {name}:\n{content}" for name, content in plans.items()])
        
        return Task(
            description=f"""
            Evaluate the strategic prioritization and sequencing logic of the provided accessibility remediation plans.
            
            AUDIT REPORT:
            {audit_report}
            
            PLANS TO EVALUATE:
            {plans_text}
            
            For each plan, assess:
            
            1. **Strategic Prioritization Logic**: 
               - Does the plan effectively synthesize multiple prioritization models (user impact, architectural leverage, effort, risk)?
               - How well does it prioritize critical user paths and high-impact, site-wide issues?
               - Does it avoid naive, single-factor prioritization approaches?
            
            2. **Sequencing Rationale**:
               - Is there clear logic behind the task ordering?
               - Does it account for dependencies between fixes?
               - Are foundational/architectural issues addressed early?
            
            3. **User Impact Focus**:
               - Does it prioritize barriers that affect the most users?
               - Are critical user journeys identified and prioritized?
               - Is there consideration of different disability types?
            
            Provide specific examples of strengths and weaknesses for each plan's strategic approach.
            Rate each plan on strategic prioritization from 1-10 with detailed justification.
            """,
            expected_output="Detailed strategic evaluation with specific examples and numerical ratings (1-10) for each plan's strategic prioritization approach.",
            agent=agent
        )
    
    @staticmethod
    def create_technical_evaluation_task(agent, audit_report: str, plans: Dict[str, str]) -> Task:
        """Create task for technical solution evaluation."""
        plans_text = "\n\n".join([f"#### {name}:\n{content}" for name, content in plans.items()])
        
        return Task(
            description=f"""
            Evaluate the technical specificity, correctness, and actionability of the proposed accessibility solutions.
            
            AUDIT REPORT:
            {audit_report}
            
            PLANS TO EVALUATE:
            {plans_text}
            
            For each plan, assess:
            
            1. **Technical Specificity**:
               - Are solutions specific enough for developers to implement without further research?
               - Do they include concrete code snippets, specific CSS values, correct ARIA roles?
               - Are implementation details clear and unambiguous?
            
            2. **Technical Correctness**:
               - Are the proposed solutions technically sound?
               - Do they align with current WCAG 2.1/2.2 guidelines?
               - Are they compatible with modern web development practices?
            
            3. **Actionability**:
               - Can a developer immediately understand what needs to be done?
               - Are the instructions complete and implementable?
               - Are there clear acceptance criteria or success metrics?
            
            4. **Best Practices Alignment**:
               - Do solutions follow semantic HTML principles?
               - Are ARIA implementations used correctly and sparingly?
               - Do they consider progressive enhancement?
            
            Identify specific technical strengths and weaknesses with examples.
            Rate each plan on technical quality from 1-10 with detailed justification.
            """,
            expected_output="Comprehensive technical evaluation with specific examples of code quality, technical accuracy, and actionability. Include numerical ratings (1-10) for each plan's technical aspects.",
            agent=agent
        )
    
    @staticmethod
    def create_comprehensive_evaluation_task(agent, audit_report: str, plans: Dict[str, str]) -> Task:
        """Create task for comprehensiveness and structure evaluation."""
        plans_text = "\n\n".join([f"#### {name}:\n{content}" for name, content in plans.items()])
        
        return Task(
            description=f"""
            Evaluate the completeness, structure, and foundational understanding of the accessibility remediation plans.
            
            AUDIT REPORT:
            {audit_report}
            
            PLANS TO EVALUATE:
            {plans_text}
            
            For each plan, assess:
            
            1. **Completeness**:
               - Does the plan address ALL violations noted in the audit report?
               - Are any critical issues missing or overlooked?
               - Is coverage comprehensive across all WCAG success criteria mentioned?
            
            2. **Structure and Organization**:
               - Is the plan well-structured and easy to understand?
               - Can multi-disciplinary teams (developers, designers, PMs) easily follow it?
               - Are phases, priorities, and dependencies clearly outlined?
            
            3. **POUR Principle Understanding**:
               - Does the plan explicitly connect fixes to POUR principles (Perceivable, Operable, Understandable, Robust)?
               - Is there evidence of deep accessibility understanding vs. surface compliance?
               - Are solutions principle-based rather than just rule-following?
            
            4. **Cross-functional Utility**:
               - Does it provide guidance for different team roles?
               - Are design implications addressed alongside development tasks?
               - Is there consideration of content and UX requirements?
            
            Create a comprehensive coverage matrix showing which audit findings are addressed by each plan.
            Rate each plan on comprehensiveness from 1-10 with detailed justification.
            """,
            expected_output="Detailed comprehensiveness analysis including coverage matrix of audit findings, assessment of POUR principle understanding, and numerical ratings (1-10) for each plan's completeness and structure.",
            agent=agent
        )
    
    @staticmethod
    def create_longterm_evaluation_task(agent, audit_report: str, plans: Dict[str, str]) -> Task:
        """Create task for long-term vision evaluation."""
        plans_text = "\n\n".join([f"#### {name}:\n{content}" for name, content in plans.items()])
        
        return Task(
            description=f"""
            Evaluate the long-term vision, sustainability, and continuous improvement aspects of the accessibility plans.
            
            AUDIT REPORT:
            {audit_report}
            
            PLANS TO EVALUATE:
            {plans_text}
            
            For each plan, assess:
            
            1. **Post-Remediation Verification**:
               - Does the plan include provisions for testing and validation after fixes?
               - Are there recommendations for user testing with people with disabilities?
               - Is there a strategy for confirming fixes actually work in practice?
            
            2. **Ongoing Monitoring**:
               - Does it address how to maintain accessibility over time?
               - Are there recommendations for automated testing integration?
               - Is there guidance on preventing future accessibility regressions?
            
            3. **Process Integration**:
               - Does it suggest embedding accessibility into development workflows?
               - Are there recommendations for team training and skill development?
               - Is there consideration of accessibility in design and content processes?
            
            4. **Cultural and Organizational Change**:
               - Does it treat accessibility as a continuous process vs. one-time fix?
               - Are there suggestions for building organizational accessibility maturity?
               - Is there guidance on governance and accountability structures?
            
            5. **Scalability and Maintenance**:
               - Can the approach scale to ongoing development?
               - Are there guidelines for handling new features and content?
               - Is there a framework for continuous improvement?
            
            Rate each plan on long-term vision from 1-10 with detailed justification.
            """,
            expected_output="Comprehensive long-term sustainability analysis covering verification, monitoring, process integration, and organizational change aspects. Include numerical ratings (1-10) for each plan's long-term vision.",
            agent=agent
        )
    
    @staticmethod
    def create_synthesis_task(agent, strategic_eval: str, technical_eval: str, 
                            comprehensive_eval: str, longterm_eval: str) -> Task:
        """Create task for synthesizing all evaluations into final recommendations."""
        return Task(
            description=f"""
            Synthesize all evaluation results to create a comprehensive final assessment and recommendations.
            
            EVALUATION RESULTS:
            
            Strategic Evaluation:
            {strategic_eval}
            
            Technical Evaluation:
            {technical_eval}
            
            Comprehensive Evaluation:
            {comprehensive_eval}
            
            Long-term Vision Evaluation:
            {longterm_eval}
            
            Create a comprehensive synthesis that includes:
            
            1. **Comparative Analysis Summary**:
               - Synthesize findings from all four evaluation dimensions
               - Identify the strongest and weakest aspects of each plan
               - Create a clear pros/cons comparison table
            
            2. **Gap Analysis - "What's Missing?"**:
               - Identify elements that an ideal, world-class remediation plan would contain
               - Highlight missing components that NONE of the plans addressed adequately  
               - Provide specific, actionable recommendations for improvement
               - Consider aspects like:
                 * More sophisticated prioritization frameworks
                 * Robust technical solutions for complex problems
                 * Better project management approaches
                 * Team training and cultural change recommendations
                 * Integration with development workflows
            
            3. **Champion Plan Recommendations**:
               - Identify the best elements from each plan that should be combined
               - Provide specific guidance on how to synthesize the strongest approaches
               - Address the collective weaknesses identified across all plans
               - Create actionable next steps for building an optimal strategy
            
            4. **Final Scoring**:
               - Apply weighted criteria: Strategic (40%), Technical (30%), Comprehensive (20%), Long-term (10%)
               - Provide final numerical scores for each plan
               - Include clear rationale for scoring decisions
               - Format final scores as clean JSON object
            
            End with a clear verdict on which plan is superior overall and why.
            """,
            expected_output="""A comprehensive evaluation report in markdown format including:
            - Executive summary with comparative analysis
            - Detailed pros/cons comparison table  
            - Gap analysis with specific missing elements
            - Champion plan synthesis recommendations
            - Final weighted scoring with JSON output
            - Clear verdict and rationale""",
            agent=agent
        )
