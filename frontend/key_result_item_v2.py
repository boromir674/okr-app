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
        with col1:  # button with text '-'
            ''
            ''
            ''
            if self.st.button("\-", key=f"minus_{self._id}", disabled=self._get_progress_state() <= 0):
                self._set_progress_state(self._get_progress_state() - self.STEP)
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
                new_progress = self._get_progress_state() + self.STEP
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

        # Define a pool of random emojis for rewards
        emoji_pool = ["🎉", "🎊", "💪", "🔥", "🌟", "🏆", "✨", "🎈", "🥳"]

        if progress >= 100:
            # Render a celebratory animation for 100% progress
            self.st.markdown("""
            <div style="text-align: center; font-size: 48px; animation: bounce 1s infinite;">
                🎉🎊💯
            </div>
            <style>
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            </style>
            """, unsafe_allow_html=True)
        elif progress >= 80:
            # Render a "muscle" emoji for high progress
            self.st.markdown(f"""
            <div style="text-align: center; font-size: 36px;">
                💪 Great job! {progress}% completed!
            </div>
            """, unsafe_allow_html=True)
        else:
            # Scale "party popper" emoji based on progress percentage with smaller baseline
            size = int(12 + (progress / 100) * 24)  # Scale size between 12px and 36px
            random_emoji = random.choice(emoji_pool)  # Pick a random emoji from the pool
            self.st.markdown(f"""
            <div style="text-align: center; font-size: {size}px;">
                {random_emoji * (progress // 10)} {progress}% completed!
            </div>
            """, unsafe_allow_html=True)
