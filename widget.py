import sys
from PyQt5 import QtWidgets
import random
from MainWindow import Ui_XPType
from time import time

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
        self.startTime = None

    def update_label(self, text):
        self.label.setText(text)
        self.originalText = text

    def colorWords(self, n, wrong = False):
        if n == len(self.originalText):
            styled_text = f'<span style="color: white;">{self.originalText}</span>'
        elif self.originalText[n] == "<":
            styled_text = (
                '<span style="color: white;">{}</span>'.format(self.originalText[:n]) +
                '<span style="color: {}; text-decoration: underline;"> </span>'.format("grey" if not wrong else "#f38ba8") +
                '<span style="color: grey;">{}</span>'.format(self.originalText[n:])
            )
        else:
            styled_text = (
                '<span style="color: white;">{}</span>'.format(self.originalText[:n]) +
                '<span style="color: {}; text-decoration: underline;">{}</span>'.format("grey" if not wrong else "#f38ba8", self.originalText[n]) +
                '<span style="color: grey;">{}</span>'.format(self.originalText[n + 1:])
            )
        self.label.setText(styled_text)

    def keyPressEvent(self, a0):
        key = a0.key()
        text = a0.text()
        print(f"Key Pressed: {key}, Text: '{text}'")
        if self.startTime is None:
            self.startTime = time()
        if self.index < len(self.originalText) and (text == self.originalText[self.index] or (text == " " and self.originalText[self.index] == "<")):
            if self.originalText[self.index] == "<":
                self.index += 3 # Skip over "<br>"
            self.index += 1
            self.colorWords(self.index)
        elif self.index < len(self.originalText):
            self.colorWords(self.index, True)
        if self.index < len(self.originalText):
            wpm = int((self.index * 12) / (time() - self.startTime)) # divide by 5 then multiply by 60 to convert from CPS to WPM
            self.wpm_label.setText(f"WPM: {wpm}")
        super().keyPressEvent(a0)

    def generateText(self):
        height = self.height()
        width = self.width()
        font = self.label.font()
        font_size = font.pointSize()
        charactersPerLine = int((1.5 * width) // font_size)
        lines = int((height // (1.5 * font_size)))
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
        text = text[:-4]  # Remove the last "<br>"
        self.update_label(text)
        self.colorWords(0)
        self.index = 0

app = QtWidgets.QApplication(sys.argv)

window = XPType()
window.show()

window.generateText()
app.exec()
