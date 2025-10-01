from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
from werkzeug.utils import secure_filename
from simplifier import process_text

app = Flask(__name__)

# Define allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process_report', methods=['POST'])
def process_report():
    """
    API endpoint to process a medical report.
    It can accept either raw text or an image file.
    """
    # --- Handle Image Input ---
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "reason": "No file selected"}), 400
        if file and allowed_file(file.filename):
            try:
                image_bytes = file.read()
                image = Image.open(io.BytesIO(image_bytes))
                # Use Tesseract OCR to extract text from the image
                extracted_text = pytesseract.image_to_string(image)
                if not extracted_text.strip():
                     return jsonify({"status": "unprocessed", "reason": "No text could be extracted from the image"}), 400
                
                # Process the extracted text
                result = process_text(extracted_text)
                return jsonify(result)

            except Exception as e:
                return jsonify({"status": "error", "reason": f"Image processing failed: {str(e)}"}), 500
        else:
            return jsonify({"status": "error", "reason": "Invalid file type. Please upload an image."}), 400

    # --- Handle Text Input ---
    elif request.is_json:
        data = request.get_json()
        if 'text' not in data or not data['text'].strip():
            return jsonify({"status": "error", "reason": "Missing or empty 'text' field in JSON payload"}), 400
        
        input_text = data['text']
        try:
            result = process_text(input_text)
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "reason": f"Text processing failed: {str(e)}"}), 500
            
    # --- Handle Invalid Input ---
    else:
        return jsonify({"status": "error", "reason": "Invalid request. Please provide a JSON payload with 'text' or upload an image file."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

