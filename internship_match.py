import pandas as pd

def internship_matcher(student_skills):
    df = pd.read_csv("data/internships.csv")
    student = set(student_skills)

    results = []

    for _, row in df.iterrows():
        required = set(row["skills"].split(";"))
        similarity = len(student & required) / len(required)

        if similarity >= 0.5:
            results.append({
                "company": row["company"],
                "role": row["role"],
                "match_percent": round(similarity * 100, 2),
                "stipend": row["stipend"]
            })

    return results
