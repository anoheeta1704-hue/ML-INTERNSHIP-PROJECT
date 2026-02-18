from skill_gap import skill_gap_analyzer
from internship_match import internship_matcher
from placement_predictor import predict_placement
from fake_detector import fake_offer_detector

print("=== Skill Gap ===")
print(skill_gap_analyzer(["python", "pandas"], "Data Scientist"))

print("\n=== Internship Match ===")
print(internship_matcher(["python", "ml"]))

print("\n=== Placement Probability ===")
print(predict_placement(6, 8.1, 3), "%")

print("\n=== Fake Internship Check ===")
print(fake_offer_detector("Guaranteed placement, pay registration fee"))
