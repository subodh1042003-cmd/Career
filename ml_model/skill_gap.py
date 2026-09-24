# ==========================================
# CAREERDECODE - SKILL GAP ANALYSIS
# ==========================================

CAREER_SKILLS = {

    "Python Developer": [
        "Python",
        "Django",
        "Flask",
        "SQL",
        "Git",
        "REST API"
    ],

    "Java Developer": [
        "Java",
        "Spring",
        "SQL",
        "Git",
        "REST API"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "SQL",
        "Git"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Excel",
        "Power BI",
        "Statistics"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Scikit-learn",
        "Statistics",
        "TensorFlow"
    ],

    "AI ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "NumPy",
        "Pandas"
    ],

    "Cloud Engineer": [
        "AWS",
        "Azure",
        "Google Cloud",
        "Docker",
        "Kubernetes",
        "Linux",
        "Git"
    ],

    "Cybersecurity": [
        "Cybersecurity",
        "Network Security",
        "Linux",
        "Ethical Hacking",
        "Cryptography",
        "Penetration Testing"
    ]
}


def analyze_skill_gap(career, user_skills):

    required_skills = CAREER_SKILLS.get(
        career,
        []
    )

    user_skills_lower = [
        skill.lower()
        for skill in user_skills
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in user_skills_lower:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    if len(required_skills) > 0:

        match_percentage = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    else:

        match_percentage = 0

    return {
        "career": career,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(
            match_percentage,
            2
        )
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    user_skills = [
        "Python",
        "SQL",
        "Pandas",
        "NumPy"
    ]

    result = analyze_skill_gap(
        "Data Scientist",
        user_skills
    )

    print("\nCareer:")
    print(result["career"])

    print("\nRequired Skills:")
    print(result["required_skills"])

    print("\nMatched Skills:")
    print(result["matched_skills"])

    print("\nMissing Skills:")
    print(result["missing_skills"])

    print("\nSkill Match:")
    print(
        result["match_percentage"],
        "%"
    )