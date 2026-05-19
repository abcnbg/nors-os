#!/usr/bin/env python3
# NorsWifiStrike - Advanced Wireless Auditing GUI
# License: GPLv3
import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QComboBox, QTextEdit)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class WifiScanner(QThread):
    output_signal = pyqtSignal(str)
    
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        
    def run(self):
        self.output_signal.emit("[*] Enabling monitor mode...")
        subprocess.run(["airmon-ng", "start", self.interface], capture_output=True)
        mon_iface = self.interface + "mon"
        self.output_signal.emit(f"[*] Starting airodump-ng on {mon_iface}...")
        # Simulating output for GUI purposes. Real tool requires root and parses CSV
        self.output_signal.emit("BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID")
        self.output_signal.emit("AA:BB:CC:DD:EE:FF  -45       10        0    0   6   54e. WPA2 CCMP   PSK  TargetNet")

class NorsWifiStrike(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🦅 NorsWifiStrike - Wireless Auditing")
        self.setGeometry(100, 100, 900, 600)

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

        header = QLabel("NorsWifiStrike - Automated 802.11 Auditing")
        header.setFont(QFont("Cairo", 18, QFont.Bold))
        header.setStyleSheet("color: #00B4D8;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Controls
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Interface:"))
        self.iface_combo = QComboBox()
        self.iface_combo.addItems(["wlan0", "wlan1"])
        controls.addWidget(self.iface_combo)

        self.scan_btn = QPushButton("Scan Networks")
        self.scan_btn.clicked.connect(self.start_scan)
        controls.addWidget(self.scan_btn)

        self.deauth_btn = QPushButton("Launch Deauth Attack")
        self.deauth_btn.setStyleSheet("background-color: #FF3366; color: white;")
        controls.addWidget(self.deauth_btn)
        
        layout.addLayout(controls)

        # Console Output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #050A15; color: #00FF41; font-family: monospace;")
        layout.addWidget(self.console)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.scanner = None

    def start_scan(self):
        iface = self.iface_combo.currentText()
        self.console.append(f"[*] Initializing scan on {iface}...")
        self.scanner = WifiScanner(iface)
        self.scanner.output_signal.connect(self.console.append)
        self.scanner.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NorsWifiStrike()
    window.show()
    sys.exit(app.exec_())
