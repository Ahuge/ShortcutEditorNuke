from PySide import QtGui, QtCore


class KeySequenceObject(QtGui.QWidget):
    """
    Modified from
    https://github.com/dbr/shortcuteditor-nuke/blob/master/shortcuteditor.py
    """

    MAX_NUM_KEYSTROKES = 1

    def __init__(self, parent=None):
        super(KeySequenceObject, self).__init__(parent=parent)
        self._modifiers = QtGui.QApplication.keyboardModifiers()
        self._modifierlessAllowed = True  # True allows "b" as a shortcut, False requires shift/alt/ctrl/etc
        self._recording_sequence = QtGui.QKeySequence()
        self._seq = QtGui.QKeySequence()
        self._timer = QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._is_recording = False
        self._timer.timeout.connect(self.done_recording)

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value):
        raise NotImplementedError

    def set_key_sequence(self, seq):
        self._seq = seq
        self.update_display()

    def key_sequence(self):
        if self._is_recording:
            self.done_recording()
        return self._seq

    def update_display(self):
        if self._is_recording:
            s = self._recording_sequence.toString(QtGui.QKeySequence.NativeText).replace('&', '&&')
            if self._modifiers:
                if s:
                    s += ","
                s += QtGui.QKeySequence(self._modifiers).toString(QtGui.QKeySequence.NativeText)
            elif self._recording_sequence.isEmpty():
                s = "Input"
        else:
            s = self._seq.toString(QtGui.QKeySequence.NativeText).replace('&', '&&')
        print s

    def is_recording(self):
        return self._is_recording

    def event(self, ev):
        if self._is_recording:
            # prevent Qt from special casing Tab and Backtab
            if ev.type() == QtCore.QEvent.KeyPress:
                self.keyPressEvent(ev)
                return True
        return super(KeySequenceObject, self).event(ev)

    def keyPressEvent(self, ev):
        if not self._is_recording:
            return super(KeySequenceObject, self).keyPressEvent(ev)
        if ev.isAutoRepeat():
            return
        modifiers = ev.modifiers()

        ev.accept()

        key = ev.key()
        # Check if key is a modifier or a character key without modifier (and if that is allowed)
        if (
                (
                    # Don't append the key if the key is -1 (garbage) or a modifier ...
                    key not in (-1, QtCore.Qt.Key_AltGr, QtCore.Qt.Key_Shift, QtCore.Qt.Key_Control, 
                                QtCore.Qt.Key_Alt, QtCore.Qt.Key_Meta, QtCore.Qt.Key_Menu
                                ) and
                    (  # Or if this is the first key and without modifier and modifier-less keys are not allowed
                        self._modifierlessAllowed or 
                        self._recording_sequence.count() > 0 or 
                        modifiers & ~QtCore.Qt.SHIFT or not 
                        ev.text() or 
                        (
                            modifiers & QtCore.Qt.SHIFT and 
                            key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Space, 
                                    QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab, 
                                    QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete, 
                                    QtCore.Qt.Key_Escape)
                        )
                    )
                ) or 
                (  # Or if this key is a modifier and there is noting else selected.
                    key in (QtCore.Qt.Key_AltGr, QtCore.Qt.Key_Shift, QtCore.Qt.Key_Control, 
                            QtCore.Qt.Key_Alt, QtCore.Qt.Key_Meta, QtCore.Qt.Key_Menu) and 
                    modifiers != QtCore.Qt.KeyboardModifiers()
                )
        ):

            # Change Shift+Backtab into Shift+Tab
            if key == QtCore.Qt.Key_Backtab and modifiers & QtCore.Qt.SHIFT:
                key = QtCore.Qt.Key_Tab | modifiers

            # Remove the Shift modifier if it doesn't make sense..
            elif QtCore.Qt.Key_Exclam <= key <= QtCore.Qt.Key_At or QtCore.Qt.Key_Z < key <= 0x0ff:
                # e.g ctrl+shift+! is impossible on, some keyboards (because ! is shift+1)
                key |= (modifiers & ~int(QtCore.Qt.SHIFT))

            elif (  # If this key is a modifier and there is noting else selected.
                    key in (QtCore.Qt.Key_AltGr, QtCore.Qt.Key_Shift, QtCore.Qt.Key_Control, 
                            QtCore.Qt.Key_Alt, QtCore.Qt.Key_Meta, QtCore.Qt.Key_Menu) and
                    modifiers != QtCore.Qt.KeyboardModifiers()
            ):
                key = modifiers
            else:
                key = key | modifiers

            # Append max number of keystrokes
            if self._recording_sequence.count() < self.MAX_NUM_KEYSTROKES:
                l = list(self._recording_sequence)
                l.append(key)
                self._recording_sequence = QtGui.QKeySequence(*l)

        self._modifiers = modifiers
        self.control_timer()

    def keyReleaseEvent(self, ev):
        if not self._is_recording:
            return super(KeySequenceObject, self).keyReleaseEvent(ev)
        modifiers = int(ev.modifiers() & (QtCore.Qt.SHIFT | QtCore.Qt.CTRL | QtCore.Qt.ALT | QtCore.Qt.META))
        ev.accept()

        self._modifiers = modifiers
        self.control_timer()

    def hideEvent(self, ev):
        if self._is_recording:
            self.cancel_recording()
            super(KeySequenceObject, self).hideEvent(ev)

    def control_timer(self):
        if self._modifiers or self._recording_sequence.isEmpty():
            self._timer.stop()
        else:
            self._timer.start(600)

    def start_recording(self):
        self._is_recording = True
        self._recording_sequence = QtGui.QKeySequence()
        self._modifiers = int(QtGui.QApplication.keyboardModifiers() & (
            QtCore.Qt.SHIFT | QtCore.Qt.CTRL | QtCore.Qt.ALT | QtCore.Qt.META))
        self.grabKeyboard()
        self.update_display()

    def done_recording(self):
        self._seq = self._recording_sequence
        self.cancel_recording()
        self.clearFocus()

    def cancel_recording(self):
        if not self._is_recording:
            return
        self._is_recording = False
        self.releaseKeyboard()
        self.update_display()
