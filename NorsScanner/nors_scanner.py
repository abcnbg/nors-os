#!/usr/bin/env python3
# NorsScanner - Advanced Network Mapping & Vulnerability Discovery
# License: GPLv3
# Description: A massive, multi-threaded network scanner utilizing Scapy, Nmap, and custom heuristics.

import sys
import os
import threading
import queue
import time
import socket
import json
from datetime import datetime
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                 QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                                 QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QTabWidget)
    from PyQt5.QtGui import QFont, QColor, QPalette
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    import nmap
    from scapy.all import ARP, Ether, srp, conf
except ImportError:
    print("[-] Missing dependencies. Run: pip install PyQt5 python-nmap scapy")
    sys.exit(1)

class ScannerThread(QThread):
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(dict)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, target, scan_type):
        super().__init__()
        self.target = target
        self.scan_type = scan_type
        self.nm = nmap.PortScanner()

    def run(self):
        self.log_signal.emit(f"[*] Starting {self.scan_type} scan on {self.target}...")
        self.progress_signal.emit(10)
        
        try:
            if self.scan_type == "ARP Discovery":
                self.arp_scan(self.target)
            elif self.scan_type == "Deep Port Scan":
                self.deep_port_scan(self.target)
            elif self.scan_type == "Vulnerability Scan":
                self.vuln_scan(self.target)
        except Exception as e:
            self.log_signal.emit(f"[-] Scan Error: {str(e)}")
            
        self.progress_signal.emit(100)
        self.finished_signal.emit()

    def arp_scan(self, ip_range):
        self.log_signal.emit("[*] Broadcasting ARP requests...")
        conf.verb = 0
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range), timeout=2)
        total = len(ans)
        for i, (snd, rcv) in enumerate(ans):
            self.progress_signal.emit(10 + int((i/total)*80))
            mac = rcv.sprintf(r"%Ether.src%")
            ip = rcv.sprintf(r"%ARP.psrc%")
            self.log_signal.emit(f"[+] Found Host: IP={ip}, MAC={mac}")
            self.result_signal.emit({"ip": ip, "mac": mac, "state": "up", "ports": "N/A", "os": "Unknown"})

    def deep_port_scan(self, target):
        self.nm.scan(target, arguments='-sS -sV -O -p 1-65535 -T4')
        for host in self.nm.all_hosts():
            state = self.nm[host].state()
            os_match = self.nm[host].get('osmatch', [{'name': 'Unknown'}])[0]['name']
            open_ports = []
            if 'tcp' in self.nm[host]:
                for port in self.nm[host]['tcp']:
                    if self.nm[host]['tcp'][port]['state'] == 'open':
                        srv = self.nm[host]['tcp'][port]['name']
                        ver = self.nm[host]['tcp'][port].get('version', '')
                        open_ports.append(f"{port}/{srv} {ver}")
            
            ports_str = ", ".join(open_ports) if open_ports else "None"
            self.log_signal.emit(f"[+] {host} is {state} | OS: {os_match} | Ports: {len(open_ports)} open")
            self.result_signal.emit({"ip": host, "mac": "Resolved", "state": state, "ports": ports_str, "os": os_match})

    def vuln_scan(self, target):
        self.log_signal.emit("[*] Running Nmap Vuln Scripts (requires nmap-vulners)...")
        self.nm.scan(target, arguments='-sV --script vuln')
        for host in self.nm.all_hosts():
            self.log_signal.emit(f"[*] Parsing vulnerabilities for {host}...")
            # Highly simplified parser for UI
            if 'tcp' in self.nm[host]:
                for port in self.nm[host]['tcp']:
                    if 'script' in self.nm[host]['tcp'][port]:
                        scripts = self.nm[host]['tcp'][port]['script']
                        for script_name, output in scripts.items():
                            self.log_signal.emit(f"[!] VULN FOUND on {host}:{port} - {script_name}")
            self.result_signal.emit({"ip": host, "mac": "-", "state": "Scanned", "ports": "Check Logs", "os": "Check Logs"})


class NorsScannerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🦅 NorsScanner - Advanced Reconnaissance")
        self.setGeometry(100, 100, 1024, 768)
        
        # NorsDark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 25, 47))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(17, 34, 64))
        palette.setColor(QPalette.AlternateBase, QColor(25, 50, 80))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 180, 216))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.Highlight, QColor(0, 180, 216))
        self.setPalette(palette)

        main_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("NorsScanner v2.0 - Ultimate Network Intelligence")
        header.setFont(QFont("Cairo", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #00B4D8; margin-bottom: 10px;")
        layout.addWidget(header)

        # Controls
        controls_layout = QHBoxLayout()
        self.target_input = QLineEdit("192.168.1.0/24")
        self.target_input.setStyleSheet("padding: 8px; border: 1px solid #B0C4DE; border-radius: 4px;")
        controls_layout.addWidget(QLabel("Target IP/CIDR:"))
        controls_layout.addWidget(self.target_input)

        self.scan_type_combo = QComboBox() if 'QComboBox' in globals() else None
        if not self.scan_type_combo:
            from PyQt5.QtWidgets import QComboBox
            self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems(["ARP Discovery", "Deep Port Scan", "Vulnerability Scan"])
        self.scan_type_combo.setStyleSheet("padding: 8px;")
        controls_layout.addWidget(self.scan_type_combo)

        self.start_btn = QPushButton("🚀 LAUNCH SCAN")
        self.start_btn.setStyleSheet("background-color: #00B4D8; color: black; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.start_btn.clicked.connect(self.start_scan)
        controls_layout.addWidget(self.start_btn)
        
        layout.addLayout(controls_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar { border: 1px solid #B0C4DE; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #00B4D8; }")
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Tabs for Results and Logs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { background: #112240; color: white; padding: 10px; } QTabBar::tab:selected { background: #00B4D8; color: black; }")
        
        # Results Table
        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "State", "Open Ports / Services", "OS Detection"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setStyleSheet("gridline-color: #00B4D8; selection-background-color: #00B4D8; selection-color: black;")
        self.tabs.addTab(self.results_table, "Network Map")

        # Logs
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setFont(QFont("Consolas", 10))
        self.log_console.setStyleSheet("background-color: #050A15; color: #00FF41; border: 1px solid #B0C4DE;")
        self.tabs.addTab(self.log_console, "Terminal Log")

        layout.addWidget(self.tabs)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.scanner_thread = None

    def log(self, message):
        self.log_console.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def start_scan(self):
        target = self.target_input.text()
        scan_type = self.scan_type_combo.currentText()
        
        if not target:
            self.log("[-] Error: Target cannot be empty.")
            return

        self.start_btn.setEnabled(False)
        self.results_table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.log(f"====== STARTING SESSION: {scan_type} ======")
        
        self.scanner_thread = ScannerThread(target, scan_type)
        self.scanner_thread.log_signal.connect(self.log)
        self.scanner_thread.progress_signal.connect(self.progress_bar.setValue)
        self.scanner_thread.result_signal.connect(self.add_result_row)
        self.scanner_thread.finished_signal.connect(self.scan_finished)
        self.scanner_thread.start()

    def add_result_row(self, data):
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        self.results_table.setItem(row, 0, QTableWidgetItem(data.get("ip", "")))
        self.results_table.setItem(row, 1, QTableWidgetItem(data.get("mac", "")))
        self.results_table.setItem(row, 2, QTableWidgetItem(data.get("state", "")))
        self.results_table.setItem(row, 3, QTableWidgetItem(data.get("ports", "")))
        self.results_table.setItem(row, 4, QTableWidgetItem(data.get("os", "")))

    def scan_finished(self):
        self.start_btn.setEnabled(True)
        self.log("====== SCAN COMPLETE ======")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NorsScannerUI()
    window.show()
    sys.exit(app.exec_())
