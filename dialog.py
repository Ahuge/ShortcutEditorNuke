import sys
from PySide import QtCore, QtGui
from keyboard import KeyboardWidget
from resources import KeySequenceObject


class Dialog(QtGui.QWidget):
    KEY_MODIFIERS = ["Shift", "Ctrl", "Alt", "Win", "Keypad", "GroupSwitch"]
    MAX_NUM_KEYSTROKES = 1

    def __init__(self):
        super(Dialog, self).__init__()
        self.current_seq = KeySequenceObject()
        self.seqs = []
        box = QtGui.QVBoxLayout()
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        self.keyboard = KeyboardWidget()
        box.addWidget(self.keyboard)

        button_box = QtGui.QWidget()
        button_box_layout = QtGui.QHBoxLayout()
        ac_button = QtGui.QPushButton("Apply and Close")
        a_button = QtGui.QPushButton("Apply")
        cancel_button = QtGui.QPushButton("Cancel")

        button_box_layout.addWidget(ac_button)
        button_box_layout.addWidget(a_button)
        button_box_layout.addWidget(cancel_button)
        button_box.setLayout(button_box_layout)

        cancel_button.clicked.connect(self.close)
        ac_button.clicked.connect(self.commit_and_close)
        a_button.clicked.connect(self.commit)

        box.addWidget(button_box)
        self.setLayout(box)
        self.setWindowTitle('Hotkey Manager')
        self.resize(650, 200)

    def commit_and_close(self):
        self.commit()
        self.close()

    def commit(self):
        print "Saved!"

    def event(self, ev):
        if ev.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(ev)
            return True
        return super(Dialog, self).event(ev)

    def keyPressEvent(self, ev):
        if not self.current_seq.timer.isActive():
            self.seqs.append(self.current_seq)
            self.current_seq = KeySequenceObject()
            self.current_seq.start_recording()
        self.current_seq.keyPressEvent(ev)
        key_sequence = self.current_seq.keySequence()
        self.keyboard.set_sequence(key_sequence)
        self.current_seq.timer.stop()

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
