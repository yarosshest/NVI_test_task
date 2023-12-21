from PyQt6.QtCore import QPointF, Qt, QPoint, QRect
from PyQt6.QtGui import QMouseEvent, QPaintEvent, QColor, QPalette, QPainter, QPen, QBrush
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.uic.Compiler.qtproxies import QtGui, QtCore


class PdfView(QPdfView):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setPageMode(QPdfView.PageMode.SinglePage)

    def beck_page(self):
        nav = self.pageNavigator()
        if nav.currentPage() > 0:
            nav.jump(nav.currentPage() - 1, QPointF(), nav.currentZoom())

    def forward_page(self):
        nav = self.pageNavigator()
        if nav.currentPage() < self.document().pageCount() - 1:
            nav.jump(nav.currentPage() + 1, QPointF(), nav.currentZoom())


class Overlay(QWidget):
    begin_rec: QPoint = None
    end_rec: QPoint = None
    left_mouse_pressed: bool = False

    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.show()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.left_mouse_pressed:
            self.end_rec = QPoint(event.pos().x(), event.pos().y())
            self.paint_user_rect()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_mouse_pressed = True
            self.begin_rec = QPoint(event.pos().x(), event.pos().y())
            self.end_rec = None

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_mouse_pressed = False
            self.end_rec = QPoint(event.pos().x(), event.pos().y())
            self.paint_user_rect()

    def paint_user_rect(self):
        print("painy")
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(168, 34, 3))
        qp.drawRect(QRect(self.begin_rec, self.end_rec))
        qp.end()


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
