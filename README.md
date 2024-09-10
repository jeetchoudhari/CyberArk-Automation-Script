# CyberArk Vault Monitoring Automation

This project provides a Python script to monitor CyberArk Vault health, automate alerts for credential expirations and policy violations, and generate usage reports. The script leverages CyberArk’s REST APIs to fetch data and utilizes email notifications for alerting

**Features**<br>
Monitors vault health and sends alerts for any issues.
Alerts for expiring credentials.
Notifies for policy violations.
Generates and logs usage reports in a SQLite database.
Sends real-time email notifications for alerts.

**Prerequisites**
1. Python 3.x installed on your machine.
2. Access to the CyberArk Vault API and the necessary API tokens.
3. An SMTP email server for sending notifications.

**Installation**
1. Clone the Repository
2. Install Required Libraries (pip install requests)


**Script Configuration**<br>
Open the script file (vault_monitoring.py) and configure the following settings:

API_BASE_URL: Set this to the base URL of your CyberArk API endpoint.<br>
VAULT_HEALTH_ENDPOINT: Set this to the endpoint for vault health status.<br>
CREDENTIALS_ENDPOINT: Set this to the endpoint for credential information.<br>
POLICY_ENDPOINT: Set this to the endpoint for policy information.<br>
EMAIL_SENDER: Your email address used for sending notifications.<br>
EMAIL_RECEIVER: The recipient's email address for notifications.<br>
EMAIL_PASSWORD: Password for the sender email.<br>
SMTP_SERVER: SMTP server address for sending emails.<br>
SMTP_PORT: SMTP server port (typically 587 for TLS).<br>
DATABASE_FILE: Name of the SQLite database file for storing reports.<br>

**Running the Script**<br>
Execute the script in command line using (python vault_monitoring.py)

**Output**<br>
Email Alerts: Alerts are sent to the specified email address for health issues, credential expirations, and policy violations.
Database Reports: The script logs the monitoring results in the specified SQLite database file.
