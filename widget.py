import sys
from PyQt5 import QtWidgets, uic

from MainWindow import Ui_XPType


class XPType(QtWidgets.QMainWindow, Ui_XPType):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)

window = XPType()
window.show()
app.exec()
