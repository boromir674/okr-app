"""Key Result Item V2"""
from attr import define, field, Factory
import typing as t
import streamlit as st
import time
import math
import random

@define
class KeyResultItemV2:
    """Single Key Result Item.

    Args:
        st (Any): Streamlit session state object.
        key_result (dict): Dictionary containing
                            'id', 'description', and 'progress'.
    """
    st: t.Any = field()
    key_result: t.Dict[str, t.Any] = field()

    _id: int = field(init=False, repr=False, default=Factory(lambda self: self.key_result['id'], takes_self=True))
    """Serves as shortcut for internal consumption"""

    STEP: t.ClassVar[int] = 1

    def _set_progress_state(self, value: float):
        """Set the progress value in session state."""
        self.st.session_state[f'progress_value_{self._id}'] = value

    def _get_progress_state(self):
        """Get the progress value from session state."""
        return self.st.session_state[f'progress_value_{self._id}']

    def _get_unit_state(self):
        """Get the unit value from session state."""
        return self.st.session_state[f'unit_value_{self._id}']


    def render(self):
        """
        Render the single key result item.
        """
        ## STATE management ##
        if not f'progress_value_{self._id}' in self.st.session_state:
            self.st.session_state[f'progress_value_{self._id}'] = self.key_result["progress"]
        if not f'should_animate_{self._id}' in self.st.session_state:
            self.st.session_state[f'should_animate_{self._id}'] = False
        ## END STATE ##

        # CSS for liquid fill animation
        if self.st.session_state[f'should_animate_{self._id}']:
            self.st.markdown(f"""
            <style>
            .progress-bar-{self._id} {{
                width: {self._get_progress_state()}%;
                height: 24px;
                background-color: #4caf50;
                border-radius: 12px;
                position: relative;
                overflow: hidden;
            }}
            .progress-bar-{self._id}::after {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                height: 100%;
                width: 100%;
                background: linear-gradient(90deg, rgba(0, 200, 255, 0.5), rgba(0, 200, 255, 0));
                animation: liquid-fill-{self._id} 1.5s ease-in-out infinite;
            }}
            @keyframes liquid-fill-{self._id} {{
                0% {{ transform: translateX(-100%); }}
                100% {{ transform: translateX(100%); }}
            }}
            .progress-container-{self._id} {{
                width: 100%;
                background-color: #f3f3f3;
                border-radius: 12px;
                overflow: hidden;
            }}
            </style>
            """, unsafe_allow_html=True)
        else:
            self.st.markdown(f"""
            <style>
            .progress-bar-{self._id} {{
                width: {self._get_progress_state()}%;
                height: 24px;
                background-color:
 #4caf50;
                border-radius: 12px;
            }}
            .progress-container-{self._id} {{
                width: 100%;
                background-color:
 #f3f3f3;
                border-radius: 12px;
                overflow: hidden;
            }}
            </style>
            """, unsafe_allow_html=True)

        ## RENDER POP-UP - retention hack ##
        # Show congratulatory message if in state
        if f'congratulations_{self._id}' in self.st.session_state:
            self.st.toast(self.st.session_state[f'congratulations_{self._id}'], icon="✅")

        # RENDER 3-column grid with '-', progress, '+' design
        col1, col2, col3 = self.st.columns([1, 4, 1])

        # Fetch unit value from session state
        unit = self._get_unit_state()

        with col1:  # button with text '-'
            ''
            ''
            ''
            if self.st.button("\-", key=f"minus_{self._id}", disabled=self._get_progress_state() <= 0):
                self._set_progress_state(max(self._get_progress_state() - unit, 0))
                self.st.rerun()
        with col2:
            # Render progress bar using custom HTML
            self.st.markdown(f"""
            <div class="progress-container-{self._id}">
                <div class="progress-bar-{self._id}"></div>
            </div>
            """, unsafe_allow_html=True)
        if self.st.session_state[f'should_animate_{self._id}'] == True:
            self.st.session_state[f'should_animate_{self._id}'] = False
            st.rerun()

        # Check if the congratulatory message should be cleared based on timestamp
        if f'congratulations_timestamp_{self._id}' in self.st.session_state:
            current_time = time.time()
            if current_time - self.st.session_state[f'congratulations_timestamp_{self._id}'] > 2:  # 2 seconds duration
                self.st.session_state.pop(f'congratulations_{self._id}', None)
                self.st.session_state.pop(f'congratulations_timestamp_{self._id}', None)

        with col3:
            ''
            ''
            ''
            if self.st.button("\+", key=f"plus_{self._id}", disabled=self._get_progress_state() >= 100):
                # Update progress state
                new_progress = min(self._get_progress_state() + unit, 100)
                self._set_progress_state(new_progress)

                # Show congratulatory message and store timestamp
                self.st.session_state[f'congratulations_{self._id}'] = f"Bravo! Progress updated to {new_progress}% 🎉"
                self.st.session_state[f'congratulations_timestamp_{self._id}'] = time.time()
                self.st.toast(self.st.session_state[f'congratulations_{self._id}'], icon="✅")

                # Trigger re-render for animation
                self.st.session_state[f'should_animate_{self._id}'] = True
                self.st.rerun()
                assert 1 == 0  # this never runs, but is here to illustrate that the re-rendering is necessary to show the updated state

        ## Dynamic Emoticon Rendering ##
        progress = self._get_progress_state()

        rewards = [
            "The journey begins, brave soul!",  # 0%
            "One step closer to greatness!",  # 1%
            "The spark of ambition ignites!",  # 2%
            "You have taken the first step, Frodo!",  # 3%
            "The road is long, but you are strong!",  # 4%
            "Every hero starts small, keep going!",  # 5%
            "You are forging your destiny, warrior!",  # 6%
            "The climb is steep, but you are relentless!",  # 7%
            "You are the spark that lights the fire!",  # 8%
            "The Fellowship is with you, keep moving!",  # 9%
            "You are the shield that guards the realms of men!",  # 10%
            "The path is clear, march forward!",  # 11%
            "You are the storm that breaks the silence!",  # 12%
            "The mountain trembles beneath your feet!",  # 13%
            "You are the sword that cuts through doubt!",  # 14%
            "The fire within you burns brighter!",  # 15%
            "You are the chosen one, keep going!",  # 16%
            "The winds of change are at your back!",  # 17%
            "You are the hammer that shapes the future!",  # 18%
            "The stars align for your victory!",  # 19%
            "Halfway to Mordor, keep pushing!",  # 20%
            "You are the roar that shakes the heavens!",  # 21%
            "The battle is fierce, but you are fiercer!",  # 22%
            "You are the beacon of hope in the darkness!",  # 23%
            "The dragon trembles before your might!",  # 24%
            "You are the flame that cannot be extinguished!",  # 25%
            "The world bends to your will, champion!",  # 26%
            "You are the thunder that rolls across the skies!",  # 27%
            "The summit is near, keep climbing!",  # 28%
            "You are the light that pierces the shadow!",  # 29%
            "The gates of victory are within sight!",  # 30%
            "You are the lion that leads the pride!",  # 31%
            "The realm sings of your deeds!",  # 32%
            "You are the phoenix rising from the ashes!",  # 33%
            "The earth shakes beneath your triumph!",  # 34%
            "You are the hero of this tale!",  # 35%
            "The drums of war beat in your favor!",  # 36%
            "You are the master of your fate!",  # 37%
            "The sword of destiny is in your hands!",  # 38%
            "You are the champion of champions!",  # 39%
            "The final stretch is near, keep going!",  # 40%
            "You are the wolf that leads the pack!",  # 41%
            "The fires of victory burn bright!",  # 42%
            "You are the conqueror of worlds!",  # 43%
            "The realm bows before your might!",  # 44%
            "You are the legend they will sing of!",  # 45%
            "The peak is within reach, keep pushing!",  # 46%
            "You are the titan that moves mountains!",  # 47%
            "The stars shine brighter for you!",  # 48%
            "You are the hero of this battlefield!",  # 49%
            "🌟 50% Reached! The realm salutes you!",  # 50%
            "You are the fire that cannot be quenched! 💪",  # 51%
            "The heavens roar in your honor! 💪",  # 52%
            "You are the unstoppable force! 💪",  # 53%
            "The world trembles at your triumph! 💪",  # 54%
            "You are the hero of this age! 💪",  # 55%
            "The summit is yours to claim! 💪",  # 56%
            "You are the thunder that shakes the skies! 💪",  # 57%
            "The final battle is near, keep going! 💪",  # 58%
            "You are the light that guides the way! 💪",  # 59%
            "The gates of victory open for you! 💪",  # 60%
            "You are the dragon that rules the skies! 💪",  # 61%
            "The realm sings of your glory! 💪",  # 62%
            "You are the champion of champions! 💪",  # 63%
            "The stars align for your triumph! 💪",  # 64%
            "You are the legend of this tale! 💪",  # 65%
            "The summit is yours to take! 💪",  # 66%
            "You are the phoenix that rises above all! 💪",  # 67%
            "The world bows before your might! 💪",  # 68%
            "You are the force that inspires greatness! 💪",  # 69%
            "💪 70% Reached! You are unstoppable!",  # 70%
            "The heavens sing of your deeds! 💪",  # 71%
            "You are the conqueror of realms! 💪",  # 72%
            "The stars shine brighter for you! 💪",  # 73%
            "You are the master of this domain! 💪",  # 74%
            "The final victory is near, keep pushing! 💪",  # 75%
            "You are the titan that rules the earth! 💪",  # 76%
            "The realm bows before your triumph! 💪",  # 77%
            "You are the hero of heroes! 💪",  # 78%
            "The gates of glory open for you! 💪",  # 79%
            "🔥 80% Reached! You are a legend!",  # 80%
            "🌟 The summit is yours to claim!",  # 81%
            "🏆 The realm celebrates your victory!",  # 82%
            "✨ You are the light that shines forever!",  # 83%
            "🎉 You are the champion of champions!",  # 84%
            "🎊 The stars sing of your triumph!",  # 85%
            "🎈 You are the force that inspires greatness!",  # 86%
            "🥳 You are the hero of this age!",  # 87%
            "💯 You are the legend of legends!",  # 89%
            "🏆 100% Reached! You are the ruler of all!",  # 100%
        ]

        # Render rewards based on progress
        reward_index = min(int(progress), len(rewards) - 1)
        self.st.markdown(f"""
        <div style="text-align: center; font-size: 24px;">
            {rewards[reward_index]}
        </div>
        """, unsafe_allow_html=True)
