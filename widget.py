import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui

from MainWindow import Ui_XPType


class XPType(QtWidgets.QMainWindow, Ui_XPType):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.originalText = self.label.text()

    def update_label(self, text):
        self.label.setText(text)
        self.originalText = text

    def color(self, n):
        styled_text = (
            f'<span style="color: white;">{self.originalText[:n]}</span>'
            f'<span style="color: grey;">{self.originalText[n:]}</span>'
        )
        self.label.setText(styled_text)

    def keyPressEvent(self, a0):
        key = a0.key()
        text = a0.text()

        print(f"Key Pressed: {key}, Text: '{text}'")

        super().keyPressEvent(a0)


app = QtWidgets.QApplication(sys.argv)

window = XPType()
window.show()

for i in range(20):
    QtCore.QTimer.singleShot(i * 1000, lambda: window.color(i))

app.exec()
