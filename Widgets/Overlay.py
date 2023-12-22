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

        parent.nav.currentPageChanged.connect(self.clear_rect)

        self.setAutoFillBackground(False)
        self.pen.setWidth(3)
        self.show()

    def clear_rect(self):
        self.begin_rec = None
        self.end_rec = None
        self.left_mouse_pressed = False

    def update_end(self, event: QMouseEvent):
        if (0 < event.pos().x() < self.size().width() and
                0 < event.pos().y() < self.size().height()):
            self.end_rec = QPoint(event.pos().x(), event.pos().y())
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.parent().doc_loaded:
            if self.left_mouse_pressed:
                self.update_end(event)

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
                self.update_end(event)
                self.parent().drawer.draw_rect(self.parent().nav.currentPage(), self.begin_rec, self.end_rec)
                self.parent().update_document()

    def paintEvent(self, event: QPaintEvent):
        if self.end_rec:
            self.painter.begin(self)
            self.painter.setPen(self.pen)
            self.painter.drawRect(QRect(self.begin_rec, self.end_rec))
            self.painter.end()
