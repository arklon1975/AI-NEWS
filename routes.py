from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import ResearchProject, Analyst, Expert, Interview, NewsSource
from workflow_manager import WorkflowManager
from ai_agents import AIAgentSystem
import threading
import json

workflow_manager = WorkflowManager()
ai_system = AIAgentSystem()

@app.route('/')
def index():
    recent_projects = ResearchProject.query.order_by(ResearchProject.created_at.desc()).limit(5).all()
    return render_template('index.html', recent_projects=recent_projects)

@app.route('/research', methods=['GET', 'POST'])
def research():
    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()
        
        if not topic:
            flash('Please enter a research topic.', 'error')
            return redirect(url_for('research'))
        
        # Create new research project
        project = ResearchProject(topic=topic, status='initialized')
        db.session.add(project)
        db.session.commit()
        
        # Start the research workflow in background
        thread = threading.Thread(
            target=workflow_manager.start_research_workflow,
            args=(project.id,)
        )
        thread.daemon = True
        thread.start()
        
        flash(f'Research project started for topic: {topic}', 'success')
        return redirect(url_for('project_status', project_id=project.id))
    
    return render_template('research.html')

@app.route('/project/<int:project_id>')
def project_status(project_id):
    project = ResearchProject.query.get_or_404(project_id)
    analysts = Analyst.query.filter_by(project_id=project_id).all()
    interviews = Interview.query.filter_by(project_id=project_id).all()
    
    # Calculate progress
    total_interviews = len(interviews)
    completed_interviews = len([i for i in interviews if i.status == 'completed'])
    progress = (completed_interviews / total_interviews * 100) if total_interviews > 0 else 0
    
    return render_template('research.html', 
                         project=project, 
                         analysts=analysts, 
                         interviews=interviews,
                         progress=progress)

@app.route('/project/<int:project_id>/intervene', methods=['POST'])
def human_intervention(project_id):
    project = ResearchProject.query.get_or_404(project_id)
    notes = request.form.get('notes', '').strip()
    action = request.form.get('action', '')
    
    if notes:
        project.human_notes = notes
        
    if action == 'approve':
        if project.status == 'reviewing':
            project.status = 'completed'
        flash('Research process approved and continued.', 'success')
    elif action == 'modify':
        # Add logic to modify the research direction
        flash('Research direction modified based on your input.', 'info')
    elif action == 'stop':
        project.status = 'stopped'
        flash('Research process stopped.', 'warning')
    
    db.session.commit()
    return redirect(url_for('project_status', project_id=project_id))

@app.route('/project/<int:project_id>/report')
def view_report(project_id):
    project = ResearchProject.query.get_or_404(project_id)
    
    if not project.final_report:
        flash('El reporte aún no está disponible. Por favor espera a que se complete la investigación.', 'info')
        return redirect(url_for('project_status', project_id=project_id))
    
    # Get all interviews for detailed view
    interviews = Interview.query.filter_by(project_id=project_id).all()
    analysts = Analyst.query.filter_by(project_id=project_id).all()
    
    # Parse the final report if it's JSON
    try:
        report_data = json.loads(project.final_report)
    except:
        report_data = {'content': project.final_report}
    
    return render_template('report.html', 
                         project=project,
                         report_data=report_data,
                         interviews=interviews,
                         analysts=analysts)

@app.route('/project/<int:project_id>/generate-report', methods=['POST'])
def generate_report(project_id):
    """Generate or regenerate the final report for a completed project"""
    project = ResearchProject.query.get_or_404(project_id)
    
    if project.status not in ['completed', 'reviewing']:
        flash('Solo se pueden generar reportes para proyectos completados.', 'error')
        return redirect(url_for('project_status', project_id=project_id))
    
    # Get completed interviews
    interviews = Interview.query.filter_by(project_id=project_id, status='completed').all()
    
    if not interviews:
        flash('No hay entrevistas completadas para generar el reporte.', 'warning')
        return redirect(url_for('project_status', project_id=project_id))
    
    try:
        # Generate report
        report_data = ai_system.generate_final_report(
            project.topic,
            interviews,
            project.human_notes
        )
        
        if report_data:
            project.final_report = json.dumps(report_data, ensure_ascii=False, indent=2)
            db.session.commit()
            flash('Reporte final generado exitosamente.', 'success')
        else:
            flash('Error al generar el reporte. Inténtalo de nuevo.', 'error')
            
    except Exception as e:
        flash(f'Error al generar el reporte: {str(e)}', 'error')
    
    return redirect(url_for('view_report', project_id=project_id))

@app.route('/api/project/<int:project_id>/status')
def api_project_status(project_id):
    project = ResearchProject.query.get_or_404(project_id)
    analysts = Analyst.query.filter_by(project_id=project_id).all()
    interviews = Interview.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'status': project.status,
        'progress': {
            'analysts_created': len(analysts),
            'interviews_scheduled': len(interviews),
            'interviews_completed': len([i for i in interviews if i.status == 'completed']),
            'total_progress': min(100, len([i for i in interviews if i.status == 'completed']) / max(1, len(interviews)) * 100)
        },
        'last_updated': project.updated_at.isoformat() if project.updated_at else None
    })

@app.route('/sources')
def news_sources():
    sources = NewsSource.query.order_by(NewsSource.credibility_rating.desc()).all()
    return render_template('sources.html', sources=sources)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
