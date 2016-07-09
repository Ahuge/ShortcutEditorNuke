import os
from PySide import QtGui, QtCore

"""
0x5900ff   - Green  - rgb(0, 89, 0)
0x7fff     - Blue  - rgb(0, 0, 127)
0x7f0000ff - Red  - rgb(127, 0, 0)
"""

IMAGE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__))).replace("\\", "/")


class ContextCheckBox(QtGui.QCheckBox):
    COLOUR = 0x000000
    HIGHLIGHT_SIGNAL = QtCore.Signal(int, bool)

    def __init__(self, *args, **kwargs):
        super(ContextCheckBox, self).__init__(*args, **kwargs)

        self.stateChanged.connect(self.emit_signal)

    def emit_signal(self, *args, **kwargs):
        self.HIGHLIGHT_SIGNAL.emit(self.COLOUR, self.isChecked())
