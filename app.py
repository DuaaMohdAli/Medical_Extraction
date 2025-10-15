from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF for PDF parsing

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_data():
    file = request.files['file']
    text = ""

    if file.filename.endswith('.pdf'):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    else:
        text = file.read().decode('utf-8')

    extracted = {
        "Patient Name": extract_field(text, "Name"),
        "Diagnosis": extract_field(text, "Diagnosis"),
        "Medications": extract_field(text, "Medications")
    }

    return jsonify(extracted)

def extract_field(text, keyword):
    for line in text.splitlines():
        if keyword.lower() in line.lower():
            parts = line.split(":")
            if len(parts) > 1:
                return parts[1].strip()
    return "Not found"

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
