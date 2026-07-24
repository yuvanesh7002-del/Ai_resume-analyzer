# Demonstration Video — Recording Guide & Script

I can't record a video for you directly, but here's everything you need to
record a clean 2–3 minute demo yourself. Total time needed: about 10 minutes.

## 1. Recording tool (Windows, built-in, free)

1. Open your Streamlit app in the browser (locally via `streamlit run app.py`,
   or your live Streamlit Cloud link).
2. Press **Windows key + G** to open the **Xbox Game Bar**.
3. Click the **Capture** widget → the round **record button** (or press
   **Windows + Alt + R**) to start recording.
4. Press **Windows + Alt + R** again to stop. The video saves automatically to:
   `This PC > Videos > Captures`

(Alternative if Game Bar doesn't work on your machine: install
[OBS Studio](https://obsproject.com) — free — or use
[Loom](https://www.loom.com) in the browser.)

## 2. Suggested narration script (~2–3 minutes)

Read this in your own words — it doesn't need to be word-for-word.

---

**[0:00–0:20] Introduction**
> "Hi, I'm [your name], and this is my AI Resume Analyzer and Job
> Recommendation System. It's an NLP-based tool that takes a resume, checks
> it against different job roles, and shows a match score, missing skills,
> and a learning roadmap."

**[0:20–0:40] Show the upload screen**
> "Here's the dashboard, built with Streamlit. I'll upload a sample resume —
> this one is for a Machine Learning Engineer role."
*(Upload `sample_resumes/resume_B_ml_engineer.pdf`)*

**[0:40–1:10] Walk through the results**
> "The app extracted these skills automatically from the resume text —
> Python, Machine Learning, Scikit-learn, Pandas, Docker — grouped by
> category. On the right, it shows a 64% match score against Machine
> Learning Engineer, and one missing skill: FastAPI."

**[1:10–1:40] Show the chart and recommendations**
> "This chart compares the resume against all 9 job roles in the dataset,
> ranked by match score. Below that, the top 3 recommended roles are listed."

**[1:40–2:10] Show the roadmap and report**
> "For the missing skill, it generates a simple weekly learning roadmap —
> here it suggests learning FastAPI basics. And I can download the full
> analysis as a text report."
*(Click "Download Analysis Report")*

**[2:10–2:30] Wrap-up**
> "The matching uses TF-IDF and cosine similarity combined with skill
> overlap, and the whole thing respects responsible-AI rules — it never
> looks at personal details like name, age, or gender, only job-related
> skills. That's the project — thank you!"

---

## 3. Checklist before you hit record

- [ ] App is running and loads without errors
- [ ] You have `sample_resumes/resume_B_ml_engineer.pdf` handy to upload
- [ ] Browser window is clean (no unrelated tabs visible)
- [ ] Audio/microphone is working (test with a 5-second trial recording first)

## 4. After recording

1. Trim the start/end if needed (Xbox Game Bar clips can be trimmed in the
   **Photos** app on Windows — open the video → **Edit & Create** → **Trim**)
2. Upload the video file to Google Drive (same steps as the notebook: **New
   → File upload**), then **Share → Anyone with the link → Viewer → Copy link**
3. Add that link to your project report / GitHub README alongside your
   repository link
