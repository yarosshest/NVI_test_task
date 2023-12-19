import sys
from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    path = ''
    filename_edit = ''

    def choose_pdf(self):
        dialog = QFileDialog()

        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("*.pdf")
        filename, ok = dialog.exec()

        if filename:
            self.path = Path(filename)
            self.filename_edit = str(self.path)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF App")

        button = QPushButton()
        button.setCheckable(True)
        button.clicked.connect(self.choose_pdf)

        self.setFixedSize(QSize(400, 300))

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
