from flask import Flask, render_template, request, redirect, url_for, flash
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import re
#import openai

# nltk 리소스 다운로드
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# OpenAI API 키 설정
#openai.api_key = ''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        text = extract_text_from_pdf(file)
        preprocessed_text = preprocess_text(text)
        summary = get_summary(preprocessed_text)

        return render_template('result.html', summary=summary)

    return render_template('index.html')


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()

    return text


def preprocess_text(text):
    # 1. 텍스트 정리
    text = text.lower()  # 소문자 변환
    #text = re.sub(r'\d+', '', text)  # 숫자 제거
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # ASCII 문자가 아닌 문자 제거

    # 2. 불필요한 섹션 제거 (이 부분은 논문 형식에 따라 맞게 조정할 필요가 있음)
    #references_start = text.find("references")
    #if references_start != -1:
    #    text = text[:references_start]

    # 3. 문장 토큰화
    sentences = sent_tokenize(text)
    print(len(sentences))

    # 4. 불용어 제거 & 5. 어근화
    stop_words = set(stopwords.words('english'))
    processed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        #words = [word for word in words if word not in stop_words]
        processed_sentences.append(' '.join(words))

    # 6 & 7. 짧은 문장 제거
    MIN_SENT_LENGTH = 3
    processed_sentences = [sent for sent in processed_sentences if len(sent.split()) > MIN_SENT_LENGTH]

    # 8. 내용 기반 필터링 (예시)
    keywords = ["result", "method", "conclusion", "finding"]
    important_sentences = [sent for sent in processed_sentences if any(keyword in sent for keyword in keywords)]

    return ' '.join(important_sentences)


def get_summary(text):
    pass
    
    """
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"Summarize the following text:\n\n{text}",
      max_tokens=150
    )
    return response.choices[0].text.strip()
    """

if __name__ == '__main__':
    app.run(debug=True)
