import re


SKILLS = [

    # Programming Languages
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "PHP",
    "R",
    "Go",
    "Ruby",
    "Kotlin",
    "Swift",

    # Web Development
    "HTML",
    "CSS",
    "Bootstrap",
    "Tailwind CSS",
    "React",
    "Angular",
    "Vue",
    "Django",
    "Flask",
    "FastAPI",
    "Node.js",
    "Express",
    "Next.js",

    # Database
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Oracle",
    "Redis",

    # Data Science
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "SciPy",
    "Statistics",
    "Data Analysis",
    "Data Visualization",

    # Artificial Intelligence
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Neural Network",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",
    "Generative AI",

    # AI / ML Frameworks
    "TensorFlow",
    "Keras",
    "PyTorch",
    "OpenCV",
    "Hugging Face",

    # Cloud
    "AWS",
    "Amazon Web Services",
    "Microsoft Azure",
    "Azure",
    "Google Cloud",
    "Google Cloud Platform",
    "GCP",
    "Docker",
    "Kubernetes",

    # Cybersecurity
    "Cybersecurity",
    "Network Security",
    "Information Security",
    "Ethical Hacking",
    "Penetration Testing",
    "Cryptography",
    "Cyber Security",

    # DevOps
    "Git",
    "GitHub",
    "GitLab",
    "Jenkins",
    "CI/CD",
    "Linux",
    "Bash",
    "REST API",
    "API",

    # Data Analytics
    "Power BI",
    "Tableau",
    "Microsoft Excel",
    "Excel",

    # Other
    "Agile",
    "Scrum",
    "Problem Solving",
    "Data Structures",
    "Algorithms",
    "OOP",
    "Object Oriented Programming"
]


def extract_skills(text):

    found_skills = []

    if not text:
        return found_skills

    text_lower = text.lower()

    for skill in SKILLS:

        skill_lower = skill.lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(skill_lower)
            + r"(?!\w)"
        )

        if re.search(pattern, text_lower):

            found_skills.append(skill)

    found_skills = list(
        dict.fromkeys(found_skills)
    )

    found_skills.sort()

    return found_skills


if __name__ == "__main__":

    sample_text = """
    I am a Python developer with experience in
    Django, React, SQL, Machine Learning,
    Pandas, NumPy and Git.
    """

    skills = extract_skills(sample_text)

    print("\nDetected Skills:")

    for skill in skills:

        print("-", skill)