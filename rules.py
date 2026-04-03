from data import foods


def get_food_recommendations(target):
    if target == "fat_loss":
        return [name for name, info in foods.items() if info["kalori"] <= 100]

    if target == "muscle_gain":
        return [name for name, info in foods.items() if info["kategori"] == "protein"]

    if target == "maintenance":
        return ["nasi_merah", "ayam", "brokoli", "apel"]

    return []


def get_exercise_recommendations(target):
    if target == "fat_loss":
        return ["jogging", "skipping"]

    if target == "muscle_gain":
        return ["push_up", "plank"]

    if target == "maintenance":
        return ["jogging", "push_up", "plank"]

    return []


def evaluate_calories(total_kalori, target_kalori):
    tolerance = 50

    if total_kalori > target_kalori:
        return "Kalori berlebih. Kurangi porsi atau ganti ke makanan yang lebih rendah kalori."
    if abs(total_kalori - target_kalori) <= tolerance:
        return "Kalori sudah mendekati target. Pertahankan pola makan."
    return "Kalori masih kurang. Tambahkan makanan sesuai target."


def get_active_rules(target, total_kalori=None, target_kalori=None):
    rules = []

    if target == "fat_loss":
        rules.append("IF target = fat_loss THEN rekomendasi_makanan = low_calorie")
        rules.append("IF target = fat_loss THEN rekomendasi_olahraga = cardio")

    elif target == "muscle_gain":
        rules.append("IF target = muscle_gain THEN rekomendasi_makanan = high_protein")
        rules.append("IF target = muscle_gain THEN rekomendasi_olahraga = strength_training")

    elif target == "maintenance":
        rules.append("IF target = maintenance THEN rekomendasi_makanan = balanced")
        rules.append("IF target = maintenance THEN rekomendasi_olahraga = cardio dan strength_training")

    if total_kalori is not None and target_kalori is not None:
        tolerance = 50

        if total_kalori > target_kalori:
            rules.append("IF total_kalori > target_kalori THEN rekomendasi = kurangi kalori atau ganti makanan")
        elif abs(total_kalori - target_kalori) <= tolerance:
            rules.append("IF total_kalori ≈ target_kalori THEN rekomendasi = pertahankan pola makan")
        else:
            rules.append("IF total_kalori < target_kalori THEN rekomendasi = tambahkan makanan")

    return rules