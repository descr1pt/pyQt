from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QFile, QCoreApplication
import fitz  # PyMuPDF
import sys


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Load button
        self.load_button = QPushButton('Load PDF', self)
        self.load_button.clicked.connect(self.open_pdf)
        self.layout.addWidget(self.load_button)

        # Navigation buttons at the top
        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton('Previous', self)
        self.prev_button.clicked.connect(self.show_previous_page)
        self.nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.show_next_page)
        self.nav_layout.addWidget(self.next_button)

        # Add the navigation button layout to the main layout
        self.layout.addLayout(self.nav_layout)

        # Label for displaying the PDF page
        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.current_page = 0
        self.document = None

    def open_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_name:
            self.document = fitz.open(file_name)
            self.show_page()

    def show_page(self):
        page = self.document[self.current_page]
        pixmap = page.get_pixmap()

        # Save the pixmap to a temporary file
        temp_filename = "temp.png"
        pixmap.save(temp_filename, "PNG")

        # Load the temporary file into a QPixmap
        temp_pixmap = QPixmap(temp_filename)
        self.label.setPixmap(temp_pixmap)

        # Clean up the temporary file
        QCoreApplication.processEvents()
        QFile(temp_filename).remove()

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def show_next_page(self):
        if self.current_page < len(self.document) - 1:
            self.current_page += 1
            self.show_page()

if __name__ == '__main__':
    app = QApplication([])
    pdf_viewer = PDFViewer()
    pdf_viewer.show()
    app.exec_()
