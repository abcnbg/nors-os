#!/usr/bin/env python3
# NorsInstaller - Elegant Graphical OS Installer
# License: GPLv3
# Description: A visually stunning, multi-step installation wizard for NORS OS.

import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QStackedWidget, 
                             QLineEdit, QComboBox, QProgressBar, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush, QPainter
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QRect

# Mock Installation Worker
class InstallWorker(QThread):
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal()

    def run(self):
        steps = [
            (5, "Formatting partitions..."),
            (15, "Mounting target filesystem..."),
            (30, "Unpacking base system..."),
            (50, "Installing NORS Core components..."),
            (65, "Deploying Cyber Security tools..."),
            (80, "Configuring NorsDream Desktop..."),
            (90, "Installing bootloader (GRUB)..."),
            (98, "Cleaning up..."),
            (100, "Installation Complete!")
        ]
        
        for val, msg in steps:
            time.sleep(2) # Simulate work
            self.progress_signal.emit(val, msg)
            
        self.finished_signal.emit()


class NorsInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🦅 Nors OS Setup")
        self.setGeometry(100, 100, 1000, 650)
        self.setWindowFlags(Qt.FramelessWindowHint) # Frameless for modern look

        # Global Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A192F;
            }
            QLabel {
                color: #E6F1FF;
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }
            QPushButton {
                background-color: #00B4D8;
                color: #0A192F;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #48CAE4;
            }
            QPushButton:disabled {
                background-color: #233554;
                color: #8892B0;
            }
            QLineEdit {
                background-color: #112240;
                border: 2px solid #233554;
                border-radius: 5px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #00B4D8;
            }
            QProgressBar {
                border: 2px solid #233554;
                border-radius: 10px;
                text-align: center;
                color: white;
                background-color: #112240;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #0077B6, stop: 1 #00B4D8);
                border-radius: 8px;
            }
        """)

        # Main Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Bar
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: rgba(17, 34, 64, 0.9);")
        header_layout = QHBoxLayout(header)
        title = QLabel("🦅 NORS OS INSTALLER")
        title.setFont(QFont("Cairo", 14, QFont.Bold))
        header_layout.addWidget(title)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet("background-color: transparent; color: white; font-size: 18px;")
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn, alignment=Qt.AlignRight)
        
        main_layout.addWidget(header)

        # Content Area (Stacked Widget for wizard steps)
        self.stack = QStackedWidget()
        self.setup_pages()
        main_layout.addWidget(self.stack)

        # Footer Bar (Navigation)
        footer = QFrame()
        footer.setFixedHeight(80)
        footer.setStyleSheet("background-color: #112240; border-top: 1px solid #233554;")
        footer_layout = QHBoxLayout(footer)
        
        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self.prev_page)
        self.back_btn.hide()
        
        self.next_btn = QPushButton("Next →")
        self.next_btn.clicked.connect(self.next_page)
        
        footer_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        footer_layout.addStretch()
        footer_layout.addWidget(self.next_btn, alignment=Qt.AlignRight)
        
        main_layout.addWidget(footer)

        self.setCentralWidget(central_widget)

    def setup_pages(self):
        # Page 1: Welcome
        page1 = QWidget()
        layout1 = QVBoxLayout(page1)
        
        welcome_title = QLabel("Welcome to the Future of Security")
        welcome_title.setFont(QFont("Cairo", 36, QFont.Bold))
        welcome_title.setAlignment(Qt.AlignCenter)
        welcome_title.setStyleSheet("color: #00B4D8;")
        
        subtitle = QLabel("Prepare to install the ultimate Penetration Testing & Reverse Engineering OS.")
        subtitle.setFont(QFont("Inter", 16))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #8892B0; margin-bottom: 30px;")
        
        lang_combo = QComboBox()
        lang_combo.addItems(["English (US)", "Arabic (العربية)", "French", "Spanish"])
        lang_combo.setFixedWidth(300)
        lang_combo.setStyleSheet("background-color: #112240; color: white; padding: 10px; font-size: 16px; border: 1px solid #00B4D8;")
        
        layout1.addStretch()
        layout1.addWidget(welcome_title)
        layout1.addWidget(subtitle)
        layout1.addWidget(lang_combo, alignment=Qt.AlignHCenter)
        layout1.addStretch()
        self.stack.addWidget(page1)

        # Page 2: Disk & Partitioning
        page2 = QWidget()
        layout2 = QVBoxLayout(page2)
        
        disk_title = QLabel("Where should we install NORS?")
        disk_title.setFont(QFont("Cairo", 24, QFont.Bold))
        disk_title.setAlignment(Qt.AlignCenter)
        
        # Mock Disk Display
        disk_frame = QFrame()
        disk_frame.setFixedSize(600, 150)
        disk_frame.setStyleSheet("background-color: #112240; border: 2px solid #00B4D8; border-radius: 10px;")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 180, 216, 100))
        disk_frame.setGraphicsEffect(shadow)
        
        df_layout = QVBoxLayout(disk_frame)
        df_layout.addWidget(QLabel("🖴 /dev/sda - 500 GB NVMe SSD", styleSheet="font-size: 18px; font-weight: bold;"))
        df_layout.addWidget(QLabel("Erase entire disk and install NORS OS.", styleSheet="color: #8892B0;"))
        
        layout2.addStretch()
        layout2.addWidget(disk_title)
        layout2.addWidget(disk_frame, alignment=Qt.AlignHCenter)
        layout2.addStretch()
        self.stack.addWidget(page2)

        # Page 3: User Setup
        page3 = QWidget()
        layout3 = QVBoxLayout(page3)
        layout3.setAlignment(Qt.AlignCenter)
        
        user_title = QLabel("Create Your Identity")
        user_title.setFont(QFont("Cairo", 24, QFont.Bold))
        user_title.setAlignment(Qt.AlignCenter)
        layout3.addWidget(user_title)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        
        self.fullname = QLineEdit(); self.fullname.setPlaceholderText("Full Name")
        self.username = QLineEdit(); self.username.setPlaceholderText("Username (e.g., hacker)")
        self.password = QLineEdit(); self.password.setPlaceholderText("Super Secret Password"); self.password.setEchoMode(QLineEdit.Password)
        self.hostname = QLineEdit(); self.hostname.setPlaceholderText("Hostname (e.g., nors-machine)")
        
        for w in [self.fullname, self.username, self.password, self.hostname]:
            w.setFixedWidth(400)
            form_layout.addWidget(w)
            
        layout3.addWidget(form_widget, alignment=Qt.AlignHCenter)
        self.stack.addWidget(page3)

        # Page 4: Installation Progress
        page4 = QWidget()
        layout4 = QVBoxLayout(page4)
        
        self.install_title = QLabel("Forging NORS System...")
        self.install_title.setFont(QFont("Cairo", 24, QFont.Bold))
        self.install_title.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(600, 30)
        self.progress_bar.setValue(0)
        
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #8892B0; font-size: 16px; margin-top: 10px;")
        
        # Slideshow frame
        self.slideshow = QLabel("Explore 800+ Penetration Testing Tools while we install.")
        self.slideshow.setAlignment(Qt.AlignCenter)
        self.slideshow.setStyleSheet("font-size: 20px; color: #00B4D8; margin-top: 40px;")
        
        layout4.addStretch()
        layout4.addWidget(self.install_title)
        layout4.addWidget(self.progress_bar, alignment=Qt.AlignHCenter)
        layout4.addWidget(self.status_label)
        layout4.addWidget(self.slideshow)
        layout4.addStretch()
        self.stack.addWidget(page4)

    def next_page(self):
        current = self.stack.currentIndex()
        if current < 2:
            self.stack.setCurrentIndex(current + 1)
            self.back_btn.show()
        elif current == 2:
            # Start installation
            self.stack.setCurrentIndex(3)
            self.back_btn.hide()
            self.next_btn.hide()
            self.start_installation()

    def prev_page(self):
        current = self.stack.currentIndex()
        if current > 0:
            self.stack.setCurrentIndex(current - 1)
        if self.stack.currentIndex() == 0:
            self.back_btn.hide()

    def start_installation(self):
        self.worker = InstallWorker()
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.install_finished)
        self.worker.start()
        
        # Simple Slideshow Timer
        self.slide_timer = QTimer()
        self.slide_texts = [
            "Native Windows Apps via Bottles & Wine.",
            "NorsDream: A beautiful, dynamic KDE Desktop.",
            "Zero Trust Network Lockdowns built-in.",
            "Advanced C2 and Fuzzing toolkits ready to fire."
        ]
        self.slide_idx = 0
        self.slide_timer.timeout.connect(self.update_slideshow)
        self.slide_timer.start(3000)

    def update_slideshow(self):
        self.slideshow.setText(self.slide_texts[self.slide_idx])
        self.slide_idx = (self.slide_idx + 1) % len(self.slide_texts)

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.status_label.setText(msg)

    def install_finished(self):
        self.slide_timer.stop()
        self.progress_bar.setValue(100)
        self.install_title.setText("Installation Successful")
        self.install_title.setStyleSheet("color: #00FF41;")
        self.status_label.setText("You can now reboot into NORS OS.")
        self.slideshow.setText("Welcome to the Elite.")
        
        self.next_btn.setText("Reboot Now")
        self.next_btn.clicked.disconnect()
        self.next_btn.clicked.connect(self.close)
        self.next_btn.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Custom Palette for Application
    app.setStyle("Fusion")
    
    window = NorsInstaller()
    window.show()
    sys.exit(app.exec_())
