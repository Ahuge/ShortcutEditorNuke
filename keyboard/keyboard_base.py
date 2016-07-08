import weakref
from keys import BaseKey, UniqueKey, DisabledKey
from PySide import QtGui


class Keyboard(QtGui.QWidget):
    key_map = {}
    keyboard_grid = [
        [("Esc", 2, BaseKey), ("", 1, BaseKey), ("F1", 2, BaseKey), ("F2", 2, BaseKey), ("F3", 2, BaseKey),
         ("F4", 2, BaseKey), ("", 1.5, BaseKey), ("F5", 2, BaseKey), ("F6", 2, BaseKey), ("F7", 2, BaseKey),
         ("F8", 2, BaseKey), ("", 1.5, BaseKey), ("F9", 2, BaseKey), ("F10", 2, BaseKey), ("F11", 2, BaseKey),
         ("F12", 2, BaseKey)],
        [('`', 1.5, BaseKey), ('1', 2, BaseKey), ('2', 2, BaseKey), ('3', 2, BaseKey),
         ('4', 2, BaseKey), ('5', 2, BaseKey), ('6', 2, BaseKey), ('7', 2, BaseKey),
         ('8', 2, BaseKey), ('9', 2, BaseKey), ('0', 2, BaseKey), ("-", 2, BaseKey),
         ("=", 2, BaseKey), ("backspace", 4.5, DisabledKey)],
        [('tab', 2.5, DisabledKey), ('q', 2, BaseKey), ('w', 2, BaseKey), ('e', 2, BaseKey),
         ('r', 2, BaseKey), ('t', 2, BaseKey), ('y', 2, BaseKey), ('u', 2, BaseKey),
         ('i', 2, BaseKey), ('o', 2, BaseKey), ('p', 2, BaseKey), ('[', 2, BaseKey),
         (']', 2, BaseKey), ('\\', 3.5, BaseKey)],
        [('caps', 2.5, DisabledKey), ('', 0.5, BaseKey), ('a', 2, BaseKey), ('s', 2, BaseKey),
         ('d', 2, BaseKey), ('f', 2, BaseKey), ('g', 2, BaseKey), ('h', 2, BaseKey),
         ('j', 2, BaseKey), ('k', 2, BaseKey), ('l', 2, BaseKey), (';', 2, BaseKey),
         ('\'', 2, BaseKey), ('return', 5, DisabledKey)],
        [('Shift', 4.5, UniqueKey), ('z', 2, BaseKey), ('x', 2, BaseKey), ('c', 2, BaseKey),
         ('v', 2, BaseKey), ('b', 2, BaseKey), ('n', 2, BaseKey), ('m', 2, BaseKey),
         (',', 2, BaseKey), ('.', 2, BaseKey), ('/', 2, BaseKey), ('Shift', 5.5, UniqueKey)],
        [('Ctrl', 3, UniqueKey), ('win', 2, DisabledKey), ('Alt', 2, UniqueKey),
         ('space', 16, DisabledKey),
         ('Alt', 2, UniqueKey), ('win', 2, DisabledKey), ('Ctrl', 3, UniqueKey)]
    ]

    def __init__(self):
        super(Keyboard, self).__init__()
        self.active_keys = {
            BaseKey.KEY_TYPE: [],
            UniqueKey.KEY_TYPE: [],
        }
        self.build_ui()

    def build_ui(self):

        grid = QtGui.QGridLayout()
        scale = 2
        for row_num, line in enumerate(self.keyboard_grid):
            col_index = 0
            for letter, width, button_type in line:
                key = button_type(letter)
                key.KEY_CLICKED.connect(self.button_press)
                if letter == "":
                    key = QtGui.QLabel("")
                grid.addWidget(key, row_num, col_index, 1, width * scale)
                col_index += width * scale
                if letter not in self.key_map:
                    self.key_map[letter] = []
                self.key_map[letter].append(weakref.ref(key))

        self.setLayout(grid)
        self.setWindowTitle('Calculator')
        self.resize(650, 200)

    def add_key_toggle(self, key):
        key_set = set(self.active_keys[key.type])
        if key.type == BaseKey.KEY_TYPE:
            for active_key in key_set:
                active_key.setChecked(False)
            key_set.clear()
        key_set.add(key)
        self.active_keys[key.type] = list(key_set)

    def remove_key_toggle(self, key):
        key_set = self.active_keys[key.type]
        try:
            key_set.remove(key)
        except ValueError:
            pass

    def button_press(self, weakref_obj):
        if not weakref_obj:
            return
        key = weakref_obj()
        if not key:
            return

        if key.isChecked():
            self.add_key_toggle(key)
        else:
            self.remove_key_toggle(key)
