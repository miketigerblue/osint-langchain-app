from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import json

engine = create_engine("sqlite:///data/threats.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class ThreatAnalysis(Base):
    __tablename__ = "threat_analysis"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(Text)
    analysis = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_name = Column(String, default="Unknown Source")
    source_url = Column(String, default="No URL Provided")

Base.metadata.create_all(engine)

def save_threat_metadata(title, content, analysis):
    threat = ThreatAnalysis(title=title, content=content, analysis=analysis)
    session.add(threat)
    session.commit()

def fetch_all_threats():
    return session.query(ThreatAnalysis).order_by(ThreatAnalysis.timestamp.desc()).all()
