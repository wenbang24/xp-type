from PyQt5 import QtWidgets

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, currentLines=5, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Settings")

        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel("Number of Lines:", self)
        layout.addWidget(label)
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10)
        self.spinBox.setValue(currentLines)
        layout.addWidget(self.spinBox)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getValue(self):
        return self.spinBox.value()
