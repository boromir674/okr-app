"""Configuration for Motivational Themes System"""

# Theme Configuration
THEME_CONFIG = {
    "active_themes": ["cinematic", "gaming", "philosophical"],
    "theme_weights": {
        "cinematic": 0.4,      # 40% chance - Movie quotes are crowd favorites
        "gaming": 0.35,        # 35% chance - Gaming culture is huge 
        "philosophical": 0.25  # 25% chance - Deep thoughts for variety
    },
    "user_customizable": True,
    "fallback_theme": "gaming",
    "phrases_per_generation": 5,  # Generate 5 options, pick 1 randomly
    "enable_cross_theme_mixing": False  # Future feature
}

# Tier definitions based on percentage ranges
TIER_RANGES = {
    "low": (0, 24),      # 0-24%
    "mid": (25, 74),     # 25-74% 
    "high": (75, 100)    # 75-100%
}