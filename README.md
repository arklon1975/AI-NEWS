# AI News Research Hub 🔍

Un sistema avanzado de investigación de noticias impulsado por inteligencia artificial que genera equipos de analistas especializados para investigar temas, realizar entrevistas con expertos y producir informes verificados mientras filtra noticias falsas.

## 🌟 Características Principales

### Sistema Multi-Agente Inteligente
- **Generación Dinámica de Analistas**: Crea analistas de IA especializados basados en el tema de investigación
- **Procesamiento Paralelo**: Múltiples agentes trabajan simultáneamente para máxima eficiencia
- **Entrevistas IA-a-IA**: Simulación de entrevistas entre analistas y expertos virtuales
- **Detección de Fake News**: Sistema integrado de verificación de credibilidad y detección de desinformación

### Investigación Integral
- **Análisis Multi-Perspectiva**: Evaluación desde múltiples ángulos (político, económico, internacional)
- **Verificación de Fuentes**: Base de datos de fuentes confiables con calificaciones de credibilidad
- **Evaluación de Credibilidad**: Análisis automático de la confiabilidad de la información
- **Informes Comprensivos**: Generación de reportes detallados con resúmenes ejecutivos

## 🚀 Tecnologías Utilizadas

### Backend
- **Flask**: Framework web principal con arquitectura modular
- **SQLAlchemy**: ORM para gestión de base de datos
- **OpenAI GPT-4o**: Modelo de IA de última generación para generación de agentes
- **PostgreSQL/SQLite**: Base de datos configurable para desarrollo y producción
- **Threading**: Procesamiento en segundo plano para workflows no bloqueantes

### Frontend
- **Bootstrap 5**: Framework CSS con tema oscuro personalizado
- **Vanilla JavaScript**: Funcionalidades interactivas sin dependencias externas
- **Feather Icons**: Sistema de iconos moderno y limpio
- **Jinja2**: Motor de plantillas para renderizado dinámico

### IA y Procesamiento
- **Multi-Threading**: Ejecución paralela de tareas de investigación
- **JSON Structured Output**: Comunicación estructurada con modelos de IA
- **Rate Limiting**: Gestión inteligente de límites de API
- **Error Handling**: Manejo robusto de errores y recuperación automática

## 📦 Instalación

### Prerrequisitos
- Python 3.11+
- Cuenta de OpenAI con API Key
- Git

### Configuración Rápida

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/ai-news-research-hub.git
cd ai-news-research-hub
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
# Crear archivo .env
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env
echo "SESSION_SECRET=tu_clave_secreta_aleatoria" >> .env
echo "DATABASE_URL=sqlite:///instance/news_research.db" >> .env
```

4. **Inicializar la base de datos**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

5. **Ejecutar la aplicación**
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## 🎯 Uso del Sistema

### 1. Crear Proyecto de Investigación
- Accede a la página principal
- Introduce el tema de investigación (ej: "Políticas económicas de Donald Trump")
- El sistema generará automáticamente analistas especializados

### 2. Proceso de Investigación Automático
El sistema ejecuta un workflow de 5 etapas:

1. **Inicialización**: Creación del proyecto y configuración inicial
2. **Análisis**: Generación de analistas especializados según el tema
3. **Entrevistas**: Ejecución paralela de entrevistas IA-experto
4. **Revisión**: Análisis de credibilidad y detección de fake news
5. **Completado**: Disponibilidad para generar reporte final

### 3. Generación de Informes
- Una vez completadas las entrevistas, usar el botón "Generar Reporte Final"
- El sistema produce un informe comprensivo con:
  - Resumen ejecutivo
  - Hallazgos principales verificados
  - Análisis de credibilidad de fuentes
  - Detección de posible desinformación
  - Múltiples perspectivas del tema
  - Recomendaciones y conclusiones

## 🏗️ Arquitectura del Sistema

### Modelos de Datos
```python
# Proyecto principal
ResearchProject
├── topic: str               # Tema de investigación
├── status: str             # Estado del workflow
├── analysts: List[Analyst] # Analistas generados
└── interviews: List[Interview] # Entrevistas realizadas

# Analistas especializados
Analyst
├── name: str              # Nombre del analista
├── specialization: str    # Área de especialización
├── background: str        # Experiencia y antecedentes
└── expertise_areas: List[str] # Áreas de expertise

