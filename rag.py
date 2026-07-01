import json

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_catalog(query, top_k=5):
    query = query.lower()

    scored = []

    for item in catalog:

        score = 0

        text = (
            f"{item.get('name','')} "
            f"{item.get('description','')} "
            f"{item.get('job_levels_raw','')} "
            f"{item.get('test_types_raw','')}"
        ).lower()

        for word in query.split():
            if word in text:
                score += 1

        if score > 0:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])

    recommendations = []

    for _, item in scored[:top_k]:

        recommendations.append({
            "name": item["name"],
            "url": item["link"],
            "test_type": item.get("test_types_raw", "Assessment"),
            "description": item.get("description", "")
        })

    return recommendations