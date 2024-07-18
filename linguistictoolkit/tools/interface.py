import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QFormLayout,
    QWidget, QPushButton, QLineEdit, QComboBox, QCheckBox, QGroupBox, QTableWidget, 
    QKeySequenceEdit, QDialogButtonBox, QDialog, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont, QFontDatabase, QKeySequence, QShortcut
from PyQt6.QtCore import Qt
import re
from linguistictoolkit.tools.engines import SplitterEngine, LookupEngine, DisplayerEngine
from linguistictoolkit.tools import langdeterminer

class ShortcutEditor(QDialog):
    def __init__(self, func_name, current_shortcut, parent = None):
        super().__init__(parent)
        self.setWindowTitle(f"修改{func_name}快捷键")
        self.layout = QFormLayout(self)
        self.key_sequence_edit = QKeySequenceEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(f"{func_name}的新快捷键:", self.key_sequence_edit)
        self.layout.addWidget(self.button_box)

class Column:
    def __init__(self, parent, displayer, fontList = [], fontSizeList = list(range(10,40,2)), isoriginal = False):
        self.parent = parent
        self.displayer = displayer
        self.isoriginal = isoriginal
        self.fontList = fontList + ['Arial','Times New Roman','BahnSchrift','Consolas','华文中宋','楷体','宋体']
        self.fontList += QFontDatabase.families()
        self.fontSizeList = fontSizeList
        self.initUI()
        self.setup_signals()
        
    def initUI(self):
        self.main_text_edit = QTextEdit()
        self.main_text_edit.setFont(QFont(self.displayer.font, self.displayer.font_size))
        
        if not self.isoriginal:
            self.keys_edit = QLineEdit()
            self.lookup_func_box = QComboBox()
            self.update_lookup()
            
        self.displayer_func_box = QComboBox()
        self.displayer_func_box.setEditable(False)
        
        self.isfocus_box = QCheckBox("标记光标位置")
        self.isnew_box = QCheckBox("标记新词")
        self.rainbow_box = QCheckBox("彩虹色")
        self.spec_rule_edit = QLineEdit()
        self.format_string_edit = QLineEdit()
        self.font_box = QComboBox()
        self.fontsize_box = QComboBox()

        self.isfocus_box.setChecked(self.displayer.highlight)
        self.isnew_box.setChecked(self.displayer.new_word)
        self.rainbow_box.setChecked(self.displayer.rainbow)
        self.refresh_spec_rule_edit()
        self.refresh_format_string_edit()

        if self.displayer.font not in self.fontList:
            self.font_box.addItem(self.fontList)
        self.font_box.addItems(self.fontList)
        self.font_box.setCurrentText(self.displayer.font)
        
        if str(self.displayer.font_size) not in self.fontSizeList:
            self.fontsize_box.addItem(str(self.displayer.font_size))
        self.fontsize_box.addItems(map(str, self.fontSizeList))
        self.fontsize_box.setCurrentText(str(self.displayer.font_size))
        
        if not self.isoriginal:
            self.key_func_layout = QHBoxLayout()
            self.key_func_layout.addWidget(self.keys_edit)
            self.key_func_layout.addWidget(self.lookup_func_box)

        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(self.isfocus_box)
        self.checkbox_layout.addWidget(self.isnew_box)
        self.checkbox_layout.addWidget(self.rainbow_box)

        self.display_layout = QHBoxLayout()
        self.display_layout.addWidget(self.displayer_func_box)
        self.display_layout.addWidget(self.font_box)
        self.display_layout.addWidget(self.fontsize_box)

        self.layout = QVBoxLayout()
        if not self.isoriginal:
            self.layout.addLayout(self.key_func_layout)
        self.layout.addWidget(self.main_text_edit)
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addLayout(self.display_layout)
        self.layout.addWidget(self.spec_rule_edit)
        self.layout.addWidget(self.format_string_edit)

    def setup_signals(self):
        if not self.isoriginal:
            self.keys_edit.returnPressed.connect(self.update_key_func_list)
            self.lookup_func_box.currentIndexChanged.connect(self.update_key_func_list)

        if self.isoriginal:
            self.displayer.highlight = False
            self.isfocus_box.setChecked(False)
            self.displayer.new_word = False
            self.isnew_box.setChecked(False)

        self.isfocus_box.stateChanged.connect(self.update_isfocus)
        self.isnew_box.stateChanged.connect(self.update_isnew)
        self.rainbow_box.stateChanged.connect(self.update_rainbow)
        self.spec_rule_edit.returnPressed.connect(self.update_spec_rule)
        self.format_string_edit.returnPressed.connect(self.update_format_string)
        self.font_box.currentIndexChanged.connect(self.update_font)
        self.fontsize_box.currentIndexChanged.connect(self.update_font_size)

    def refresh_display(self):        
        if self.isoriginal:
            self.main_text_edit.blockSignals(True)
            
        cursor = self.main_text_edit.textCursor()
        cursor_pos = cursor.position()
        vertical_scroll_pos = self.main_text_edit.verticalScrollBar().value()
        self.main_text_edit.setHtml(self.displayer.display(self.parent.split_text))
        cursor.setPosition(cursor_pos)
        self.main_text_edit.setTextCursor(cursor)
        self.main_text_edit.verticalScrollBar().setValue(vertical_scroll_pos)
        
        if self.isoriginal:
            self.main_text_edit.blockSignals(False)
            
    def update_key_func_list(self):
        if self.isoriginal:
            return
        self.displayer.key = self.keys_edit.text()
        self.parent.update_key_func_list()

    def update_isfocus(self):
        self.displayer.highlight = self.isfocus_box.isChecked()
        self.refresh_display()

    def update_isnew(self):
        self.displayer.new_word = self.isnew_box.isChecked()
        self.refresh_display()

    def update_rainbow(self):
        self.displayer.rainbow = self.rainbow_box.isChecked()
        self.refresh_display()

    def update_lookup(self):
        self.lookup_func_box.blockSignals(True)
        self.lookup_func_box.clear()
        self.lookup_func_box.addItems(self.parent.lookup.get_func_list())
        self.lookup_func_box.setEditable(False)
        self.lookup_func_box.setCurrentText(self.lookup_func_box.itemText(0))
        self.lookup_func_box.blockSignals(False)

    def update_spec_rule(self):
        self.displayer.parse_spec_rules(self.spec_rule_edit.text())
        self.refresh_spec_rule_edit()
        self.refresh_display()

    def update_format_string(self):
        self.displayer.set_format_string(self.format_string_edit.text())
        self.refresh_format_string_edit()
        self.refresh_display()

    def update_font(self):
        self.displayer.font = self.font_box.currentText()
        self.main_text_edit.setFont(QFont(self.displayer.font, self.displayer.font_size))

    def update_font_size(self):
        self.displayer.font_size = int(self.fontsize_box.currentText())
        self.main_text_edit.setFont(QFont(self.displayer.font, self.displayer.font_size))
    
    def refresh_spec_rule_edit(self):
        string = self.displayer.get_spec_rule()
        if string:
            self.spec_rule_edit.setText(string)
        else:
            self.spec_rule_edit.setPlaceholderText("特殊规则")

    def refresh_format_string_edit(self):
        string = self.displayer.format_string
        if string.strip() != "":
            self.format_string_edit.setText(string)
        else:
            self.format_string_edit.setPlaceholderText("格式化字符串")
        
