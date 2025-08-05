# Overview

AI News Research Hub is a comprehensive AI-powered news research application that generates teams of specialized AI analysts to investigate topics, conduct expert interviews, and produce verified reports while filtering out fake news. The system uses OpenAI's GPT-4o model to create intelligent agents that work in parallel to gather information from credible sources and provide multi-perspective analysis.

# User Preferences

Preferred communication style: Simple, everyday language.

# Recent Changes (2025-08-05)

## ✅ Critical Bug Fixes Completed
- **Token Limit Issue Resolved**: Fixed OpenAI API rate limit error (13,443 tokens exceeded 10,000 limit)
- **Interview Completion Bug Fixed**: Corrected workflow where interviews were scheduled but never executed
- **Type Safety Improvements**: Fixed `str | None` error in JSON parsing throughout ai_agents.py
- **Report Generation Optimized**: Implemented condensed summaries to prevent token overflow

## ✅ Performance Improvements
- **Interview Processing**: Successfully executed 5+ interviews with real AI-generated content
- **Report Generation**: Both projects 3 and 5 now generate comprehensive reports successfully
- **Database Integrity**: All interview data properly stored with UTF-8 encoding
- **Error Handling**: Enhanced logging and traceback for better debugging

## ✅ System Status
- **Workflow Manager**: Fully operational with improved error recovery
- **AI Agent System**: Stable with optimized token usage
- **Report Templates**: Working correctly with Spanish interface
- **Database**: All projects have properly completed interviews and generated reports

# System Architecture

## Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database**: SQLite for development with PostgreSQL-ready configuration
- **AI Integration**: OpenAI GPT-4o for generating analysts and conducting research
- **Workflow Management**: Multi-threaded background processing for research workflows
- **Session Management**: Flask sessions with configurable secret keys

## Data Model Design
- **ResearchProject**: Central entity tracking research topics and workflow status
- **Analyst**: AI-generated specialists with unique expertise areas
- **Expert**: Virtual experts for interview simulation
- **Interview**: Records of AI-conducted expert interviews with credibility assessment
- **NewsSource**: Managed repository of verified news sources with credibility ratings

## Frontend Architecture
- **Templates**: Jinja2-based HTML templates with Bootstrap dark theme
- **Styling**: Custom CSS with responsive design and hover effects
- **JavaScript**: Vanilla JS with Feather icons integration and auto-refresh functionality
- **UI Components**: Card-based layout with progress tracking and status indicators

## AI Agent System
- **Dynamic Analyst Generation**: Creates specialized AI analysts based on research topic
- **Multi-Agent Workflow**: Parallel processing of research tasks
- **Credibility Assessment**: Built-in fake news detection and source verification
- **Interview Simulation**: AI-to-AI expert interviews for comprehensive coverage

## Workflow Management
- **Status Tracking**: Multi-stage process (initialized → analyzing → interviewing → reviewing → completed)
- **Background Processing**: Threaded execution to prevent blocking user interface
- **Progress Monitoring**: Real-time status updates and completion tracking
- **Error Handling**: Comprehensive logging and error recovery mechanisms

# External Dependencies

## AI Services
- **OpenAI API**: GPT-4o model for AI agent generation and natural language processing
- **API Key Management**: Environment variable configuration for secure access

## Web Framework Stack
- **Flask**: Core web application framework
- **SQLAlchemy**: Database ORM with connection pooling
- **Werkzeug**: WSGI utilities and proxy fix middleware

## Frontend Libraries
- **Bootstrap**: Dark theme CSS framework via CDN
- **Feather Icons**: Icon system via unpkg CDN
- **Custom CSS/JS**: Local static assets for application-specific styling and functionality

## Database Configuration
- **SQLite**: Default development database
- **PostgreSQL Support**: Production-ready database configuration via DATABASE_URL
- **Connection Management**: Pool recycling and health checks for reliability

## News Source Integration
- **Credible Source Database**: Pre-configured trusted news sources (Reuters, AP, BBC, NPR)
- **Credibility Scoring**: Built-in rating system for source verification
- **Bias Assessment**: Multi-dimensional evaluation of news source reliability