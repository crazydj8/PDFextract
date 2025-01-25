import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from modules.pdfextractor import pdf_extractor
from modules.llm import LLM

app = Flask(__name__)
CORS(app)

result = {}
llm_instance = None  # Global variable to store the LLM instance

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global llm_instance, result

    if 'pdf' not in request.files:
        return jsonify(error="No PDF file provided"), 400

    pdf_file = request.files['pdf']
    file_stream = pdf_file.read()
    api_key = request.form.get('apiKey')  # Get API key from form data

    result = pdf_extractor.extract_pdf_data(file_stream)

    if not result['text_found']:
        return jsonify(metadata=result['metadata']), 200

    # Create an LLM instance and generate embeddings
    try:
        llm_instance = LLM(result, api_key)
    except ValueError as e:
        return jsonify(error=str(e)), 400

    return jsonify(result), 200

@app.route('/ask', methods=['POST'])
def ask_question():
    global llm_instance  # Use the global variable

    if not llm_instance:
        return jsonify(error="LLM instance not initialized"), 400

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify(error="No question provided"), 400

    try:
        answer = llm_instance.answer(question)
    except ValueError as e:
        return jsonify(error=str(e)), 429

    return jsonify(answer=answer["content"]), 200

@app.route('/extracted_text', methods=['GET'])
def get_extracted_text():
    return jsonify(extracted_text=result['text']), 200

@app.route('/metadata', methods=['GET'])
def get_metadata():
    return jsonify(metadata=result['metadata']), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)