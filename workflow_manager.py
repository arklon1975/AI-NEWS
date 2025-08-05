import threading
import time
import logging
from datetime import datetime
from app import db
from models import ResearchProject, Analyst, Expert, Interview
from ai_agents import AIAgentSystem
from news_sources import NewsSourceManager
import json

class WorkflowManager:
    def __init__(self):
        self.ai_system = AIAgentSystem()
        self.news_manager = NewsSourceManager()
        self.logger = logging.getLogger(__name__)
    
    def start_research_workflow(self, project_id):
        """Main workflow orchestrator - runs the complete research process"""
        from app import app
        
        with app.app_context():
            try:
                project = db.session.get(ResearchProject, project_id)
                if not project:
                    self.logger.error(f"Project {project_id} not found")
                    return
                
                self.logger.info(f"Starting research workflow for project {project_id}: {project.topic}")
                
                # Step 1: Generate analyst team
                project.status = 'analyzing'
                db.session.commit()
                
                analysts_data = self.ai_system.generate_analysts(project.topic)
                analysts = []
                
                for analyst_data in analysts_data:
                    analyst = Analyst(
                        project_id=project_id,
                        name=analyst_data.get('name', 'AI Analyst'),
                        specialization=analyst_data.get('specialization', 'General'),
                        research_focus=analyst_data.get('research_focus', 'General research')
                    )
                    db.session.add(analyst)
                    analysts.append(analyst)
                
                db.session.commit()
                self.logger.info(f"Created {len(analysts)} analysts for project {project_id}")
                
                # Step 2: Generate experts and schedule interviews
                project.status = 'interviewing'
                db.session.commit()
                
                # Create interview threads for parallel processing
                interview_threads = []
                
                for analyst in analysts:
                    thread = threading.Thread(
                        target=self._conduct_analyst_interviews,
                        args=(project_id, analyst.id)
                    )
                    interview_threads.append(thread)
                    thread.start()
                
                # Wait for all interviews to complete
                for thread in interview_threads:
                    thread.join()
                
                # Step 3: Human review checkpoint
                project.status = 'reviewing'
                project.updated_at = datetime.utcnow()
                db.session.commit()
                
                # Wait for human intervention or timeout
                self._wait_for_human_review(project_id, timeout=300)  # 5 minutes timeout
                
                # Step 4: Generate final report
                project = db.session.get(ResearchProject, project_id)
                if project.status != 'stopped':
                    self._generate_final_report(project_id)
                    project.status = 'completed'
                    project.updated_at = datetime.utcnow()
                    db.session.commit()
                
                self.logger.info(f"Research workflow completed for project {project_id}")
                
            except Exception as e:
                self.logger.error(f"Error in research workflow for project {project_id}: {e}")
                try:
                    project = db.session.get(ResearchProject, project_id)
                    if project:
                        project.status = 'error'
                        db.session.commit()
                except Exception as db_error:
                    self.logger.error(f"Error updating project status: {db_error}")
    
    def _conduct_analyst_interviews(self, project_id, analyst_id):
        """Conduct interviews for a specific analyst"""
        from app import app
        
        with app.app_context():
            try:
                analyst = db.session.get(Analyst, analyst_id)
                project = db.session.get(ResearchProject, project_id)
                
                if not analyst or not project:
                    return
                
                self.logger.info(f"Starting interviews for analyst {analyst.name}")
                
                # Generate experts for this analyst
                experts_data = self.ai_system.generate_experts(project.topic, analyst.specialization)
                
                for expert_data in experts_data:
                    # Create or find expert
                    expert = Expert.query.filter_by(
                        name=expert_data.get('name', 'AI Expert'),
                        expertise_area=expert_data.get('expertise_area', 'General')
                    ).first()
                    
                    if not expert:
                        expert = Expert(
                            name=expert_data.get('name', 'AI Expert'),
                            expertise_area=expert_data.get('expertise_area', 'General'),
                            background=expert_data.get('background', 'AI-generated expert'),
                            credibility_score=expert_data.get('credibility_score', 0.8)
                        )
                        db.session.add(expert)
                        db.session.flush()  # Get the ID
                    
                    # Create interview
                    interview = Interview(
                        project_id=project_id,
                        analyst_id=analyst_id,
                        expert_id=expert.id,
                        status='scheduled'
                    )
                    db.session.add(interview)
                    db.session.flush()
                    
                    # Conduct the interview
                    self._conduct_single_interview(interview.id)
                
                analyst.status = 'completed'
                db.session.commit()
                
            except Exception as e:
                self.logger.error(f"Error conducting interviews for analyst {analyst_id}: {e}")
    
    def _conduct_single_interview(self, interview_id):
        """Conduct a single interview between analyst and expert"""
        from app import app
        
        with app.app_context():
            try:
                interview = db.session.get(Interview, interview_id)
                if not interview:
                    return
                
                interview.status = 'in_progress'
                db.session.commit()
                
                # Generate questions
                questions = self.ai_system.generate_interview_questions(
                    interview.project.topic,
                    interview.analyst.specialization,
                    interview.expert.expertise_area
                )
                
                # Conduct interview
                responses = self.ai_system.conduct_interview(
                    questions,
                    interview.expert.background,
                    interview.project.topic
                )
                
                # Analyze credibility
                credibility_analysis = self.ai_system.analyze_credibility(
                    responses,
                    interview.project.topic
                )
                
                # Store results with proper encoding
                interview.questions = json.dumps(questions, ensure_ascii=False)
                interview.responses = json.dumps(responses, ensure_ascii=False)
                interview.insights = json.dumps({
                    'key_insights': [r.get('answer', '') for r in responses],
                    'sources': [s for r in responses for s in r.get('sources', [])],
                    'credibility_notes': [r.get('credibility_notes', '') for r in responses]
                }, ensure_ascii=False)
                interview.credibility_assessment = json.dumps(credibility_analysis, ensure_ascii=False)
                interview.fake_news_flags = json.dumps(credibility_analysis.get('fake_news_indicators', []), ensure_ascii=False)
                interview.status = 'completed'
                interview.completed_at = datetime.utcnow()
                
                db.session.commit()
                self.logger.info(f"Interview {interview_id} completed successfully")
                
            except Exception as e:
                self.logger.error(f"Error conducting interview {interview_id}: {e}")
                import traceback
                self.logger.error(f"Full traceback: {traceback.format_exc()}")
                
                try:
                    interview = db.session.get(Interview, interview_id)
                    if interview:
                        interview.status = 'error'
                        db.session.commit()
                except Exception as db_error:
                    self.logger.error(f"Error updating interview status to error: {db_error}")
    
    def _wait_for_human_review(self, project_id, timeout=300):
        """Wait for human intervention or timeout"""
        from app import app
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            with app.app_context():
                project = db.session.get(ResearchProject, project_id)
                if project.status != 'reviewing':
                    break
            time.sleep(10)  # Check every 10 seconds
        
        # If still in review state after timeout, continue automatically
        with app.app_context():
            project = db.session.get(ResearchProject, project_id)
            if project.status == 'reviewing':
                self.logger.info(f"Human review timeout for project {project_id}, continuing automatically")
    
    def _generate_final_report(self, project_id):
        """Generate the final comprehensive report"""
        from app import app
        
        with app.app_context():
            try:
                project = db.session.get(ResearchProject, project_id)
                interviews = Interview.query.filter_by(project_id=project_id, status='completed').all()
                
                if not interviews:
                    self.logger.warning(f"No completed interviews found for project {project_id}")
                    # Still mark as completed but without final report
                    project.status = 'completed'
                    db.session.commit()
                    return
                
                self.logger.info(f"Generating final report for project {project_id} with {len(interviews)} interviews")
                
                # Generate final report using AI
                report_data = self.ai_system.generate_final_report(
                    project.topic,
                    interviews,
                    project.human_notes
                )
                
                if report_data:
                    project.final_report = json.dumps(report_data, ensure_ascii=False, indent=2)
                    project.status = 'completed'
                    project.updated_at = datetime.utcnow()
                    db.session.commit()
                    
                    self.logger.info(f"Final report successfully generated for project {project_id}")
                else:
                    self.logger.error(f"No report data returned for project {project_id}")
                    project.status = 'completed'  # Mark as completed even if report generation failed
                    db.session.commit()
                
            except Exception as e:
                self.logger.error(f"Error generating final report for project {project_id}: {e}")
                # Mark as completed anyway to prevent infinite loops
                with app.app_context():
                    project = db.session.get(ResearchProject, project_id)
                    if project:
                        project.status = 'completed'
                        db.session.commit()
