import sys
from PySide import QtCore, QtGui
from keyboard import KeyboardWidget


class Dialog(QtGui.QWidget):
    KEY_MODIFIERS = ["Shift", "Ctrl", "Alt", "Win", "Keypad", "GroupSwitch"]

    def __init__(self):
        super(Dialog, self).__init__()
        box = QtGui.QVBoxLayout()
        self.keyboard = KeyboardWidget()
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
