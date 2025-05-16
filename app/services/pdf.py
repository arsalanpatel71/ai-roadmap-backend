import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from ..schemas.pdf import PDFRequest
from ..core.config import settings 

TEMPLATE_DIR = "app/templates"
OUTPUT_DIR = "app/static/pdfs"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

pdfkit_config = None
if settings.WKHTMLTOPDF_PATH:
    try:
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
       
    except Exception as e:
        print(f"Warning: Could not configure pdfkit with path '{settings.WKHTMLTOPDF_PATH}': {e}")

async def generate_pdf(request: PDFRequest) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    template = env.get_template(f"{request.template_name}.html")
    
    if "generated_at" not in request.data:
        request.data["generated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    html_content = template.render(**request.data)
    
    if not request.output_filename:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        request.output_filename = f"generated_document_{timestamp}.pdf"
        
    output_path = os.path.join(OUTPUT_DIR, request.output_filename)
    
    options = {
        'page-size': 'A4',
        'margin-top': '25mm',
        'margin-right': '25mm',
        'margin-bottom': '25mm',
        'margin-left': '25mm',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': None
    }
    
    pdfkit.from_string(
        html_content,
        output_path,
        options=options,
        configuration=pdfkit_config
    )
    return output_path