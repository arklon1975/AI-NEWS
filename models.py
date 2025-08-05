from app import db
from datetime import datetime
import json

class ResearchProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='initialized')  # initialized, analyzing, interviewing, reviewing, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    final_report = db.Column(db.Text)
    human_notes = db.Column(db.Text)
    
    # Relationships
    analysts = db.relationship('Analyst', backref='project', lazy=True, cascade='all, delete-orphan')
    interviews = db.relationship('Interview', backref='project', lazy=True, cascade='all, delete-orphan')

class Analyst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('research_project.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(200), nullable=False)
    research_focus = db.Column(db.Text)
    status = db.Column(db.String(50), default='assigned')  # assigned, researching, interviewing, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expertise_area = db.Column(db.String(200), nullable=False)
    background = db.Column(db.Text)
    credibility_score = db.Column(db.Float, default=0.8)
    
    # Relationships
    interviews = db.relationship('Interview', backref='expert', lazy=True)

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('research_project.id'), nullable=False)
    analyst_id = db.Column(db.Integer, db.ForeignKey('analyst.id'), nullable=False)
    expert_id = db.Column(db.Integer, db.ForeignKey('expert.id'), nullable=False)
    questions = db.Column(db.Text)  # JSON string of questions
    responses = db.Column(db.Text)  # JSON string of responses
    insights = db.Column(db.Text)
    credibility_assessment = db.Column(db.Text)
    fake_news_flags = db.Column(db.Text)  # JSON string of potential fake news indicators
    status = db.Column(db.String(50), default='scheduled')  # scheduled, in_progress, completed, reviewed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    analyst = db.relationship('Analyst', backref='interviews')

class NewsSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500))
    credibility_rating = db.Column(db.Float, default=0.5)  # 0.0 to 1.0
    bias_rating = db.Column(db.String(50))  # left, center, right, mixed
    fact_check_rating = db.Column(db.String(50))  # high, medium, low
    is_verified = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'credibility_rating': self.credibility_rating,
            'bias_rating': self.bias_rating,
            'fact_check_rating': self.fact_check_rating,
            'is_verified': self.is_verified
        }
