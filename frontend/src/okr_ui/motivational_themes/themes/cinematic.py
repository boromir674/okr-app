"""Cinematic Theme - Movie Quotes & Film References"""
from typing import List
from ..base_theme import BaseTheme


class CinematicTheme(BaseTheme):
    """Movie quotes, film references, and epic cinematic one-liners"""
    
    @property
    def name(self) -> str:
        return "cinematic"
    
    @property
    def description(self) -> str:
        return "Epic movie quotes and cinematic references from sci-fi, action, and adventure films"
    
    def get_phrases(self, tier: str, sentence_type: str) -> List[str]:
        """Get cinematic phrases by tier and type"""
        
        phrases = {
            "low": {
                "statement": [
                    "This is where the fun begins!",
                    "You're beginning to believe in your potential",
                    "The journey of a thousand objectives begins with a single step",
                    "Hope is kindling... and you've just lit the spark",
                    "Your story is just getting started, hero",
                    "Every legend begins with someone who dared to try"
                ],
                "question": [
                    "Ready to take the red pill of progress?",
                    "Do you feel lucky? Well, do ya?", 
                    "What if I told you... this is just the beginning?",
                    "Are you not entertained by your own growth?",
                    "Why so serious about limits?"
                ],
                "imperative": [
                    "Use the Force, young padawan!",
                    "Choose your destiny wisely!",
                    "Take the first step into a larger world!",
                    "Believe in something greater!",
                    "Trust the process, Neo!"
                ],
                "exclamation": [
                    "Adventure awaits!",
                    "The spark has been ignited!",
                    "Your origin story begins now!",
                    "Destiny calls your name!",
                    "The hero's journey starts here!"
                ]
            },
            "mid": {
                "statement": [
                    "I am inevitable... and so is your progress!",
                    "You're not trapped with your goals... they're trapped with YOU!",
                    "The Force is strong with this one",
                    "Houston, we have... VICTORY!",
                    "Frankly my dear, I don't give a damn about your limits!",
                    "You have become more powerful than any Jedi could imagine"
                ],
                "question": [
                    "Who said you couldn't be extraordinary?",
                    "Are you feeling it now, Mr. Krabs?",
                    "Do you want to know how deep the rabbit hole goes?",
                    "What's your superpower again?",
                    "Is it a bird? Is it a plane? No, it's YOU!"
                ],
                "imperative": [
                    "Embrace your power, young Skywalker!",
                    "Show them what you're made of!",
                    "Channel your inner Tony Stark!",
                    "Release the Kraken of your potential!",
                    "Execute Order: VICTORY!"
                ],
                "exclamation": [
                    "Avengers... ASSEMBLE your success!",
                    "I have the high ground now!",
                    "THIS! IS! PROGRESS!",
                    "You magnificent beast!",
                    "Great Scott! You're on fire!"
                ]
            },
            "high": {
                "statement": [
                    "I... AM... INEVITABLE! *snaps objectives complete*",
                    "You have become the master of your own Matrix",
                    "Your name will be legend... in every database",
                    "You are the chosen one of this multiverse",
                    "Reality can be whatever you want it to be",
                    "You have transcended from mortal to myth"
                ],
                "question": [
                    "How does it feel to be unstoppable?",
                    "What's it like being the protagonist of reality?",
                    "Ready to take your place among legends?",
                    "Who's the master now?",
                    "Feeling godlike yet?"
                ],
                "imperative": [
                    "CLAIM YOUR THRONE!",
                    "RULE YOUR DOMAIN!",
                    "RESHAPE REALITY ITSELF!",
                    "BECOME THE LEGEND!",
                    "TRANSCEND ALL LIMITS!"
                ],
                "exclamation": [
                    "I AM THE CAPTAIN NOW!",
                    "YOU'VE ACHIEVED THE IMPOSSIBLE!",
                    "REALITY HAS BEEN CONQUERED!",
                    "THE UNIVERSE ACKNOWLEDGES YOUR SUPREMACY!",
                    "INFINITY STONES HAVE NOTHING ON YOU!"
                ]
            }
        }
        
        return phrases.get(tier, {}).get(sentence_type, ["Epic progress achieved!"])
    
    def get_emoji_style(self, tier: str) -> str:
        """Get emoji style for cinematic theme"""
        styles = {
            "low": "🎬",
            "mid": "🎬⚡",
            "high": "🎬⚡🌟👑"
        }
        return styles.get(tier, "🎬")