"""SQLAlchemy models for TikTok AI system"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from app.config import settings

Base = declarative_base()


class AnalysisRecord(Base):
    __tablename__ = "analysis_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, index=True)
    analysis_type = Column(String(50), default="competitor")  # competitor | strategy
    report_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="completed")  # completed | failed
    error_msg = Column(Text, nullable=True)


# Engine and session factory
_engine = None
_Session = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(f"sqlite:///{settings.SQLITE_PATH}", echo=False)
        Base.metadata.create_all(_engine)
    return _engine


def get_session():
    global _Session
    if _Session is None:
        _Session = sessionmaker(bind=get_engine())
    return _Session()
