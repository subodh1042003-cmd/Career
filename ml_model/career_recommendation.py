import os
import joblib
import numpy as np


# ==========================================
# PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "career_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "tfidf_vectorizer.pkl"
)


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(
    VECTORIZER_PATH
)


# ==========================================
# 12 CAREER PATHS
# ==========================================

ALL_CAREERS = [
    "Backend Developer",
    "Data Analyst",
    "Data Scientist",
    "Database Developer",
    "DevOps Engineer",
    "Frontend Developer",
    "Full Stack Developer",
    "Java Developer",
    "Machine Learning Engineer",
    "Python/Django Developer",
    "UI/UX Designer",
    "Cloud Engineer"
]


# ==========================================
# KEYWORDS FOR ADDITIONAL CAREERS
# ==========================================

EXTRA_CAREER_KEYWORDS = {

    "UI/UX Designer": [
        "ui",
        "ux",
        "figma",
        "adobe xd",
        "wireframe",
        "prototype",
        "user experience",
        "user interface",
        "photoshop"
    ],

    "Cloud Engineer": [
        "aws",
        "azure",
        "gcp",
        "google cloud",
        "cloud computing",
        "cloud engineer",
        "ec2",
        "s3",
        "cloud"
    ]
}


# ==========================================
# RECOMMEND CAREERS
# ==========================================

def recommend_careers(resume_text):

    # ======================================
    # TF-IDF
    # ======================================

    resume_vector = vectorizer.transform(
        [resume_text]
    )


    # ======================================
    # MODEL PROBABILITIES
    # ======================================

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            resume_vector
        )[0]

        classes = model.classes_

    else:

        decision_scores = model.decision_function(
            resume_vector
        )

        if len(decision_scores.shape) > 1:
            decision_scores = decision_scores[0]

        classes = model.classes_

        exp_scores = np.exp(
            decision_scores -
            np.max(decision_scores)
        )

        probabilities = (
            exp_scores /
            exp_scores.sum()
        )


    # ======================================
    # MODEL SCORE LIST
    # ======================================

    career_scores = []

    for career, probability in zip(
        classes,
        probabilities
    ):

        career_scores.append({

            "career": career,

            "score": round(
                float(probability) * 100,
                2
            )

        })


    # ======================================
    # ADD UI/UX + CLOUD
    # ======================================

    text = resume_text.lower()

    for career, keywords in EXTRA_CAREER_KEYWORDS.items():

        matches = 0

        for keyword in keywords:

            if keyword in text:
                matches += 1


        if matches > 0:

            extra_score = min(
                matches * 3.0,
                15.0
            )

        else:

            extra_score = 0.5


        career_scores.append({

            "career": career,

            "score": round(
                extra_score,
                2
            )

        })


    # ======================================
    # NORMALIZE ALL SCORES TO 100%
    # ======================================

    total = sum(
        item["score"]
        for item in career_scores
    )


    if total > 0:

        for item in career_scores:

            item["score"] = round(
                (
                    item["score"] /
                    total
                ) * 100,
                2
            )


    # ======================================
    # SORT HIGH → LOW
    # ======================================

    career_scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # ======================================
    # ALWAYS RETURN 12
    # ======================================

    return career_scores[:12]


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    sample_resume = """

    Python Django REST API PostgreSQL
    Pandas NumPy Machine Learning
    React AWS Docker SQL

    """

    recommendations = recommend_careers(
        sample_resume
    )


    print(
        "\n===================================="
    )

    print(
        "ALL 12 CAREER RECOMMENDATIONS"
    )

    print(
        "===================================="
    )


    for index, result in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{index}. "
            f"{result['career']} "
            f"- "
            f"{result['score']}%"
        )
