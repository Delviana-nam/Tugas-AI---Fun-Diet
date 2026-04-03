def hitung_bmr(jenis_kelamin, berat, tinggi, umur):
    if jenis_kelamin == "Laki-laki":
        return 10 * berat + 6.25 * tinggi - 5 * umur + 5
    return 10 * berat + 6.25 * tinggi - 5 * umur - 161


def hitung_tdee(bmr, activity_factor=1.2):
    return bmr * activity_factor


def hitung_target_kalori(tdee, target):
    if target == "fat_loss":
        return tdee - 300
    if target == "muscle_gain":
        return tdee + 300
    return tdee


def hitung_total_kalori(selected_foods, foods):
    return sum(foods[item]["kalori"] for item in selected_foods if item in foods)


def hitung_sisa_kalori(target_kalori, total_kalori):
    return target_kalori - total_kalori