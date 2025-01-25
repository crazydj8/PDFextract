import os
import sys
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_session import Session

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.pdfextractor import pdf_extractor
from modules.llm import LLM

app = Flask(__name__)
CORS(app)

# Configure session
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify(error="No PDF file provided"), 400

    pdf_file = request.files['pdf']
    file_stream = pdf_file.read()
    api_key = request.form.get('apiKey')  # Get API key from form data

    result = pdf_extractor.extract_pdf_data(file_stream)

    if not result['text_found']:
        session['metadata'] = result['metadata']
        return jsonify(metadata=result['metadata']), 200

    # Store the extracted text and API key in the session
    session['result'] = result
    session['api_key'] = api_key

    return jsonify(result), 200

@app.route('/api/ask', methods=['POST'])
def ask_question():
    result = session.get('result')
    api_key = session.get('api_key')

    if not result or not api_key:
        return jsonify(error="LLM instance not initialized"), 400

    llm_instance = LLM(result, api_key)

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify(error="No question provided"), 400

    try:
        answer = llm_instance.answer(question)
    except ValueError as e:
        return jsonify(error=str(e)), 429

    return jsonify(answer=answer["content"]), 200

@app.route('/api/extracted_text', methods=['GET'])
def get_extracted_text():
    result = session.get('result')
    if not result:
        return jsonify(error="No extracted text found"), 400
    return jsonify(extracted_text=result['text']), 200

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    metadata = session.get('metadata')
    if not metadata:
        return jsonify(error="No metadata found"), 400
    return jsonify(metadata=metadata), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)