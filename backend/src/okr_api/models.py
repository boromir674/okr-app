from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Objective(Base):
    """Represents an Objective in the database."""
    __tablename__ = "objectives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    progress = Column(Float, default=0.0)

    # Configure cascading delete for key_results
    key_results = relationship(
        "KeyResult",
        back_populates="objective",
        cascade="all, delete-orphan"
    )

class KeyResult(Base):
    """Represents a Key Result in the database."""
    __tablename__ = "key_results"

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(Integer, ForeignKey("objectives.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)
    progress = Column(Float, default=0.0)
    metric = Column(String)

    objective = relationship("Objective", back_populates="key_results")
