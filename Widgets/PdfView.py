from PyQt6.QtCore import QPointF, QMargins, QSize
from PyQt6.QtPdf import QPdfDocument, QPdfPageNavigator
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget

from UseCase.DrawInPdf import PdfDrawer


class PdfView(QPdfView):
    document: QPdfDocument = None
    doc_loaded: bool = False
    filename: str = None
    nav: QPdfPageNavigator = None
    drawer: PdfDrawer = None

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.document = QPdfDocument(self)
        self.setPageMode(QPdfView.PageMode.SinglePage)
        self.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.setDocumentMargins(QMargins(0, 0, 0, 0))

        self.nav = self.pageNavigator()

    def resize_view(self):
        size = self.document.pagePointSize(self.nav.currentPage())
        self.setFixedSize(QSize(int(size.width() * 1.3333), int(size.height() * 1.333)))

    def set_document(self, filename: str):
        self.filename = filename
        self.document.load(filename)

        self.setDocument(self.document)
        self.doc_loaded = True
        self.drawer = PdfDrawer(filename)

        self.resize_view()

        self.show()

    def update_document(self):
        self.document.load(self.filename)

    def beck_page(self):
        if self.nav.currentPage() > 0:
            self.nav.jump(self.nav.currentPage() - 1, QPointF(), self.nav.currentZoom())

            self.resize_view()

    def forward_page(self):
        if self.nav.currentPage() < self.document.pageCount() - 1:
            self.nav.jump(self.nav.currentPage() + 1, QPointF(), self.nav.currentZoom())

            self.resize_view()
