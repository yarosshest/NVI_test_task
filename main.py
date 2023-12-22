import sys
from typing import Callable
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

from Widgets.DrawablePdf import DrawablePdf


class ButtonChoosePdf(QPushButton):
    def __init__(self, choose_pdf: Callable):
        super().__init__()
        self.setText("Загрузить")
        self.setMaximumWidth(100)
        self.clicked.connect(choose_pdf)


class ButtonPage(QPushButton):

    def __init__(self, lable: str, new_page: Callable):
        super().__init__()
        self.setText(lable)
        self.setMaximumWidth(100)
        self.clicked.connect(new_page)


class MainWindow(QMainWindow):
    view: DrawablePdf = None

    def choose_pdf(self):
        dialog = QFileDialog()

        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("*.pdf")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.view.pdf.set_document(filename)

    def create_upper_layout(self) -> QHBoxLayout:
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(ButtonChoosePdf(self.choose_pdf))
        upper_layout.addWidget(ButtonPage("<", self.view.pdf.beck_page))
        upper_layout.addWidget(ButtonPage(">", self.view.pdf.forward_page))

        return upper_layout

    def _init_variables(self):
        self.view = DrawablePdf(self)

    def __init__(self):
        super().__init__()

        self._init_variables()

        self.setWindowTitle("PDF App")

        main_layout = QVBoxLayout()
        upper_layout = self.create_upper_layout()

        self.frameGeometry().width()
        self.frameGeometry().height()

        self.resize(QSize(300, 400))

        main_layout.addLayout(upper_layout)

        main_layout.addWidget(self.view)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
