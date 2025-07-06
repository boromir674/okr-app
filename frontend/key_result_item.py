"""Key Result Item"""
from attr import define, field, Factory
import typing as t
import requests
import json
import os

from key_result_item_view import KeyResultItemView
from key_result_item_edit import KeyResultItemEdit

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

def get_progress_bar_value(st: t.Any, kr_id: int) -> float:
    """Get the progress bar value from session state."""
    return st.session_state.get(f'progress_slider_{kr_id}', 0.0)


def set_progress_state(self, kr_id: int, value: float):
    """Set the progress value in session state."""
    self.st.session_state[f'progress_value_{kr_id}'] = value

def set_edit_mode_state(self, kr_id: int, value: bool):
    """Set the edit mode state in session state."""
    self.st.session_state[f'edit_{kr_id}'] = value


## Main

@define
class KeyResultItem:
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

    def _set_edit_mode_state(self, value: bool):
        """Set the edit mode state in session state."""
        self.st.session_state[f'edit_{self._id}'] = value

    def set_progress_state(self, kr_id: int, value: float):
        """Set the progress value in session state."""
        self.st.session_state[f'progress_value_{kr_id}'] = value

    def _get_progress_state(self, kr_id: int, value = None):
        """Get the progress value from session state."""
        return self.st.session_state.get(f'progress_value_{kr_id}', value)

    def render(self):
        """
        Render the sinlge key result item.
        """
        ## STATE management ##
        if not f'progress_value_{self._id}' in self.st.session_state:
            self.st.session_state[f'progress_value_{self._id}'] = self.key_result["progress"]

        if not f'edit_{self._id}' in self.st.session_state:  # at first we are in View Mode
            self.st.session_state[f'edit_{self._id}'] = False
        if not f'toggle_{self._id}' in self.st.session_state:
            self.st.session_state[f'toggle_{self._id}'] = False
        ## END STATE ##

        # value to use for next render
        progress_bar_value = self.st.session_state[f'progress_value_{self._id}']

        # RENDER the Key Result Item text Description (no title exists in data model)
        self.st.write(self.key_result['description'])

        ## EDIT MODE
        if self.st.session_state[f'edit_{self._id}']:
            key_result_item = KeyResultItemEdit(self.st, self.key_result)
            key_result_item.render()             

            put_key_results = create_put_key_results_callback({
                'progress': self._get_progress_state(self._id, progress_bar_value),  # use value from session state, where potentially user changes (through interactive UI) come
                'kr_id': self.key_result['id']
            })
            if self.st.button(f"Save Progress", key=f"update_{self.key_result['id']}"):
                update_response = put_key_results()
                if update_response.status_code == 200:
                    self.st.success("Progress updated successfully!")

                    self._set_edit_mode_state(False)  # switch back to View Mode

                    # maybe below can be modified so that the render function retunrs the objects that we can delete on-by-one, otherwise we are getting collisoin on the slider_:id" pattern on session_state dict !
                    # del key_result_item
                    # key_result_item = KeyResultItemEdit(self.st, self.key_result)
                    # key_result_item.render()
                    
                    # manually call re-run script !
                    self.st.rerun()
                else:
                    self.st.error(f"Failed to update progress: {update_response.status_code}")

        ## VIEW MODE
        else:
            key_result_item = KeyResultItemView(self.st, self.key_result)
            # 2 columns where left column is 5:1 ratio in width to the right column
            cols = self.st.columns([5, 1])
            # render progress bar in left column
            with cols[0]:
                elements = key_result_item.render()
            with cols[1]:
                toggle = self._create_toggle()
                # manually call re-run script !
                # if toggle:
                #     self.st.rerun()



    def _create_toggle(self):
        r"""Display a toggle widget.

        Parameters
        ----------
        label : str
            A short label explaining to the user what this toggle is for.
            The label can optionally contain GitHub-flavored Markdown of the
            following types: Bold, Italics, Strikethroughs, Inline Code, Links,
            and Images. Images display like icons, with a max height equal to
            the font height.

            Unsupported Markdown elements are unwrapped so only their children
            (text contents) render. Display unsupported elements as literal
            characters by backslash-escaping them. E.g.,
            ``"1\. Not an ordered list"``.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            For accessibility reasons, you should never set an empty label, but
            you can hide it with ``label_visibility`` if needed. In the future,
            we may disallow empty labels by raising an exception.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown

        value : bool
            Preselect the toggle when it first renders. This will be
            cast to bool internally.

        key : str or int
            An optional string or integer to use as the unique key for the widget.
            If this is omitted, a key will be generated for the widget
            based on its content. No two widgets may have the same key.

        help : str or None
            A tooltip that gets displayed next to the widget label. Streamlit
            only displays the tooltip when ``label_visibility="visible"``. If
            this is ``None`` (default), no tooltip is displayed.

            The tooltip can optionally contain GitHub-flavored Markdown,
            including the Markdown directives described in the ``body``
            parameter of ``st.markdown``.

        on_change : callable
            An optional callback invoked when this toggle's value changes.

        args : tuple
            An optional tuple of args to pass to the callback.

        kwargs : dict
            An optional dict of kwargs to pass to the callback.

        disabled : bool
            An optional boolean that disables the toggle if set to ``True``.
            The default is ``False``.

        label_visibility : "visible", "hidden", or "collapsed"
            The visibility of the label. The default is ``"visible"``. If this
            is ``"hidden"``, Streamlit displays an empty spacer instead of the
            label, which can help keep the widget aligned with other widgets.
            If this is ``"collapsed"``, Streamlit displays no label or spacer.

        width : "content", "stretch", or int
            The width of the toggle widget. This can be one of the following:

            - ``"content"`` (default): The width of the widget matches the
              width of its content, but doesn't exceed the width of the parent
              container.
            - ``"stretch"``: The width of the widget matches the width of the
              parent container.
            - An integer specifying the width in pixels: The widget has a
              fixed width. If the specified width is greater than the width of
              the parent container, the width of the widget matches the width
              of the parent container.

        Returns
        -------
        bool
            Whether or not the toggle is checked.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> on = st.toggle("Activate feature")
        >>>
        >>> if on:
        ...     st.write("Feature activated!")

        .. output::
           https://doc-toggle.streamlit.app/
           height: 220px

        """
        return self.st.toggle(
            label="Edit",
            value=self.st.session_state.get(f'edit_{self._id}', False),
            key=f'toggle_{self._id}',
            # set the bar value in edit_ session variable which should control top-level component rendering logic.. same value as "this" (f'toggle_{self._id}')
            on_change=self._set_edit_mode_state_adapted,
            args=(lambda: self.st.session_state[f'toggle_{self._id}'],),
            label_visibility="collapsed",
        )

    def _set_edit_mode_state_adapted(self, value_getter: t.Callable[[], bool]):
        """Set the edit mode state in session state using a value getter."""
        self._set_edit_mode_state(value_getter())
