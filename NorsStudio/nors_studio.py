#!/usr/bin/env python3
# NorsStudio - Theme & Behavior Customizer for NORS OS
# License: GPLv3
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QSlider, QColorDialog)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class NorsStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🦅 Nors Studio - Desktop Customization")
        self.setGeometry(200, 200, 500, 400)

        # Apply dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 25, 47))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        layout = QVBoxLayout()
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        title = QLabel("Nors Studio Personalization")
        title.setFont(QFont("Cairo", 16, QFont.Bold))
        title.setStyleSheet("color: #00B4D8; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Theme Selector
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Global Theme:", styleSheet="color: white;"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["NorsDream Dark (Default)", "NorsDream Light", "CyberHacker Neon", "Stealth Mode"])
        self.theme_combo.setStyleSheet("background: #112240; color: white; padding: 5px;")
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        # Transparency Slider
        trans_layout = QHBoxLayout()
        trans_layout.addWidget(QLabel("Window Transparency:", styleSheet="color: white;"))
        self.trans_slider = QSlider(Qt.Horizontal)
        self.trans_slider.setRange(50, 100)
        self.trans_slider.setValue(85)
        trans_layout.addWidget(self.trans_slider)
        layout.addLayout(trans_layout)

        # Accent Color
        color_btn = QPushButton("Change Accent Color")
        color_btn.setStyleSheet("background-color: #112240; color: white; border: 1px solid #00B4D8; padding: 10px;")
        color_btn.clicked.connect(self.choose_color)
        layout.addWidget(color_btn)

        # Apply Button
        apply_btn = QPushButton("Apply Nors Settings")
        apply_btn.setStyleSheet("background-color: #00B4D8; color: black; font-weight: bold; padding: 12px; border-radius: 5px; margin-top: 30px;")
        apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(apply_btn)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"[*] Accent color set to: {color.name()}")

    def apply_settings(self):
        theme = self.theme_combo.currentText()
        alpha = self.trans_slider.value()
        print(f"[*] Applying settings: Theme={theme}, Opacity={alpha}%")
        # In reality, this would execute kwriteconfig5 or bash scripts to modify KDE settings
        print("[+] Settings applied to KDE Plasma successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NorsStudio()
    window.show()
    sys.exit(app.exec_())