# Entrevistas y expertos
Interview
├── questions: JSON        # Preguntas generadas
├── responses: JSON        # Respuestas del experto
├── credibility_assessment: JSON # Análisis de credibilidad
└── fake_news_flags: JSON  # Indicadores de desinformación
```

### Flujo de Trabajo Multi-Agente
```
Entrada de Usuario → Generación de Analistas → Creación de Expertos
        ↓                    ↓                        ↓
Ejecución Paralela ← Entrevistas IA-a-IA ← Generación de Preguntas
        ↓
Análisis de Credibilidad → Detección de Fake News → Reporte Final
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# API Keys
OPENAI_API_KEY=sk-...           # Clave de OpenAI (requerida)

# Configuración de Base de Datos
DATABASE_URL=postgresql://...   # URL de PostgreSQL para producción
DATABASE_URL=sqlite:///...      # SQLite para desarrollo

# Seguridad
SESSION_SECRET=clave_aleatoria  # Clave para sesiones de Flask

# Configuración de Logging
LOG_LEVEL=INFO                  # Nivel de logging (DEBUG, INFO, WARNING, ERROR)
```

### Fuentes de Noticias Verificadas
El sistema incluye una base de datos pre-configurada de fuentes confiables:

| Fuente | Credibilidad | Tipo | Sesgo |
|--------|-------------|------|-------|
| Reuters | 9.5/10 | Agencia Internacional | Mínimo |
| Associated Press | 9.5/10 | Agencia de Noticias | Mínimo |
| BBC News | 9.0/10 | Broadcaster Público | Centro |
| NPR | 9.0/10 | Radio Pública | Centro-Izquierda |

## 🧪 Testing y Desarrollo

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/

# Coverage
python -m pytest --cov=. tests/

# Tests de integración
python -m pytest tests/integration/
```

### Modo de Desarrollo
```bash
# Con recarga automática
export FLASK_ENV=development
python main.py

# Con debugging detallado
export LOG_LEVEL=DEBUG
python main.py
```

## 🚀 Despliegue

### Usando Replit (Recomendado)
1. Importar proyecto en Replit
2. Configurar secrets: `OPENAI_API_KEY`, `SESSION_SECRET`
3. Ejecutar: `gunicorn --bind 0.0.0.0:5000 main:app`

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Producción con PostgreSQL
```bash
# Configurar DATABASE_URL
export DATABASE_URL="postgresql://usuario:password@host:5432/database"

# Migrar base de datos
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 📊 Métricas y Monitoring

### Logs del Sistema
- **INFO**: Operaciones normales y estados de workflow
- **DEBUG**: Detalles de llamadas a API y procesamiento interno
- **WARNING**: Problemas de credibilidad o fuentes cuestionables
- **ERROR**: Fallos en API, base de datos o procesamiento

### Métricas de Credibilidad
- **Puntuación de Credibilidad**: 0.0 - 1.0 basada en análisis de fuentes
- **Indicadores de Fake News**: Lista de señales de alerta identificadas
- **Verificación de Hechos**: Confirmación cruzada con fuentes confiables

## 🤝 Contribuir

### Guías de Contribución
1. Fork el repositorio
2. Crear branch para feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push al branch: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Estándares de Código
- **Python**: PEP 8, type hints, docstrings
- **JavaScript**: ESLint, código modular
- **CSS**: BEM methodology, mobile-first
- **Tests**: Cobertura mínima 80%

## 📝 Changelog

### v1.0.0 (2025-08-05)
- ✅ Sistema multi-agente completo implementado
- ✅ Integración con OpenAI GPT-4o
- ✅ Detección de fake news y verificación de credibilidad
- ✅ Interfaz web responsive en español
- ✅ Base de datos de fuentes verificadas
- ✅ Generación de informes comprensivos
- ✅ Procesamiento paralelo de entrevistas
- ✅ Sistema de logging y manejo de errores

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

### Problemas Comunes

**Error de API Key de OpenAI**
```bash
# Verificar que la clave esté configurada
echo $OPENAI_API_KEY
# Si está vacía, configurarla
export OPENAI_API_KEY="tu_clave_aqui"
```

**Base de Datos No Inicializada**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**Puerto 5000 en Uso**
```bash
# Cambiar puerto
gunicorn --bind 0.0.0.0:8000 main:app
```

### Contacto y Reportar Bugs
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/ai-news-research-hub/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/ai-news-research-hub/discussions)

---

**Desarrollado con ❤️ usando IA de última generación para combatir la desinformación y promover el periodismo verificado.**