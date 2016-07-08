import weakref
from PySide import QtGui, QtCore


class BaseKey(QtGui.QPushButton):
    KEY_TYPE = "default"
    KEY_CLICKED = QtCore.Signal(weakref.ReferenceType)

    def __init__(self, *args, **kwargs):
        super(BaseKey, self).__init__(*args, **kwargs)
        self.type = self.KEY_TYPE
        self.setMinimumWidth(32)
        self.setMinimumHeight(32)
        self.setCheckable(True)
        self.clicked.connect(self.emit_clicked)

    def emit_clicked(self, *args, **kwargs):
        weak_self = weakref.ref(self)
        self.KEY_CLICKED.emit(weak_self)

    def click(self, set_to=None):
        r = super(BaseKey, self).click()
        if set_to:
            self.setChecked(set_to)
        return r
