import json
import os
import logging
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "default-key")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

class AIAgentSystem:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_analysts(self, topic, num_analysts=3):
        """Generate a team of AI analysts specialized for the given topic"""
        try:
            prompt = f"""
            Create a team of {num_analysts} AI news analysts to research the topic: "{topic}"
            
            Each analyst should have:
            - A unique name
            - A specific specialization relevant to the topic
            - A research focus area
            
            Provide diverse perspectives and specializations that would comprehensively cover the topic.
            
            Respond with JSON in this format:
            {{
                "analysts": [
                    {{
                        "name": "analyst name",
                        "specialization": "specific area of expertise",
                        "research_focus": "what aspects they will investigate"
                    }}
                ]
            }}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("analysts", [])
            
        except Exception as e:
            self.logger.error(f"Error generating analysts: {e}")
            return []
    
    def generate_experts(self, topic, analyst_specialization):
        """Generate AI experts that can be interviewed by analysts"""
        try:
            prompt = f"""
            For the research topic "{topic}" and analyst specialization "{analyst_specialization}",
            create 2-3 AI experts who would have valuable insights.
            
            Each expert should have:
            - A realistic name
            - An expertise area relevant to the topic
            - A background description
            - A credibility score (0.0 to 1.0)
            
            Focus on experts from credible institutions, verified sources, and established authorities.
            
            Respond with JSON in this format:
            {{
                "experts": [
                    {{
                        "name": "expert name",
                        "expertise_area": "area of expertise",
                        "background": "professional background and credentials",
                        "credibility_score": 0.9
                    }}
                ]
            }}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("experts", [])
            
        except Exception as e:
            self.logger.error(f"Error generating experts: {e}")
            return []
    
    def generate_interview_questions(self, topic, analyst_specialization, expert_expertise):
        """Generate interview questions for analyst-expert conversation"""
        try:
            prompt = f"""
            Generate 5-7 insightful interview questions for researching: "{topic}"
            
            Context:
            - Analyst specialization: {analyst_specialization}
            - Expert expertise: {expert_expertise}
            
            Focus on:
            - Fact verification and source credibility
            - Identifying potential misinformation
            - Getting authoritative insights
            - Understanding different perspectives
            - Uncovering key facts and evidence
            
            Respond with JSON in this format:
            {{
                "questions": [
                    "question 1",
                    "question 2",
                    "..."
                ]
            }}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("questions", [])
            
        except Exception as e:
            self.logger.error(f"Error generating questions: {e}")
            return []
    
    def conduct_interview(self, questions, expert_background, topic):
        """Simulate an interview between analyst and expert"""
        try:
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            
            prompt = f"""
            You are an AI expert with the following background: {expert_background}
            
            You are being interviewed about the topic: "{topic}"
            
            Please provide detailed, authoritative responses to these questions:
            {questions_text}
            
            For each response:
            - Provide factual, evidence-based answers
            - Cite credible sources when possible
            - Flag any potential misinformation you're aware of
            - Maintain your expertise perspective
            - Be thorough but concise
            
            Respond with JSON in this format:
            {{
                "responses": [
                    {{
                        "question": "the question",
                        "answer": "detailed answer",
                        "sources": ["source1", "source2"],
                        "credibility_notes": "notes about information reliability",
                        "misinformation_flags": ["any red flags identified"]
                    }}
                ]
            }}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("responses", [])
            
        except Exception as e:
            self.logger.error(f"Error conducting interview: {e}")
            return []
    
    def analyze_credibility(self, interview_responses, topic):
        """Analyze the credibility of interview responses and detect fake news"""
        try:
            responses_text = json.dumps(interview_responses, indent=2)
            
            prompt = f"""
            Analyze the credibility of these interview responses about "{topic}":
            
            {responses_text}
            
            Assess:
            - Source reliability and verification
            - Fact-checking against known information
            - Potential bias or misinformation
            - Consistency across responses
            - Red flags for fake news
            
            Respond with JSON in this format:
            {{
                "overall_credibility": 0.85,
                "credibility_assessment": "detailed assessment",
                "fake_news_indicators": ["list of potential issues"],
                "verified_facts": ["list of verified information"],
                "recommendations": ["recommendations for further verification"]
            }}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing credibility: {e}")
            return {
                "overall_credibility": 0.5,
                "credibility_assessment": "Unable to assess credibility due to processing error",
                "fake_news_indicators": [],
                "verified_facts": [],
                "recommendations": []
            }
    
    def generate_final_report(self, topic, all_interviews, human_notes=None):
        """Generate final comprehensive report from all interviews"""
        try:
            interviews_summary = []
            for interview in all_interviews:
                interview_data = {
                    "analyst": interview.analyst.name if interview.analyst else "Unknown",
                    "expert": interview.expert.name if interview.expert else "Unknown",
                    "insights": interview.insights,
                    "credibility": interview.credibility_assessment
                }
                interviews_summary.append(interview_data)
            
            interviews_text = json.dumps(interviews_summary, indent=2)
            human_notes_text = f"\n\nHuman Notes: {human_notes}" if human_notes else ""
            
            prompt = f"""
            Create a comprehensive research report on: "{topic}"
            
            Based on the following analyst-expert interviews:
            {interviews_text}
            {human_notes_text}
            
            The report should include:
            - Executive Summary
            - Key Findings
            - Verified Facts vs. Potential Misinformation
            - Source Credibility Analysis
            - Multiple Perspectives
            - Recommendations
            - Conclusion
            
            Focus on factual accuracy, source verification, and identifying any fake news or misinformation.
            
            Respond with JSON in this format:
            {{
                "executive_summary": "brief overview",
                "key_findings": ["finding 1", "finding 2", "..."],
                "verified_facts": ["fact 1", "fact 2", "..."],
                "potential_misinformation": ["concern 1", "concern 2", "..."],
                "source_analysis": "analysis of source credibility",
                "perspectives": {{
                    "perspective_1": "description",
                    "perspective_2": "description"
                }},
                "recommendations": ["recommendation 1", "recommendation 2", "..."],
                "conclusion": "final conclusion",
                "credibility_score": 0.87
            }}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating final report: {e}")
            return {
                "executive_summary": "Error generating report",
                "key_findings": [],
                "verified_facts": [],
                "potential_misinformation": [],
                "source_analysis": "Unable to analyze sources",
                "perspectives": {},
                "recommendations": [],
                "conclusion": "Report generation failed",
                "credibility_score": 0.0
            }
