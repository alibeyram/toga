from travertino.size import at_least

from toga_android.keys import toga_key

from ..libs.android.text import InputType, TextWatcher
from ..libs.android.view import (
    Gravity,
    OnKeyListener,
    View__MeasureSpec,
    View__OnFocusChangeListener,
)
from ..libs.android.widget import EditText
from .label import TextViewWidget


class TogaTextWatcher(TextWatcher):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def beforeTextChanged(self, _charSequence, _start, _count, _after):
        pass

    def afterTextChanged(self, _editable):
        self.interface.on_change(None)
        self.interface._validate()

    def onTextChanged(self, _charSequence, _start, _before, _count):
        pass


class TogaKeyListener(OnKeyListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def onKey(self, _view, _key, _event):
        event_info = toga_key(_event)
        if event_info is None:
            pass  # pragma: nocover
        else:
            key_pressed = event_info["key"].value
            if (key_pressed == "<enter>" or key_pressed == "numpad:enter") and (
                int(_event.getAction()) == 1
            ):
                self.interface.on_confirm(None)
        return False


class TogaFocusListener(View__OnFocusChangeListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def onFocusChange(self, view, has_focus):
        if has_focus:
            self.interface.on_gain_focus(None)
        else:
            self.interface.on_lose_focus(None)


class TextInput(TextViewWidget):
    def create(
        self,
        *,
        input_type=InputType.TYPE_CLASS_TEXT,
        handle_confirm=True,
        handle_focus=True,
    ):
        self.native = EditText(self._native_activity)
        self.native.setInputType(input_type)
        self.cache_textview_defaults()

        self.native.addTextChangedListener(TogaTextWatcher(self))
        if handle_confirm:
            self.native.setOnKeyListener(TogaKeyListener(self))
        if handle_focus:
            self.native.setOnFocusChangeListener(TogaFocusListener(self))

    def get_value(self):
        return str(self.native.getText())

    def set_value(self, value):
        self.native.setText(value)

    def get_readonly(self):
        return not self.native.isFocusable()

    def set_readonly(self, readonly):
        if readonly:
            # Implicitly calls setFocusableInTouchMode(False)
            self.native.setFocusable(False)
        else:
            # Implicitly calls setFocusable(True)
            self.native.setFocusableInTouchMode(True)

    def get_placeholder(self):
        return str(self.native.getHint())

    def set_placeholder(self, value):
        self.native.setHint(value)

    def set_alignment(self, value):
        self.set_textview_alignment(value, Gravity.CENTER_VERTICAL)

    def set_background_color(self, value):
        # This causes any custom color to hide the bottom border line, but it's better
        # than set_background_filter, which affects *only* the bottom border line.
        self.set_background_simple(value)

    def set_error(self, error_message):
        self.native.setError(error_message)

    def clear_error(self):
        self.native.setError(None)

    def is_valid(self):
        return self.native.getError() is None

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        # Refuse to call measure() if widget has no container, i.e., has no LayoutParams.
        # On Android, EditText's measure() throws NullPointerException if the widget has no
        # LayoutParams.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
