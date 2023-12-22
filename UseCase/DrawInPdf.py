from PyQt6.QtCore import QPoint
from fitz import open, Document, Rect, Point
from fitz.utils import getColor


def create_rect(point_a: QPoint, point_b: QPoint) -> Rect:
    if point_a.x() > point_b.x():
        buf = point_a
        point_a = point_b
        point_b = buf

    if point_a.y() > point_b.y():
        buf_y = point_a.y()
        point_a.setY(point_b.y())
        point_b.setY(buf_y)

    inc = 1

    return Rect(Point(point_a.x()*0.75, point_a.y()*0.75),
                Point(point_b.x()*0.75 + inc, point_b.y()*0.75 + inc))


class PdfDrawer:
    doc: Document
    filename: str

    def __init__(self, filename: str):
        self.filename = filename
        self.doc = open(filename)

    def draw_rect(self, page_n: int, point_a: QPoint, point_b: QPoint):
        page = self.doc[page_n]

        # page.draw_rect(Rect(point_a.x(), point_a.y(), point_b.x(), point_b.y()), color=(255, 0, 0), width=3)
        page.draw_rect(create_rect(point_a, point_b), width=3, color=getColor("red"))

        self.doc.save(self.filename, incremental=True, encryption=0)
        self.doc = open(self.filename)