class MainWindow(QMainWindow):
    def __init__(self, column_count = 3, splitter: SplitterEngine = None, lookup: LookupEngine = None, displayer: DisplayerEngine = None, splitter_funcs=None, lookup_funcs=None, lookup_general_funcs = None, displayer_funcs=None, shortcut_funcs = None, dictionary_file=None, font_list=None, cursor_follow = True):
        super().__init__()

        self.column_count = column_count
        self.splitter = splitter if splitter is not None else SplitterEngine()
        self.lookup = lookup if lookup is not None else LookupEngine()
        self.cursor_follow = cursor_follow
        self.loginfo = ''
        self.shortcut_dic = {}
        self.lookup.dictionary_file = dictionary_file if dictionary_file else None

        if displayer is None:
            self.displayers = [DisplayerEngine() for _ in range(column_count)]
        elif isinstance(displayer, DisplayerEngine):
            self.displayers = [displayer] * column_count
        elif isinstance(displayer, list):
            if len(displayer) == column_count and all([isinstance(d, DisplayerEngine) for d in displayer]):
                self.displayers = displayer
            else:
                raise ValueError("Wrong displays.")
        else:
            raise ValueError("Wrong displays.")
        if splitter_funcs:
            for func in splitter_funcs:
                self.splitter.introduce_func(func)
        if lookup_funcs:
            for func in lookup_funcs:
                self.lookup.introduce_func(func)
        if lookup_general_funcs:
            for func in lookup_general_funcs:
                self.lookup.introduce_gen_func(func)
        if displayer_funcs:
            for func in displayer_funcs:
                for displayer in self.displayers:
                    displayer.introduce_func(func)
        if shortcut_funcs:
            for func in shortcut_funcs:
                self.shortcut_dic[func.__name__] = (func,None)
        self.font_list = font_list if font_list else []
        self.split_text = self.splitter.split('')

        self.setWindowTitle("Text Processor")
        self.setGeometry(100, 100, 1000, 800)
        self.initUI()
        self.setup_signals()
        self.update_lookup()

    def initUI(self):
        self.columns = [Column(self, self.displayers[i], self.font_list, isoriginal=(i==0)) for i in range(self.column_count)]
        for idx, column in enumerate(self.columns):
            if not column.isoriginal:
                column.keys_edit.setText(f"列{idx+1}")

        self.dict_path_edit = QLineEdit()
        self.dict_path_edit.setPlaceholderText("词典路径")
        self.index_column_edit = QLineEdit()
        self.index_column_edit.setPlaceholderText("索引列")
        self.index_column_edit.setText(str(1))
        self.update_lookup_button = QPushButton("更新词典")
        self.clear_cache_button = QPushButton("清理缓存")
        self.cursor_follow_box = QCheckBox("光标跟踪")
        self.cursor_follow_box.setChecked(self.cursor_follow)
        
        self.splitter_func_box = QComboBox()
        self.splitter_func_box.addItems(self.splitter.get_splitter_dict())
        self.splitter_func_box.setCurrentText(self.splitter.get_splitter_name())
        self.splitter_func_box.setEditable(False)
        
        self.islang_regex_edit = QLineEdit()
        self.islang_regex_edit.setPlaceholderText("语言识别函数或正则字符串")
        self.splitter_lang_edit = QLineEdit()
        self.splitter_lang_edit.setPlaceholderText("当前语言")

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        
        self.shortcut_table = QTableWidget(len(self.shortcut_dic),2)
        self.shortcut_table.setHorizontalHeaderLabels(["函数", "快捷键"])
        header = self.shortcut_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.update_shortcut_table()

        text_layout = QHBoxLayout()
        for column in self.columns:
            text_layout.addLayout(column.layout)        

        splitter_layout = QHBoxLayout()
        splitter_layout.addWidget(self.splitter_func_box)
        splitter_layout.addWidget(self.islang_regex_edit)
        splitter_layout.setStretch(1,4) #伸缩比为4
        splitter_layout.addWidget(self.splitter_lang_edit)   
        splitter_layout.setStretch(2,1) #伸缩比为1（islang_regex_edit的1/4）
        splitter_layout.addWidget(self.cursor_follow_box) 
        
        

        lookup_layout = QHBoxLayout()
        lookup_layout.addWidget(self.dict_path_edit)
        lookup_layout.setStretch(0,4) #伸缩比为4
        lookup_layout.addWidget(self.index_column_edit)
        lookup_layout.setStretch(1,1) #伸缩比为1
        lookup_layout.addWidget(self.update_lookup_button)
        lookup_layout.addWidget(self.clear_cache_button)

        log_layout = QHBoxLayout()
        log_layout.addWidget(self.log_text_edit)
        log_layout.setStretch(0,3) #伸缩比为3
        log_layout.addWidget(self.shortcut_table)
        log_layout.setStretch(1,2) #伸缩比为1

        main_layout = QVBoxLayout()
        main_layout.addLayout(text_layout)
        main_layout.addLayout(splitter_layout)
        main_layout.addLayout(lookup_layout)
        main_layout.addLayout(log_layout)

        main_layout.setStretchFactor(text_layout, 4)
        main_layout.setStretchFactor(log_layout, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_signals(self):
        self.update_lookup_button.clicked.connect(self.update_lookup)
        self.clear_cache_button.clicked.connect(self.clear_cache)
        self.splitter_func_box.currentIndexChanged.connect(self.update_splitter)
        self.islang_regex_edit.returnPressed.connect(self.update_islang_regex)
        self.splitter_lang_edit.returnPressed.connect(self.update_splitter_lang)
        self.cursor_follow_box.stateChanged.connect(self.update_cursor_follow)
        self.shortcut_table.cellDoubleClicked.connect(self.on_shortcut_table_double_click)

        self.columns[0].isoriginal = True
        self.columns[0].main_text_edit.textChanged.connect(self.refresh_text)
        
        if self.cursor_follow:
            self.columns[0].main_text_edit.cursorPositionChanged.connect(self.on_cursor_moved)

    def update_shortcut_table(self):
        self.shortcut_table.setRowCount(len(self.shortcut_dic))
        for row, (func_name, (func, shortcut)) in enumerate(self.shortcut_dic.items()):
            self.shortcut_table.setItem(row,0,QTableWidgetItem(func_name))
            self.shortcut_table.setItem(row,1,QTableWidgetItem(shortcut.key().toString() if shortcut else ""))

    def update_lookup(self):
        try:
            try:
                dict_path = self.dict_path_edit.text()
                if not dict_path:
                    dict_path = ' '
                try:
                    index_column = int(self.index_column_edit.text())
                except Exception as e:
                    index_column = 1
                self.lookup.update_dictionary_file(dict_path, index_column)
            except Exception as e:
                raise e
            finally:
                self.dict_path_edit.setText(self.lookup.dictionary_file if self.lookup.dictionary_file else "")
                self.index_column_edit.setText(str(self.lookup.index_column))
                self.refresh_text()
                for idx,column in enumerate(self.columns):
                    if not column.isoriginal:
                        column.update_lookup()
                        if idx < column.lookup_func_box.count():
                            column.lookup_func_box.setCurrentIndex(idx)
                        else:
                            column.lookup_func_box.setCurrentIndex(column.lookup_func_box.count()-1)
                self.update_key_func_list() 
        except Exception as e:
            self.log_error(f"Error in update_lookup: {str(e)}")

    def clear_cache(self):
        try:
            self.lookup.clear_cache()
            self.refresh_text()
        except Exception as e:
            self.log_error(f"Error in clear_cache: {str(e)}")

    def update_splitter(self):
        try:
            func_name = self.splitter_func_box.currentText()
            self.splitter.set_splitter(func_name)
            self.refresh_text()
        except Exception as e:
            self.log_error(f"Error in update_splitter: {str(e)}")

    def update_islang_regex(self):
        try:
            regex = self.islang_regex_edit.text()
            self.splitter.set_is_lang_by_regex(regex)
            self.refresh_text()
        except Exception as e:
            self.log_error(f"Error in update_islang_regex: {str(e)}")

    def update_splitter_lang(self):
        try:
            lang = self.splitter_lang_edit.text()
            self.splitter.set_language(lang)
            self.refresh_text()
        except Exception as e:
            self.log_error(f"Error in update_splitter_lang: {str(e)}")

    def update_cursor_follow(self):
        try:
            self.cursor_follow = self.cursor_follow_box.isChecked()
            if self.cursor_follow:
                self.columns[0].main_text_edit.cursorPositionChanged.connect(self.on_cursor_moved)
            else:
                self.columns[0].main_text_edit.cursorPositionChanged.disconnect(self.on_cursor_moved)
        except Exception as e:
            self.log_error(f"Error in update_cursor_follow: {str(e)}")


    def refresh_text(self):
        try:
            text = self.columns[0].main_text_edit.toPlainText()
            self.split_text = self.splitter.split(text)
            self.lookup.lookup(self.split_text)
            self.refresh_columns()
        except Exception as e:
            self.log_error(f"Error in refresh_text: {str(e)}")
            raise e

    def refresh_columns(self):
        try:
            for column in self.columns:
                column.refresh_display()
        except Exception as e:
            self.log_error(f"Error in refresh_columns: {str(e)}")

    def on_cursor_moved(self):
        try:
            cursor = self.columns[0].main_text_edit.textCursor()
            cursor_pos = cursor.position()
            self.split_text.set_word_focus(cursor_pos)
            if self.columns[1:]:
                for column in self.columns[1:]:
                    column.refresh_display()
        except Exception as e:
            self.log_error(f"Error in refresh_columns: {str(e)}")

    def on_shortcut_table_double_click(self,row,column):
        try:
            main_text_edit = self.columns[0].main_text_edit
            func_name = self.shortcut_table.item(row,0).text()
            func = self.shortcut_dic[func_name][0]
            dialog = ShortcutEditor(func_name, self.shortcut_dic[func_name][1],self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_shortcut = dialog.key_sequence_edit.keySequence()
                try:
                    self.shortcut_dic[func_name][1].setParent(None)
                except:
                    pass
                if new_shortcut.toString():
                    shortcut_obj = QShortcut(new_shortcut,main_text_edit)
                    shortcut_obj.activated.connect(lambda func=func: self.on_text_key_press(func))
                    self.shortcut_dic[func_name] = (func,shortcut_obj)
                    
                else:
                    self.shortcut_dic[func_name] = (self.shortcut_dic[func_name][0],None)
                self.update_shortcut_table()
        except Exception as e:
            self.log_error(f"Error in on_shortcut_table_clicked: {str(e)}")

    def on_text_key_press(self, func):
        try:
            main_text_edit = self.columns[0].main_text_edit
            cursor = main_text_edit.textCursor()
            if cursor.hasSelection():
                selected_text = func(cursor.selectedText())
                cursor.insertText(selected_text)
        except Exception as e:
            self.log_error(f"Error in on_text_key_press: {str(e)}")

    def update_key_func_list(self):
        try:
            key_func_list = []
            for column in self.columns:
                if not column.isoriginal:
                    key = column.keys_edit.text().strip()
                    func = column.lookup_func_box.currentText().strip()
                    if key:
                        key_func_list.append((key, func))
            self.lookup.update_key_func_list(key_func_list)
            self.refresh_text()
        except Exception as e:
            self.log_error(f"Error in update_key_func_list: {str(e)}")
            

    def log_error(self, message):
        self.loginfo += message + "\n"
        self.log_text_edit.setPlainText(self.loginfo)
        import traceback
        print(traceback.print_exc())

def LangInterface(column_count = 3, splitter: SplitterEngine = None, lookup: LookupEngine = None, displayer: DisplayerEngine = None, splitter_funcs=None, lookup_funcs=None, lookup_general_funcs = None, displayer_funcs=None, shortcut_funcs = None, dictionary_file=None, font_list=None, cursor_follow = True):
    app = QApplication(sys.argv)
    window = MainWindow(column_count=column_count, splitter=splitter, lookup=lookup, displayer=displayer, splitter_funcs=splitter_funcs, lookup_funcs=lookup_funcs, lookup_general_funcs=lookup_general_funcs, displayer_funcs=displayer_funcs, shortcut_funcs=shortcut_funcs, dictionary_file=dictionary_file, font_list=font_list, cursor_follow=cursor_follow)
    window.show()
    sys.exit(app.exec())

#For test
if __name__ == "__main__":
    def set_sp(lemma):
	    if langdeterminer.is_punct(lemma.original[0]):
		    lemma.properties['space'] = 'space'   
    LangInterface(1,lookup_general_funcs=[set_sp])