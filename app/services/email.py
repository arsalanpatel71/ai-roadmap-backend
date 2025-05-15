import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from ..core.config import settings
import os

async def send_pdf_email(email: str, company_name: str, pdf_path: str):
    """Send PDF via email using Gmail"""
    
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = f'AI Implementation Roadmap for {company_name}'
    
    body = f"""
    Dear {company_name},

    Please find attached your AI Implementation Roadmap.

    Best regards,
    AI Roadmap Team
    """
    msg.attach(MIMEText(body, 'plain'))
    
    with open(pdf_path, 'rb') as f:
        pdf = MIMEApplication(f.read(), _subtype='pdf')
        pdf.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
        msg.attach(pdf)
    
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return {"status": "success"}
    except Exception as e:
        print(f"Email error: {str(e)}")
        raise e 