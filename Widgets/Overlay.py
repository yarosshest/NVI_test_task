from PyQt6.QtCore import QPointF, Qt, QPoint, QRect
from PyQt6.QtGui import QMouseEvent, QPaintEvent, QColor, QPalette, QPainter, QPen, QBrush
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.uic.Compiler.qtproxies import QtGui, QtCore

from Widgets.DrawablePdf import PdfView


class Overlay(QWidget):
    begin_rec: QPoint | None = None
    end_rec: QPoint | None = None
    left_mouse_pressed: bool = False
    painter: QPainter = QPainter()
    pen: QPen = QPen(QColor(255, 0, 0))

    def __init__(self, parent: PdfView):
        super(Overlay, self).__init__(parent)
        self.setAutoFillBackground(False)

        self.pen.setWidth(3)

        self.show()



    def mouseMoveEvent(self, event: QMouseEvent):
        if self.parent().doc_loaded:
            if self.left_mouse_pressed:
                self.end_rec = QPoint(event.pos().x(), event.pos().y())
                self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.parent().doc_loaded:
            if event.button() == Qt.MouseButton.LeftButton:
                self.left_mouse_pressed = True
                self.begin_rec = QPoint(event.pos().x(), event.pos().y())
                self.end_rec = None

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.parent().doc_loaded:
            if event.button() == Qt.MouseButton.LeftButton:
                self.left_mouse_pressed = False
                self.end_rec = QPoint(event.pos().x(), event.pos().y())

    def paintEvent(self, event: QPaintEvent):
        if self.end_rec:
            self.painter.begin(self)
            self.painter.setPen(self.pen)
            self.painter.drawRect(QRect(self.begin_rec, self.end_rec))
            self.painter.end()