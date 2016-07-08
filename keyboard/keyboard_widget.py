from PySide import QtGui
from keyboard_base import Keyboard
from keyboard_context import NukeCheckBox, NodesCheckBox, ViewerCheckBox


class KeyboardWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(KeyboardWidget, self).__init__(*args, **kwargs)
        self.key_map = {}

        layout = QtGui.QVBoxLayout()

        # Setting up the context checkboxes above.
        self.init_context_box(layout)

        # Setting up the main keyboard view.
        self.init_keyboard_base(layout)

        # Setting up the bottom area. The search area and the extra keyboard buttons.

        self.setLayout(layout)

    def init_context_box(self, layout):
        context_box_group = QtGui.QGroupBox("Context")
        context_box_group_layout = QtGui.QHBoxLayout()
        context_box_group_layout.setSpacing(0)
        for check in [NukeCheckBox, NodesCheckBox, ViewerCheckBox]:
            checkbox = check()
            checkbox.HIGHLIGHT_SIGNAL.connect(self.colour_keyboard)
            context_box_group_layout.addWidget(checkbox)
        context_box_group.setLayout(context_box_group_layout)
        layout.addWidget(context_box_group)

    def init_keyboard_base(self, layout):
        keyboard_group = QtGui.QGroupBox("Keyboard")
        keyboard_group_layout = QtGui.QVBoxLayout()
        keyboard_group_layout.setSpacing(0)
        keyboard_group_layout.setContentsMargins(0, 0, 0, 0)
        keyboard_inst = Keyboard(self.key_map)
        keyboard_group_layout.addWidget(keyboard_inst)
        keyboard_group.setLayout(keyboard_group_layout)
        layout.addWidget(keyboard_group)

    def colour_keyboard(self, colour_hex, is_checked):
        print colour_hex, hex(colour_hex), is_checked
