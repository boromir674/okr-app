"""Key Results Container"""
from attr import define, field
import typing as t

from key_result_item import KeyResultItem


@define
class KeyResultsCard:
    """Container Card of Key Results belonging to an Objective.

    Args:
        st (Any): Streamlit session state object.
        key_results (list): A list of key result dictionaries, each containing
                            'id', 'description', and 'progress'.
    """
    st: t.Any = field()
    key_results: t.List[t.Dict[str, t.Any]] = field()

    def render(self):
        """
        Render the key results card.
        """
        for kr in self.key_results:
            key_result_item = KeyResultItem(self.st, kr)
            key_result_item.render()
