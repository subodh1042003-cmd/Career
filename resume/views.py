import os
import re
import joblib
import pymupdf

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from .models import TeamMember
from ml_model.skills import extract_skills
from ml_model.career_recommendation import recommend_careers


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "career_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "ml_model", "tfidf_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


CAREER_SKILLS = {
    "Python/Django Developer": [
        "python", "django", "flask", "fastapi",
        "rest api", "postgresql", "sql", "pandas"
    ],
    "Java Developer": [
        "java", "spring", "spring boot", "hibernate",
        "j2ee", "jsp", "servlet", "maven", "sql"
    ],
    "Frontend Developer": [
        "html", "css", "javascript", "react",
        "angular", "vue", "bootstrap", "typescript"
    ],
    "Backend Developer": [
        "node.js", "nodejs", "express", "backend",
        "rest api", "php", "laravel", "mongodb", "mysql"
    ],
    "Full Stack Developer": [
        "html", "css", "javascript", "react",
        "node.js", "nodejs", "express", "mongodb",
        "mysql", "full stack"
    ],
    "DevOps Engineer": [
        "aws", "azure", "docker", "kubernetes",
        "jenkins", "terraform", "ansible", "linux", "ci/cd"
    ],
    "Database Developer": [
        "sql", "mysql", "postgresql", "oracle",
        "mongodb", "database", "pl/sql",
        "database design", "normalization"
    ],
    "Data Analyst": [
        "excel", "power bi", "tableau", "sql",
        "data analysis", "data visualization",
        "business intelligence", "reporting", "statistics"
    ],
    "Data Scientist": [
        "python", "pandas", "numpy", "scipy",
        "statistics", "machine learning", "data science",
        "predictive modeling", "matplotlib", "seaborn"
    ],
    "Machine Learning Engineer": [
        "python", "machine learning", "tensorflow",
        "pytorch", "scikit-learn", "keras",
        "deep learning", "neural network", "ml model"
    ]
}


def contains_skill(text, skill):
    text = text.lower()
    skill = skill.lower()

    if skill in ["node.js", "nodejs"]:
        return bool(
            re.search(r"\bnode\s*\.?\s*js\b", text)
            or re.search(r"\bnodejs\b", text)
        )

    if skill in ["ci/cd", "pl/sql"]:
        return skill in text

    return bool(
        re.search(
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill)
            + r"(?![a-zA-Z0-9])",
            text
        )
    )


def smart_career_prediction(resume_text):
    scores = {}

    for career, skills in CAREER_SKILLS.items():
        score = 0

        for skill in skills:
            if contains_skill(resume_text, skill):
                score += 3 if len(skill.split()) >= 2 else 1

        scores[career] = score

    best_career = max(scores, key=scores.get)
    best_score = scores[best_career]

    if best_score >= 2:
        return best_career

    resume_vector = vectorizer.transform([resume_text])
    return model.predict(resume_vector)[0]


def calculate_skill_match(career, resume_text):
    required_skills = CAREER_SKILLS.get(career, [])

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if contains_skill(resume_text, skill):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if required_skills:
        percentage = (len(matched_skills) / len(required_skills)) * 100
    else:
        percentage = 0

    return {
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(percentage, 2)
    }


def home(request):
    return render(request, "home.html")


@ensure_csrf_cookie
def analyze_resume(request):
    if request.method != "POST":
        return render(request, "predict.html")

    uploaded_file = request.FILES.get("resume")

    if not uploaded_file:
        return render(
            request,
            "predict.html",
            {"error": "Please upload a resume."}
        )

    filename = uploaded_file.name
    extension = os.path.splitext(filename)[1].lower()

    if extension not in [".pdf", ".docx"]:
        return render(
            request,
            "predict.html",
            {"error": "Only PDF and DOCX files are supported."}
        )

    media_path = os.path.join(BASE_DIR, "media")
    os.makedirs(media_path, exist_ok=True)

    fs = FileSystemStorage(location=media_path)
    saved_filename = fs.save(filename, uploaded_file)
    file_path = fs.path(saved_filename)

    resume_text = ""

    if extension == ".pdf":
        try:
            document = pymupdf.open(file_path)

            for page in document:
                resume_text += page.get_text() + "\n"

            document.close()

        except Exception as e:
            return render(
                request,
                "predict.html",
                {"error": f"PDF reading error: {e}"}
            )

    elif extension == ".docx":
        try:
            from docx import Document

            document = Document(file_path)

            for paragraph in document.paragraphs:
                resume_text += paragraph.text + "\n"

        except Exception as e:
            return render(
                request,
                "predict.html",
                {"error": f"DOCX reading error: {e}"}
            )

    resume_text = resume_text.strip()

    if not resume_text:
        return render(
            request,
            "predict.html",
            {"error": "Could not extract text from resume."}
        )

    predicted_career = smart_career_prediction(resume_text)

    detected_skills = extract_skills(resume_text)

    skill_gap = calculate_skill_match(
        predicted_career,
        resume_text
    )

    try:
        recommendations = recommend_careers(resume_text)
    except Exception:
        recommendations = []

    context = {
        "predicted_career": predicted_career,
        "detected_skills": detected_skills,

        "required_skills": skill_gap["required_skills"],
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],

        "skill_match": skill_gap["match_percentage"],
        "resume_score": skill_gap["match_percentage"],

        "recommendations": recommendations,
        "resume_text": resume_text,
    }

    return render(
        request,
        "result.html",
        context
    )


def team(request):
    members = TeamMember.objects.filter(is_active=True)

    return render(
        request,
        "team.html",
        {"members": members}
    )


def about(request):
    return render(request, "about.html")


def analysis(request):
    return render(request, "analysis.html")


def predict(request):
    return analyze_resume(request)


def contact(request):
    return render(request, "contact.html")

