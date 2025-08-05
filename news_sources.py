import logging
from app import db
from models import NewsSource

class NewsSourceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Don't initialize sources in __init__ to avoid context issues
    
    def initialize_default_sources(self):
        """Initialize database with credible news sources"""
        try:
            # Check if sources already exist
            if NewsSource.query.count() > 0:
                return
            
            # Default credible news sources
            default_sources = [
                {
                    'name': 'Reuters',
                    'url': 'https://www.reuters.com',
                    'credibility_rating': 0.95,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'Associated Press (AP)',
                    'url': 'https://apnews.com',
                    'credibility_rating': 0.94,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'BBC News',
                    'url': 'https://www.bbc.com/news',
                    'credibility_rating': 0.90,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'NPR',
                    'url': 'https://www.npr.org',
                    'credibility_rating': 0.89,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'Wall Street Journal',
                    'url': 'https://www.wsj.com',
                    'credibility_rating': 0.87,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'The Guardian',
                    'url': 'https://www.theguardian.com',
                    'credibility_rating': 0.85,
                    'bias_rating': 'left',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'The New York Times',
                    'url': 'https://www.nytimes.com',
                    'credibility_rating': 0.84,
                    'bias_rating': 'left',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'FactCheck.org',
                    'url': 'https://www.factcheck.org',
                    'credibility_rating': 0.96,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'Snopes',
                    'url': 'https://www.snopes.com',
                    'credibility_rating': 0.93,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                },
                {
                    'name': 'PolitiFact',
                    'url': 'https://www.politifact.com',
                    'credibility_rating': 0.91,
                    'bias_rating': 'center',
                    'fact_check_rating': 'high',
                    'is_verified': True
                }
            ]
            
            for source_data in default_sources:
                source = NewsSource(**source_data)
                db.session.add(source)
            
            db.session.commit()
            self.logger.info(f"Initialized {len(default_sources)} default news sources")
            
        except Exception as e:
            self.logger.error(f"Error initializing news sources: {e}")
            db.session.rollback()
    
    def get_credible_sources(self, min_credibility=0.8):
        """Get list of credible news sources"""
        return NewsSource.query.filter(
            NewsSource.credibility_rating >= min_credibility,
            NewsSource.is_verified == True
        ).all()
    
    def assess_source_credibility(self, source_name):
        """Assess the credibility of a given source"""
        source = NewsSource.query.filter_by(name=source_name).first()
        if source:
            return {
                'credibility_rating': source.credibility_rating,
                'bias_rating': source.bias_rating,
                'fact_check_rating': source.fact_check_rating,
                'is_verified': source.is_verified
            }
        
        # Return default low credibility for unknown sources
        return {
            'credibility_rating': 0.3,
            'bias_rating': 'unknown',
            'fact_check_rating': 'low',
            'is_verified': False
        }
    
    def add_source(self, name, url, credibility_rating, bias_rating, fact_check_rating):
        """Add a new news source to the database"""
        try:
            source = NewsSource(
                name=name,
                url=url,
                credibility_rating=credibility_rating,
                bias_rating=bias_rating,
                fact_check_rating=fact_check_rating,
                is_verified=False  # New sources need manual verification
            )
            db.session.add(source)
            db.session.commit()
            return source
        except Exception as e:
            self.logger.error(f"Error adding news source: {e}")
            db.session.rollback()
            return None
