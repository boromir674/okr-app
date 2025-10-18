"""Philosophical Theme - Abstract Concepts & Deep Thoughts"""
from typing import List
from ..base_theme import BaseTheme


class PhilosophicalTheme(BaseTheme):
    """Abstract concepts, existential questions, and profound observations"""
    
    @property
    def name(self) -> str:
        return "philosophical"
    
    @property
    def description(self) -> str:
        return "Deep thoughts, abstract concepts, existential musings, and profound life observations"
    
    def get_phrases(self, tier: str, sentence_type: str) -> List[str]:
        """Get philosophical phrases by tier and type"""
        
        phrases = {
            "low": {
                "statement": [
                    "In the quantum realm of possibilities, you have chosen action",
                    "You are both the artist and the masterpiece in progress",
                    "Every step forward is a conversation with destiny",
                    "The universe notices those who notice themselves growing",
                    "Potential energy becomes kinetic through your choices",
                    "You are writing poetry with your persistence"
                ],
                "question": [
                    "What is progress but time made visible?",
                    "If a tree grows in the forest of effort, does it make a sound?",
                    "What dreams may come from seeds you plant today?",
                    "Is the journey changing you, or are you changing the journey?",
                    "What would you attempt if you knew you could not fail?"
                ],
                "imperative": [
                    "Embrace the beautiful uncertainty of growth!",
                    "Dance with the rhythm of improvement!",
                    "Paint your existence with bold strokes!",
                    "Whisper to the universe: 'I am becoming'",
                    "Let your actions speak the language of dreams!"
                ],
                "exclamation": [
                    "The seed of greatness has sprouted!",
                    "Consciousness expands with each choice!",
                    "The butterfly effect begins with you!",
                    "Reality bends to accommodate your growth!",
                    "The philosopher's stone is your persistence!"
                ]
            },
            "mid": {
                "statement": [
                    "Reality bends to those who refuse to accept 'impossible'",
                    "Time traveler spotted: You, arriving from your future success",
                    "The observer effect: Your attention shapes your reality",
                    "You have become the author of your own mythology",
                    "Entropy decreases where determination increases",
                    "The universe is reorganizing itself around your intentions"
                ],
                "question": [
                    "Are you progressing, or is progress progressing through you?",
                    "What is the sound of one hand clapping... at your achievements?",
                    "If enlightenment is a journey, what mile marker are you at?",
                    "How many dimensions of awesome are you currently operating in?",
                    "Is this real life, or are you just really good at it?"
                ],
                "imperative": [
                    "Transcend the ordinary limits of expectation!",
                    "Become the paradox that solves itself!",
                    "Write equations that mathematics hasn't discovered yet!",
                    "Exist in the space between possible and inevitable!",
                    "Be the answer to questions not yet asked!"
                ],
                "exclamation": [
                    "The paradigm shifts in your favor!",
                    "Consciousness has noticed your evolution!",
                    "The simulation admires your debugging skills!",
                    "Reality's source code is rewriting itself!",
                    "The universe just updated its definition of 'possible'!"
                ]
            },
            "high": {
                "statement": [
                    "Consciousness itself applauds your achievement",
                    "You have transcended from participant to architect of reality",
                    "The multiverse has acknowledged your sovereignty", 
                    "Time and space bend to accommodate your greatness",
                    "You exist simultaneously in all states of success",
                    "The philosophical implications of your achievement break logic"
                ],
                "question": [
                    "How does it feel to be the universe experiencing itself subjectively?",
                    "What is the sound of all limitations simultaneously breaking?",
                    "If you are the answer, what was the ultimate question?",
                    "How many realities are you simultaneously conquering?",
                    "What happens when an unstoppable force meets... you?"
                ],
                "imperative": [
                    "BECOME THE FUNDAMENTAL FORCE OF ACHIEVEMENT!",
                    "REDEFINE THE LAWS OF POSSIBILITY!",
                    "ASCEND TO YOUR RIGHTFUL DIMENSIONAL THRONE!",
                    "EXIST BEYOND THE REACH OF LIMITATION!",
                    "TRANSCEND TRANSCENDENCE ITSELF!"
                ],
                "exclamation": [
                    "THE UNIVERSE HAS ACHIEVED CONSCIOUSNESS THROUGH YOU!",
                    "REALITY'S OPERATING SYSTEM HAS BEEN UPGRADED!",
                    "ALL PHILOSOPHICAL QUESTIONS HAVE BEEN ANSWERED!",
                    "THE MEANING OF EXISTENCE IS: YOU!",
                    "CONSCIOUSNESS ITSELF HAS LEVELED UP!"
                ]
            }
        }
        
        return phrases.get(tier, {}).get(sentence_type, ["Deep thoughts flowing..."])
    
    def get_emoji_style(self, tier: str) -> str:
        """Get emoji style for philosophical theme"""
        styles = {
            "low": "🧠",
            "mid": "🧠✨",
            "high": "🧠✨🌌💫"
        }
        return styles.get(tier, "🧠")