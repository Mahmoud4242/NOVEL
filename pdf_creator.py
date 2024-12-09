# pdf_creator.py
from fpdf import FPDF

class PDFCreator:
    def __init__(self, title):
        self.pdf = FPDF()
        self.title = title
        self.create_cover_page()

    def create_cover_page(self):
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, self.title, ln=True, align="C")

    def add_chapter(self, chapter_title, content):
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.pdf.multi_cell(0, 10, f"{chapter_title}\n\n{content}")

    def save_pdf(self, file_path):
        self.pdf.output(file_path)
