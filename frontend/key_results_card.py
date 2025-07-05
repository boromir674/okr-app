"""Key Results Container"""
from attr import define, field
import typing as t
import requests
import json


## Helpers

BASE_URL = "http://backend:8000"


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
class KeyResultsCard:
    """Container of Key Results belonging to the same Objective.

    Args:
        st (Any): Streamlit session state object.
        key_results (list): A list of key result dictionaries, each containing
                            'id', 'description', and 'progress'.
    """
    st: t.Any = field()
    key_results: t.List[t.Dict[str, t.Any]] = field()

    STEP: t.ClassVar[int] = 1

    def set_progress_state(self, kr_id: int, value: float):
        """Set the progress value in session state."""
        self.st.session_state[f'progress_value_{kr_id}'] = value

    def render(self):
        """
        Render the key results card.
        """
        for kr in self.key_results:

            ## STATE management ##
            if not f'progress_value_{kr["id"]}' in self.st.session_state:
                self.st.session_state[f'progress_value_{kr["id"]}'] = kr["progress"]

            if not f'edit_{kr["id"]}' in self.st.session_state:  # at first we are in View Mode
                self.st.session_state[f'edit_{kr["id"]}'] = False

            # value to use for next render
            progress_bar_value = self.st.session_state[f'progress_value_{kr["id"]}']
            
            self.st.write(kr['description'])
            # 3-column grid with '-', progress, '+' design
            # col 1 and 2 have very small buttons that "fit" text length
            col1, col2, col3 = self.st.columns([1, 4, 1])
            with col2:
                if self.st.session_state[f'edit_{kr["id"]}']:  # Edit Mode
                    # If in edit mode, show slider
                    progress = self.st.slider(
                        f"Progress:",
                        min_value=0.0,
                        max_value=10.0,
                        value=progress_bar_value,
                        step=KeyResultsCard.STEP,
                    )
                else:  # View Mode
                    # If not in edit mode, show progress bar
                    self.st.progress(kr['progress'])
                    progress = kr['progress']
            with col1:  # button with text '-'
                ''  # add empty components as a "hack" to "push" this element to the bottom
                ''
                ''
                if self.st.button("\-", key=f"minus_{kr['id']}", disabled=progress <= 0.0):
                    # self.st.session_state[f'progress_value_{kr["id"]}'] = progress - STEP
                    self.set_progress_state(kr['id'], progress - KeyResultsCard.STEP)
            with col3:
                ''  # add empty components to "push" this to the bottom
                ''
                ''
                if self.st.button("\+", key=f"plus_{kr['id']}", disabled=progress >= 10.0):
                    self.set_progress_state(kr['id'], progress + KeyResultsCard.STEP)

                    # self.st.session_state[f'progress_value_{kr["id"]}'] = progress + STEP
                    # progress += STEP

            put_key_results = create_put_key_results_callback({
                'progress': progress,  # use value of Interactive slider
                'kr_id': kr['id']
            })
            if self.st.button(f"Save Progress", key=f"update_{kr['id']}"):
                update_response = put_key_results()
                if update_response.status_code == 200:
                    self.st.success("Progress updated successfully!")
                else:
                    self.st.error(f"Failed to update progress: {update_response.status_code}")
