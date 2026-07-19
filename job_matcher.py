"""
job_matcher.py
--------------
Loads the job-role dataset (data/job_roles.csv) and scores a resume against
every role using a blend of two explainable signals:

  1. skill_overlap  -> (# required skills found in resume) / (# required skills)
  2. tfidf_similarity -> cosine similarity between TF-IDF vectors of the
                          resume text and the role's required-skills text

final match_score = 0.6 * skill_overlap + 0.4 * tfidf_similarity

Skill overlap is weighted higher because it is directly explainable to a
user ("you have 4 of 5 required skills"), while TF-IDF similarity adds
useful signal from the broader wording of the resume (projects, summary,
etc.), not just the exact skill dictionary.
"""

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_JOB_CSV = Path(__file__).parent / "data" / "job_roles.csv"

SKILL_OVERLAP_WEIGHT = 0.6
TFIDF_WEIGHT = 0.4


def load_job_roles(csv_path: Path = DEFAULT_JOB_CSV) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["job_role"] = df["job_role"].astype(str).str.strip()
    df["required_skills_list"] = df["required_skills"].apply(
        lambda s: [skill.strip() for skill in str(s).split(",") if skill.strip()]
    )
    return df


def compute_match_scores(
    cleaned_resume_text: str, resume_skills: list, job_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns job_df with extra columns: tfidf_similarity, skill_overlap,
    match_score (0-1), match_score_pct (0-100), sorted best match first.
    """
    role_documents = [", ".join(skills) for skills in job_df["required_skills_list"]]
    documents = [cleaned_resume_text] + role_documents

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0:1]
    role_vectors = tfidf_matrix[1:]
    tfidf_scores = cosine_similarity(resume_vector, role_vectors).flatten()

    resume_skills_lower = {s.lower() for s in resume_skills}
    overlap_scores = []
    for skills in job_df["required_skills_list"]:
        required_lower = {s.lower() for s in skills}
        if not required_lower:
            overlap_scores.append(0.0)
            continue
        matched = required_lower & resume_skills_lower
        overlap_scores.append(len(matched) / len(required_lower))

    results = job_df.copy()
    results["tfidf_similarity"] = tfidf_scores
    results["skill_overlap"] = overlap_scores
    results["match_score"] = (
        SKILL_OVERLAP_WEIGHT * results["skill_overlap"]
        + TFIDF_WEIGHT * results["tfidf_similarity"]
    )
    results["match_score_pct"] = (results["match_score"] * 100).round(1)
    results = results.sort_values("match_score_pct", ascending=False).reset_index(drop=True)
    return results


def get_missing_skills(job_row: pd.Series, resume_skills: list) -> list:
    """Required skills for a role that were NOT found in the resume."""
    resume_skills_lower = {s.lower() for s in resume_skills}
    return [
        skill
        for skill in job_row["required_skills_list"]
        if skill.lower() not in resume_skills_lower
    ]


def get_matched_skills(job_row: pd.Series, resume_skills: list) -> list:
    """Required skills for a role that WERE found in the resume."""
    resume_skills_lower = {s.lower() for s in resume_skills}
    return [
        skill
        for skill in job_row["required_skills_list"]
        if skill.lower() in resume_skills_lower
    ]
