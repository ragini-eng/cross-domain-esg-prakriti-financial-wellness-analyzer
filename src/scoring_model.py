def calculate_final_wellness_score(row):
    """
    Combines Financial Health, Prakriti Index, and Sustainability Score
    into a single Wellness Score.
    """

    finance_weight = 0.4
    prakriti_weight = 0.3
    sustainability_weight = 0.3

    final_score = (
        row["Finance_Health_Score"] * finance_weight +
        row["Prakriti_Index"] * prakriti_weight +
        row["Sustainability_Score"] * sustainability_weight
    )

    return round(final_score, 2)

