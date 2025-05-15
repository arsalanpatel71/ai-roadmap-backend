from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from ..core.config import settings
import base64
import os

async def send_email(to_email: str, subject: str, content: str, attachment_path: str = None):
    """Send email using SendGrid"""
    try:
        print(f"Attempting to send email to: {to_email}")
        print(f"Using SendGrid API key: {settings.SENDGRID_API_KEY[:10]}...")
        print(f"From email: {settings.FROM_EMAIL}")
        
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )

        if attachment_path and os.path.exists(attachment_path):
            print(f"Adding attachment: {attachment_path}")
            with open(attachment_path, 'rb') as f:
                file_content = base64.b64encode(f.read()).decode()
                
            attachment = Attachment(
                FileContent(file_content),
                FileName(os.path.basename(attachment_path)),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.attachment = attachment
        else:
            print(f"Warning: Attachment path not found: {attachment_path}")

        print("Sending email via SendGrid...")
        response = sg.send(message)
        
        print(f"SendGrid Response Status Code: {response.status_code}")
        print(f"SendGrid Response Headers: {response.headers}")
        
        if response.status_code in [200, 201, 202]:
            print("Email sent successfully!")
            return {
                "status": "success",
                "message": "Email sent successfully",
                "status_code": response.status_code
            }
        else:
            print(f"SendGrid error: Status code {response.status_code}")
            return {
                "status": "error",
                "message": f"Failed to send email. Status code: {response.status_code}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"SendGrid error: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}",
            "status_code": 500
        } 