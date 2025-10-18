"""Base Theme Interface"""
from abc import ABC, abstractmethod
from typing import List, Dict
import typing as t


class BaseTheme(ABC):
    """Base class for all motivational themes"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Theme name identifier"""
        pass
    
    @property
    @abstractmethod  
    def description(self) -> str:
        """Human-readable theme description"""
        pass
    
    @abstractmethod
    def get_phrases(self, tier: str, sentence_type: str) -> List[str]:
        """Get phrases for specific tier and sentence type
        
        Args:
            tier: 'low', 'mid', or 'high'
            sentence_type: 'question', 'imperative', 'exclamation', 'statement'
        """
        pass
    
    @abstractmethod
    def get_emoji_style(self, tier: str) -> str:
        """Get emoji pattern for tier"""
        pass
    
    def get_theme_metadata(self) -> Dict[str, t.Any]:
        """Return theme metadata"""
        return {
            'name': self.name,
            'description': self.description,
            'tiers': ['low', 'mid', 'high'],
            'sentence_types': ['question', 'imperative', 'exclamation', 'statement']
        }