"""
text_cleaner.py
----------------
Cleans and normalizes raw resume text so it can be reliably searched for
skills and compared against job-role requirements.

Design note (useful for the viva):
Standard cleaning (lowercasing + stripping punctuation) would destroy
technical tokens like "C++", "C#", ".NET" and "Node.js" because the
symbols (+, #, .) are removed. To avoid that, we "protect" a short list
of known technical tokens before stripping punctuation, then restore
them afterwards.
"""

import re

# Technical tokens whose punctuation must be preserved.
# Add more here if your resumes use other symbol-heavy tech names.
_PROTECTED_TOKENS = [
    r"c\+\+",
    r"c#",
    r"f#",
    r"\.net",
    r"asp\.net",
    r"node\.js",
    r"vue\.js",
    r"next\.js",
]
_PROTECT_PATTERN = re.compile("(" + "|".join(_PROTECTED_TOKENS) + ")", re.IGNORECASE)


def clean_text(text: str) -> str:
    """
    Lowercases text, removes extra whitespace and irrelevant symbols,
    while preserving important technical tokens (C++, C#, .NET, etc.).
    """
    if not text:
        return ""

    working_text = text.replace("\r", " ").replace("\n", " ")

    # Step 1: protect known technical tokens with unique placeholders
    placeholders = {}

    def _protect(match: re.Match) -> str:
        token = match.group(0).lower()
        placeholder = f"TECHTOKEN{len(placeholders)}"
        placeholders[placeholder] = token
        return f" {placeholder} "

    working_text = _PROTECT_PATTERN.sub(_protect, working_text)

    # Step 2: lowercase everything
    working_text = working_text.lower()

    # Step 3: remove anything that isn't a letter, digit, underscore, or space
    working_text = re.sub(r"[^a-z0-9_\s]", " ", working_text)

    # Step 4: collapse repeated whitespace
    working_text = re.sub(r"\s+", " ", working_text).strip()

    # Step 5: restore the protected technical tokens
    for placeholder, token in placeholders.items():
        working_text = working_text.replace(placeholder.lower(), token)

    return working_text
