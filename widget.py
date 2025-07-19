import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import random
from MainWindow import Ui_XPType

with open("google-10000-english-no-swears.txt", "r") as f:
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
        self.originalText = self.label.text()
        self.pushButton.clicked.connect(self.generateText)
        self.index = 0

    def update_label(self, text):
        self.label.setText(text)
        self.originalText = text

    def colorWords(self, n):
        styled_text = (
            f'<span style="color: white;">{self.originalText[:n]}</span>'
            f'<span style="color: grey;">{self.originalText[n:]}</span>'
        )
        self.label.setText(styled_text)

    def keyPressEvent(self, a0):
        key = a0.key()
        text = a0.text()
        print(f"Key Pressed: {key}, Text: '{text}'")
        if text == self.originalText[self.index] or text == " " and self.originalText[self.index] == "<":
            if self.originalText[self.index] == "<":
                self.index += 3 # Skip over "<br>"
            self.index += 1
            if self.index >= len(self.originalText):
                self.index = 0
                self.generateText()
            else:
                self.colorWords(self.index)
            wpm = int((self.index / 5) / (self.label.text().count("<br>") + 1) * 60)
            self.wpm_label.setText(f"WPM: {wpm}")

        super().keyPressEvent(a0)

    def generateText(self):
        height = self.height()
        width = self.width()
        font = self.label.font()
        font_size = font.pointSize()
        charactersPerLine = int((1.5 * width) // font_size - 6)
        lines = int((height // (1.5 * font_size)) - 6)
        text = ""
        for _ in range(lines):
            line = ""
            while len(line) < charactersPerLine:
                word = random.choice(words)
                if len(line) + len(word) >= charactersPerLine:
                    remCharacters = charactersPerLine - len(line)
                    if remCharacters > 0:
                        word = random.choice(wordsByLen.get(remCharacters, words))
                line += word + " "
            line = line.strip()
            text += line + "<br>"
        text = text.strip()
        self.update_label(text)
        self.colorWords(0)
        self.index = 0

app = QtWidgets.QApplication(sys.argv)

window = XPType()
window.show()

window.generateText()
app.exec()
