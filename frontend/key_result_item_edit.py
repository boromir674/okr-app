"""Key Result Item in Edit mode"""
from attr import define, field, Factory
import typing as t


## Main

@define
class KeyResultItemEdit:
    """Single Key Result Item in Edit Mode.

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

    def set_progress_state(self, kr_id: int, value: float):
        """Set the progress value in session state."""
        self.st.session_state[f'progress_value_{kr_id}'] = value

    def set_progress_state_adapted(self, kr_id: int, value_getter: t.Callable[[], float]):
        """Set the progress value in session state using a value getter."""
        self.set_progress_state(kr_id, value_getter())

    def render(self):
        """
        Render the sinlge key result item in Edit Mode.
        """
        # value to use for next render, use state value since this takes into account slider movement (regardless of whether it was persisted (yet))
        progress_bar_value = self.st.session_state.get(f'progress_value_{self._id}', self.key_result["progress"])

        # self.st.write(self.key_result['description'])
        # 3-column grid with '-', progress, '+' design
        # col 1 and 2 have very small buttons that "fit" text length
        col1, col2, col3 = self.st.columns([1, 4, 1])
        with col2:
            # render Interactive slider
            progress = self.st.slider(
                f"Progress:",
                min_value=0,
                max_value=100,
                value=int(progress_bar_value),
                step=KeyResultItemEdit.STEP,

                on_change=self.set_progress_state_adapted,
                args=(self.key_result['id'], lambda: self.st.session_state.get(f"progress_slider_{self._id}", self.key_result["progress"])),

                key=f"progress_slider_{self._id}",
            )
        with col1:  # button with text '-'
            ''  # add empty components as a "hack" to "push" this element to the bottom
            ''
            ''
            if self.st.button("\-", key=f"minus_{self.key_result['id']}", disabled=progress <= 0):
                # self.st.session_state[f'progress_value_{self._id}'] = progress - STEP
                self.set_progress_state(self.key_result['id'], progress - KeyResultItemEdit.STEP)
                # this not react: manually call re-run script to re-render given updated state
                self.st.rerun()
        with col3:
            ''  # add empty components to "push" this to the bottom
            ''
            ''
            if self.st.button("\+", key=f"plus_{self.key_result['id']}", disabled=progress >= 100):
                self.set_progress_state(self.key_result['id'], progress + KeyResultItemEdit.STEP)
                # this not react: manually call re-run script to re-render given updated state
                self.st.rerun()
        return [progress]
