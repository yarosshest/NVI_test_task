import sys
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtPdf import QPdfDocument, QPdfPageNavigator
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout


class ButtonChoosePdf(QPushButton):
    def __init__(self, choose_pdf: Callable):
        super().__init__()
        self.setCheckable(True)
        self.setText("Загрузить")
        self.clicked.connect(choose_pdf)


class ButtonPage(QPushButton):

    def __init__(self, lable: str, new_page: Callable):
        super().__init__()
        self.setCheckable(True)
        self.setText(lable)
        self.clicked.connect(new_page)


class MainWindow(QMainWindow):
    path: Path = ''
    filename_edit: str = ''

    page: int = 0
    page_navigator: QPdfPageNavigator = None

    document: QPdfDocument = None
    view: QPdfView = None

    def create_button_choose_pdf(self) -> QPushButton:
        button = QPushButton()
        button.setCheckable(True)
        button.setText("Загрузить")
        button.clicked.connect(self.choose_pdf)

        self.document = QPdfDocument(self)
        return button

    def create_button_left(self) -> QPushButton:
        button = QPushButton()
        button.setCheckable(True)
        button.setText("<")
        button.clicked.connect(self.choose_pdf)

        self.document = QPdfDocument(self)
        return button

    def choose_pdf(self):
        dialog = QFileDialog()

        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("*.pdf")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.path = Path(filename)
            self.filename_edit = str(self.path)
            self.document.load(self.filename_edit)
            self.page = 0

            self.view.show()

    def create_pdf_view(self) -> QPdfView:
        view = QPdfView(None)
        view.setPageMode(QPdfView.PageMode.SinglePage)
        view.setDocument(self.document)
        self.page_navigator = view.pageNavigator()
        return view

    def left_page(self):
        self.page_navigator.back()
        self.page_navigator.update()

    def right_page(self):
        self.page_navigator.forward()

    def create_upper_layout(self) -> QHBoxLayout:
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(ButtonChoosePdf(self.choose_pdf))
        upper_layout.addWidget(ButtonPage("<", self.left_page))
        upper_layout.addWidget(ButtonPage(">", self.right_page))

        return upper_layout

    def _init_variables(self):
        self.document = QPdfDocument(self)

        view = QPdfView(None)
        view.setPageMode(QPdfView.PageMode.SinglePage)
        view.setDocument(self.document)

    def __init__(self):
        super().__init__()

        self.page_navigator = None
        self._init_variables()

        self.setWindowTitle("PDF App")

        main_layout = QVBoxLayout()
        upper_layout = self.create_upper_layout()

        self.setFixedSize(QSize(1000, 500))

        main_layout.addLayout(upper_layout)
        self.view = self.create_pdf_view()
        main_layout.addWidget(self.view)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
