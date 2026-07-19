"""
skill_extractor.py
-------------------
Loads a controlled skill dictionary (data/skill_dictionary.csv) and searches
cleaned resume text for those skills using whole-word / whole-phrase
keyword matching.

Why keyword matching (the "beginner approach" from the project brief) and
not free-form NLP entity extraction? It is fast, has zero training cost,
and is fully explainable ("your resume contains skill X because the exact
phrase X was found") -- important for a viva. spaCy / an LLM can be swapped
in later as an "advanced improvement" without changing the rest of the
pipeline (see ai_feedback.py for an optional LLM extension point).
"""

import re
from pathlib import Path

import pandas as pd

from text_cleaner import clean_text

DEFAULT_SKILL_CSV = Path(__file__).parent / "data" / "skill_dictionary.csv"


def load_skill_dictionary(csv_path: Path = DEFAULT_SKILL_CSV) -> pd.DataFrame:
    """
    Loads the skill dictionary CSV (columns: skill, category) and pre-computes
    a normalized version of each skill using the same cleaning pipeline used
    on resume text, so the two sides always compare like-for-like.
    """
    df = pd.read_csv(csv_path)
    df["skill"] = df["skill"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["skill_normalized"] = df["skill"].apply(clean_text)
    return df


def _build_pattern(skill_normalized: str) -> re.Pattern:
    """Whole word/phrase match: 'r' should not match inside 'react'."""
    escaped = re.escape(skill_normalized)
    return re.compile(rf"(?<![a-z0-9_]){escaped}(?![a-z0-9_])")


def extract_skills(cleaned_text: str, skill_df: pd.DataFrame) -> dict:
    """
    Returns skills found in the resume, grouped by category:
        {"Programming": ["Python", "SQL"], "Cloud": ["AWS"], ...}
    """
    found: dict[str, list] = {}
    for _, row in skill_df.iterrows():
        skill_normalized = row["skill_normalized"]
        if not skill_normalized:
            continue
        pattern = _build_pattern(skill_normalized)
        if pattern.search(cleaned_text):
            category = row["category"]
            bucket = found.setdefault(category, [])
            if row["skill"] not in bucket:
                bucket.append(row["skill"])
    return found


def flatten_skills(found_skills: dict) -> list:
    """Flattens the {category: [skills]} dict into a single sorted list."""
    flat = []
    for skills in found_skills.values():
        flat.extend(skills)
    return sorted(set(flat))
