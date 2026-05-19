#!/usr/bin/env python3
# NorsLabs - Local Vulnerable Environment Manager
# License: GPLv3
# Description: Manages Docker-based vulnerable environments for educational purposes.

import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

# Educational Lab Images
LAB_IMAGES = {
    "DVWA (Damn Vulnerable Web App)": "vulnerables/web-dvwa",
    "OWASP Juice Shop": "bkimminich/juice-shop",
    "Metasploitable 2": "tleemcjr/metasploitable2",
    "WebGoat": "webgoat/webgoat-8.0"
}

class NorsLabsUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🦅 NorsLabs - Educational Training Environments")
        self.setGeometry(150, 150, 800, 500)

        # NorsDark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 25, 47))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(17, 34, 64))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 180, 216))
        palette.setColor(QPalette.ButtonText, Qt.black)
        self.setPalette(palette)

        central_widget = QWidget()
        layout = QVBoxLayout()

        header = QLabel("NorsLabs: Safe Offline Training Environments")
        header.setFont(QFont("Cairo", 16, QFont.Bold))
        header.setStyleSheet("color: #00B4D8; margin-bottom: 10px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Info text
        info = QLabel("Deploy local, isolated vulnerable applications for safe ethical hacking practice.\nRequires Docker engine to be running.")
        info.setStyleSheet("color: #B0C4DE;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        # Table
        self.table = QTableWidget(len(LAB_IMAGES), 3)
        self.table.setHorizontalHeaderLabels(["Environment Name", "Docker Image", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setStyleSheet("gridline-color: #00B4D8; selection-background-color: #00B4D8;")

        row = 0
        for name, img in LAB_IMAGES.items():
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(img))
            
            btn_layout = QHBoxLayout()
            start_btn = QPushButton("▶ Deploy")
            start_btn.setStyleSheet("background-color: #00B4D8; color: black; padding: 5px;")
            start_btn.clicked.connect(lambda checked, i=img: self.deploy_lab(i))
            
            stop_btn = QPushButton("⏹ Stop")
            stop_btn.setStyleSheet("background-color: #FF3366; color: white; padding: 5px;")
            stop_btn.clicked.connect(lambda checked, i=img: self.stop_lab(i))
            
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(0,0,0,0)
            cell_layout.addWidget(start_btn)
            cell_layout.addWidget(stop_btn)
            
            self.table.setCellWidget(row, 2, cell_widget)
            row += 1

        layout.addWidget(self.table)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def deploy_lab(self, image):
        try:
            print(f"[*] Deploying lab container for {image}...")
            # Run detached, map a random high port or default port if known. Simplified for UI.
            # Real implementation would map ports specifically per app
            cmd = ["docker", "run", "-d", "-P", image]
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            QMessageBox.information(self, "Success", f"Initiated deployment of {image}.\nCheck 'docker ps' for mapped ports.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run Docker: {str(e)}")

    def stop_lab(self, image):
        try:
            print(f"[*] Stopping containers based on {image}...")
            # Find running container ID
            cmd_ps = ["docker", "ps", "-q", "--filter", f"ancestor={image}"]
            process = subprocess.Popen(cmd_ps, stdout=subprocess.PIPE)
            out, _ = process.communicate()
            c_ids = out.decode().splitlines()
            
            for cid in c_ids:
                subprocess.Popen(["docker", "stop", cid])
            
            QMessageBox.information(self, "Stopped", f"Stopped container(s) for {image}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop Docker: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NorsLabsUI()
    window.show()
    sys.exit(app.exec_())
