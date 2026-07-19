"""
app.py
------
Streamlit dashboard for the AI Resume Analyzer & Job Recommendation System.

Run locally with:
    streamlit run app.py
"""

from datetime import datetime

import plotly.express as px
import streamlit as st

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills, flatten_skills
from job_matcher import load_job_roles, compute_match_scores, get_missing_skills
from roadmap_generator import generate_roadmap

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

MAX_FILE_SIZE_MB = 5


@st.cache_data
def get_skill_dictionary():
    return load_skill_dictionary()


@st.cache_data
def get_job_roles():
    return load_job_roles()


def build_report_text(target_role: str, match_pct: float, found_skills_flat: list,
                       missing_skills: list, roadmap: list) -> str:
    lines = [
        "AI RESUME ANALYSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "-" * 50,
        f"Target Role: {target_role}",
        f"Match Score: {match_pct}%",
        "",
        "Skills Found:",
    ]
    lines += [f"  - {s}" for s in found_skills_flat] if found_skills_flat else ["  (none detected)"]

    lines += ["", "Missing Skills:"]
    lines += [f"  - {s}" for s in missing_skills] if missing_skills else ["  (none - great match!)"]

    if roadmap:
        lines += ["", "Suggested Learning Roadmap:"]
        for week in roadmap:
            lines.append(f"  Week {week['week']}:")
            for topic in week["topics"]:
                lines.append(f"    - {topic['skill']}: {topic['suggestion']}")

    lines += [
        "",
        "Note: This match score is an automated estimate based on skill and",
        "keyword overlap. It is intended for self-guidance only and should",
        "not be treated as a hiring or rejection decision.",
    ]
    return "\n".join(lines)


def main():
    st.title("📄 AI Resume Analyzer & Job Recommendation System")
    st.caption(
        "Upload your resume to see how well it matches different job roles, "
        "discover missing skills, and get a personalized learning roadmap."
    )

    with st.expander("ℹ️ How this tool works & its limits"):
        st.markdown(
            "- This tool gives **guidance**, not a hiring decision.\n"
            "- It only looks at job-related **skills, education, projects, and "
            "experience** — never your name, photo, age, gender, or other "
            "personal attributes.\n"
            "- Match scores are estimates based on keyword and skill overlap; "
            "missing a keyword does not always mean missing the ability.\n"
            "- Your uploaded file is processed **in memory for this session "
            "only** and is not stored permanently."
        )

    job_df = get_job_roles()
    skill_df = get_skill_dictionary()

    col_upload, col_role = st.columns([2, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF or DOCX, max 5MB)", type=["pdf", "docx"]
        )
    with col_role:
        role_options = ["Auto-recommend best role"] + job_df["job_role"].tolist()
        target_role_choice = st.selectbox("Target role", role_options)

    if uploaded_file is None:
        st.info("👆 Upload a resume to get started.")
        return

    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"File is too large. Please upload a file under {MAX_FILE_SIZE_MB}MB.")
        return

    st.success(f"Uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

    try:
        raw_text = extract_resume_text(uploaded_file)
    except ValueError as e:
        st.error(str(e))
        return
    except Exception:
        st.error(
            "Couldn't read this file. It may be corrupted, password-protected, "
            "or an image-based (scanned) PDF with no selectable text."
        )
        return

    if not raw_text.strip():
        st.warning(
            "No readable text was found in this file. If it's a scanned/image-based "
            "PDF, please upload a text-based resume instead."
        )
        return

    cleaned = clean_text(raw_text)
    found_skills = extract_skills(cleaned, skill_df)
    found_skills_flat = flatten_skills(found_skills)

    results = compute_match_scores(cleaned, found_skills_flat, job_df)

    if target_role_choice == "Auto-recommend best role":
        target_row = results.iloc[0]
    else:
        target_row = results[results["job_role"] == target_role_choice].iloc[0]

    missing = get_missing_skills(target_row, found_skills_flat)
    roadmap = generate_roadmap(missing, weeks=4)

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("🧠 Extracted Skills")
        if found_skills:
            for category, skills in found_skills.items():
                st.markdown(f"**{category}**")
                st.write(", ".join(skills))
        else:
            st.warning("No known skills were detected. Try adding more detail to your resume.")

    with right:
        st.subheader(f"🎯 Match: {target_row['job_role']}")
        st.metric("Match Score", f"{target_row['match_score_pct']}%")
        st.progress(min(int(target_row["match_score_pct"]), 100))
        if missing:
            st.markdown("**Missing Skills**")
            st.write(", ".join(missing))
        else:
            st.success("All required skills for this role were found in your resume!")

    st.divider()
    st.subheader("📊 Match Score Across Roles")
    chart_df = results[["job_role", "match_score_pct"]]
    fig = px.bar(
        chart_df,
        x="match_score_pct",
        y="job_role",
        orientation="h",
        labels={"match_score_pct": "Match Score (%)", "job_role": "Job Role"},
        text="match_score_pct",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Top 3 Recommended Roles")
    for i, row in results.head(3).iterrows():
        st.markdown(f"**{i + 1}. {row['job_role']}** — {row['match_score_pct']}%")

    if roadmap:
        st.divider()
        st.subheader(f"🗺️ Learning Roadmap for {target_row['job_role']}")
        for week in roadmap:
            with st.expander(f"Week {week['week']}", expanded=(week["week"] == 1)):
                for topic in week["topics"]:
                    st.markdown(f"- **{topic['skill']}**: {topic['suggestion']}")

    st.divider()
    report_text = build_report_text(
        target_row["job_role"],
        target_row["match_score_pct"],
        found_skills_flat,
        missing,
        roadmap,
    )
    st.download_button(
        "⬇️ Download Analysis Report",
        data=report_text,
        file_name=f"resume_analysis_{target_row['job_role'].replace(' ', '_')}.txt",
        mime="text/plain",
    )


if __name__ == "__main__":
    main()
