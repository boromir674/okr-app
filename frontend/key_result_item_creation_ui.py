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
        ## END STATE ##

        # RENDER UI, accepting input in different forms
        kr_description = self.st.text_area("Key Result Description", value='', key=f"new_kr_description_{self._id}")
        kr_progress = self.st.slider(
            "Progress", min_value=0, max_value=100, step=self.STEP, value=self._get_progress_state(), key=f"new_kr_progress_{self._id}",

            # use same key to report this to another sharable state variable
            on_change=self._set_progress_state_adapted,
            args=(lambda: self.st.session_state[f'new_kr_progress_{self._id}'],),
        )
        kr_metric = self.st.text_input("Metric (Optional)", key=f"new_kr_metric_{self._id}")

        # Render unit input field
        # value to use for next render, use state value since this takes into account units value set in ui (regardless of whether it was persisted (yet))
        units_value_to_render = self.st.session_state.get(f'unit_value_{self._id}', self.key_result.get("unit", 1))
        kr_unit = self.st.number_input(
            "Unit (Optional):",
            min_value=1,
            max_value=99,
            value=units_value_to_render,
            step=1,
            on_change=self._set_unit_state_adapted,
            args=(lambda: self.st.session_state.get(f"new_kr_unit_input_{self._id}", self.key_result.get("unit", 1)),),

            key=f"new_kr_unit_input_{self._id}",
        )

        return [kr_description, kr_progress, kr_metric, kr_unit]
