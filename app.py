from flask import Flask, request, render_template
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from keybert import KeyBERT

# Flask 앱 초기화
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# KeyBERT 모델 초기화
kw_model = KeyBERT()

# CSV 시각화 함수
def create_plot(csv_file, low_intervals):
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(10, 5))
    plt.plot(df['Timestamp'], df['Attention Value'], marker='o', linestyle='-', color='b')
    plt.title('Attention Value Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Attention Value')
    plt.ylim(0, 100)
    plt.grid(True)

    # X축 레이블 회전 (사선 출력)
    plt.xticks(rotation=45)

    # 집중도 저하 구간 강조
    for start, end in low_intervals:
        start_idx = df[df['Timestamp'] == start].index[0]
        end_idx = df[df['Timestamp'] == end].index[0]
        plt.axvspan(df['Timestamp'].iloc[start_idx], df['Timestamp'].iloc[end_idx], color='red', alpha=0.3)

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

# 집중도 평가 함수
def find_low_attention_intervals(csv_file):
    df = pd.read_csv(csv_file)
    if 'Attention Value' not in df.columns:
        raise ValueError("CSV 파일에 'Attention Value' 열이 없습니다.")

    low_intervals = []
    window_size = 8

    for i in range(len(df) - window_size + 1):
        window = df['Attention Value'].iloc[i:i + window_size]
        if (window < 50).sum() >= 3:
            start = df['Timestamp'].iloc[i]
            end = df['Timestamp'].iloc[i + window_size - 1]
            if not low_intervals or start > low_intervals[-1][1]:
                low_intervals.append((start, end))

    return low_intervals

# 블랭크 문제 생성 함수
def generate_blank_questions(text, threshold=0.5, blank="_____"):
    lines = text.splitlines()
    questions = []

    for line in lines:
        if line.strip():
            try:
                keywords = kw_model.extract_keywords(line, top_n=3)
                filtered_keywords = [(kw, score) for kw, score in keywords if score >= threshold]

                for keyword, _ in filtered_keywords:
                    blank_line = line.replace(keyword, blank, 1)
                    questions.append((blank_line, keyword))

            except Exception as e:
                print(f"[오류 발생] 키워드 추출 실패: {e}")

    return questions

@app.route('/', methods=['GET', 'POST'])
def upload_text():
    if request.method == 'POST':
        text_content = request.form.get('text_content')
        if not text_content.strip():
            return render_template('error.html', message="텍스트 입력이 비어 있습니다.")
        questions = generate_blank_questions(text_content)
        return render_template('csv_upload.html', questions=questions, text_content=text_content)
    return render_template('upload_text.html')

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    csv_file = request.files.get('csv_file')
    text_content = request.form.get('text_content')

    if not csv_file:
        return render_template('error.html', message="CSV 파일이 업로드되지 않았습니다.")

    try:
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
        csv_file.save(csv_path)
        low_intervals = find_low_attention_intervals(csv_path)
        plot_url = create_plot(csv_path, low_intervals)

        if not low_intervals:
            return render_template('review.html', plot_url=plot_url, low_intervals=low_intervals, message="완전히 몰입한 당신은 멋쟁이!")

        questions = generate_blank_questions(text_content)
        return render_template('quiz.html', questions=questions, plot_url=plot_url)

    except Exception as e:
        print(f"[오류 발생] {e}")
        return render_template('error.html', message=f"오류 발생: {str(e)}")

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    correct_answers = request.form.getlist('correct_answers')
    user_answers = request.form.getlist('user_answers')

    if correct_answers == user_answers:
        return "고생했어요!"  
    else:
        return "다시 시도해보세요."

if __name__ == '__main__':
    app.run(debug=True)
