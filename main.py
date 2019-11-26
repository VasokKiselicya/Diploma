# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

import resources

from interpreter import interpreter


class InterpreterUI(QtWidgets.QMainWindow):

    DIPLOMA_NAME = "Операції над множинами"

    ICON_PATH = ":/images/empty-set.jpg"

    NEW_PATH = ":/images/new.png"
    OPEN_PATH = ":/images/open.png"
    SAVE_PATH = ":/images/save.png"

    COPY_PATH = ":/images/copy.png"
    CUT_PATH = ":/images/cut.png"
    PASTE_PATH = ":/images/paste.png"

    def __init__(self):
        super().__init__()

        self.filename = ""
        self.changes_saved = True

        self._input = self._output = None
        
        self._new_action = self._open_action = self._save_action = None

        self._copy_action = self._cut_action = self._paste_action = None
        
        self._toolbar = None

        self._general_layout = self._central_widget = None

        self.build_ui()

    def build_toolbar(self):

        setattr(self, '_new_action', QtWidgets.QAction(QtGui.QIcon(self.NEW_PATH), "Новий файл", self))

        self._new_action.setShortcut("Ctrl+N")
        self._new_action.setStatusTip("Створити новий документ")
        # self.newAction.triggered.connect(self.new)

        self._open_action = QtWidgets.QAction(QtGui.QIcon(self.OPEN_PATH), "Відкрити файл", self)
        self._open_action.setStatusTip("Відкрити існуючий документ")
        self._open_action.setShortcut("Ctrl+O")
        # self._open_action.triggered.connect(self.open)

        self._save_action = QtWidgets.QAction(QtGui.QIcon(self.SAVE_PATH), "Зберегти", self)
        self._save_action.setStatusTip("Зберегти документ")
        self._save_action.setShortcut("Ctrl+S")
        # self._save_action.triggered.connect(self.save)

        self._copy_action = QtWidgets.QAction(QtGui.QIcon(self.COPY_PATH), "Копіювати", self)
        self._copy_action.setStatusTip("Копіювати текст")
        self._copy_action.setShortcut("Ctrl+C")
        self._copy_action.triggered.connect(self._input.copy)

        self._cut_action = QtWidgets.QAction(QtGui.QIcon(self.CUT_PATH), "Вирізати", self)
        self._cut_action.setStatusTip("Видалити та скопіювати текст")
        self._cut_action.setShortcut("Ctrl+X")
        self._cut_action.triggered.connect(self._input.cut)

        self._paste_action = QtWidgets.QAction(QtGui.QIcon(self.PASTE_PATH), "Вставити", self)
        self._paste_action.setStatusTip("Вставити раніше скопійований текст")
        self._paste_action.setShortcut("Ctrl+V")
        self._paste_action.triggered.connect(self._input.paste)

        self._toolbar = QtWidgets.QToolBar("Налаштування")
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self._toolbar)

        self._toolbar.addAction(self._new_action)
        self._toolbar.addAction(self._open_action)
        self._toolbar.addAction(self._save_action)

        self._toolbar.addSeparator()

        self._toolbar.addAction(self._cut_action)
        self._toolbar.addAction(self._copy_action)
        self._toolbar.addAction(self._paste_action)

        self._toolbar.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    def build_ui(self):

        self._general_layout = QtWidgets.QVBoxLayout()
        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self._general_layout)

        self._input = QtWidgets.QLineEdit(self)
        self._input.setFixedHeight(35)
        self._input.setAlignment(QtCore.Qt.AlignRight)

        self._input.textChanged[str].connect(self.text_changed)
        self.text_changed("")

        self._output = QtWidgets.QTextEdit(self)
        self._output.setTabStopWidth(33)
        self._output.setReadOnly(True)

        self._general_layout.addWidget(self._input)
        self._general_layout.addWidget(self._output)

        self.build_toolbar()

        self.setGeometry(200, 50, 800, 600)
        self.setWindowTitle(self.DIPLOMA_NAME)
        self.setWindowIcon(QtGui.QIcon(self.ICON_PATH))
        # interpreter()

    def set_input_color(self, *color):
        assert isinstance(color, (tuple, list)) and len(color) == 3
        self._input.setStyleSheet("""
            border-color: rgb(18, 18, 18);
            color: {};
            font: bold "Times New Roman";
        """.format(QtGui.QColor(*color).name()))

    def text_changed(self, text):
        if text.startswith(interpreter.COMMENT_SYMBOL):
            self.set_input_color(50, 50, 50)
        elif text.startswith(interpreter.PRINT_SYMBOL):
            self.set_input_color(87, 173, 104)
        else:
            self.set_input_color(27, 121, 173)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    ui = InterpreterUI()
    ui.show()
    sys.exit(app.exec_())
