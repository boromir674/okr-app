"""Key Result Item in view mode, with clickable progress bar's +1/-1 buttons

Should be rendered in the main Dashboard UI.
"""
import typing as t
import time

from attr import define, field, Factory
import streamlit as st


@define
class KeyResultItemView:
    """Key Result Item in view mode, with clickable progress bar's +1/-1 buttons

    Should be rendered in the main app Dashboard UI.

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

    def _get_motivational_quote(self):
        """Get the motivational quote from session state."""
        return self.st.session_state[f'motivational_phrase_{self._id}']
    
    def _set_motivational_quote(self, value: str):
        """Set the motivational quote in session state."""
        self.st.session_state[f'motivational_phrase_{self._id}'] = value

    def _calculate_percentage(self, progress_value=None, min_val=None, max_val=None):
        """Calculate percentage based on min/max range."""
        if progress_value is None:
            progress_value = self._get_progress_state()
        if min_val is None:
            min_val = float(self.key_result.get('min_progress_value', 0))
        if max_val is None:
            max_val = float(self.key_result.get('max_progress_value', 100))
            
        if max_val > min_val:
            percentage = ((progress_value - min_val) / (max_val - min_val)) * 100
            return max(0, min(100, percentage))  # Clamp between 0-100%
        return 0
    
    def _get_display_percentage(self):
        """Get the display percentage for the progress bar."""
        return self._calculate_percentage()


    def render(self):
        """
        Render the single key result item.
        """
        ## STATE management ##
        if not f'progress_value_{self._id}' in self.st.session_state:
            # Store the original progress value for calculations
            self.st.session_state[f'progress_value_{self._id}'] = self.key_result.get("original_progress", self.key_result.get("progress", 0))

        
        if not f'unit_value_{self._id}' in self.st.session_state:
            # Store the unit/step value for increments
            self.st.session_state[f'unit_value_{self._id}'] = self.key_result.get("step", self.STEP)
        
        if not f'should_animate_{self._id}' in self.st.session_state:
            self.st.session_state[f'should_animate_{self._id}'] = False

        # Use the calculated percentage for dynamic phrase generation
        progress_percentage = self._get_display_percentage()

        # on first "render" generate a quote and save to state, that way on re-render same quote can be reused
        if not f'motivational_phrase_{self._id}' in self.st.session_state:
            self.st.session_state[f'motivational_phrase_{self._id}'] = self._generate_motivational_phrase(progress_percentage)
        ## END STATE ##

        # Get progress range information as local variables
        min_progress = float(self.key_result.get("min_progress_value", 0))
        max_progress = float(self.key_result.get("max_progress_value", 100))
        current_progress = self.st.session_state[f'progress_value_{self._id}']

        # CSS for liquid fill animation
        if self.st.session_state[f'should_animate_{self._id}']:
            self.st.markdown(f"""
            <style>
            .progress-bar-{self._id} {{
                width: {self._get_display_percentage()}%;
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
                width: {self._get_display_percentage()}%;
                height: 24px;
                background-color: #4caf50;
                border-radius: 12px;
            }}
            .progress-container-{self._id} {{
                width: 100%;
                background-color: #f3f3f3;
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
            min_val = float(self.key_result.get('min_progress_value', 0))
            if self.st.button("\-", key=f"minus_{self._id}", disabled=self._get_progress_state() <= min_val):
                self._set_progress_state(max(self._get_progress_state() - unit, min_val))
                percentage = self._get_display_percentage()
                self._set_motivational_quote(self._generate_motivational_phrase(percentage))
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
            if current_time - self.st.session_state[f'congratulations_timestamp_{self._id}'] > 4:  # 2 seconds duration
                self.st.session_state.pop(f'congratulations_{self._id}', None)
                self.st.session_state.pop(f'congratulations_timestamp_{self._id}', None)

        with col3:
            ''
            ''
            ''
            max_val = float(self.key_result.get('max_progress_value', 100))
            if self.st.button("\+", key=f"plus_{self._id}", disabled=self._get_progress_state() >= max_val):
                # Update progress state
                self._set_progress_state(min(self._get_progress_state() + unit, max_val))

                percentage = self._get_display_percentage()
                # update motivational quote state
                self._set_motivational_quote(self._generate_motivational_phrase(percentage))
                self.st.session_state[f'congratulations_{self._id}'] = f"Bravo re malaka!!! Progress updated to {percentage:.1f}% 🎉"
                self.st.session_state[f'congratulations_timestamp_{self._id}'] = time.time()
                # Show congratulatory message with percentage
                self.st.toast(self.st.session_state[f'congratulations_{self._id}'], icon="✅")

                # Trigger re-render for animation
                self.st.session_state[f'should_animate_{self._id}'] = True
                self.st.rerun()
                assert 1 == 0  # this never runs, but is here to illustrate that the re-rendering is necessary to show the updated state

        ## Dynamic Themed Motivational Phrases ##
        
        # Render the dynamic phrase
        self.st.markdown(f"""
        <div style="text-align: center; font-size: 24px; margin: 10px 0; padding: 15px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 10px; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            {self.st.session_state[f'motivational_phrase_{self._id}']}
        </div>
        """, unsafe_allow_html=True)

    def _generate_motivational_phrase(self, percentage: float) -> str:
        """Generate dynamic motivational phrase using theme system"""
        from ..motivational_themes import MotivationalThemeManager
        
        # Initialize theme manager (could be cached as class variable in production)
        if not hasattr(self, '_theme_manager'):
            theme_manager = MotivationalThemeManager()
        
        return theme_manager.generate_phrase(percentage)
