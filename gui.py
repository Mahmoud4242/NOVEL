# gui.py
import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit, QProgressBar,
                             QFileDialog, QLabel, QCheckBox)
from scraper import Scraper
from translator import TextTranslator
from pdf_creator import PDFCreator
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    log_signal = pyqtSignal(str)

    def __init__(self, url, save_folder, translate, language):
        super().__init__()
        self.url = url
        self.save_folder = save_folder
        self.translate = translate
        self.language = language

    def run(self):
        scraper = Scraper(self.url)
        translator = TextTranslator(self.language) if self.translate else None
        pdf_creator = PDFCreator("Downloaded Novel")
        try:
            chapters = scraper.fetch_chapters()
            total = len(chapters)
            for i, (title, content) in enumerate(chapters.items()):
                self.log_signal.emit(f"Downloading chapter: {title}")
                if translator:
                    content = translator.translate(content)
                pdf_creator.add_chapter(title, content)
                self.progress.emit(int((i + 1) / total * 100))
            pdf_path = os.path.join(self.save_folder, "Novel.pdf")
            pdf_creator.save_pdf(pdf_path)
            self.log_signal.emit(f"Novel saved to {pdf_path}")
        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Novel Downloader")
        self.setGeometry(100, 100, 800, 600)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter novel URL")
        self.save_button = QPushButton("Choose Save Folder", self)
        self.download_button = QPushButton("Download Novel", self)
        self.log_output = QTextEdit(self)
        self.progress_bar = QProgressBar(self)
        self.translate_checkbox = QCheckBox("Translate to Arabic")
        self.folder_label = QLabel("Save to: Not Selected")

        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.translate_checkbox)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.save_button.clicked.connect(self.select_folder)
        self.download_button.clicked.connect(self.start_download)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            self.folder_label.setText(f"Save to: {folder}")
            self.save_folder = folder

    def start_download(self):
        url = self.url_input.text()
        if not hasattr(self, "save_folder"):
            self.log_output.append("Please select a save folder first.")
            return

        self.thread = DownloadThread(url, self.save_folder, self.translate_checkbox.isChecked(), "ar")
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.log_signal.connect(self.log_output.append)
        self.thread.start()
