import sys
import weakref
from pprint import pprint
from PySide import QtCore, QtGui


class BaseButton(QtGui.QPushButton):
    KEY_TYPE = "default"
    KEY_CLICKED = QtCore.Signal(weakref.ReferenceType)

    def __init__(self, *args, **kwargs):
        super(BaseButton, self).__init__(*args, **kwargs)
        self.type = self.KEY_TYPE
        self.setMinimumWidth(35)
        self.setCheckable(True)
        self.clicked.connect(self.emit_clicked)

    def emit_clicked(self, *args, **kwargs):
        weak_self = weakref.ref(self)
        self.KEY_CLICKED.emit(weak_self)

    def click(self, set_to=None):
        r = super(BaseButton, self).click()
        if set_to:
            self.setChecked(set_to)
        return r


class ToggleButton(BaseButton):
    KEY_TYPE = "toggle"


class ModifierButton(BaseButton):
    KEY_TYPE = "modifier"


class DisabledButton(BaseButton):
    def __init__(self, *args, **kwargs):
        super(DisabledButton, self).__init__(*args, **kwargs)
        self.setDisabled(True)
        self.setMinimumWidth(50)


class Keyboard(QtGui.QWidget):
    key_map = {}
    keyboard_grid = [
        [('`', 1.5, ToggleButton), ('1', 2, ToggleButton), ('2', 2, ToggleButton), ('3', 2, ToggleButton),
         ('4', 2, ToggleButton), ('5', 2, ToggleButton), ('6', 2, ToggleButton), ('7', 2, ToggleButton),
         ('8', 2, ToggleButton), ('9', 2, ToggleButton), ('0', 2, ToggleButton), ("-", 2, ToggleButton),
         ("=", 2, ToggleButton), ("backspace", 4.5, DisabledButton)],
        [('tab', 2.5, DisabledButton), ('q', 2, ToggleButton), ('w', 2, ToggleButton), ('e', 2, ToggleButton),
         ('r', 2, ToggleButton), ('t', 2, ToggleButton), ('y', 2, ToggleButton), ('u', 2, ToggleButton),
         ('i', 2, ToggleButton), ('o', 2, ToggleButton), ('p', 2, ToggleButton), ('[', 2, ToggleButton),
         (']', 2, ToggleButton), ('\\', 3.5, ToggleButton)],
        [('caps', 2.5, DisabledButton), ('', 0.5, ToggleButton), ('a', 2, ToggleButton), ('s', 2, ToggleButton),
         ('d', 2, ToggleButton), ('f', 2, ToggleButton), ('g', 2, ToggleButton), ('h', 2, ToggleButton),
         ('j', 2, ToggleButton), ('k', 2, ToggleButton), ('l', 2, ToggleButton), (';', 2, ToggleButton),
         ('\'', 2, ToggleButton), ('return', 5, DisabledButton)],
        [('Shift', 4.5, ModifierButton), ('z', 2, ToggleButton), ('x', 2, ToggleButton), ('c', 2, ToggleButton),
         ('v', 2, ToggleButton), ('b', 2, ToggleButton), ('n', 2, ToggleButton), ('m', 2, ToggleButton),
         (',', 2, ToggleButton), ('.', 2, ToggleButton), ('/', 2, ToggleButton), ('Shift', 5.5, ModifierButton)],
        [('Ctrl', 3, ModifierButton), ('win', 2, DisabledButton), ('Alt', 2, ModifierButton),
         ('space', 16, DisabledButton),
         ('Alt', 2, ModifierButton), ('win', 2, DisabledButton), ('Ctrl', 3, ModifierButton)]
    ]

    def __init__(self):
        super(Keyboard, self).__init__()
        self.active_keys = {
            BaseButton.KEY_TYPE: [],
            ToggleButton.KEY_TYPE: [],
            ModifierButton.KEY_TYPE: [],
        }
        self.initUI()

    def initUI(self):

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
        self.resize(844, 161)

    def add_key_toggle(self, key):
        key_set = set(self.active_keys[key.type])
        if key.type == ToggleButton.KEY_TYPE:
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

        name = key.text()
        if key.isChecked():
            self.add_key_toggle(key)
        else:
            self.remove_key_toggle(key)


class Dialog(QtGui.QWidget):
    KEY_MODIFIERS = ["Shift", "Ctrl", "Alt", "Win", "Keypad", "GroupSwitch"]

    def __init__(self):
        super(Dialog, self).__init__()
        box = QtGui.QVBoxLayout()
        self.keyboard = Keyboard()
        box.addWidget(self.keyboard)

        button_box = QtGui.QWidget()
        button_box_layout = QtGui.QHBoxLayout()
        button_box_layout.addWidget(QtGui.QPushButton("Ok"))
        button_box_layout.addWidget(QtGui.QPushButton("Cancel"))
        button_box.setLayout(button_box_layout)

        box.addWidget(button_box)
        self.setLayout(box)
        self.setWindowTitle('Calculator')
        self.resize(650, 200)

    def keyPressEvent(self, e):
        keys = []
        if e.text():
            keys.append(e.text())
        else:
            modifier = QtGui.QApplication.instance().keyboardModifiers()
            if modifier & QtCore.Qt.ShiftModifier:
                keys.append("Shift")
            if modifier & QtCore.Qt.ControlModifier:
                keys.append("Ctrl")
            if modifier & QtCore.Qt.AltModifier:
                keys.append("Alt")
            if modifier & QtCore.Qt.MetaModifier:
                keys.append("Win")
            if modifier & QtCore.Qt.KeypadModifier:
                keys.append("Keypad")
            if modifier & QtCore.Qt.GroupSwitchModifier:
                keys.append("GroupSwitch")
            if modifier & QtCore.Qt.NoModifier:
                return

        print keys
        if len(keys) > 1:
            for mod_name in self.KEY_MODIFIERS:
                for mod_key in self.keyboard.key_map.get(mod_name, []):
                    if mod_key and mod_key() is not None:
                        mod_key().setChecked(False)
        for key_name in keys:
            key_list = self.keyboard.key_map.get(key_name, [])
            for key in key_list:
                if key and key() is not None:
                    k = key()
                    if k.isChecked() and len(keys) <= 1:
                        key().click(set_to=False)
                    else:
                        key().click(set_to=True)
        print self.size()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Dialog()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
