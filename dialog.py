import sys
from PySide import QtCore, QtGui
from keyboard import KeyboardWidget


class Dialog(QtGui.QWidget):
    KEY_MODIFIERS = ["Shift", "Ctrl", "Alt", "Win", "Keypad", "GroupSwitch"]

    def __init__(self):
        super(Dialog, self).__init__()
        box = QtGui.QVBoxLayout()
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        self.keyboard = KeyboardWidget()
        box.addWidget(self.keyboard)

        button_box = QtGui.QWidget()
        button_box_layout = QtGui.QHBoxLayout()
        button_box_layout.addWidget(QtGui.QPushButton("Ok"))
        button_box_layout.addWidget(QtGui.QPushButton("Cancel"))
        button_box.setLayout(button_box_layout)

        box.addWidget(button_box)
        self.setLayout(box)
        self.setWindowTitle('Hotkey Manager')
        self.resize(650, 200)

    def keyPressEvent(self, e):
        # TODO: Can I make this better?
        keys = []
        if not e.text():
            if e.key() == QtCore.Qt.Key_Control:
                keys.append("Ctrl")
            if e.key() == QtCore.Qt.Key_Shift:
                keys.append("Shift")
            if e.key() == QtCore.Qt.Key_Alt:
                keys.append("Alt")
            if e.key() == QtCore.Qt.Key_Meta:
                keys.append("Win")
            if e.key() == QtCore.Qt.Key_F1:
                keys.append("F1")
            if e.key() == QtCore.Qt.Key_F2:
                keys.append("F2")
            if e.key() == QtCore.Qt.Key_F3:
                keys.append("F3")
            if e.key() == QtCore.Qt.Key_F4:
                keys.append("F4")
            if e.key() == QtCore.Qt.Key_F5:
                keys.append("F5")
            if e.key() == QtCore.Qt.Key_F6:
                keys.append("F6")
            if e.key() == QtCore.Qt.Key_F7:
                keys.append("F7")
            if e.key() == QtCore.Qt.Key_F8:
                keys.append("F8")
            if e.key() == QtCore.Qt.Key_F9:
                keys.append("F9")
            if e.key() == QtCore.Qt.Key_F10:
                keys.append("F10")
            if e.key() == QtCore.Qt.Key_F11:
                keys.append("F11")
            if e.key() == QtCore.Qt.Key_F12:
                keys.append("F12")
            if e.key() == QtCore.Qt.Key_Tab:
                keys.append("Tab")
            if e.key() == QtCore.Qt.Key_CapsLock:
                keys.append("Caps Lock")
            if e.key() == QtCore.Qt.Key_Return:
                keys.append("Return")
            if e.key() == QtCore.Qt.Key_Space:
                keys.append("Space")
        else:
            if e.text() == "\r":
                keys.append("Return")
            elif e.text() == "\x1b":
                keys.append("Esc")
            else:
                keys.append(e.text())

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

    def __del__(self):
        print "DELETING DIALOG OBJECT!"


def main():

    try:
        app = QtGui.QApplication(sys.argv)
        exec__ = app.exec_
    except RuntimeError:
        app = QtGui.QApplication.instance()
        exec__ = None
    ex = Dialog()
    ex.show()
    if exec__ is None:
        ex.exec_()
    else:
        exec__()


if __name__ == '__main__':
    main()
