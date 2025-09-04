import fitz
import docx
import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + " "
    return text

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    words = text.split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return set(keywords)

def compare_resumes(job_resume, candidate_resume):
    job_keywords = preprocess(extract_text(job_resume))
    candidate_keywords = preprocess(extract_text(candidate_resume))

    if len(job_keywords) == 0:
        return 0

    common = job_keywords & candidate_keywords
    score = (len(common) / len(job_keywords)) * 100
    return score

job_resume = r"C:\Users\G.VINAY\OneDrive\Desktop\ATS\sample_resume.pdf"
candidate_resume = r"C:\Users\G.VINAY\OneDrive\Desktop\Resumes\Vinay_resume.docx"

score = compare_resumes(job_resume, candidate_resume)
print(f"Match Score: {score:.2f}%")
