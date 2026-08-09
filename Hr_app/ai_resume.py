import fitz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_resume_text(pdf_path):

    text = ""

    document = fitz.open(pdf_path)

    for page in document:

        text += page.get_text()

    document.close()

    return text.lower()


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(job_description, resume_text):

    documents = [
        job_description.lower(),
        resume_text.lower()
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(vectors)[0][1]

    # Convert to percentage
    score = similarity * 100

    # Normalize the score
    if score < 20:
        score = score * 4

    elif score < 40:
        score = score * 2

    score = min(round(score), 100)

    return score