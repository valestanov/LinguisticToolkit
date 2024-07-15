import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLineEdit, QComboBox
)
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt
import unicodedata
import re
from textsplitter import SentenceSplitter
from langsplitter import split_text_by_char, split_text_by_word, split_text_sea_lang

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Processing with Dictionary")
        self.setGeometry(100, 100, 1000, 600)

        # Initialize dictionary
        self.dictionary = {}
        self.dictionary_path = r""
        
        # Create text edit widgets
        self.left_text_edit = QTextEdit()
        self.right_text_edit = QTextEdit()
        self.pronunciation_text_edit = QTextEdit()

        # Set default fonts
        self.left_text_edit.setFont(QFont("Arial", 16))
        self.right_text_edit.setFont(QFont("Arial", 14))
        self.pronunciation_text_edit.setFont(QFont("Arial", 14))

        # Create dictionary file path input and button
        self.dict_path_edit = QLineEdit()
        self.load_dict_button = QPushButton("Load Dictionary")
        self.dict_path_edit = QLineEdit(self.dictionary_path)

        #font_database = QFontDatabase.families()
        font_database = ['Arial','Times New Roman','Consolas','华文中宋','楷体','宋体','Noto Serif KR','Noto Sans Khmer']
        # Create font selection combo box
        self.font_combo_box = QComboBox()
        self.font_combo_box.addItems(font_database)
        self.font_combo_box.setCurrentText("Arial")
        self.font_combo_box.currentTextChanged.connect(self.change_font)

        # Create font selection combo box
        self.pronunciation_font_combo_box = QComboBox()
        self.pronunciation_font_combo_box.addItems(font_database)
        self.pronunciation_font_combo_box.setCurrentText("Arial")
        self.pronunciation_font_combo_box.currentTextChanged.connect(self.pronunciation_change_font)

        # Create font selection combo box
        self.right_font_combo_box = QComboBox()
        self.right_font_combo_box.addItems(font_database)
        self.right_font_combo_box.setCurrentText("Arial")
        self.right_font_combo_box.currentTextChanged.connect(self.right_change_font)
        
        # Layout
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.left_text_edit)
        text_layout.addWidget(self.pronunciation_text_edit)
        text_layout.addWidget(self.right_text_edit)

        dict_layout = QHBoxLayout()
        dict_layout.addWidget(self.dict_path_edit)
        dict_layout.addWidget(self.load_dict_button)

        font_layout = QVBoxLayout()
        font_layout.addWidget(self.font_combo_box)
        font_layout.addWidget(self.pronunciation_font_combo_box)
        font_layout.addWidget(self.right_font_combo_box)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(text_layout)
        main_layout.addLayout(dict_layout)
        main_layout.addLayout(font_layout)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect signals
        self.left_text_edit.textChanged.connect(self.on_text_changed)
        self.load_dict_button.clicked.connect(self.load_dictionary)

        # Initial dictionary load
        self.load_dictionary()

    def load_dictionary(self):
        dict_path = self.dict_path_edit.text()
        if not dict_path:
            dict_path = "dictionary.txt"  # default path
        try:
            self.dictionary = self.read_dictionary(dict_path)
            self.on_text_changed()  # Refresh text processing
        except Exception as e:
            print(f"Failed to load dictionary: {e}")

    def read_dictionary(self, filename):
        dictionary = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    word, pronunciation, definition = line.strip('\ufeff\n \t').split("\t")
                    if word not in dictionary:
                        dictionary[word] = ("","")
                    dictionary[word] = (dictionary[word][0]+'|'+pronunciation, dictionary[word][1]+'|'+definition)
                    dictionary[word] = (dictionary[word][0].strip('| '),dictionary[word][1].strip('| '))
                except:
                    print(line)
        return dictionary

    def on_text_changed(self):
        cursor = self.left_text_edit.textCursor()
        cursor_pos = cursor.position()
        
        text = self.left_text_edit.toPlainText()
        words = self.sentence_split(text)
        colored_text = self.apply_rainbow_colors(words)
        self.left_text_edit.blockSignals(True)
        self.left_text_edit.setHtml(colored_text.replace('\n', '<br>'))
        cursor.setPosition(cursor_pos)
        self.left_text_edit.setTextCursor(cursor)
        self.left_text_edit.blockSignals(False)
        pronunciations, definitions = self.get_pronunciations_and_definitions(words)
        self.right_text_edit.setHtml(definitions)
        self.pronunciation_text_edit.setHtml(pronunciations)

    def sentence_split(self, sentence):
        # 将词典中的词按照长度逆向排序
        dictionary_items = sorted(self.dictionary.items(), key=lambda x: len(x[0].strip()), reverse=True)
        dictionary_items = [i[0] for i in dictionary_items if i[0].strip() != '']
        # 替换句子中的词为特殊标记
        for i, word in enumerate(dictionary_items):
            if word in sentence:
                sentence = sentence.replace(word, "\uffff\ufffe%06d\ufffe\uffff" % i)
        # 按特殊标记分割句子
        sentence_parts = sentence.split('\uffff')
        sentence_parts = [i for i in sentence_parts if i != '']
        # 恢复句子中的词
        for i, word in enumerate(dictionary_items):
            for j, part in enumerate(sentence_parts):
                sentence_parts[j] = part.replace("\ufffe%06d\ufffe" % i, word)
        return sentence_parts

    def apply_rainbow_colors(self, words):
        colors = ["red", "green", "blue", "indigo"]
        colored_text = ""
        for i, word in enumerate(words):
            color = colors[i % len(colors)]
            colored_text += f'<span style="color: {color};">{word}</span>'
        return colored_text

    def get_pronunciations_and_definitions(self, words):
        colors = ["red", "green", "blue", "indigo"]
        pronunciations = ""
        definitions = ""
        for i, word in enumerate(words):
            word = word
            color = colors[i % len(colors)]
            if word in self.dictionary:
                pronunciation, definition = self.dictionary[word]
                pronunciations += f'<span style="color: {color};"> {pronunciation}</span>\n'
                definitions += f'<span style="color: {color};"> {definition}</span>\n'
            else:
                word = word.replace('\n', '<br>')
                pronunciations += f'<span style="color: {color};">{word}</span>\n'
                definitions += f'<span style="color: {color};">{word}</span>\n'
        return pronunciations, definitions

    def change_font(self, font_name):
        self.left_text_edit.setFont(QFont(font_name, 16))

    def pronunciation_change_font(self, font_name):
        self.pronunciation_text_edit.setFont(QFont(font_name, 14))

    def right_change_font(self, font_name):
        self.right_text_edit.setFont(QFont(font_name, 14))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
