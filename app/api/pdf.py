from fastapi import APIRouter, HTTPException
from ..schemas.pdf import PDFRequest, PDFResponse
from ..services.pdf import generate_pdf, OUTPUT_DIR
from ..services.form import get_user_request
from ..services.sendgrid_email import send_email
from ..utils.format import format_chat_history_for_html
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

@router.post("/export-chat-history/{request_id}")
async def export_chat_history_pdf(request_id: str):
    """Generate PDF of full chat history and send via email"""
    try:
        user_data = await get_user_request(request_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="Request not found")

        if 'form' not in user_data or 'email' not in user_data['form']:
            raise HTTPException(status_code=400, detail="Email not found in form data for this request")

        email = user_data['form']['email']
        company_name = user_data['form'].get('company_name', 'N/A')
        industry = user_data['form'].get('industry')
        company_size = user_data['form'].get('company_size')

        chat_history = user_data.get('chat_history', [])
        if not chat_history:
            raise HTTPException(status_code=404, detail="No chat history found for this request")

        chat_html_content = format_chat_history_for_html(chat_history)

        safe_company_name = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in company_name).rstrip()
        output_filename = f"chat_history_{safe_company_name.lower().replace(' ', '_')}_{request_id}.pdf"
        
        pdf_data_for_template = {
            "title": f"Chat History for {company_name}",
            "company_name": company_name,
            "industry": industry,
            "company_size": company_size,
            "chat_html_content": chat_html_content
        }

        pdf_request = PDFRequest(
            template_name="chat_export_template", 
            data=pdf_data_for_template,
            output_filename=output_filename
        )

        pdf_path = await generate_pdf(pdf_request) 

        email_subject = f"Exported Chat History for {company_name}"
        email_body = f"""Dear {company_name},

Please find attached the exported chat history for your records.

Best regards,
AI Roadmap Team"""

        email_result = await send_email(
            to_email=email,
            subject=email_subject,
            content=email_body,
            attachment_path=pdf_path
        )

        if email_result.get("status") == "success":
            return {
                "status": "success",
                "message": "Chat history PDF generated and sent to email successfully.",
                "filename": output_filename,
                "pdf_path": pdf_path 
            }
        else:
            print(f"Email sending failed for chat history export (request_id: {request_id}): {email_result}")
            return {
                "status": "partial_success",
                "message": f"Chat history PDF generated successfully but email sending failed: {email_result.get('message', 'Unknown error')}",
                "filename": output_filename,
                "pdf_path": pdf_path
            }

    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        error_detail = f"Error exporting chat history: {str(e)}"
        print(f"Chat History Export Error (request_id: {request_id}): {error_detail}\n{traceback.format_exc()}")
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