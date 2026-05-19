from flask import Flask, render_template_string
import markdown
import os

app = Flask(__name__)

# Basic Markdown content for the Academy
MARKDOWN_TUTORIALS = {
    "intro": """
# Introduction to Ethical Hacking
Welcome to the Nors OS Cyber Academy.
Ethical hacking involves authorized attempts to gain unauthorized access to a computer system, application, or data.
**Key Principles:**
- Stay legal and within scope.
- Report all vulnerabilities.
- Respect data privacy.
    """,
    "recon": """
# Network Reconnaissance
Recon is the first step of an assessment.
Tools in Nors OS:
- **Nmap**: For port scanning and OS detection.
- **NorsScanner**: Our custom automated intelligence tool.
Always ensure you have permission before scanning a network.
    """,
    "defense": """
# Blue Teaming & Defense
Understanding how to defend is critical.
- **NorsDefender**: Our built-in HIDS (Host Intrusion Detection System) monitors for suspicious files and processes.
- **Hardening**: Use `nors_harden.sh` to secure your OS stack against common attacks.
    """
}

HTML_SHELL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Nors Academy - Offline Learning</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0A192F; color: #E6F1FF; margin: 0; display: flex; }
        .sidebar { width: 250px; background-color: #112240; padding: 20px; height: 100vh; position: fixed; border-right: 2px solid #00B4D8; }
        .content { margin-left: 270px; padding: 40px; max-width: 800px; line-height: 1.6; }
        h1, h2, h3 { color: #00B4D8; }
        a { color: #00B4D8; text-decoration: none; display: block; margin: 10px 0; font-size: 18px; }
        a:hover { color: #fff; }
        pre { background: #050A15; padding: 15px; border-radius: 5px; border: 1px solid #B0C4DE; }
        code { color: #00FF41; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2 style="color: white;">🦅 Nors Academy</h2>
        <hr style="border-color: #233554;">
        <a href="/">🏠 Home</a>
        <a href="/topic/intro">📘 Intro to Hacking</a>
        <a href="/topic/recon">🔍 Reconnaissance</a>
        <a href="/topic/defense">🛡️ Defense & Blue Team</a>
    </div>
    <div class="content">
        {{ content|safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    welcome = "# Welcome to Nors Academy\nYour offline cybersecurity training portal. Select a topic from the left sidebar to begin your journey."
    html_content = markdown.markdown(welcome)
    return render_template_string(HTML_SHELL, content=html_content)

@app.route('/topic/<name>')
def topic(name):
    md_text = MARKDOWN_TUTORIALS.get(name, "# 404\nTopic not found.")
    html_content = markdown.markdown(md_text)
    return render_template_string(HTML_SHELL, content=html_content)

if __name__ == '__main__':
    print("[*] Starting Nors Academy Offline Portal on port 8080...")
    app.run(host='127.0.0.1', port=8080, debug=False)
