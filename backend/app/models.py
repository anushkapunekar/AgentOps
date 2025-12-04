from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    gitlab_user_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    access_token = Column(String, nullable=True)      # user's GitLab access token
    refresh_token = Column(String, nullable=True)
    token_expires_at = Column(Integer, nullable=True)
    session_token = Column(String, nullable=True, unique=True)  # simple session token for frontend auth

class Installation(Base):
    __tablename__ = "installations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)               # who installed it
    project_id = Column(Integer, nullable=False)            # GitLab project id
    project_name = Column(String, nullable=True)
    webhook_id = Column(Integer, nullable=True)             # GitLab returned webhook ID
    webhook_token = Column(String, nullable=True)           # secret per installation
    pipeline_trigger_token = Column(String, nullable=True)  # trigger token for pipelines
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MRAnalysis(Base):
    __tablename__ = "mr_analyses"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)
    mr_iid = Column(Integer, nullable=False)
    summary_markdown = Column(Text, nullable=True)
    problems_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Boolean, default=False)
