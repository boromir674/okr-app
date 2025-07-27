import typing as t
# from attr import define, Field
from collections import OrderedDict


# @define
class ObjectivesState:

    def __init__(self, objectives: t.List[t.Dict[str, t.Any]]):
        """Initialize the ObjectivesState with a list of objectives.

        Args:
            objectives (List[Dict[str, Any]]): List of objectives, each containing 'id', 'name', 'description', and 'key_results'.
        """
        self.objectives = objectives
        self._state = OrderedDict()
        self._obj_ids_2_data = OrderedDict()
        self.__attrs_post_init__()

    # objectives = Field()
    # _state = Field(init=False, factory=OrderedDict)
    
    # _obj_ids_2_data = Field(init=False, factory=OrderedDict)

    def __attrs_post_init__(self):
        for obj in self.objectives:
            self._obj_ids_2_data[obj['id']] = obj
            self._state[f"objective_{obj['id']}_name"] = obj.get("name", "")
            self._state[f"objective_{obj['id']}_description"] = obj.get("description", "")
            for kr in obj.get("key_results", []):
                # Short Description
                self._state[f"objective_{obj['id']}_key_result_{kr['id']}_{'short_description'}"] = kr.get("short_description", "")
                # Description
                self._state[f"objective_{obj['id']}_key_result_{kr['id']}_{'description'}"] = kr.get("description", "")

    def __iter__(self):
        """Iterate over objectives."""
        for key, objective_dict in self._obj_ids_2_data.items():
            yield key, objective_dict

    def get_objective_state(self, objective_id, field):
        """Get the state value for a specific Objective field."""
        return self._state.get(f"objective_{objective_id}_{field}", "")

    def set_objective_state(self, objective_id, field, value):
        """Set the state value for a specific Objective field."""
        self._state[f"objective_{objective_id}_{field}"] = value
    
    def get_key_result_state(self, objective_id, key_result_id, field):
        """Get the state value for a specific Key Result field."""
        return self._state.get(f"objective_{objective_id}_key_result_{key_result_id}_{field}", "")

    def set_key_result_state(self, objective_id, key_result_id, field, value):
        """Set the state value for a specific Key Result field."""
        self._state[f"objective_{objective_id}_key_result_{key_result_id}_{field}"] = value

    def iter_state(self) -> t.Iterator[t.Tuple[str, str]]:
        """Iterate over the state dictionary.
        
        Example Usage with next:
            >>> state = ObjectivesState(objectives=[...])
            >>> next(state.iter_state())
            ('objective_1_key_result_1_short_description', 'Initial Short Description')
        """
        for key, value in self._state.items():
            yield key, value

    def set_objective_name_state_adapted(self, objective_id: int, name_getter: t.Callable[[], str]):
        """Set the name state for a specific Objective using a getter."""
        objective_name: str = name_getter()
        self.set_objective_state(objective_id, "name", objective_name)
        self._obj_ids_2_data[objective_id]['name'] = objective_name

    def set_objective_description_state_adapted(self, objective_id: int, description_getter: t.Callable[[], str]):
        """Set the description state for a specific Objective using a getter."""
        description: str = description_getter()
        self.set_objective_state(objective_id, "description", description)
        self._obj_ids_2_data[objective_id]['description'] = description
