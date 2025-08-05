# Documentación Técnica - AI News Research Hub

## 🏗️ Arquitectura del Sistema

### Visión General
AI News Research Hub utiliza una arquitectura multi-agente donde diferentes componentes de IA trabajan en paralelo para investigar temas, verificar información y generar reportes comprensivos.

### Componentes Principales

#### 1. Sistema de Agentes IA (`ai_agents.py`)
```python
class AIAgentSystem:
    """Sistema principal de gestión de agentes IA"""
    
    def generate_specialized_analysts(self, topic: str, count: int) -> List[Dict]
    def generate_interview_questions(self, topic: str, specialization: str, expertise: str) -> List[str]
    def conduct_interview(self, questions: List[str], expert_background: str, topic: str) -> List[Dict]
    def analyze_credibility(self, responses: List[Dict], topic: str) -> Dict
    def generate_final_report(self, topic: str, interviews: List, human_notes: str = None) -> Dict
```

#### 2. Gestor de Workflows (`workflow_manager.py`)
```python
class WorkflowManager:
    """Gestor de flujos de trabajo de investigación"""
    
    def start_research_workflow(self, project_id: int) -> None
    def process_interviews(self, project: ResearchProject) -> None
    def update_project_status(self, project_id: int, status: str) -> None
```

#### 3. Modelos de Datos (`models.py`)
```python
# Modelos SQLAlchemy
ResearchProject, Analyst, Expert, Interview, NewsSource
```

### Flujo de Procesamiento

```
1. Usuario envía tema → 2. Generación de analistas → 3. Creación de expertos
                          ↓                           ↓
6. Reporte final ← 5. Análisis credibilidad ← 4. Entrevistas paralelas
```

## 🔧 Integración con OpenAI API

### Configuración del Cliente
```python
from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
```

### Patrón de Uso Estructurado
```python
def ai_function_example(self, input_data: str) -> Dict:
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # Modelo más reciente
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}  # Salida estructurada
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("No content received from OpenAI response")
        
        result = json.loads(content)
        return result
        
    except Exception as e:
        self.logger.error(f"Error in AI function: {e}")
        return fallback_response
```

### Gestión de Rate Limits
```python
import time
from openai.error import RateLimitError

def handle_rate_limit(func):
    """Decorator para manejar límites de rate"""
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Backoff exponencial
        return wrapper
```

## 🗄️ Base de Datos

### Schema de Tablas

#### research_project
```sql
CREATE TABLE research_project (
    id INTEGER PRIMARY KEY,
    topic VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'initialized',
    created_at DATETIME,
    updated_at DATETIME,
    final_report TEXT,
    human_notes TEXT
);
```

#### analyst
```sql
CREATE TABLE analyst (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES research_project(id),
    name VARCHAR(200) NOT NULL,
    specialization VARCHAR(300),
    background TEXT,
    expertise_areas TEXT,
    created_at DATETIME
);
```

#### interview
```sql
CREATE TABLE interview (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES research_project(id),
    analyst_id INTEGER REFERENCES analyst(id),
    expert_id INTEGER REFERENCES expert(id),
    questions TEXT,  -- JSON
    responses TEXT,  -- JSON
    insights TEXT,   -- JSON
    credibility_assessment TEXT,  -- JSON
    fake_news_flags TEXT,  -- JSON
    status VARCHAR(50) DEFAULT 'scheduled',
    completed_at DATETIME
);
```

### Operaciones de Base de Datos

#### Consultas Optimizadas
```python
# Cargar proyecto con todas las relaciones
project = db.session.query(ResearchProject)\
    .options(
        joinedload(ResearchProject.analysts),
        joinedload(ResearchProject.interviews).joinedload(Interview.expert)
    )\
    .filter_by(id=project_id)\
    .first()

# Contar entrevistas completadas eficientemente
completed_count = db.session.query(Interview)\
    .filter_by(project_id=project_id, status='completed')\
    .count()
```

#### Transacciones
```python
def create_project_with_analysts(topic: str, analysts_data: List[Dict]) -> ResearchProject:
    try:
        # Crear proyecto
        project = ResearchProject(topic=topic)
        db.session.add(project)
        db.session.flush()  # Obtener ID sin commit
        
        # Crear analistas
        for analyst_data in analysts_data:
            analyst = Analyst(
                project_id=project.id,
                **analyst_data
            )
            db.session.add(analyst)
        
        db.session.commit()
        return project
        
    except Exception as e:
        db.session.rollback()
        raise e
```

