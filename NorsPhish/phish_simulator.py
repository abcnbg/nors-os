#!/usr/bin/env python3
# NorsPhish - Phishing Campaign Simulator & Tracker
# License: GPLv3
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import datetime
import uuid

# Database setup for tracking
conn = sqlite3.connect('/tmp/nors_phish.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS campaigns 
                  (id TEXT PRIMARY KEY, target_email TEXT, status TEXT, timestamp TEXT)''')
conn.commit()

TEMPLATES = {
    "IT_UPDATE": {
        "subject": "URGENT: Password Expiry Notice",
        "body": """
        <html><body>
        <h2>IT Security Notice</h2>
        <p>Your corporate password will expire in 2 hours.</p>
        <p>Please update it immediately using the link below to avoid account lockout:</p>
        <a href="{link}" style="background-color: #00B4D8; color: black; padding: 10px; text-decoration: none;">Update Password</a>
        </body></html>
        """
    },
    "HR_BENEFITS": {
        "subject": "ACTION REQUIRED: 2026 Benefits Enrollment",
        "body": """
        <html><body>
        <h2>HR Department</h2>
        <p>The open enrollment period for your 2026 health benefits closes today.</p>
        <p>Review and confirm your plan here:</p>
        <a href="{link}">Confirm Benefits</a>
        </body></html>
        """
    }
}

def send_phish(target, template_name, tracking_link, smtp_server, smtp_port, sender_email, sender_pass):
    print(f"[*] Simulating phishing email to: {target}")
    campaign_id = str(uuid.uuid4())
    
    template = TEMPLATES.get(template_name)
    if not template:
        print("[-] Invalid template.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target
    msg['Subject'] = template['subject']
    
    # Embed tracking token in link
    full_link = f"{tracking_link}?token={campaign_id}"
    body = template['body'].format(link=full_link)
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # In a real tool, this would connect to the SMTP server. 
        # For the OS, we simulate success if no credentials provided.
        if smtp_server and sender_pass:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_pass)
            server.send_message(msg)
            server.quit()
        
        cursor.execute("INSERT INTO campaigns VALUES (?, ?, ?, ?)", 
                       (campaign_id, target, 'Sent', datetime.datetime.now().isoformat()))
        conn.commit()
        print(f"[+] Email sent successfully. Tracking ID: {campaign_id}")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")

def track_results():
    print("\n🦅 NorsPhish Campaign Status")
    print("-" * 50)
    cursor.execute("SELECT * FROM campaigns")
    for row in cursor.fetchall():
        print(f"ID: {row[0][:8]}... | Target: {row[1]} | Status: {row[2]} | Date: {row[3]}")
    print("-" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NorsPhish - Educational Phishing Simulator")
    parser.add_argument("--target", help="Target email address")
    parser.add_argument("--template", choices=list(TEMPLATES.keys()), help="Phishing template to use")
    parser.add_argument("--link", help="URL to point the victim to", default="http://nors.local/login")
    parser.add_argument("--track", action="store_true", help="View campaign tracking database")
    
    args = parser.parse_args()
    
    if args.track:
        track_results()
    elif args.target and args.template:
        # SMTP details would normally be configured here
        send_phish(args.target, args.template, args.link, None, None, "it@company.local", None)
    else:
        parser.print_help()
