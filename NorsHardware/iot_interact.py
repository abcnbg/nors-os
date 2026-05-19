#!/usr/bin/env python3
# NorsHardware - IoT & Hardware Interaction Tool
# License: GPLv3
import sys

# Mock implementation since PySerial/SMBus might not be available, 
# but represents the GUI for NORS OS IoT hacking toolkit.

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class NorsHardware(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🦅 NorsHardware - IoT Interface")
        self.setGeometry(200, 200, 700, 500)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 25, 47))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        main_widget = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Hardware Hacking Interface (UART/SPI/I2C)")
        header.setFont(QFont("Cairo", 16, QFont.Bold))
        header.setStyleSheet("color: #00B4D8;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Connection settings
        conn_layout = QHBoxLayout()
        conn_layout.addWidget(QLabel("Protocol:"))
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["UART (Serial)", "SPI", "I2C", "JTAG"])
        conn_layout.addWidget(self.protocol_combo)

        conn_layout.addWidget(QLabel("Port/Device:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems(["/dev/ttyUSB0", "/dev/ttyAMA0", "/dev/i2c-1", "/dev/spidev0.0"])
        conn_layout.addWidget(self.port_combo)
        
        self.connect_btn = QPushButton("Connect Device")
        self.connect_btn.setStyleSheet("background-color: #00B4D8; color: black;")
        self.connect_btn.clicked.connect(self.simulate_connection)
        conn_layout.addWidget(self.connect_btn)
        
        layout.addLayout(conn_layout)

        # Terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #050A15; color: #00FF41; font-family: monospace;")
        layout.addWidget(self.terminal)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def simulate_connection(self):
        proto = self.protocol_combo.currentText()
        port = self.port_combo.currentText()
        self.terminal.append(f"[*] Attempting to initialize {proto} on {port}...")
        self.terminal.append("[!] Connecting to BusPirate / FTDI interface...")
        self.terminal.append(f"[+] Connection Established. Baudrate/Speed auto-negotiated.")
        if proto == "UART (Serial)":
            self.terminal.append(">> Root shell dropping in 3... 2... 1...")
            self.terminal.append("root@iot-camera:~# ")
        elif proto == "SPI":
            self.terminal.append("[+] Flash chip detected: Winbond W25Q128 (16MB)")
            self.terminal.append("[*] Ready to dump firmware.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NorsHardware()
    window.show()
    sys.exit(app.exec_())
