import weakref
from PySide import QtGui, QtCore
from resources import HEX_COLOUR_NONE, HEX_COLOUR_RED, HEX_COLOUR_GREEN, HEX_COLOUR_BLUE


class BaseKey(QtGui.QPushButton):
    KEY_TYPE = "default"
    KEY_CLICKED = QtCore.Signal(weakref.ReferenceType)
    BG_COLOUR = HEX_COLOUR_NONE

    def __init__(self, *args, **kwargs):
        super(BaseKey, self).__init__(*args, **kwargs)
        self.colour = self.BG_COLOUR
        self.type = self.KEY_TYPE
        self.setMinimumWidth(32)
        self.setMinimumHeight(32)
        self.setCheckable(True)
        self.clicked.connect(self.emit_clicked)

    def emit_clicked(self, *args, **kwargs):
        weak_self = weakref.ref(self)
        self.KEY_CLICKED.emit(weak_self)

    def set_colour(self):
        self.setStyleSheet("")

        if self.colour is not HEX_COLOUR_NONE:
            css_colour = "#{message:{fill}{align}{width}}".format(message=hex(self.colour)[2:], fill='0',
                                                                  align='>', width=6)
            print css_colour
            self.setStyleSheet("""
            QPushButton {
                background-color: %s;
            }
            """ % css_colour)

    def click(self, set_to=None):
        r = super(BaseKey, self).click()
        if set_to:
            self.setChecked(set_to)
        self.set_colour()
        return r
