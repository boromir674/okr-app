"""Key Result creation UI - Component"""

from attr import define, field, Factory
import typing as t
# import streamlit as st

## Main

@define
class KeyResultItemEditUI:
    """Single Key Result Item (form) creation UI component.

    Args:
        st (Any): Streamlit session state object.
        key_result (dict): Dictionary containing 'id'
    """
    st: t.Any = field()
    key_result: t.Dict[str, t.Any] = field(factory=dict)

    _id: int = field(init=False, repr=False, default=Factory(lambda self: self.key_result.get('id', 100), takes_self=True))
    """Serves as shortcut for internal consumption"""

    STEP: t.ClassVar[int] = 1

    def _set_progress_state(self, value: float):
        """Set the progress value in session state."""
        self.st.session_state[f'progress_value_{self._id}'] = value

    def _get_progress_state(self):
        """Get the progress value from session state."""
        return self.st.session_state[f'progress_value_{self._id}']

    def _set_progress_state_adapted(self, value_getter: t.Callable[[], bool]):
        self._set_progress_state(value_getter())

    # Min/Max Progress Value state management
    def _set_min_progress_state(self, value: int):
        """Set the min progress value in session state."""
        self.st.session_state[f'min_progress_value_{self._id}'] = value

    def _get_min_progress_state(self):
        """Get the min progress value from session state."""
        return self.st.session_state.get(f'min_progress_value_{self._id}', self.key_result.get("min_progress_value", 0))

    def _set_max_progress_state(self, value: int):
        """Set the max progress value in session state."""
        self.st.session_state[f'max_progress_value_{self._id}'] = value

    def _get_max_progress_state(self):
        """Get the max progress value from session state."""
        return self.st.session_state.get(f'max_progress_value_{self._id}', self.key_result.get("max_progress_value", 100))

    def _set_min_progress_state_adapted(self, value_getter: t.Callable[[], int]):
        """Set the min progress value in session state using a value getter."""
        self._set_min_progress_state(value_getter())

    def _set_max_progress_state_adapted(self, value_getter: t.Callable[[], int]):
        """Set the max progress value in session state using a value getter."""
        self._set_max_progress_state(value_getter())

    # KR Unit value state
    def set_unit_state(self, value: int):
        """Set the unit value in session state."""
        self.st.session_state[f'unit_value_{self._id}'] = value

    def _set_unit_state_adapted(self, value_getter: t.Callable[[], float]):
        """Set the unit value in session state using a value getter."""
        self.set_unit_state(value_getter())

    def render(self):
        """Render the Key Result creation UI."""

        ## STATE management ##
        if not f'progress_value_{self._id}' in self.st.session_state:
            self.st.session_state[f'progress_value_{self._id}'] = self.key_result.get("progress", 0)
        
        # Initialize min/max progress values in state
        if not f'min_progress_value_{self._id}' in self.st.session_state:
            self.st.session_state[f'min_progress_value_{self._id}'] = self.key_result.get("min_progress_value", 0)
        if not f'max_progress_value_{self._id}' in self.st.session_state:
            self.st.session_state[f'max_progress_value_{self._id}'] = self.key_result.get("max_progress_value", 100)
        ## END STATE ##

        ## RENDER UI, accepting input in different forms ##
        
        # RENDER Description Text Input
        kr_short_description = self.st.text_input(
            "Key Result Short Description",
            value=self.key_result.get("short_description", ''),
            key=f"new_kr_short_description_{self._id}"
        )

        # RENDER Description Text Input Area
        kr_description = self.st.text_area("Key Result Description", value='', key=f"new_kr_description_{self._id}")
        
        # RENDER Min Progress Value Input
        self.st.markdown("### Progress Tracking Bounds")
        col1, col2 = self.st.columns(2)
        
        with col1:
            min_val = self._get_min_progress_state()
            kr_min_progress = self.st.number_input(
                "Minimum Progress Value",
                min_value=0,
                value=min_val,
                step=1,
                key=f"new_kr_min_progress_{self._id}",
                on_change=self._set_min_progress_state_adapted,
                args=(lambda: self.st.session_state[f"new_kr_min_progress_{self._id}"],),
                help="Starting value for progress tracking (must be >= 0)"
            )
        
        with col2:
            max_val = self._get_max_progress_state()
            min_val_for_max = self._get_min_progress_state()
            kr_max_progress = self.st.number_input(
                "Maximum Progress Value",
                min_value=min_val_for_max + 1,  # Ensure max > min
                value=max(max_val, min_val_for_max + 1),  # Ensure valid value
                step=1,
                key=f"new_kr_max_progress_{self._id}",
                on_change=self._set_max_progress_state_adapted,
                args=(lambda: self.st.session_state[f"new_kr_max_progress_{self._id}"],),
                help="Target value for progress tracking (must be > min value)"
            )
        
        # Validation feedback
        if kr_min_progress >= kr_max_progress:
            self.st.error("⚠️ Maximum progress value must be greater than minimum progress value!")
        
        # Render unit input field with validation
        self.st.markdown("### Progress Unit Configuration")
        progress_range = kr_max_progress - kr_min_progress
        max_reasonable_unit = max(1, progress_range // 10)  # Reasonable step size
        
        units_value_to_render = self.st.session_state.get(f'unit_value_{self._id}', self.key_result.get("unit", 1))
        kr_unit = self.st.number_input(
            "Unit Step Size:",
            min_value=1,
            max_value=max_reasonable_unit,
            value=min(units_value_to_render, max_reasonable_unit),
            step=1,
            on_change=self._set_unit_state_adapted,
            args=(lambda: self.st.session_state.get(f"new_kr_unit_input_{self._id}", self.key_result.get("unit", 1)),),
            key=f"new_kr_unit_input_{self._id}",
            help=f"Step size for progress updates (1 to {max_reasonable_unit})"
        )
        
        # RENDER Progress Slider with dynamic bounds and step
        self.st.markdown("### Current Progress")
        current_progress = self.st.session_state.get(f'progress_value_{self._id}', kr_min_progress)
        
        # Ensure current progress is within bounds
        if current_progress < kr_min_progress:
            current_progress = kr_min_progress
            self.st.session_state[f'progress_value_{self._id}'] = current_progress
        elif current_progress > kr_max_progress:
            current_progress = kr_max_progress  
            self.st.session_state[f'progress_value_{self._id}'] = current_progress
        
        kr_progress = self.st.slider(
            "Current Progress",
            min_value=int(kr_min_progress),
            max_value=int(kr_max_progress),
            value=int(current_progress),
            step=int(kr_unit),
            key=f"new_kr_progress_{self._id}",
            on_change=self._set_progress_state_adapted,
            args=(lambda: self.st.session_state[f'new_kr_progress_{self._id}'],),
            help=f"Current progress between {kr_min_progress} and {kr_max_progress}"
        )
        
        # Show percentage calculation
        if kr_max_progress > kr_min_progress:
            percentage = ((kr_progress - kr_min_progress) / (kr_max_progress - kr_min_progress)) * 100
            self.st.info(f"📊 Progress: **{percentage:.1f}%** ({kr_progress} / {kr_max_progress})")
        
        # RENDER Metric Input
        kr_metric = self.st.text_input("Metric (Optional)", key=f"new_kr_metric_{self._id}")

        return [kr_description, kr_progress, kr_metric, kr_unit, kr_short_description, kr_min_progress, kr_max_progress]
