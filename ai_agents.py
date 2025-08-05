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
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("No content received from OpenAI response")
            
            result = json.loads(content)
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
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("No content received from OpenAI response")
            
            result = json.loads(content)
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
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("No content received from OpenAI response")
            
            result = json.loads(content)
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
            experts_consulted = []
            total_credibility = 0
            credible_count = 0
            
            for interview in all_interviews:
                # Parse insights and credibility data
                insights_data = {}
                credibility_data = {}
                
                try:
                    if interview.insights:
                        insights_data = json.loads(interview.insights) if isinstance(interview.insights, str) else interview.insights
                    if interview.credibility_assessment:
                        credibility_data = json.loads(interview.credibility_assessment) if isinstance(interview.credibility_assessment, str) else interview.credibility_assessment
                        if credibility_data.get('overall_credibility'):
                            total_credibility += credibility_data['overall_credibility']
                            credible_count += 1
                except:
                    pass
                
                interview_data = {
                    "analyst": interview.analyst.name if interview.analyst else "Unknown",
                    "analyst_specialization": interview.analyst.specialization if interview.analyst else "Unknown",
                    "expert": interview.expert.name if interview.expert else "Unknown",
                    "expert_expertise": interview.expert.expertise_area if interview.expert else "Unknown",
                    "expert_credibility": interview.expert.credibility_score if interview.expert else 0.5,
                    "insights": insights_data,
                    "credibility_analysis": credibility_data,
                    "responses": json.loads(interview.responses) if interview.responses else []
                }
                interviews_summary.append(interview_data)
                
                # Collect expert information
                if interview.expert:
                    experts_consulted.append(f"{interview.expert.name} - {interview.expert.expertise_area} (Credibilidad: {interview.expert.credibility_score:.2f})")
            
            avg_credibility = total_credibility / credible_count if credible_count > 0 else 0.8
            interviews_text = json.dumps(interviews_summary, indent=2)
            human_notes_text = f"\n\nInstrucciones humanas: {human_notes}" if human_notes else ""
            
            prompt = f"""
            Crea un informe de investigación completo sobre: "{topic}"
            
            Basado en las siguientes entrevistas analista-experto:
            {interviews_text}
            {human_notes_text}
            
            Expertos consultados:
            {chr(10).join(experts_consulted)}
            
            El informe debe incluir (en español):
            - Resumen Ejecutivo
            - Hallazgos Principales  
            - Hechos Verificados vs. Desinformación Potencial
            - Análisis de Credibilidad de Fuentes
            - Múltiples Perspectivas
            - Recomendaciones
            - Conclusión
            
            Enfócate en precisión factual, verificación de fuentes, e identificación de fake news o desinformación.
            
            Responde con JSON en este formato:
            {{
                "executive_summary": "resumen ejecutivo breve pero completo",
                "key_findings": ["hallazgo 1", "hallazgo 2", "hallazgo 3", "..."],
                "verified_facts": ["hecho verificado 1", "hecho verificado 2", "..."],
                "potential_misinformation": ["preocupación 1", "preocupación 2", "..."],
                "source_analysis": "análisis detallado de la credibilidad de las fuentes",
                "perspectives": {{
                    "political_perspective": "perspectiva política y gubernamental",
                    "economic_perspective": "perspectiva económica y fiscal", 
                    "international_perspective": "perspectiva internacional y comercial"
                }},
                "recommendations": ["recomendación 1", "recomendación 2", "..."],
                "conclusion": "conclusión final detallada",
                "credibility_score": {avg_credibility:.2f},
                "experts_consulted": {len(experts_consulted)},
                "methodology": "Análisis multi-agente con procesamiento paralelo y verificación de fuentes"
            }}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("No content received from OpenAI response")
            
            result = json.loads(content)
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
