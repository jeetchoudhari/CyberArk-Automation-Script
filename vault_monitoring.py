import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime

# Configuration
API_BASE_URL = 'https://your-cyberark-api-endpoint'
VAULT_HEALTH_ENDPOINT = '/api/v1/vault/health'
CREDENTIALS_ENDPOINT = '/api/v1/credentials'
POLICY_ENDPOINT = '/api/v1/policies'
EMAIL_SENDER = 'your-email@example.com'
EMAIL_RECEIVER = 'receiver-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
DATABASE_FILE = 'vault_monitoring.db'

# Function to fetch data from CyberArk API
def fetch_data(endpoint):
    response = requests.get(API_BASE_URL + endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {endpoint}: {response.status_code}")
        return None

# Function to send email notifications
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text)

# Function to log report to database
def log_report(health_status, credentials, policies):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            timestamp TEXT,
            health_status TEXT,
            credentials TEXT,
            policies TEXT
        )
    ''')
    c.execute('''
        INSERT INTO reports (timestamp, health_status, credentials, policies)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().isoformat(), health_status, credentials, policies))
    conn.commit()
    conn.close()

# Main monitoring function
def monitor_vault():
    # Fetch vault health
    health_data = fetch_data(VAULT_HEALTH_ENDPOINT)
    if health_data:
        health_status = health_data.get('status', 'Unknown')
        if health_status != 'Healthy':
            send_email('Vault Health Alert', f'Vault health status: {health_status}')

    # Fetch credentials
    credentials_data = fetch_data(CREDENTIALS_ENDPOINT)
    if credentials_data:
        for credential in credentials_data:
            if credential.get('status') == 'Expiring':
                send_email('Credential Expiration Alert', f'Credential expiring: {credential}')

    # Fetch policies
    policies_data = fetch_data(POLICY_ENDPOINT)
    if policies_data:
        for policy in policies_data:
            if not policy.get('compliant'):
                send_email('Policy Violation Alert', f'Policy violation detected: {policy}')

    # Generate and log report
    log_report(
        health_status=str(health_data),
        credentials=str(credentials_data),
        policies=str(policies_data)
    )

if __name__ == '__main__':
    monitor_vault()
