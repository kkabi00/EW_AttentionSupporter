from flask import Flask, request, render_template
import pandas as pd
import random
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def evaluate_concentration(csv_file):
    df = pd.read_csv(csv_file)
    fail_count = 0
    window_size = 8

    for i in range(len(df) - window_size + 1):
        window = df['Attention Value'].iloc[i:i+window_size]
        if (window <= 50).sum() >= 3:
            fail_count += 1

    if fail_count > 0:
        return "fail"
    elif (df['Attention Value'] > 50).all():
        return "pass"
    else:
        return "undecided"

def generate_quiz(text_content):
    content = text_content.splitlines()
    questions = random.sample(content, min(5, len(content)))
    return questions

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        csv_file = request.files.get('csv_file')
        text_content = request.form.get('text_content')

        if csv_file and text_content.strip():
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
            csv_file.save(csv_path)

            result = evaluate_concentration(csv_path)

            if result == "fail":
                quiz_questions = generate_quiz(text_content)
                return render_template('quiz.html', questions=quiz_questions)
            elif result == "pass":
                return "굉장한 집중력이에요!"
            else:
                return "집중도 평가를 진행할 수 없습니다."

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
