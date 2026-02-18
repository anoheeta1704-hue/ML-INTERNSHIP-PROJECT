import streamlit as st

from skill_gap import skill_gap_analyzer
from internship_match import internship_matcher
from placement_predictor import predict_placement
from fake_detector import fake_offer_detector

st.title("🎓 AI Career Companion")

tabs = st.tabs([
    "Skill Gap",
    "Internship Match",
    "Placement Predictor",
    "Fake Internship Detector"
])

# ---------------- Skill Gap ----------------
with tabs[0]:
    skills_input = st.text_input("Enter skills (comma separated):")
    role = st.selectbox("Select Role", ["Data Scientist", "Web Developer", "ML Engineer"])

    if st.button("Analyze"):
        skills = [s.strip().lower() for s in skills_input.split(",")]
        matched, missing = skill_gap_analyzer(skills, role)

        st.write("Matched Skills:", matched)
        st.write("Missing Skills:", missing)

# ---------------- Internship ----------------
with tabs[1]:
    skills_input = st.text_input("Enter skills for internship matching:")

    if st.button("Find Internships"):
        skills = [s.strip().lower() for s in skills_input.split(",")]
        results = internship_matcher(skills)
        st.write(results)

# ---------------- Placement ----------------
with tabs[2]:
    skills_count = st.slider("Number of skills", 1, 20, 5)
    cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
    projects = st.slider("Number of projects", 0, 10, 2)

    if st.button("Predict Placement"):
        probability = predict_placement(skills_count, cgpa, projects)
        st.success(f"Placement Probability: {probability}%")

# ---------------- Fake Detector ----------------
with tabs[3]:
    text = st.text_area("Paste internship message:")

    if st.button("Check"):
        result = fake_offer_detector(text)
        st.warning(result)