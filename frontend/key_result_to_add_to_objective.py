"""Key Result Item selected for being added to an Objective."""

from attr import define, field, Factory
import typing as t
import requests
import json
import os


## Helpers

BASE_URL = os.environ['OKR_BACKEND_URL']


class KRUpdateDate(t.TypedDict):
    progress: float
    kr_id: int


def create_put_key_results_callback(data: KRUpdateDate):

    def put_key_results():
        payload = {"progress": data['progress']}
        update_response = requests.put(
            f"{BASE_URL}/key_results/{data['kr_id']}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        return update_response
    return put_key_results



## Main

@define
class KeyResultItemSelectedForObjectiveUnderConstruction:
    """Single Key Result Item, selected to be added to a new Objective when created.

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

        # DESIGN: box with 2 columns: 1st is Description 2/5 , 2nd is progress 3/5
        
        c1, c2 = self.st.columns([2, 3])
        # RENDER the Key Result Item text Description (no title exists in data model)
        with c1:
            self.st.write(self.key_result['description'])
        with c2:

            # RENDER Interactive slider
            progress = self.st.slider(
                f"Progress:",
                min_value=0,
                max_value=100,
                # progress bar value from session state
                value=int(self._get_progress_state()),
                step=self.STEP,

                on_change=self._set_progress_state_adapted,
                args=(lambda: self.st.session_state.get(f"progress_slider_obj_crud_{self._id}", self._get_progress_state())),

                key=f"progress_slider_obj_crud_{self._id}",
            )

    def _set_progress_state_adapted(self, value_getter: t.Callable[[], float]):
        """Set the progress value in session state using a value getter."""
        self._set_progress_state(self._id, value_getter())
