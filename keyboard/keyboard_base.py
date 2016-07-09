import weakref
from keys import UniqueKey, BaseKey, DisabledKey
from PySide import QtGui


class Keyboard(QtGui.QWidget):
    keyboard_grid = [
        [("Esc", 2.5, UniqueKey), ("", 0.5, UniqueKey), ("F1", 2, UniqueKey), ("F2", 2, UniqueKey),
         ("F3", 2, UniqueKey), ("F4", 2, UniqueKey), ("", 1.5, UniqueKey), ("F5", 2, UniqueKey), ("F6", 2, UniqueKey),
         ("F7", 2, UniqueKey), ("F8", 2, UniqueKey), ("", 1.5, UniqueKey), ("F9", 2, UniqueKey), ("F10", 2, UniqueKey),
         ("F11", 2, UniqueKey), ("F12", 2, UniqueKey)],

        [('`', 1.5, UniqueKey), ('1', 2, UniqueKey), ('2', 2, UniqueKey), ('3', 2, UniqueKey),
         ('4', 2, UniqueKey), ('5', 2, UniqueKey), ('6', 2, UniqueKey), ('7', 2, UniqueKey),
         ('8', 2, UniqueKey), ('9', 2, UniqueKey), ('0', 2, UniqueKey), ("-", 2, UniqueKey),
         ("=", 2, UniqueKey), ("backspace", 4.5, UniqueKey)],

        [('tab', 2.5, UniqueKey), ('q', 2, UniqueKey), ('w', 2, UniqueKey), ('e', 2, UniqueKey),
         ('r', 2, UniqueKey), ('t', 2, UniqueKey), ('y', 2, UniqueKey), ('u', 2, UniqueKey),
         ('i', 2, UniqueKey), ('o', 2, UniqueKey), ('p', 2, UniqueKey), ('[', 2, UniqueKey),
         (']', 2, UniqueKey), ('\\', 3.5, UniqueKey)],

        [('CapsLock', 3.5, UniqueKey), ('', 0.5, UniqueKey), ('a', 2, UniqueKey), ('s', 2, UniqueKey),
         ('d', 2, UniqueKey), ('f', 2, UniqueKey), ('g', 2, UniqueKey), ('h', 2, UniqueKey),
         ('j', 2, UniqueKey), ('k', 2, UniqueKey), ('l', 2, UniqueKey), (';', 2, UniqueKey),
         ('\'', 2, UniqueKey), ('Return', 4, UniqueKey)],

        [('Shift', 4.5, BaseKey), ('z', 2, UniqueKey), ('x', 2, UniqueKey), ('c', 2, UniqueKey),
         ('v', 2, UniqueKey), ('b', 2, UniqueKey), ('n', 2, UniqueKey), ('m', 2, UniqueKey),
         (',', 2, UniqueKey), ('.', 2, UniqueKey), ('/', 2, UniqueKey), ('Shift', 5.5, BaseKey)],

        [('Ctrl', 3, BaseKey), ('Win', 2, DisabledKey), ('Alt', 2, BaseKey),
         ('Space', 16, UniqueKey),
         ('Alt', 2, BaseKey), ('Win', 2, DisabledKey), ('Ctrl', 3, BaseKey)]
    ]

    def __init__(self, key_map=None, active_keys=None):
        super(Keyboard, self).__init__()
        if key_map is None:
            self.key_map = {}
        else:
            self.key_map = key_map

        if active_keys is None:
            self.active_keys = {
                UniqueKey.KEY_TYPE: [],
                BaseKey.KEY_TYPE: [],
            }
        else:
            self.active_keys = active_keys
        self.build_ui()

    def build_ui(self):

        grid = QtGui.QGridLayout()
        grid.setVerticalSpacing(1)
        grid.setHorizontalSpacing(2)
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
        if key.type == UniqueKey.KEY_TYPE:
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
