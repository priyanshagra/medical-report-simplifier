# medical-report-simplifier
AI-Powered Medical Report Simplifier API
This backend service takes medical reports (as raw text or images), extracts key test results, normalizes them, and provides a patient-friendly summary.

Features
OCR Support: Extracts text from uploaded images of medical reports.

Text Extraction: Parses raw text to find test names, values, and units.

Normalization: Standardizes test names and determines status (low, high, normal) based on reference ranges.

Patient-Friendly Summary: Generates simple, non-diagnostic explanations for the findings.

Guardrails: Includes basic checks to handle errors and invalid inputs.

API Endpoints
Process a Report
URL: /process_report

Method: POST

Description: Processes a medical report. Can be used in two ways:

Text Input (JSON): Send a JSON payload with a text key.

Image Input (Form Data): Upload an image file with the key file.

Sample curl Requests
1. Using Text Input:

curl -X POST -H "Content-Type: application/json" \
-d '{"text": "CBC: Hemoglobin 10.2 g/dL (Low), WBC 11,200 /uL (High)"}' \
[http://127.0.0.1:5000/process_report](http://127.0.0.1:5000/process_report)

2. Using Image Input:

Replace path/to/your/report.png with the actual path to your image file.

curl -X POST -F "file=@path/to/your/report.png" \
[http://127.0.0.1:5000/process_report](http://127.0.0.1:5000/process_report)

Setup and Running Locally
Clone the repository:

git clone <your-repo-url>
cd medical-report-simplifier

Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Install Tesseract OCR:

macOS: brew install tesseract

Ubuntu/Debian: sudo apt-get install tesseract-ocr

Run the application:

python app.py

The server will be running at http://127.0.0.1:5000.
