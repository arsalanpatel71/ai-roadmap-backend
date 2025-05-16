import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from ..schemas.pdf import PDFRequest

TEMPLATE_DIR = "app/templates"
OUTPUT_DIR = "/tmp/pdfs"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Construct the absolute path to the wkhtmltopdf binary
# This assumes your 'bin' directory is at the project root.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
WKHTMLTOPDF_BINARY_PATH = os.path.join(PROJECT_ROOT, 'bin', 'wkhtmltopdf')

# Check if the binary exists at the constructed path for debugging
if not os.path.exists(WKHTMLTOPDF_BINARY_PATH):
    print(f"Warning: wkhtmltopdf binary not found at {WKHTMLTOPDF_BINARY_PATH}")
    # Fallback or raise an error if needed, for now, pdfkit will try to find it in PATH
    config = pdfkit.configuration() 
else:
    print(f"Using wkhtmltopdf binary at {WKHTMLTOPDF_BINARY_PATH}")
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_BINARY_PATH)

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