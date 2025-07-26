import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
import random
from MainWindow import Ui_XPType
from time import time
import os

if getattr(sys, 'frozen', False):
    base = sys._MEIPASS # pyinstaller compatibility
else:
    base = os.path.dirname(__file__)

path = os.path.join(base, 'words.txt')

with open(path, "r") as f:
    global words, wordsByLen
    words = list(f.read().split())
    wordsByLen = dict()
    for word in words:
        length = len(word)
        if length not in wordsByLen:
            wordsByLen[length] = []
        wordsByLen[length].append(word)

class XPType(QtWidgets.QWidget, Ui_XPType):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.originalText = ""
        self.charactersPerLine = 0
        self.typed = ""
        self.startTime = None

        font = QtGui.QFont("Courier New", 32)
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self.label.setFont(font)
        metrics = QtGui.QFontMetrics(font)
        self.fontWidth = metrics.horizontalAdvance("a")
        self.fontHeight = metrics.height() + 2 * metrics.leading()

        self.label.setWordWrap(True)
        self.pushButton.clicked.connect(self.generateText)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        try:
            self.pushButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        except AttributeError:
            try:
                self.pushButton.setFocusPolicy(Qt.NoFocus)
            except AttributeError:
                print("cry about it")
        try:
            self.label.setAlignment(Qt.AlignCenter)
        except AttributeError:
            try:
                self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            except AttributeError:
                print("keep crying about it")
        try:
            self.verticalLayout.setAlignment(self.label, Qt.AlignCenter)
        except AttributeError:
            try:
                self.verticalLayout.setAlignment(self.label, Qt.AlignmentFlag.AlignCenter)
            except AttributeError:
                print("cry more about it")

    def update_label(self):
        coloredText = ""
        correct = 0
        for i in range(len(self.originalText)):
            if i < len(self.typed):
                if self.typed[i] == self.originalText[i]:
                    coloredText += '<span style="color: white;">{}</span>'.format(self.typed[i])
                    correct += 1
                else:
                    coloredText += '<span style="color: #f38ba8; text-decoration: underline;">{}</span>'.format(self.typed[i])
            elif i == len(self.typed):
                coloredText += '<span style="color: grey; text-decoration: underline;">{}</span>'.format(self.originalText[i])
            else:
                coloredText += '<span style="color: grey;">{}</span>'.format(self.originalText[i])
            coloredText += "&#8203;"
        self.label.setText(coloredText)
        return correct

    def keyPressEvent(self, a0):
        key = a0.key()
        text = a0.text()
        correct = 0
        if self.startTime is None:
            self.startTime = time()
        if len(self.typed) < len(self.originalText):
            if key == 16777219: # backspace
                if len(self.typed) > 0:
                    self.typed = self.typed[:-1]
            else:
                self.typed += text
            correct = self.update_label()
            if len(self.typed) > 0:
                rawWpm = int((len(self.typed) * 12) / max(0.0001, time() - self.startTime)) # divide by 5 then multiply by 60 to convert from CPS to WPM
                wpm = int((correct * 12) / max(0.0001, time() - self.startTime))
                self.wpm_label.setText("Raw WPM: " + str(rawWpm) + " | WPM: " + str(wpm) + " | Accuracy: " + str(int((correct / len(self.typed)) * 100)) + "%")
        super().keyPressEvent(a0)

    def generateText(self):
        width = self.label.width()
        charactersPerLine = int(width // self.fontWidth)
        self.charactersPerLine = charactersPerLine
        self.label.setFixedWidth(charactersPerLine * self.fontWidth)
        lines = 5 # seems like a good amount
        text = ""
        for _ in range(lines):
            line = ""
            while len(line) < charactersPerLine:
                word = random.choice(words)
                if len(line) + len(word) >= charactersPerLine:
                    remCharacters = charactersPerLine - len(line) - 1
                    if remCharacters > 0:
                        word = random.choice(wordsByLen.get(remCharacters, words))
                line += word + " "
            text += line
        text = text.strip()
        print(text)

        # reset stuff
        self.typed = ""
        self.wpm_label.setText("Raw WPM: 0 | WPM: 0 | Accuracy: 0%")
        self.originalText = text
        self.update_label()
        self.startTime = None

app = QtWidgets.QApplication(sys.argv)

window = XPType()
window.show()

window.generateText()
app.exec()
