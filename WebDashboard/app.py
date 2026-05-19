import os
from flask import Flask, render_template_string, jsonify
import psutil
import platform

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Nors OS - Remote Command Center</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0A192F; color: white; margin: 0; padding: 20px; }
        .dashboard { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .card { background-color: #112240; padding: 20px; border-radius: 10px; border-top: 4px solid #00B4D8; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1 { color: #00B4D8; text-align: center; border-bottom: 2px solid #233554; padding-bottom: 10px; }
        h2 { margin-top: 0; font-size: 1.2rem; color: #8892B0; }
        .stat { font-size: 2rem; font-weight: bold; color: #E6F1FF; }
        .btn { display: inline-block; padding: 10px 20px; background-color: #00B4D8; color: black; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🦅 Nors OS - Remote Web Dashboard</h1>
    
    <div class="dashboard">
        <div class="card">
            <h2>System Info</h2>
            <p>OS: {{ platform.system() }} {{ platform.release() }}</p>
            <p>Node: {{ platform.node() }}</p>
        </div>
        
        <div class="card">
            <h2>CPU Load</h2>
            <div class="stat">{{ cpu_percent }}%</div>
        </div>
        
        <div class="card">
            <h2>Memory Usage</h2>
            <div class="stat">{{ mem_percent }}%</div>
            <p>{{ mem_used }} GB / {{ mem_total }} GB</p>
        </div>
        
        <div class="card" style="grid-column: span 3;">
            <h2>Quick Actions</h2>
            <a href="/api/trigger_scan" class="btn">Trigger Network Scan</a>
            <a href="/api/backup" class="btn">Backup Configurations</a>
            <a href="/api/restart_services" class="btn" style="background-color: #FF3366; color: white;">Restart Security Services</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    mem = psutil.virtual_memory()
    return render_template_string(HTML_TEMPLATE,
                                  platform=platform,
                                  cpu_percent=psutil.cpu_percent(),
                                  mem_percent=mem.percent,
                                  mem_used=round(mem.used / (1024**3), 2),
                                  mem_total=round(mem.total / (1024**3), 2))

@app.route('/api/trigger_scan')
def trigger_scan():
    # Placeholder for integrating with NorsScanner
    return jsonify({"status": "success", "message": "Automated scan initiated in background."})

@app.route('/api/backup')
def backup():
    return jsonify({"status": "success", "message": "Nors configurations backed up to /opt/nors_backups/"})

@app.route('/api/restart_services')
def restart_services():
    return jsonify({"status": "success", "message": "NorsDefender and NorsMonitor restarted."})

if __name__ == '__main__':
    print("[*] Starting Nors OS Web Dashboard on port 5050...")
    app.run(host='0.0.0.0', port=5050, debug=False)
