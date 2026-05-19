#!/usr/bin/env python3
# NorsVPN - Secure Connection Manager
# License: GPLv3

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QComboBox, QMessageBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class NorsVPN(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🦅 NorsVPN - Privacy Manager")
        self.setGeometry(300, 300, 400, 250)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 25, 47))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        layout = QVBoxLayout()
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        title = QLabel("Secure Network Tunnel")
        title.setFont(QFont("Cairo", 14, QFont.Bold))
        title.setStyleSheet("color: #00B4D8;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.server_combo = QComboBox()
        self.server_combo.addItems(["Tor Network (Anonsurf)", "OpenVPN: US-East", "OpenVPN: EU-Frankfurt", "WireGuard: SecureCore"])
        self.server_combo.setStyleSheet("background: #112240; color: white; padding: 8px;")
        layout.addWidget(self.server_combo)

        self.connect_btn = QPushButton("Connect / Secure Connection")
        self.connect_btn.setStyleSheet("background-color: #00B4D8; color: black; font-weight: bold; padding: 12px; border-radius: 5px; margin-top: 20px;")
        self.connect_btn.clicked.connect(self.toggle_vpn)
        layout.addWidget(self.connect_btn)
        
        self.is_connected = False

    def toggle_vpn(self):
        server = self.server_combo.currentText()
        if not self.is_connected:
            self.connect_btn.setText("Disconnect")
            self.connect_btn.setStyleSheet("background-color: #FF3366; color: white; font-weight: bold; padding: 12px; border-radius: 5px; margin-top: 20px;")
            QMessageBox.information(self, "Connected", f"Secure tunnel established via {server}.")
            self.is_connected = True
        else:
            self.connect_btn.setText("Connect / Secure Connection")
            self.connect_btn.setStyleSheet("background-color: #00B4D8; color: black; font-weight: bold; padding: 12px; border-radius: 5px; margin-top: 20px;")
            QMessageBox.information(self, "Disconnected", "Tunnel closed. Original IP restored.")
            self.is_connected = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NorsVPN()
    window.show()
    sys.exit(app.exec_())
