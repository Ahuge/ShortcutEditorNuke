import os
from PySide import QtGui, QtCore

"""
0x5900ff   - Green  - rgb(0, 89, 0)
0x7fff     - Blue  - rgb(0, 0, 127)
0x7f0000ff - Red  - rgb(127, 0, 0)
"""


class ContextCheckBox(QtGui.QCheckBox):
    COLOUR = 0x000000
    HIGHLIGHT_SIGNAL = QtCore.Signal(int, bool)

    def __init__(self, *args, **kwargs):
        super(ContextCheckBox, self).__init__(*args, **kwargs)

        self.stateChanged.connect(self.emit_signal)

    def emit_signal(self, *args, **kwargs):
        self.HIGHLIGHT_SIGNAL.emit(self.COLOUR, self.isChecked())


class NukeCheckBox(ContextCheckBox):
    COLOUR = 0x5900ff

    def __init__(self, *args, **kwargs):
        super(NukeCheckBox, self).__init__(*args, **kwargs)
        self.setText("Nuke")
        root = os.path.dirname(os.path.dirname(__file__)).replace("\\", "/")
        self.setStyleSheet("""
            QCheckBox::indicator:unchecked {
                image: url(%s/images/green_checkbox_unchecked.png);
            }

            QCheckBox::indicator:unchecked:hover {
                image: url(%s/images/green_checkbox_unchecked_hover.png);
            }

            QCheckBox::indicator:unchecked:pressed {
                image: url(%s/images/green_checkbox_unchecked_pressed.png);
            }

            QCheckBox::indicator:checked {
                image: url(%s/images/green_checkbox_checked.png);
            }

            QCheckBox::indicator:checked:hover {
                image: url(%s/images/green_checkbox_checked_hover.png);
            }

            QCheckBox::indicator:checked:pressed {
                image: url(%s/images/green_checkbox_checked_pressed.png);
            }
            """ % (root, root, root, root, root, root))


class NodesCheckBox(ContextCheckBox):
    COLOUR = 0x7fff

    def __init__(self, *args, **kwargs):
        super(NodesCheckBox, self).__init__(*args, **kwargs)
        self.setText("Nodes")
        root = os.path.dirname(os.path.dirname(__file__)).replace("\\", "/")
        self.setStyleSheet("""
            QCheckBox::indicator:unchecked {
                image: url(%s/images/blue_checkbox_unchecked.png);
            }

            QCheckBox::indicator:unchecked:hover {
                image: url(%s/images/blue_checkbox_unchecked_hover.png);
            }

            QCheckBox::indicator:unchecked:pressed {
                image: url(%s/images/blue_checkbox_unchecked_pressed.png);
            }

            QCheckBox::indicator:checked {
                image: url(%s/images/blue_checkbox_checked.png);
            }

            QCheckBox::indicator:checked:hover {
                image: url(%s/images/blue_checkbox_checked_hover.png);
            }

            QCheckBox::indicator:checked:pressed {
                image: url(%s/images/blue_checkbox_checked_pressed.png);
            }
            """ % (root, root, root, root, root, root))


class ViewerCheckBox(ContextCheckBox):
    COLOUR = 0x7f0000ff

    def __init__(self, *args, **kwargs):
        super(ViewerCheckBox, self).__init__(*args, **kwargs)
        self.setText("Viewer")
        root = os.path.dirname(os.path.dirname(__file__)).replace("\\", "/")
        self.setStyleSheet("""
            QCheckBox::indicator:unchecked {
                image: url(%s/images/red_checkbox_unchecked.png);
            }

            QCheckBox::indicator:unchecked:hover {
                image: url(%s/images/red_checkbox_unchecked_hover.png);
            }

            QCheckBox::indicator:unchecked:pressed {
                image: url(%s/images/red_checkbox_unchecked_pressed.png);
            }

            QCheckBox::indicator:checked {
                image: url(%s/images/red_checkbox_checked.png);
            }

            QCheckBox::indicator:checked:hover {
                image: url(%s/images/red_checkbox_checked_hover.png);
            }

            QCheckBox::indicator:checked:pressed {
                image: url(%s/images/red_checkbox_checked_pressed.png);
            }
            """ % (root, root, root, root, root, root))
