def calculate_sustainability_score(row):
    """
    Calculates Sustainability Score based on lifestyle and behavior indicators.
    This function documents the ESG logic used in the project.
    """

    score = 0

    # Lifestyle sustainability indicators
    if row["diet_type"].lower() in ["vegetarian", "vegan"]:
        score += 20

    if row["meditation_minutes"] >= 15:
        score += 20

    if row["activity_level"].lower() in ["active", "high"]:
        score += 20

    # Financial behavior (indirect governance signal)
    if row["Finance_Health_Score"] >= 70:
        score += 20

    # Stress & sleep (social sustainability)
    if row["stress_level"] <= 4 and row["sleep_hours"] >= 7:
        score += 20

    return min(score, 100)
