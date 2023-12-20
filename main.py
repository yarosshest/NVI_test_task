import sys
from pathlib import Path
from typing import Callable
from PyQt6.QtCore import QSize, QPointF, Qt
from PyQt6.QtGui import QPainter, QColor
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


class PdfView(QPdfView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setPageMode(QPdfView.PageMode.SinglePage)


class MainWindow(QMainWindow):
    path: Path = ''
    filename_edit: str = ''

    page: int = 0

    document: QPdfDocument = None
    view: QPdfView = None

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

            self.view.setDocument(self.document)

            self.view.show()

    def left_page(self):
        nav = self.view.pageNavigator()
        if nav.currentPage() > 0:
            nav.jump(nav.currentPage() - 1, QPointF(), nav.currentZoom())

    def right_page(self):
        nav = self.view.pageNavigator()
        if nav.currentPage() < self.view.document().pageCount() - 1:
            nav.jump(nav.currentPage() + 1, QPointF(), nav.currentZoom())

    def create_upper_layout(self) -> QHBoxLayout:
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(ButtonChoosePdf(self.choose_pdf))
        upper_layout.addWidget(ButtonPage("<", self.left_page))
        upper_layout.addWidget(ButtonPage(">", self.right_page))

        return upper_layout

    def _init_variables(self):
        self.document = QPdfDocument(self)

    def __init__(self):
        super().__init__()

        self._init_variables()

        self.setWindowTitle("PDF App")

        main_layout = QVBoxLayout()
        upper_layout = self.create_upper_layout()

        self.frameGeometry().width()
        self.frameGeometry().height()

        self.resize(QSize(1000, 1000))

        main_layout.addLayout(upper_layout)

        self.view = PdfView(self)
        main_layout.addWidget(self.view)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
