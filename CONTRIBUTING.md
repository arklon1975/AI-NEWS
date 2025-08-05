# Guía de Contribución - AI News Research Hub

¡Gracias por tu interés en contribuir al AI News Research Hub! Esta guía te ayudará a empezar.

## 🚀 Primeros Pasos

### Configuración del Entorno de Desarrollo

1. **Fork y clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/ai-news-research-hub.git
cd ai-news-research-hub
```

2. **Configurar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus claves de API
```

5. **Inicializar base de datos**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 📋 Tipos de Contribuciones

### 🐛 Reportar Bugs
- Usar la [plantilla de bug report](https://github.com/tu-usuario/ai-news-research-hub/issues/new?template=bug_report.md)
- Incluir pasos para reproducir el error
- Especificar versión de Python y sistema operativo
- Agregar logs relevantes

### ✨ Solicitar Features
- Usar la [plantilla de feature request](https://github.com/tu-usuario/ai-news-research-hub/issues/new?template=feature_request.md)
- Describir el problema que resuelve
- Proponer implementación si es posible
- Considerar casos de uso alternativos

### 🔧 Contribuir Código

#### Áreas de Contribución Prioritarias
- **Detectores de Fake News**: Mejorar algoritmos de detección
- **Fuentes de Noticias**: Agregar nuevas fuentes verificadas
- **Interfaz de Usuario**: Mejoras de UX/UI
- **Performance**: Optimizaciones de velocidad y memoria
- **Testing**: Cobertura de tests y casos edge
- **Documentación**: Guías y ejemplos

## 🎯 Estándares de Código

### Python (Backend)
```python
# Usar type hints
def analyze_credibility(self, responses: List[Dict], topic: str) -> Dict[str, Any]:
    """
    Analiza la credibilidad de las respuestas.
    
    Args:
        responses: Lista de respuestas de entrevistas
        topic: Tema de investigación
        
    Returns:
        Diccionario con análisis de credibilidad
    """
    pass

# Usar docstrings descriptivos
# Seguir PEP 8
# Usar logging apropiado
```

### JavaScript (Frontend)
```javascript
// Usar ES6+ features
const analyzeData = async (data) => {
    try {
        const result = await processData(data);
        return result;
    } catch (error) {
        console.error('Error processing data:', error);
        throw error;
    }
};

// Comentarios claros para lógica compleja
// Manejo de errores consistente
```

### CSS/SCSS
```css
/* Usar metodología BEM */
.research-project__title {
    font-size: 1.5rem;
    color: var(--bs-primary);
}

/* Mobile-first approach */
@media (min-width: 768px) {
    .research-project__title {
        font-size: 2rem;
    }
}
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/unit/

# Tests de integración
python -m pytest tests/integration/

# Coverage
python -m pytest --cov=. --cov-report=html tests/
```

### Escribir Tests
```python
# tests/test_ai_agents.py
import pytest
from ai_agents import AIAgentSystem

class TestAIAgentSystem:
    def test_generate_analysts(self):
        """Test de generación de analistas"""
        ai_system = AIAgentSystem()
        analysts = ai_system.generate_specialized_analysts("Test topic", 3)
        
        assert len(analysts) == 3
        assert all(analyst.get('name') for analyst in analysts)
        assert all(analyst.get('specialization') for analyst in analysts)

    @pytest.mark.asyncio
    async def test_conduct_interview(self):
        """Test de realización de entrevistas"""
        # Test implementation
        pass
```

## 📝 Proceso de Pull Request

### 1. Preparación
```bash
# Crear branch para feature
git checkout -b feature/nueva-funcionalidad

# O para fix
git checkout -b fix/corregir-bug
```

### 2. Desarrollo
- Escribir código siguiendo estándares
- Agregar tests para nuevo código
- Actualizar documentación si es necesario
- Hacer commits descriptivos

### 3. Commits
```bash
# Mensajes de commit descriptivos
git commit -m "feat: agregar detector de sesgo político en fuentes

- Implementar algoritmo de detección de sesgo
- Agregar scoring de neutralidad 0-10
- Incluir tests unitarios
- Actualizar documentación de API"
```

### 4. Pull Request
- Usar la plantilla de PR
- Describir cambios realizados
- Incluir screenshots si aplica
- Referenciar issues relacionados
- Asegurar que todos los tests pasen

### Plantilla de PR
```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva feature
- [ ] Breaking change
- [ ] Documentación

## Testing
- [ ] Tests unitarios agregados/actualizados
- [ ] Tests de integración agregados/actualizados
- [ ] Todos los tests existentes pasan

## Checklist
- [ ] Código sigue estándares del proyecto
- [ ] Self-review realizado
- [ ] Documentación actualizada
- [ ] No introduce breaking changes
```

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios
```
ai-news-research-hub/
├── app.py                 # Configuración Flask
├── main.py               # Punto de entrada
├── models.py             # Modelos de base de datos
├── routes.py             # Rutas de la aplicación
├── ai_agents.py          # Sistema de agentes IA
├── workflow_manager.py   # Gestor de workflows
├── news_sources.py       # Fuentes de noticias verificadas
├── templates/            # Plantillas HTML
├── static/              # Archivos estáticos (CSS, JS)
├── tests/               # Tests unitarios e integración
└── docs/                # Documentación adicional
```

### Flujo de Datos
```
Usuario → Flask Routes → Workflow Manager → AI Agents → Database
                    ↓
Templates ← Jinja2 ← Response Data ← OpenAI API ← Analysis
```

## 🔍 Debugging y Troubleshooting

### Logs de Debugging
```python
import logging

# Configurar logging detallado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# En el código
logger.debug(f"Processing interview with expert: {expert.name}")
logger.info(f"Generated {len(questions)} questions for topic: {topic}")
logger.warning(f"Low credibility score: {score}")
logger.error(f"Failed to generate report: {error}")
```

### Problemas Comunes

**Error de API Key**
```bash
# Verificar configuración
python -c "import os; print(os.environ.get('OPENAI_API_KEY', 'NOT SET'))"
```

**Base de Datos**
```bash
# Recrear tablas
python -c "from app import app, db; app.app_context().push(); db.drop_all(); db.create_all()"
```

## 📚 Recursos Útiles

### Documentación Técnica
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Bootstrap Components](https://getbootstrap.com/docs/5.1/components/)

### Herramientas Recomendadas
- **IDE**: VS Code con extensiones Python, Prettier
- **Testing**: pytest, pytest-cov
- **Linting**: flake8, black, mypy
- **API Testing**: Postman, curl
- **Database**: SQLite Browser, pgAdmin

## 🤝 Comunidad

### Canales de Comunicación
- **GitHub Issues**: Para bugs y feature requests
- **GitHub Discussions**: Para preguntas y ideas
- **Code Review**: Comentarios constructivos en PRs

### Código de Conducta
- Ser respetuoso y constructivo
- Proveer feedback útil y específico  
- Colaborar de manera inclusiva
- Reportar comportamiento inapropiado

## 🎉 Reconocimientos

Los contribuidores serán reconocidos en:
- README principal del proyecto
- Release notes
- Página de contributors en la documentación

¡Gracias por ayudar a mejorar AI News Research Hub! 🚀