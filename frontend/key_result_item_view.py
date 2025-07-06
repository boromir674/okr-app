"""Key Result Item in View mode"""
from attr import define, field, Factory
import typing as t
import requests
import json


## Helpers

def set_edit_mode_state(self, kr_id: int, value: bool):
    """Set the edit mode state in session state."""
    self.st.session_state[f'edit_{kr_id}'] = value


## Main

from streamlit import toggle


@define
class KeyResultItemView:
    """Single Key Result Item in View Mode.

    Args:
        st (Any): Streamlit session state object.
        key_result (dict): Dictionary containing
                            'id', 'description', and 'progress'.
    """
    st: t.Any = field()
    key_result: t.Dict[str, t.Any] = field()

    _id: int = field(init=False, repr=False, default=Factory(lambda self: self.key_result['id'], takes_self=True))
    """Serves as shortcut for internal consumption"""

    def set_progress_state(self, kr_id: int, value: float):
        """Set the progress value in session state."""
        self.st.session_state[f'progress_value_{kr_id}'] = value

    def _set_edit_mode_state(self, kr_id: int, value: bool):
        """Set the edit mode state in session state."""
        self.st.session_state[f'edit_{kr_id}'] = value


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
            on_change=self._set_edit_mode_state,
            args=(self.key_result['id'], self.st.session_state[f'toggle_{self._id}']),
            label_visibility="collapsed",
        )


    def render(self):
        """
        Render the sinlge key result item in View Mode.
        """
        # value to use for next render, use state value since this takes into account slider movement (regardless of whether it was persisted (yet))
        progress_bar_value = self.st.session_state.get(f'progress_value_{self._id}', self.key_result["progress"])
        # RENDER PROGRESS BAR
        return [self._create_progress(
            value=int(progress_bar_value),
            text=f'Progress: {progress_bar_value}%' if progress_bar_value is not None else None,
        )]

    def _create_progress(self, value, text=None):
        r"""Display a progress bar.

        Parameters
        ----------
        value : int or float
            0 <= value <= 100 for int

            0.0 <= value <= 1.0 for float

        text : str or None
            A message to display above the progress bar. The text can optionally
            contain GitHub-flavored Markdown of the following types: Bold, Italics,
            Strikethroughs, Inline Code, Links, and Images. Images display like
            icons, with a max height equal to the font height.

            Unsupported Markdown elements are unwrapped so only their children
            (text contents) render. Display unsupported elements as literal
            characters by backslash-escaping them. E.g.,
            ``"1\. Not an ordered list"``.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown

        width : "stretch" or int
            The width of the progress element. This can be one of the following:

            - ``"stretch"`` (default): The width of the element matches the
              width of the parent container.
            - An integer specifying the width in pixels: The element has a
              fixed width. If the specified width is greater than the width of
              the parent container, the width of the element matches the width
              of the parent container.

        Example
        -------
        Here is an example of a progress bar increasing over time and disappearing when it reaches completion:

        >>> import streamlit as st
        >>> import time
        >>>
        >>> progress_text = "Operation in progress. Please wait."
        >>> my_bar = st.progress(0, text=progress_text)
        >>>
        >>> for percent_complete in range(100):
        ...     time.sleep(0.01)
        ...     my_bar.progress(percent_complete + 1, text=progress_text)
        >>> time.sleep(1)
        >>> my_bar.empty()
        >>>
        >>> st.button("Rerun")

        .. output::
           https://doc-status-progress.streamlit.app/
           height: 220px

        """
        self.st.progress(
            value=value,
            text=text,
            # width="stretch",
        )
