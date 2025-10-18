"""Gaming Theme - RPG, Achievement Unlocks & Level-Ups"""
from typing import List
from ..base_theme import BaseTheme


class GamingTheme(BaseTheme):
    """RPG terminology, achievement unlocks, gaming references"""
    
    @property
    def name(self) -> str:
        return "gaming"
    
    @property
    def description(self) -> str:
        return "Gaming culture references, RPG progression, achievement unlocks, and level-up celebrations"
    
    def get_phrases(self, tier: str, sentence_type: str) -> List[str]:
        """Get gaming phrases by tier and type"""
        
        phrases = {
            "low": {
                "statement": [
                    "Tutorial complete! Ready for the real challenge?",
                    "New player has entered the game",
                    "Character creation successful - stats looking good!",
                    "Loading screen: 'Great adventures await brave souls'",
                    "You've spawned into your destiny",
                    "First quest accepted: Become Legendary"
                ],
                "question": [
                    "Ready to level up your life?",
                    "Want to unlock your hidden potential?",
                    "Shall we begin this epic campaign?",
                    "Choose your class: Hero or Legend?",
                    "Ready Player One?"
                ],
                "imperative": [
                    "Press START to begin your journey!",
                    "Collect experience points like a pro!",
                    "Equip your determination!",
                    "Save your progress often!",
                    "Level up your mindset!"
                ],
                "exclamation": [
                    "Game ON!",
                    "New adventure unlocked!",
                    "Character boost activated!",
                    "Quest accepted!",
                    "Power-up acquired!"
                ]
            },
            "mid": {
                "statement": [
                    "COMBO MULTIPLIER: Your streak is unstoppable!",
                    "Boss battle initiated - you're winning!",
                    "Rare loot discovered: PURE DETERMINATION",
                    "Guild leader status: EARNED",
                    "Your skill tree is evolving beautifully",
                    "Critical hit! Double damage to obstacles!"
                ],
                "question": [
                    "Ready to raid the final dungeon?",
                    "Who needs cheat codes when you have skill?",
                    "Feeling overpowered yet?",
                    "Want to see your final form?",
                    "Ready for the championship match?"
                ],
                "imperative": [
                    "Activate BEAST MODE!",
                    "Chain those combo attacks!",
                    "Upgrade your weapons!",
                    "Dominate the leaderboard!",
                    "Execute your special move!"
                ],
                "exclamation": [
                    "LEGENDARY COMBO ACHIEVED!",
                    "BOSS DEFEATED!",
                    "RARE ACHIEVEMENT UNLOCKED!",
                    "POWER LEVEL: OVER 9000!",
                    "FLAWLESS VICTORY!"
                ]
            },
            "high": {
                "statement": [
                    "ACHIEVEMENT UNLOCKED: OKR Master Supreme 👑",
                    "You have reached MAX LEVEL in life",
                    "Speedrun world record: OBLITERATED",
                    "Final boss defeated - you ARE the final boss now",
                    "Platinum trophy earned: REALITY DOMINATION",
                    "Game completed at 100% - New Game+ unlocked"
                ],
                "question": [
                    "How does it feel to break the game?",
                    "Ready to write your own cheat codes?",
                    "Want to become the final boss of success?",
                    "Feeling like the main character yet?",
                    "Ready to mod reality itself?"
                ],
                "imperative": [
                    "CLAIM YOUR HIGH SCORE!",
                    "ACTIVATE GOD MODE!",
                    "BREAK ALL THE RECORDS!",
                    "RULE THE SERVER!",
                    "BECOME THE LEGEND!"
                ],
                "exclamation": [
                    "GAME OVER - YOU WIN EVERYTHING!",
                    "PERFECT SCORE ACHIEVED!",
                    "YOU'VE BROKEN THE GAME!",
                    "ULTIMATE ACHIEVEMENT UNLOCKED!",
                    "HALL OF FAME ENTRY CONFIRMED!"
                ]
            }
        }
        
        return phrases.get(tier, {}).get(sentence_type, ["Achievement unlocked!"])
    
    def get_emoji_style(self, tier: str) -> str:
        """Get emoji style for gaming theme"""
        styles = {
            "low": "🎮",
            "mid": "🎮🔥",
            "high": "🎮🔥👑🏆"
        }
        return styles.get(tier, "🎮")