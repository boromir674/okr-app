"""ORM - Declarative Data models in SQL Alchemy"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Objective(Base):
    """Database model for Objectives."""
    __tablename__ = 'objectives'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    progress = Column(Integer, nullable=True, server_default="0")


class KeyResult(Base):
    """Database model for Key Results."""
    __tablename__ = 'key_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    objective_id = Column(Integer, ForeignKey('objectives.id', ondelete='CASCADE'), nullable=False)
    description = Column(Text, nullable=False)
    # title-like short description
    short_description = Column(String(255), nullable=True)

    # Live progress tracker
    progress = Column(Integer, nullable=True, server_default="0",
        comment="Current progress value between min_progress_value and max_progress_value"
    )
    metric = Column(String(255), nullable=True, comment="Metric for measuring progress")
    unit = Column(Integer, nullable=True, server_default="1")

    # Progress tracking bounds
    min_progress_value = Column(Integer, nullable=False, server_default="0",
        comment="Minimum value for progress tracking (>=0)"
    )
    max_progress_value = Column(Integer, nullable=False, server_default="100",
        comment="Maximum value for progress tracking (>min_progress_value)"
    )
