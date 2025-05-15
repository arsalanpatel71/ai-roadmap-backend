from fastapi import APIRouter, HTTPException
from ..schemas.pdf import PDFRequest, PDFResponse
from ..services.pdf import generate_pdf, OUTPUT_DIR
from ..services.form import get_user_request
from ..services.sendgrid_email import send_email
import os
from datetime import datetime

router = APIRouter()

@router.post("/generate/{request_id}/{message_id}")
async def generate_pdf_for_message(request_id: str, message_id: str):
    """Generate PDF and send via email"""
    try:
        user_data = await get_user_request(request_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="Request not found")
            
        if 'form' not in user_data or 'email' not in user_data['form']:
            raise HTTPException(status_code=400, detail="Email not found in form data")
            
        chat_history = user_data.get('chat_history', [])
        
        message = next((
            msg for msg in chat_history 
            if str(msg.get('id', msg.get('_id', ''))) == message_id
        ), None)
        
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        message_content = message.get('message', message.get('content', ''))
        company_name = user_data['form']['company_name']
        email = user_data['form']['email']
        
        formatted_content = message_content.replace("\n", "<br>")
        formatted_content = formatted_content.replace("###", "<h3>").replace("\n\n", "</h3>")
        
        output_filename = f"roadmap_{company_name.lower().replace(' ', '_')}_{message_id}.pdf"
        
        pdf_request = PDFRequest(
            template_name="ai_roadmap",
            data={
                "title": f"AI Implementation Roadmap for {company_name}",
                "company_name": company_name,
                "industry": user_data['form']['industry'],
                "company_size": user_data['form']['company_size'],
                "content": formatted_content
            },
            output_filename=output_filename
        )
        
        await generate_pdf(pdf_request)
        pdf_path = os.path.join(OUTPUT_DIR, output_filename)
        
        email_result = await send_email(
            to_email=email,
            subject=f'AI Implementation Roadmap for {company_name}',
            content=f"""Dear {company_name},

Please find attached your AI Implementation Roadmap.

Best regards,
AI Roadmap Team""",
            attachment_path=pdf_path
        )
        
        if email_result["status"] == "success":
            return {
                "status": "success",
                "message": "PDF generated and sent to email successfully"
            }
        else:
            return {
                "status": "partial_success",
                "message": f"PDF generated successfully but email sending failed: {email_result['message']}"
            }
            
    except Exception as e:
        error_detail = f"Error: {str(e)}"
        print(f"PDF Generation Error: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)

@router.post("/test-email")
async def test_email():
    """Test email functionality"""
    try:
        pdf_request = PDFRequest(
            template_name="ai_roadmap",
            data={
                "title": "Test Roadmap",
                "company_name": "Test Company",
                "industry": "Testing",
                "company_size": "Small",
                "content": "This is a test PDF"
            },
            output_filename="test.pdf"
        )
        await generate_pdf(pdf_request)
        pdf_path = os.path.join(OUTPUT_DIR, "test.pdf")
        
        result = await send_email(
            to_email="arsalanpatel71@gmail.com",
            subject="Test Email from AI Roadmap",
            content="This is a test email from the AI Roadmap application.",
            attachment_path=pdf_path
        )
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)} 