## 🎨 Frontend Architecture

### Estructura de Templates
```
templates/
├── base.html           # Layout base con Bootstrap
├── index.html          # Página principal
├── project.html        # Vista detalle de proyecto
├── report.html         # Visualización de reportes
└── components/         # Componentes reutilizables
    ├── analyst_card.html
    ├── interview_card.html
    └── progress_bar.html
```

### JavaScript Modular
```javascript
// static/js/main.js
class ProjectManager {
    constructor(projectId) {
        this.projectId = projectId;
        this.initEventListeners();
        this.startStatusPolling();
    }
    
    async generateReport() {
        try {
            const response = await fetch(`/project/${this.projectId}/generate_report`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to generate report');
            }
            
            const result = await response.json();
            this.handleReportGenerated(result);
            
        } catch (error) {
            console.error('Error generating report:', error);
            this.showErrorMessage('Error al generar el reporte');
        }
    }
}
```

### Estilos CSS Organizados
```css
/* static/css/main.css */

/* Variables CSS personalizadas */
:root {
    --ai-primary: #2563eb;
    --ai-secondary: #64748b;
    --ai-success: #059669;
    --ai-warning: #d97706;
    --ai-danger: #dc2626;
}

/* Componentes específicos */
.research-project {
    border-radius: 12px;
    transition: all 0.3s ease;
}

.research-project:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.analyst-card {
    background: linear-gradient(135deg, var(--ai-primary), var(--ai-secondary));
    color: white;
}

.credibility-score {
    display: inline-flex;
    align-items: center;
    font-weight: 600;
}

.credibility-score.high { color: var(--ai-success); }
.credibility-score.medium { color: var(--ai-warning); }
.credibility-score.low { color: var(--ai-danger); }
```

## 🔍 Sistema de Logging

### Configuración de Logging
```python
import logging
import structlog
from datetime import datetime

# Configuración estructurada
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.WriteLoggerFactory(),
)

logger = structlog.get_logger()
```

### Logging por Componente
```python
# En ai_agents.py
class AIAgentSystem:
    def __init__(self):
        self.logger = structlog.get_logger("ai_agents")
    
    def generate_specialized_analysts(self, topic, count):
        self.logger.info(
            "Generating analysts",
            topic=topic,
            count=count,
            timestamp=datetime.now().isoformat()
        )
        
        try:
            # Proceso de generación
            result = self._generate_analysts(topic, count)
            
            self.logger.info(
                "Analysts generated successfully",
                generated_count=len(result),
                specializations=[a.get('specialization') for a in result]
            )
            
            return result
            
        except Exception as e:
            self.logger.error(
                "Failed to generate analysts",
                error=str(e),
                topic=topic,
                count=count
            )
            raise
```

## 🧪 Testing Strategy

### Estructura de Tests
```
tests/
├── unit/
│   ├── test_ai_agents.py
│   ├── test_models.py
│   └── test_workflow_manager.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_full_workflow.py
└── fixtures/
    ├── sample_data.json
    └── mock_responses.py
```

### Tests Unitarios
```python
# tests/unit/test_ai_agents.py
import pytest
from unittest.mock import patch, MagicMock
from ai_agents import AIAgentSystem

class TestAIAgentSystem:
    @pytest.fixture
    def ai_system(self):
        return AIAgentSystem()
    
    @patch('ai_agents.openai_client')
    def test_generate_analysts_success(self, mock_openai, ai_system):
        # Mock de respuesta de OpenAI
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
            "analysts": [
                {
                    "name": "Dr. Test Analyst",
                    "specialization": "Test Specialization",
                    "background": "Test background"
                }
            ]
        }'''
        mock_openai.chat.completions.create.return_value = mock_response
        
        # Ejecutar función
        result = ai_system.generate_specialized_analysts("Test topic", 1)
        
        # Assertions
        assert len(result) == 1
        assert result[0]['name'] == "Dr. Test Analyst"
        mock_openai.chat.completions.create.assert_called_once()
    
    def test_analyze_credibility_invalid_input(self, ai_system):
        with pytest.raises(ValueError):
            ai_system.analyze_credibility([], "")
```

