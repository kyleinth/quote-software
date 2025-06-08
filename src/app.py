from flask import Flask, request, jsonify, render_template_string
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

PDF_RATE = 0.05  # price per page in USD
STEP_RATE = 0.1  # price per MB in USD

HTML_FORM = """
<!doctype html>
<title>Quote Generator</title>
<h1>Upload PDF and STEP files</h1>
<form method=post enctype=multipart/form-data action="/quote">
  <label>PDF file:</label><input type=file name=pdf><br>
  <label>STEP file:</label><input type=file name=step><br>
  <input type=submit value=Get Quote>
</form>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FORM)


def calculate_quote(pdf_path: str, step_path: str) -> dict:
    """Calculate quote based on page count and file size."""
    pdf_pages = 0
    if pdf_path and os.path.getsize(pdf_path) > 0:
        try:
            reader = PdfReader(pdf_path)
            pdf_pages = len(reader.pages)
        except Exception:
            pdf_pages = 0

    step_size_mb = 0.0
    if step_path and os.path.getsize(step_path) > 0:
        step_size_mb = os.path.getsize(step_path) / (1024 * 1024)

    cost_pdf = pdf_pages * PDF_RATE
    cost_step = step_size_mb * STEP_RATE
    total = cost_pdf + cost_step

    return {
        "pdf_pages": pdf_pages,
        "step_size_mb": round(step_size_mb, 2),
        "cost_pdf": round(cost_pdf, 2),
        "cost_step": round(cost_step, 2),
        "total": round(total, 2),
    }


@app.route('/quote', methods=['POST'])
def quote():
    pdf_file = request.files.get('pdf')
    step_file = request.files.get('step')

    pdf_path = None
    step_path = None
    try:
        if pdf_file:
            pdf_path = os.path.join('/tmp', pdf_file.filename)
            pdf_file.save(pdf_path)
        if step_file:
            step_path = os.path.join('/tmp', step_file.filename)
            step_file.save(step_path)

        result = calculate_quote(pdf_path, step_path)
        return jsonify(result)
    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
        if step_path and os.path.exists(step_path):
            os.remove(step_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
