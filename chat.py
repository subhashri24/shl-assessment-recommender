import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from rag import search_catalog

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

OFF_TOPIC = [
    "weather",
    "ipl",
    "cricket",
    "football",
    "movie",
    "recipe",
    "bitcoin",
    "stock",
    "medical",
    "legal",
    "politics",
    "news"
]

VAGUE = [
    "assessment",
    "test",
    "hire",
    "candidate",
    "recommend",
    "looking for assessment"
]


def latest_user(messages):
    for m in reversed(messages):
        if m["role"] == "user":
            return m["content"]
    return ""


def chat(messages):

    query = latest_user(messages)
    conversation_history = " ".join(
    m["content"] for m in messages if m["role"] == "user"
    )

    q = query.lower()

    # -------------------------
    # OFF TOPIC
    # -------------------------
    for word in OFF_TOPIC:
        if word in q:
            return (
                "I can only help with SHL assessment recommendations and comparisons.",
                [],
                False
            )

    # -------------------------
    # PROMPT INJECTION
    # -------------------------

    INJECTION = [
    "ignore previous",
    "ignore all instructions",
    "forget previous",
    "system prompt",
    "developer prompt",
    "reveal prompt"
    ]
    
    if any(i in q for i in INJECTION):
        return (
            "Sorry, I can only answer questions using the SHL assessment catalog.",
            [],
            False
        )

    # -------------------------
    # COMPARISON
    # -------------------------
    if "compare" in q:

        assessments = search_catalog(query, top_k=2)

        context = ""

        for a in assessments:
            context += f"""
Assessment:
{a["name"]}

{a["description"]}
"""

        prompt = f"""
Compare ONLY these SHL assessments.

{context}

Explain:

Purpose

Skills measured

Best use case

Difference

Do not hallucinate.
"""

        answer = model.generate_content(prompt).text

        return answer, [], True

    # -------------------------
    # CLARIFICATION
    # -------------------------

    important_words = [
    "developer",
    "engineer",
    "manager",
    "sales",
    "java",
    "python",
    "leadership",
    "personality",
    "ability",
    "graduate",
    "experience"
    ]
    has_role = any(word in q for word in important_words)
    
    if not has_role:

        return (
            "Sure! Could you tell me:\n\n• Which role are you hiring for?\n• Required skills?\n• Experience level?\n• Do you also want personality or cognitive ability assessments?",
            [],
            False
        )
    REFINE_WORDS = [
    "actually",
    "instead",
    "also",
    "add",
    "remove",
    "change",
    "include",
    "exclude"
    ]
    is_refinement = any(word in q for word in REFINE_WORDS)

    # -------------------------
    # RECOMMENDATION
    # -------------------------

    if is_refinement:
        search_query = conversation_history
    else:
        search_query = query
        
    recommendations = search_catalog(search_query, top_k=5)
    context = ""

    for r in recommendations:

        context += f"""
Assessment:
{r['name']}

Description:
{r['description']}

URL:
{r['url']}

-------------------
"""

    prompt = f"""
You are an SHL Assessment Expert.

Use ONLY the assessments below.

Recommend the most suitable ones.

Explain WHY each is relevant.

Never invent assessments.

Context:

{context}

User request:

{query}
"""

    reply = model.generate_content(prompt).text

    return reply, recommendations, True