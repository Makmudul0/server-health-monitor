import psutil
import smtplib
from email.mime.text import MIMEText




# Thresholds
CPU_THRESHOLD = 80  # 80% CPU usage
MEMORY_THRESHOLD = 80  # 80% Memory usage
DISK_THRESHOLD = 80  # 80% Disk usage

import datetimeimport os
from dotenv import load_dotenv
load_dotenv()  # Loads .env file
EMAIL_ADDRESS = os.getenv("GMAIL_USER")
EMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
TO_EMAIL = "makmudulweb@gmail.com"


def check_system():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("C:").percent

    # Log data
    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = f"[{log_time}] CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%"

    with open("system_log.txt", "a") as log_file:
        log_file.write(log_data + "\n")

    # Check if any threshold is exceeded
    if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD or disk_usage > DISK_THRESHOLD:
        send_alert(cpu_usage, memory_usage, disk_usage)


def send_alert(cpu, memory, disk):
    subject = "🚨 HIGH SYSTEM USAGE ALERT!"
    body = f"""
    Warning! System usage exceeds threshold:
    - CPU: {cpu}%
    - Memory: {memory}%
    - Disk: {disk}%
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print("Alert email sent!")
    except Exception as e:
        print(f"Email failed: {e}")


if __name__ == "__main__":
    check_system()