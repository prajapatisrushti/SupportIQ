
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FAQS = [
    {
        "question": "How can I reset my password?",
        "answer": "Go to the login page, select Forgot Password, and follow the instructions sent to your email.",
        "category": "Account"
    },
    {
        "question": "How can I track my order?",
        "answer": "Visit the Orders section of your account to view your latest order status.",
        "category": "Orders"
    },
    {
        "question": "How can I request a refund?",
        "answer": "Contact our support team with your order ID and refund reason to start a refund request.",
        "category": "Billing"
    },
    {
        "question": "How do I update my email address?",
        "answer": "Open your account settings and update your registered email address.",
        "category": "Account"
    },
    {
        "question": "How can I contact customer support?",
        "answer": "Create a support ticket with your question and our support team will review it.",
        "category": "General"
    },
    {
        "question": "Why was my payment declined?",
        "answer": "Check your payment details, available balance, and bank restrictions. If the issue continues, contact support.",
        "category": "Billing"
    }
]

vectorizer = TfidfVectorizer()

faq_questions = [faq["question"] for faq in FAQS]
faq_vectors = vectorizer.fit_transform(faq_questions)


def find_faq_answer(user_query):
    query_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, faq_vectors)[0]

    best_match_index = similarities.argmax()
    confidence = similarities[best_match_index]

    if confidence < 0.15:
        return {
            "answer": "I couldn't find a suitable answer. Please create a support ticket.",
            "category": "General",
            "confidence": round(float(confidence), 2),
            "matched": False
        }

    matched_faq = FAQS[best_match_index]

    return {
        "answer": matched_faq["answer"],
        "category": matched_faq["category"],
        "confidence": round(float(confidence), 2),
        "matched": True
    }


def categorize_ticket(description):
    result = find_faq_answer(description)
    return result["category"]
