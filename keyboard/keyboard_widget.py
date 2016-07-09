from PySide import QtGui
from keyboard_base import Keyboard
from checkboxes import NukeCheckBox, NodesCheckBox, ViewerCheckBox


class KeyboardWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(KeyboardWidget, self).__init__(*args, **kwargs)
        self.key_map = {}
        self.active_sequence = QtGui.QKeySequence()

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
        from resources import HEX_COLOUR_BLUE, HEX_COLOUR_GREEN, HEX_COLOUR_RED
        keys = []
        if HEX_COLOUR_RED == colour_hex:
            keys.append(self.get_key("A")[0]())
            keys.append(self.get_key("S")[0]())
            keys.append(self.get_key("D")[0]())
            keys.append(self.get_key("F")[0]())
        if HEX_COLOUR_GREEN == colour_hex:
            keys.append(self.get_key("W")[0]())
            keys.append(self.get_key("S")[0]())
            keys.append(self.get_key("E")[0]())
            keys.append(self.get_key("F")[0]())
        if HEX_COLOUR_BLUE == colour_hex:
            keys.append(self.get_key("X")[0]())
            keys.append(self.get_key("E")[0]())
            keys.append(self.get_key("D")[0]())
            keys.append(self.get_key("F")[0]())
        for k in keys:
            if is_checked:
                k.colour |= colour_hex
            else:
                k.colour &= ~colour_hex
            k.set_colour()

        print colour_hex, hex(colour_hex), is_checked

    @staticmethod
    def str_to_key_int(key_name):
        seq = QtGui.QKeySequence(key_name)
        if seq.count() == 1:
            code = seq[0]
        else:
            assert seq.count() == 0
            seq = QtGui.QKeySequence(key_name + "+A")
            assert seq.count() == 1
            assert seq[0] > 65
            code = seq[0] - 65
        return code

    def get_key(self, key_str):
        key_list = self.key_map.get(key_str, [])
        if not key_list:
            key_list = self.key_map.get(key_str.lower(), [])
        return key_list

    @staticmethod
    def _key_str_list_from_sequence(key_sequence):
        clean_key_list = []
        keys = key_sequence.toString(QtGui.QKeySequence.NativeText)
        keys = keys.split(",")[0]
        keys = keys.split("+")
        for key_str in keys:
            if key_str:
                clean_key_list.append(key_str)
        return clean_key_list

    def clear_active_sequence(self):
        keys = self._key_str_list_from_sequence(self.active_sequence)
        for key_name in keys:
            key_list = self.get_key(key_name)
            for key in key_list:
                key().click(set_to=False)

    def toggle_key(self, key_str):
        self.set_key(key_str, state=-1)
        self.active_sequence = QtGui.QKeySequence()

    def set_key(self, key_str, state=True):
        """
        set_key takes a key name as a string. It then set's they key's clicked value to state.
        State can be True or False to perform as set operation, or a non bool to toggle the key.

        :param str key_str: Name of the key to set.
        :param Any state: State can be True or False to perform as set operation, or a non bool to toggle the key.
        """
        key_list = self.get_key(key_str)
        for key in key_list:
            if key and key():
                if isinstance(state, bool):
                    key().click(set_to=state)
                else:
                    key().click()
            else:
                print "Failed setting", key_str

    def set_sequence(self, key_sequence):
        func = self.set_key
        if key_sequence.matches(self.active_sequence) == QtGui.QKeySequence.SequenceMatch.NoMatch:
            self.clear_active_sequence()
            self.active_sequence = QtGui.QKeySequence(key_sequence.toString(QtGui.QKeySequence.NativeText))
        else:
            func = self.toggle_key

        key_name_list = self._key_str_list_from_sequence(self.active_sequence)
        print key_name_list
        for key_name in key_name_list:
            func(key_name)
        return True