### Tests de Integración
```python
# tests/integration/test_full_workflow.py
import pytest
from app import app, db
from models import ResearchProject

class TestFullWorkflow:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()
    
    def test_complete_research_workflow(self, client):
        # 1. Crear proyecto
        response = client.post('/create_project', data={'topic': 'Test Topic'})
        assert response.status_code == 302
        
        # 2. Verificar proyecto creado
        project = ResearchProject.query.first()
        assert project.topic == 'Test Topic'
        assert project.status == 'initialized'
        
        # 3. Iniciar workflow
        response = client.post(f'/project/{project.id}/start_workflow')
        assert response.status_code == 200
        
        # 4. Verificar estado final (podría requerir mocking de OpenAI)
        # ... más assertions
```

## 🚀 Performance Optimization

### Optimizaciones de Base de Datos
```python
# Índices recomendados
CREATE INDEX idx_interview_project_status ON interview(project_id, status);
CREATE INDEX idx_project_status ON research_project(status);
CREATE INDEX idx_analyst_project ON analyst(project_id);

# Connection pooling
from sqlalchemy import create_engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

### Caching de Respuestas
```python
from functools import lru_cache
import hashlib

class AIAgentSystem:
    @lru_cache(maxsize=128)
    def _cached_openai_call(self, prompt_hash: str, model: str) -> str:
        """Cache de llamadas a OpenAI basado en hash del prompt"""
        # Esta función sería llamada internamente
        pass
    
    def generate_specialized_analysts(self, topic: str, count: int):
        # Crear hash del prompt para caching
        prompt_data = f"{topic}_{count}_analysts"
        prompt_hash = hashlib.md5(prompt_data.encode()).hexdigest()
        
        # Usar cache si está disponible
        cached_result = self._get_cached_result(prompt_hash)
        if cached_result:
            return cached_result
            
        # Continuar con llamada normal a OpenAI
        # ...
```

### Async Processing
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class WorkflowManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    async def process_interviews_async(self, project: ResearchProject):
        """Procesar entrevistas de forma asíncrona"""
        interviews = project.interviews.filter_by(status='scheduled').all()
        
        tasks = []
        for interview in interviews:
            task = asyncio.create_task(
                self._process_single_interview_async(interview)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def _process_single_interview_async(self, interview):
        """Procesar una entrevista individual"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._conduct_interview_sync,
            interview
        )
```

## 🔒 Seguridad

### Validación de Entrada
```python
from marshmallow import Schema, fields, validate

class ProjectCreateSchema(Schema):
    topic = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=500),
        error_messages={'required': 'Topic is required'}
    )
    human_notes = fields.Str(
        validate=validate.Length(max=2000),
        missing=None
    )

# En routes.py
@app.route('/create_project', methods=['POST'])
def create_project():
    schema = ProjectCreateSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as err:
        flash(f'Error de validación: {err.messages}', 'error')
        return redirect(url_for('index'))
    
    # Procesar datos validados
    topic = data['topic']
    # ...
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/project/<int:project_id>/generate_report', methods=['POST'])
@limiter.limit("5 per minute")
def generate_report(project_id):
    # Lógica de generación de reporte
    pass
```

### Sanitización de Datos
```python
import bleach
from markupsafe import Markup

def sanitize_html(content: str) -> str:
    """Sanitizar contenido HTML"""
    allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
    allowed_attributes = {}
    
    clean_content = bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    
    return clean_content

# En templates (usando Jinja2)
{{ user_content | safe }}  # Solo después de sanitizar
```

## 📊 Monitoring y Métricas

### Health Checks
```python
@app.route('/health')
def health_check():
    """Endpoint de verificación de salud del sistema"""
    try:
        # Verificar conexión a base de datos
        db.session.execute('SELECT 1')
        
        # Verificar API de OpenAI (opcional)
        # openai_status = check_openai_api()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'openai': 'available'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
```

### Métricas de Performance
```python
import time
from functools import wraps

def measure_performance(func):
    """Decorator para medir tiempo de ejecución"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Log métricas
        logger.info(
            "Function performance",
            function=func.__name__,
            execution_time=execution_time,
            args_count=len(args),
            kwargs_count=len(kwargs)
        )
        
        return result
    return wrapper

# Uso
@measure_performance
def generate_specialized_analysts(self, topic, count):
    # Lógica de función
    pass
```

Esta documentación técnica proporciona una visión comprensiva de la arquitectura, implementación y mejores prácticas del sistema AI News Research Hub.