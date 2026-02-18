import pandas as pd

def skill_gap_analyzer(student_skills, target_role):
    df = pd.read_csv("data/roles.csv")

    role_dict = {}
    for _, row in df.iterrows():
        role_dict[row["role"]] = row["skills"].split(";")

    required = set(role_dict[target_role])
    student = set(student_skills)

    matched = required & student
    missing = required - student

    return list(matched), list(missing)
