from PyQt6.QtCore import QPointF, QMargins
from PyQt6.QtPdf import QPdfDocument, QPdfPageNavigator
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QWidget


class PdfView(QPdfView):
    document: QPdfDocument = None
    doc_loaded: bool = False
    filename: str = None
    nav: QPdfPageNavigator = None

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.document = QPdfDocument(self)
        self.setPageMode(QPdfView.PageMode.SinglePage)
        self.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.setDocumentMargins(QMargins(0, 0, 0, 0))

    def set_document(self, filename: str):
        self.filename = filename
        self.document.load(filename)

        self.setDocument(self.document)
        self.doc_loaded = True

        self.show()

    def beck_page(self):
        nav = self.pageNavigator()
        if nav.currentPage() > 0:
            nav.jump(nav.currentPage() - 1, QPointF(), nav.currentZoom())

    def forward_page(self):
        nav = self.pageNavigator()
        if nav.currentPage() < self.document.pageCount() - 1:
            nav.jump(nav.currentPage() + 1, QPointF(), nav.currentZoom())
