from PyQt6.QtCore import QPointF, Qt, QPoint, QRect
from PyQt6.QtGui import QMouseEvent, QPaintEvent, QColor, QPalette, QPainter, QPen, QBrush
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.uic.Compiler.qtproxies import QtGui, QtCore

from Widgets.PdfView import PdfView
from Widgets.Overlay import Overlay


class DrawablePdf(QWidget):
    pdf: PdfView

    def __init__(self, parent=None):
        super(DrawablePdf, self).__init__(parent)

        self.pdf = PdfView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.pdf)

        self.overlay = Overlay(self.pdf)

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()
