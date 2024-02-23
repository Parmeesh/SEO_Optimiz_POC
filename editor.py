from flask import Flask, request, send_from_directory, jsonify, send_file
import os
from flask_cors import CORS
from docx import Document
import io


app=Flask(__name__)
CORS(app)
content=""
# sample=st.session_state['final_html_with_img_gemini']

@app.route("/get-html-content", methods=["POST"])
def get_html_content():
    # with open(file='sample_html_file.html', mode='r') as file:
    #     content = file.read()
    global content#
    content=request.json.get('content')
    # if not content:"<p> Edit me...</p>"
    return jsonify({"content":content})

@app.route("/content-flask", methods=["POST"])
def content_flask():
    global content
    return jsonify({"content": content})

@app.route("/download-html-content", methods=["POST"])
def download_html_content():
    content = request.json.get('content')
    document = Document()
    document.add_paragraph(content)
    # Save the document to a BytesIO object
    file_stream = io.BytesIO()
    document.save(file_stream)
    file_stream.seek(0)
    return send_file(file_stream, as_attachment=True, download_name="document.docx", mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


@app.route("/")
def index():
    return send_from_directory('.', 'editor.html')

if __name__ == "__main__":
    app.run(port='3002',debug=True)
