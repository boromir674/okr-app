"""Key Result Item V2"""
from attr import define, field, Factory
import typing as t


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
        ## END STATE ##

        # RENDER the Key Result Item text Description (no title exists in data model)
        # self.st.write(self.key_result['description'])
        
        # RENDER 3-column grid with '-', progress, '+' design
        col1, col2, col3 = self.st.columns([1, 4, 1])
        with col2:
            # render Static Progress bar
            progress = self.st.progress(
                value=int(self._get_progress_state()),
                text=f"Progress: {self._get_progress_state()}%",
                # key=f"progress_slider_{self._id}",
            )
        with col1:  # button with text '-'
            ''  # add empty components as a "hack" to "push" this element to the bottom
            ''
            ''
            if self.st.button("\-", key=f"minus_{self._id}", disabled=self._get_progress_state() <= 0):
                self._set_progress_state(self._get_progress_state() - self.STEP)
                # this not react: manually call re-run script to re-render given updated state
                self.st.rerun()
        with col3:
            ''  # add empty components to "push" this to the bottom
            ''
            ''
            if self.st.button("\+", key=f"plus_{self._id}", disabled=self._get_progress_state() >= 100):
                self._set_progress_state(self._get_progress_state() + self.STEP)
                # this not react: manually call re-run script to re-render given updated state
                self.st.rerun()
