FAKE_KEYWORDS = [
    "registration fee",
    "pay first",
    "guaranteed placement",
    "whatsapp only",
    "limited slots",
    "no interview"
]

def fake_offer_detector(text):
    text = text.lower()
    score = 0

    for word in FAKE_KEYWORDS:
        if word in text:
            score += 1

    if score >= 2:
        return "Likely Fake Internship"
    else:
        return "Likely Genuine Internship"
