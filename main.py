# -*- coding: utf-8 -*-
import sys
import re

from PyQt5 import QtWidgets, QtGui, QtCore

from analyzer.view import ANTLRTreeView
from resources import qInitResources

from interpreter import SetInterpreter


class InterpreterUI(QtWidgets.QMainWindow):

    DIPLOMA_NAME = "Операції над множинами"

    ICON_PATH = ":/images/empty-set.jpg"

    OPEN_PATH = ":/images/open.png"
    SAVE_PATH = ":/images/save.png"

    COPY_PATH = ":/images/copy.png"
    CUT_PATH = ":/images/cut.png"
    PASTE_PATH = ":/images/paste.png"

    ANALYZE_PATH = ":/images/analyze.png"

    SAVE_FORMAT = ".sol"

    def __init__(self):
        super().__init__()

        self.interpreter = SetInterpreter()
        self.interpreter_io = []

        self.filename = ""
        self.changes_saved = True

        self._input = self._output = None
        
        self._new_action = self._open_action = self._save_action = None

        self._copy_action = self._cut_action = self._paste_action = None
        self._analyze_action = None

        self._toolbar = None

        self._general_layout = self._central_widget = None

        self.build_ui()

    def build_toolbar(self):

        self._open_action = QtWidgets.QAction(QtGui.QIcon(self.OPEN_PATH), "Відкрити файл", self)
        self._open_action.setStatusTip("Відкрити існуючий документ")
        self._open_action.setShortcut("Ctrl+O")
        self._open_action.triggered.connect(self.open_program_and_run)

        self._save_action = QtWidgets.QAction(QtGui.QIcon(self.SAVE_PATH), "Зберегти", self)
        self._save_action.setStatusTip("Зберегти документ")
        self._save_action.setShortcut("Ctrl+S")
        self._save_action.triggered.connect(self.save_program)

        self._copy_action = QtWidgets.QAction(QtGui.QIcon(self.COPY_PATH), "Копіювати", self)
        self._copy_action.setStatusTip("Копіювати текст")
        self._copy_action.setShortcut("Ctrl+C")
        self._copy_action.triggered.connect(self._output.copy)

        self._paste_action = QtWidgets.QAction(QtGui.QIcon(self.PASTE_PATH), "Вставити", self)
        self._paste_action.setStatusTip("Вставити раніше скопійований текст")
        self._paste_action.setShortcut("Ctrl+V")
        self._paste_action.triggered.connect(self._input.paste)

        self._analyze_action = QtWidgets.QAction(QtGui.QIcon(self.ANALYZE_PATH), "Аналізувати", self)
        self._analyze_action.setStatusTip("Побудувати дерево розбору рядка")
        self._analyze_action.triggered.connect(self.analyze_code)

        self._toolbar = QtWidgets.QToolBar("Налаштування")
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self._toolbar)

        self._toolbar.addAction(self._open_action)
        self._toolbar.addAction(self._save_action)

        self._toolbar.addSeparator()

        self._toolbar.addAction(self._cut_action)
        self._toolbar.addAction(self._copy_action)
        self._toolbar.addAction(self._paste_action)

        self._toolbar.addSeparator()
        self._toolbar.addAction(self._analyze_action)

        self._toolbar.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    @classmethod
    def get_font(cls, **options):
        font = QtGui.QFont()
        font.setBold(options.get("bold", True))
        font.setFamily(options.get("font", "Times New Roman"))
        font.setPointSize(options.get("size", 20))
        return font

    def build_ui(self):

        self._general_layout = QtWidgets.QVBoxLayout()
        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self._general_layout)

        self._input = QtWidgets.QLineEdit(self)
        self._input.setFixedHeight(35)
        self._input.setFont(self.get_font())
        self._input.setAlignment(QtCore.Qt.AlignLeft)

        self._input.returnPressed.connect(self.input_submit)
        self._input.textChanged[str].connect(self.text_changed)
        self.text_changed("")

        self._output = QtWidgets.QTextEdit(self)
        self._output.setTabStopWidth(33)
        self._output.setFont(self.get_font(size=13))
        self._output.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse |
                                             QtCore.Qt.TextSelectableByKeyboard)

        self._general_layout.addWidget(self._input)
        self._general_layout.addWidget(self._output)

        self.build_toolbar()

        self.setGeometry(200, 50, 800, 600)
        self.setWindowTitle(self.DIPLOMA_NAME)
        self.setWindowIcon(QtGui.QIcon(self.ICON_PATH))

    def closeEvent(self, event):

        if self.changes_saved:
            return event.accept()

        popup = QtWidgets.QMessageBox(self)

        popup.setIcon(QtWidgets.QMessageBox.Warning)
        popup.setWindowTitle(self.DIPLOMA_NAME)

        popup.setText("Додкумент змнінено!")

        popup.setInformativeText("Ви бажаєте зберегти зміни?")

        popup.setStandardButtons(QtWidgets.QMessageBox.Save |
                                 QtWidgets.QMessageBox.Cancel |
                                 QtWidgets.QMessageBox.Discard)

        popup.setDefaultButton(QtWidgets.QMessageBox.Save)

        answer = popup.exec_()

        if answer == QtWidgets.QMessageBox.Save:
            self.save_program()
        elif answer == QtWidgets.QMessageBox.Discard:
            event.accept()
        else:
            event.ignore()

    def analyze_error_answer(self, error_text):
        popup = QtWidgets.QMessageBox(self)

        popup.setIcon(QtWidgets.QMessageBox.Warning)
        popup.setWindowTitle(self.DIPLOMA_NAME)

        popup.setText("Увага!")

        popup.setInformativeText(error_text)

        popup.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        popup.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        popup.exec_()

    def analyze_code(self):
        pos = self._output.textCursor().blockNumber()
        output_lines = self._output.toPlainText().split("\n")

        if pos + 1 > len(output_lines):
            return self.analyze_error_answer("Некоректно вибраний рядок для аналізу.")

        code_line = output_lines[pos]

        if not re.match(r'In\[(?:\d+)\]', code_line):
            return self.analyze_error_answer("Можливо аналізувати тільки вхідні дані.")

        operation_no = int(re.findall(r'\d+', code_line)[0])

        _input, _result, _success = self.interpreter_io[operation_no - 1]

        if not _success:
            return self.analyze_error_answer("Можливо аналізувати тільки вірні конструкції.")

        try:
            tk = ANTLRTreeView(_input + "\r\n")
            tk.mainloop()
        except Exception as e:
            return self.analyze_error_answer(str(e))

    def save_program(self):

        if not self.interpreter_io:
            return

        if not self.filename:
            self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Зберегти файл')[0]

        if self.filename:

            if not self.filename.endswith(self.SAVE_FORMAT):
                self.filename += self.SAVE_FORMAT

            with open(self.filename, "w+") as file:
                file.write("\n".join([op[0] for op in self.interpreter_io if op[2]]) + "\n")

            self.changes_saved = True

    def open_program_and_run(self):

        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Відкрити файл',
                                                              ".", "(*{})".format(self.SAVE_FORMAT))[0]

        if self.filename:
            with open(self.filename, "r") as file:
                self.clear_all()
                for line in file.readlines():
                    self.run_interpretation(line.strip())

    def clear_all(self):
        self.interpreter = SetInterpreter()
        self.interpreter_io = []
        self.clear_input()
        self._output.setText("")

    def print_line(self,
                   _text,
                   _row,
                   _type="in",
                   _style="success"
                   ):

        assert _type in ("in", "out")
        assert _style in ("success", "error")

        operation_colors = {"in": "green", "out": "orange"}
        text_colors = {
            "default": "rgb(87, 173, 104)",
            "error": "red",
            "comment": "rgb(122, 122, 122)",
        }
        output = """
        <span style="font-size:12pt; font-weight:700; color: {operation_color};">{operation}[{row}]: </span> 
        <span style="font-size:12pt; font-weight:500; color: {text_color};"> {text_result}</span>
        """.format(operation_color=operation_colors.get(_type), operation=_type.capitalize(), row=_row,
                   text_color=text_colors.get(_style), text_result=_text)

        self._output.append(output)

    def clear_input(self):
        self._input.setText("")

    def input_submit(self):
        self.run_interpretation(self._input.text())
        self.changes_saved = False

    def run_interpretation(self, _input):
        result, success = self.interpreter(_input)

        self.interpreter_io.append((_input if not success else self.interpreter.format(_input), result, success))
        operation_no = len(self.interpreter_io)

        self.print_line(_input, operation_no)

        if result is None:
            return self.clear_input()

        if not success:
            self.print_line(result, operation_no, _type="out", _style="error")
            return self.clear_input()

        if _input.startswith(SetInterpreter.COMMENT_SYMBOL):
            self._output.append("\n")
            return self.clear_input()

        self.print_line(result, operation_no, _type="out")
        return self.clear_input()

    def set_input_color(self, *color):
        assert isinstance(color, (tuple, list)) and len(color) == 3
        self._input.setStyleSheet("""
            border-color: rgb(18, 18, 18);
            color: {};
            font: bold "Times New Roman";
        """.format(QtGui.QColor(*color).name()))

    def text_changed(self, text):
        if text.startswith(SetInterpreter.COMMENT_SYMBOL):
            self.set_input_color(122, 122, 122)
        elif text.startswith(SetInterpreter.PRINT_SYMBOL):
            self.set_input_color(87, 173, 104)
        else:
            self.set_input_color(27, 121, 173)


if __name__ == '__main__':

    qInitResources()

    app = QtWidgets.QApplication(sys.argv)

    ui = InterpreterUI()
    ui.show()

    sys.exit(app.exec_())
