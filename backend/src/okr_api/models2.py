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
    progress = Column(Integer, nullable=True, server_default="0")
    metric = Column(String(255), nullable=True)
    unit = Column(Integer, nullable=True, server_default="1")
