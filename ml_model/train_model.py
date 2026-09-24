import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "career_dataset.csv"
)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(DATASET_PATH)

print("\nDataset loaded successfully!")

print(
    "\nTotal resumes:",
    len(df)
)

print(
    "\nDataset columns:"
)

print(
    df.columns.tolist()
)


# ==========================================
# FIND TEXT & TARGET COLUMNS
# ==========================================

# IMPORTANT:
# Change these two names only if your CSV
# uses different column names.

TEXT_COLUMN = "resume_text"

TARGET_COLUMN = "career"


# ==========================================
# REMOVE EMPTY DATA
# ==========================================

df = df.dropna(
    subset=[
        TEXT_COLUMN,
        TARGET_COLUMN
    ]
)


X = df[TEXT_COLUMN].astype(str)

y = df[TARGET_COLUMN].astype(str)


print(
    "\nCareer classes:"
)

print(
    y.value_counts()
)


# ==========================================
# TF-IDF
# ==========================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2)
)


X_tfidf = vectorizer.fit_transform(X)


print(
    "\nTF-IDF created successfully!"
)

print(
    "Feature count:",
    X_tfidf.shape[1]
)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X_tfidf,
    y,

    test_size=0.25,

    random_state=42,

    stratify=y
)


# ==========================================
# MODELS
# ==========================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=2000
        ),

    "Naive Bayes":
        MultinomialNB(),

    "SVM":
        LinearSVC(),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
}


results = {}


# ==========================================
# TRAIN & EVALUATE
# ==========================================

for name, model in models.items():

    print(
        "\n================================"
    )

    print(
        "Training:",
        name
    )

    print(
        "================================"
    )


    model.fit(
        X_train,
        y_train
    )


    y_pred = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        y_pred
    )


    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )


    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )


    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )


    results[name] = {
        "model": model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


    print(
        f"Accuracy  : {accuracy * 100:.2f}%"
    )

    print(
        f"Precision : {precision * 100:.2f}%"
    )

    print(
        f"Recall    : {recall * 100:.2f}%"
    )

    print(
        f"F1 Score  : {f1 * 100:.2f}%"
    )


# ==========================================
# MODEL COMPARISON
# ==========================================

print(
    "\n\n"
)

print(
    "========================================"
)

print(
    "MODEL COMPARISON"
)

print(
    "========================================"
)


for name, result in results.items():

    print(
        f"{name:20}"
        f" Accuracy: "
        f"{result['accuracy'] * 100:.2f}%"
        f" | F1: "
        f"{result['f1'] * 100:.2f}%"
    )


# ==========================================
# BEST MODEL
# ==========================================

best_name = max(
    results,
    key=lambda x:
        results[x]["f1"]
)

best_model = results[
    best_name
]["model"]


print(
    "\n========================================"
)

print(
    "BEST MODEL:",
    best_name
)

print(
    "========================================"
)


# ==========================================
# FINAL CLASSIFICATION REPORT
# ==========================================

y_best_pred = best_model.predict(
    X_test
)


print(
    "\nCLASSIFICATION REPORT"
)

print(
    "========================================"
)

print(
    classification_report(
        y_test,
        y_best_pred,
        zero_division=0
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

print(
    "\nCONFUSION MATRIX"
)

print(
    "========================================"
)

print(
    confusion_matrix(
        y_test,
        y_best_pred
    )
)


# ==========================================
# SAVE BEST MODEL
# ==========================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "career_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "tfidf_vectorizer.pkl"
)


joblib.dump(
    best_model,
    MODEL_PATH
)

joblib.dump(
    vectorizer,
    VECTORIZER_PATH
)


print(
    "\n========================================"
)

print(
    "MODEL SAVED SUCCESSFULLY!"
)

print(
    "========================================"
)

print(
    "Best Model:",
    best_name
)

print(
    "Model:",
    MODEL_PATH
)

print(
    "Vectorizer:",
    VECTORIZER_PATH
)