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
        with col3:
            ''
            ''
            ''
            if self.st.button("\+", key=f"plus_{self._id}", disabled=self._get_progress_state() >= 100):
                
                # Render a Toast notification !! to Celebrate the progress !!!!
                # st.toast(body, *, icon=None))
                self.st.toast(f"Bravo re malaka 🎉 ({self._get_progress_state()}%) 🎉", icon="✅")
                time.sleep(4)
                # Simulate a delay for the animation effect
                
                # Update State variables
                self._set_progress_state(self._get_progress_state() + self.STEP)
                self.st.session_state[f'should_animate_{self._id}'] = True
                # Re-render instruction
                self.st.rerun()
                assert 1 == 0  # never runs 


        # RENDER celebration 🎉 emoticons based on progress percentage (10th percentile rounded-up for integer!)
        celebration_count = int((self._get_progress_state() + 9) // 10)
        self.st.write("🎉" * celebration_count)
