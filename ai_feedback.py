"""
ai_feedback.py
--------------
OPTIONAL / ADVANCED feature (Section 13 of the project brief:
"LLM-generated resume feedback using a controlled prompt").

This module is intentionally NOT called by app.py by default -- it needs
an API key that only you can provide, and the sandbox this project was
generated in has no internet access to LLM providers, so this code has
NOT been run or tested. Treat it as a starting point.

To enable it:
1. pip install openai   (or the SDK for your provider of choice)
2. Add OPENAI_API_KEY=... to your .env file
3. In app.py, add a checkbox like:
       if st.checkbox("Get AI-generated resume feedback"):
           feedback = get_ai_feedback(raw_text, missing_skills)
           if feedback:
               st.write(feedback)
"""

import os

from dotenv import load_dotenv

load_dotenv()

_SYSTEM_PROMPT = (
    "You are a career coach. You will be given resume text and a list of "
    "missing skills for a target job role. Give 3-4 short, encouraging, "
    "specific bullet points on how the candidate could strengthen their "
    "resume and close those skill gaps. Do not comment on personal "
    "attributes (name, age, gender, photo). Keep it under 120 words."
)


def get_ai_feedback(resume_text: str, missing_skills: list) -> str | None:
    """
    Returns AI-generated feedback text, or None if no API key is configured
    or the call fails (the app should degrade gracefully in that case).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        user_prompt = (
            f"Resume text:\n{resume_text[:3000]}\n\n"
            f"Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=250,
        )
        return response.choices[0].message.content
    except Exception as exc:  # noqa: BLE001 - degrade gracefully in the UI
        print(f"[ai_feedback] Skipping AI feedback: {exc}")
        return None
