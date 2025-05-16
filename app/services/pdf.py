import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from ..schemas.pdf import PDFRequest
from ..core.config import settings # Import settings

TEMPLATE_DIR = "app/templates"
OUTPUT_DIR = "app/static/pdfs"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Configure pdfkit using the path from settings
pdfkit_config = None
if settings.WKHTMLTOPDF_PATH:
    try:
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
        # You might want to add a check here to see if the path is valid
        # e.g., if not os.path.isfile(settings.WKHTMLTOPDF_PATH):
        #    print(f"Warning: WKHTMLTOPDF_PATH '{settings.WKHTMLTOPDF_PATH}' does not point to a valid file.")
        #    pdfkit_config = None # Fallback to system PATH
    except Exception as e:
        print(f"Warning: Could not configure pdfkit with path '{settings.WKHTMLTOPDF_PATH}': {e}")
        # pdfkit_config will remain None, allowing pdfkit to try the system PATH

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
        configuration=pdfkit_config
    ) 