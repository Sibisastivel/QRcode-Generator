from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QLineEdit, QComboBox, QFrame
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import Qt
import qrcode
from PIL import ImageQt
import sys

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 420, 500)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        # Create main layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)

        # Title label
        self.title_label = QLabel("QR Code Generator", self)
        self.title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.title_label.setStyleSheet("margin-bottom: 10px; color: #ecf0f1;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Text input field
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Enter text for QR code")
        self.input_text.setStyleSheet("""
            padding: 10px; 
            font-size: 14px; 
            border: 2px solid #3498db; 
            border-radius: 8px;
            background-color: white;
            color: black;
        """)
        self.layout.addWidget(self.input_text)

        # Size selection dropdown
        self.size_selector = QComboBox(self)
        self.size_selector.addItems(["Small (5)", "Medium (10)", "Large (15)", "Extra Large (20)"])
        self.size_selector.setCurrentIndex(1)  # Default to Medium (10)
        self.size_selector.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border-radius: 8px;
            background-color: white;
            color: black;
        """)
        self.layout.addWidget(self.size_selector)

        # Generate button
        self.generate_btn = QPushButton("Generate QR Code", self)
        self.generate_btn.clicked.connect(self.generate_qr)
        self.generate_btn.setStyleSheet("""
            padding: 10px; 
            font-size: 14px; 
            border-radius: 8px;
            background-color: #3498db; 
            color: white;
        """)
        self.layout.addWidget(self.generate_btn)

        # QR code display frame
        self.qr_frame = QFrame(self)
        self.qr_frame.setStyleSheet("border: 2px dashed #ecf0f1; padding: 10px;")
        self.qr_frame_layout = QVBoxLayout()
        self.qr_label = QLabel(self)
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_frame_layout.addWidget(self.qr_label)
        self.qr_frame.setLayout(self.qr_frame_layout)
        self.layout.addWidget(self.qr_frame)

        # Save button
        self.save_btn = QPushButton("Save QR Code", self)
        self.save_btn.clicked.connect(self.save_qr)
        self.save_btn.setStyleSheet("""
            padding: 10px; 
            font-size: 14px; 
            border-radius: 8px;
            background-color: #2ecc71; 
            color: white;
        """)
        self.layout.addWidget(self.save_btn)

        # Set main layout
        self.setLayout(self.layout)
        
        # Initialize the QR code image
        self.qr_image = None
        self.qr_color = "black"
    
    def generate_qr(self):
        text = self.input_text.text()
        size_mapping = {"Small (5)": 5, "Medium (10)": 10, "Large (15)": 15, "Extra Large (20)": 20}
        selected_size_text = self.size_selector.currentText()
        box_size = size_mapping[selected_size_text]  # Get corresponding box size
        
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=box_size,
                border=4
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            # Generate QR code with black color and white background
            img = qr.make_image(fill_color=self.qr_color, back_color="white")
            self.qr_image = img
            qimage = ImageQt.ImageQt(img)
            pixmap = QPixmap.fromImage(qimage)
            self.qr_label.setPixmap(pixmap)

            # Fix: Adjust window size dynamically based on QR code size
            self.adjustSize()
    
    def save_qr(self):
        if self.qr_image:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
            if file_path:
                self.qr_image.save(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec())
