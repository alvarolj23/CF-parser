import os
import secrets
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from parser import ResumeParser
import argparse

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.add_url_rule("/resume/<name>", endpoint="resume", build_only=True)
app.secret_key = secrets.token_urlsafe(32)

parser = ResumeParser(os.getenv("OPENAI_API_KEY"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
@app.route("/resume", methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('resume', name=filename))
    return render_template('index.html')

def decompose_basic_info(basic_info):
    decomposed_info = []
    for key, value in basic_info.items():
        decomposed_info.append({
            'field': key.replace('_', ' ').capitalize(),
            'value': value
        })
    return decomposed_info

def decompose_work_experience(work_experience):
    decomposed_experience = []
    for experience in work_experience:
        decomposed_experience.append({
            'job_title': experience['job_title'],
            'company': experience['company'],
            'location': experience['location'],
            'duration': experience['duration'],
            'job_summary': experience['job_summary']
        })
    return decomposed_experience

def decompose_skills(skills):
    decomposed_skills = []
    for skill in skills:
        decomposed_skills.append({
            'skill_name': skill['skill_name'],
            'skill_level': skill['skill_level']
        })
    return decomposed_skills


@app.route('/resume/<name>')
def display_resume(name):
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], name)
    resume_data = parser.query_resume(resume_path)

    # Perform further decomposition of the JSON data if needed
    resume_data['basic_info'] = decompose_basic_info(resume_data['basic_info'])
    resume_data['work_experience'] = decompose_work_experience(resume_data['work_experience'])
    resume_data['skills'] = decompose_skills(resume_data['skills'])

    return render_template('resume.html', resume_data=resume_data)

if __name__ == "__main__":
    host = os.getenv("RESUME_PARSER_HOST", '127.0.0.1')
    port = os.getenv("RESUME_PARSER_PORT", '5000')
    assert port.isnumeric(), 'port must be an integer'
    port = int(port)
    app.run(host=host, port=port, debug=True)

