"""Motivational Theme Manager - Core Engine"""
import random
import logging
from typing import List, Dict, Optional

from .base_theme import BaseTheme
from .config import THEME_CONFIG, TIER_RANGES
from .themes import CinematicTheme, GamingTheme, PhilosophicalTheme


logger = logging.getLogger(__name__)


class MotivationalThemeManager:
    """Central manager for themed motivational phrase generation"""
    
    def __init__(self):
        """Initialize theme manager with default themes"""
        self.themes: Dict[str, BaseTheme] = {}
        self._load_default_themes()
        self.config = THEME_CONFIG.copy()
    
    def _load_default_themes(self):
        """Load the core theme collection"""
        themes = [
            CinematicTheme(),
            GamingTheme(), 
            PhilosophicalTheme()
        ]
        
        for theme in themes:
            self.themes[theme.name] = theme
    
    def _get_tier_from_percentage(self, percentage: float) -> str:
        """Determine tier based on percentage"""
        for tier, (min_val, max_val) in TIER_RANGES.items():
            if min_val <= percentage <= max_val:
                return tier
        return "low"  # fallback
    
    def _select_random_theme(self) -> BaseTheme:
        """Select theme based on weighted probabilities"""
        active_themes = [name for name in self.config["active_themes"] if name in self.themes]
        
        if not active_themes:
            # Fallback to any available theme
            return list(self.themes.values())[0]
        
        # Use weights if configured
        weights = []
        themes_list = []
        
        for theme_name in active_themes:
            themes_list.append(self.themes[theme_name])
            weights.append(self.config["theme_weights"].get(theme_name, 1.0))
        
        return random.choices(themes_list, weights=weights)[0]
    
    def generate_phrase(self, percentage: float, force_theme: Optional[str] = None) -> str:
        """Generate a motivational phrase based on percentage
        
        Args:
            percentage: Progress percentage (0-100)
            force_theme: Optional theme name to force selection
            
        Returns:
            Formatted motivational phrase with emoji
        """
        try:
            # Determine tier and sentence type
            tier = self._get_tier_from_percentage(percentage)
            sentence_types = ["question", "imperative", "exclamation", "statement"]
            sentence_type = random.choice(sentence_types)
            
            # Select theme
            if force_theme and force_theme in self.themes:
                theme = self.themes[force_theme]
            else:
                theme = self._select_random_theme()
            
            # Generate multiple options and pick one
            phrases_count = self.config.get("phrases_per_generation", 5)
            potential_phrases = []
            
            for _ in range(phrases_count):
                # Get phrases from theme
                phrase_options = theme.get_phrases(tier, sentence_type)
                if phrase_options:
                    selected_phrase = random.choice(phrase_options)
                    emoji_style = theme.get_emoji_style(tier)
                    
                    # Format final phrase
                    if emoji_style and not selected_phrase.endswith(emoji_style):
                        formatted_phrase = f"{selected_phrase} {emoji_style}"
                    else:
                        formatted_phrase = selected_phrase
                    
                    potential_phrases.append(formatted_phrase)
            
            # Return random selection from generated options
            return random.choice(potential_phrases) if potential_phrases else "Keep going, champion! 🏆"
            
        except Exception as e:
            # log what happened
            logger.exception("Error generating motivational phrase: %s", e)
            # Graceful fallback
            return f"Amazing progress! You're at {percentage:.1f}% 🌟"

    def add_theme(self, theme: BaseTheme) -> bool:
        """Add a new theme to the manager"""
        try:
            self.themes[theme.name] = theme
            return True
        except Exception:
            return False
    
    def remove_theme(self, theme_name: str) -> bool:
        """Remove a theme from active themes"""
        if theme_name in self.themes:
            # Remove from active list but keep the theme object
            if theme_name in self.config["active_themes"]:
                self.config["active_themes"].remove(theme_name)
            return True
        return False
    
    def list_available_themes(self) -> List[Dict[str, str]]:
        """Get metadata for all available themes"""
        return [theme.get_theme_metadata() for theme in self.themes.values()]
    
    def set_theme_weights(self, weights: Dict[str, float]):
        """Update theme selection weights"""
        self.config["theme_weights"].update(weights)
    
    def get_theme_stats(self) -> Dict[str, int]:
        """Get statistics about available themes (for debugging/analytics)"""
        stats = {}
        for theme_name, theme in self.themes.items():
            phrase_count = 0
            for tier in ["low", "mid", "high"]:
                for sentence_type in ["question", "imperative", "exclamation", "statement"]:
                    phrases = theme.get_phrases(tier, sentence_type)
                    phrase_count += len(phrases)
            stats[theme_name] = phrase_count
        return stats