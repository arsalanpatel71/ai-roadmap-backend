import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from ..schemas.pdf import PDFRequest

TEMPLATE_DIR = "app/templates"
OUTPUT_DIR = "/tmp/pdfs"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
# config = pdfkit.configuration()

async def generate_pdf(request: PDFRequest) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    template = env.get_template(f"{request.template_name}.html")
    
    request.data["generated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = template.render(**request.data)
    
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
        configuration=config
    ) 