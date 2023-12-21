from PyQt6.QtCore import QPoint
from fitz import open, Document


class PdfDrawer:
    doc: Document
    filename: str

    def __init__(self, filename: str):
        self.filename = filename
        self.doc = open(filename)

    def draw_rect(self, page_n: int, point_a: QPoint, point_b: QPoint, ):
        page = self.doc[page_n]

        page.draw_rect([point_a.x(), point_a.y(), point_b.x(), point_b.y()], color=(255, 0, 0), width=3)

        self.doc.save(self.filename)

