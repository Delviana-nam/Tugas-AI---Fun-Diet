import streamlit as st

from data import foods, menu_categories
from calculator import (
    hitung_bmr,
    hitung_tdee,
    hitung_target_kalori,
    hitung_total_kalori,
    hitung_sisa_kalori,
)
from rules import (
    get_food_recommendations,
    get_exercise_recommendations,
    evaluate_calories,
    get_active_rules,
)


def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def format_food_name(name):
    return name.replace("_", " ").title()


def format_exercise_name(name):
    return name.replace("_", " ").title()


def card(title, value, subtitle=""):
    st.markdown(
        f"""
        <div class="custom-card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            <div class="card-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_session():
    defaults = {
        "generated": False,
        "nama": "",
        "umur": 20,
        "jenis_kelamin": "Laki-laki",
        "berat": 50,
        "tinggi": 160,
        "target_label": "Fat Loss",
        "target": "fat_loss",
        "bmr": 0,
        "tdee": 0,
        "target_kal": 0,
        "food_rec": [],
        "exercise_rec": [],
        "karbo": "-",
        "protein": "-",
        "sayur": "-",
        "buah": "-",
        "olahraga_dilakukan": [],
        "kalori_olahraga_manual": 0,
        "page": "Dashboard",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def generate_recommendation():
    target_options = {
        "Fat Loss": "fat_loss",
        "Maintenance": "maintenance",
        "Muscle Gain": "muscle_gain",
    }

    st.session_state.target = target_options[st.session_state.target_label]

    bmr = hitung_bmr(
        st.session_state.jenis_kelamin,
        st.session_state.berat,
        st.session_state.tinggi,
        st.session_state.umur,
    )
    tdee = hitung_tdee(bmr)
    target_kal = hitung_target_kalori(tdee, st.session_state.target)

    st.session_state.bmr = bmr
    st.session_state.tdee = tdee
    st.session_state.target_kal = target_kal
    st.session_state.food_rec = get_food_recommendations(st.session_state.target)
    st.session_state.exercise_rec = get_exercise_recommendations(st.session_state.target)
    st.session_state.generated = True
    st.session_state.page = "Dashboard"


exercise_burn = {
    "jogging": 180,
    "skipping": 220,
    "push_up": 80,
    "plank": 60,
}


st.set_page_config(
    page_title="Fun Diet",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
init_session()

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">✨ Fun Diet ✨</div>
        <div class="hero-subtitle">Personalized diet & workout recommendations just for you!</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Input Pengguna")

    st.session_state.nama = st.text_input("Nama", value=st.session_state.nama)
    st.session_state.umur = st.number_input(
        "Umur", min_value=10, max_value=80, value=st.session_state.umur
    )
    st.session_state.jenis_kelamin = st.selectbox(
        "Jenis Kelamin",
        ["Laki-laki", "Perempuan"],
        index=0 if st.session_state.jenis_kelamin == "Laki-laki" else 1,
    )
    st.session_state.berat = st.number_input(
        "Berat Badan (kg)",
        min_value=30,
        max_value=200,
        value=st.session_state.berat,
    )
    st.session_state.tinggi = st.number_input(
        "Tinggi Badan (cm)",
        min_value=100,
        max_value=220,
        value=st.session_state.tinggi,
    )
    st.session_state.target_label = st.selectbox(
        "Target Diet",
        ["Fat Loss", "Maintenance", "Muscle Gain"],
        index=["Fat Loss", "Maintenance", "Muscle Gain"].index(st.session_state.target_label),
    )

    if st.button("Generate Recommendation", use_container_width=True):
        generate_recommendation()

    st.markdown("---")
    st.markdown("## Navigasi")

    if st.session_state.generated:
        st.session_state.page = st.radio(
            "Pilih Halaman",
            ["Dashboard", "Rekomendasi Sistem", "Tracking Makanan", "AI / KBS Insight"],
            index=["Dashboard", "Rekomendasi Sistem", "Tracking Makanan", "AI / KBS Insight"].index(
                st.session_state.page
            ),
            label_visibility="collapsed",
            key="sidebar_nav",
        )
    else:
        st.info("Klik Generate dulu untuk membuka hasil.")

if not st.session_state.generated:
    st.info("Isi data di sidebar lalu klik Generate Recommendation.")
else:
    st.markdown("## Menu Utama")
    st.session_state.page = st.radio(
        "Menu Utama",
        ["Dashboard", "Rekomendasi Sistem", "Tracking Makanan", "AI / KBS Insight"],
        index=["Dashboard", "Rekomendasi Sistem", "Tracking Makanan", "AI / KBS Insight"].index(
            st.session_state.page
        ),
        horizontal=True,
        label_visibility="collapsed",
        key="main_navigation_radio",
    )

    if st.session_state.page == "Dashboard":
        st.markdown("## Dashboard Hasil")

        c1, c2, c3 = st.columns(3)
        with c1:
            card("BMR", f"{round(st.session_state.bmr)} kcal", "Basal Metabolic Rate")
        with c2:
            card("TDEE", f"{round(st.session_state.tdee)} kcal", "Daily Energy Need")
        with c3:
            card("Target Kalori", f"{round(st.session_state.target_kal)} kcal", st.session_state.target_label)

        st.success(
            f"Halo {st.session_state.nama if st.session_state.nama else 'User'} 👋, ini ringkasan rekomendasi untuk kamu."
        )

        st.markdown("### Ringkasan Profil")
        p1, p2, p3 = st.columns(3)

        with p1:
            card("Nama", st.session_state.nama if st.session_state.nama else "User", "Nama pengguna")

        with p2:
            card(
                "Profil Tubuh",
                f"{st.session_state.berat} kg / {st.session_state.tinggi} cm",
                st.session_state.jenis_kelamin,
            )

        with p3:
            card("Target", st.session_state.target_label, f"Umur {st.session_state.umur} tahun")

    elif st.session_state.page == "Rekomendasi Sistem":
        st.markdown("## Rekomendasi Sistem")

        r1, r2 = st.columns(2)

        with r1:
            st.markdown(
                '<div class="panel panel-pink"><div class="panel-title">🍽️ Rekomendasi Makanan</div>',
                unsafe_allow_html=True,
            )
            for item in st.session_state.food_rec:
                st.markdown(f"- {format_food_name(item)}")
            st.markdown("</div>", unsafe_allow_html=True)

        with r2:
            st.markdown(
                '<div class="panel panel-blue"><div class="panel-title">🏃 Rekomendasi Olahraga</div>',
                unsafe_allow_html=True,
            )
            for item in st.session_state.exercise_rec:
                st.markdown(f"- {format_exercise_name(item)}")
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == "Tracking Makanan":
        st.markdown("## Tracking Kalori Harian")

        st.markdown("### 1. Pilih Makanan Hari Ini")
        t1, t2 = st.columns(2)

        with t1:
            karbo_options = ["-"] + menu_categories["Karbohidrat"]
            protein_options = ["-"] + menu_categories["Protein"]

            st.session_state.karbo = st.selectbox(
                "Pilih Karbohidrat",
                karbo_options,
                index=karbo_options.index(st.session_state.karbo),
            )
            st.session_state.protein = st.selectbox(
                "Pilih Protein",
                protein_options,
                index=protein_options.index(st.session_state.protein),
            )

        with t2:
            sayur_options = ["-"] + menu_categories["Sayur"]
            buah_options = ["-"] + menu_categories["Buah"]

            st.session_state.sayur = st.selectbox(
                "Pilih Sayur",
                sayur_options,
                index=sayur_options.index(st.session_state.sayur),
            )
            st.session_state.buah = st.selectbox(
                "Pilih Buah",
                buah_options,
                index=buah_options.index(st.session_state.buah),
            )

        selected_foods = [
            item
            for item in [
                st.session_state.karbo,
                st.session_state.protein,
                st.session_state.sayur,
                st.session_state.buah,
            ]
            if item != "-"
        ]

        st.markdown("### 2. Input Olahraga yang Sudah Dilakukan")
        o1, o2 = st.columns(2)

        with o1:
            st.session_state.olahraga_dilakukan = st.multiselect(
                "Pilih olahraga",
                list(exercise_burn.keys()),
                default=st.session_state.olahraga_dilakukan,
                format_func=format_exercise_name,
            )

        with o2:
            st.session_state.kalori_olahraga_manual = st.number_input(
                "Kalori olahraga manual (opsional)",
                min_value=0,
                max_value=2000,
                value=st.session_state.kalori_olahraga_manual,
                step=10,
            )

        total_kalori_makanan = hitung_total_kalori(selected_foods, foods) if selected_foods else 0
        kalori_olahraga_otomatis = sum(exercise_burn[item] for item in st.session_state.olahraga_dilakukan)
        total_kalori_terbakar = kalori_olahraga_otomatis + st.session_state.kalori_olahraga_manual
        kalori_bersih = total_kalori_makanan - total_kalori_terbakar
        sisa_kalori = hitung_sisa_kalori(st.session_state.target_kal, kalori_bersih)

        st.markdown("### 3. Ringkasan Kalori")
        s1, s2, s3 = st.columns(3)
        with s1:
            card("Kalori Makanan", f"{round(total_kalori_makanan)} kcal", "Total kalori masuk")
        with s2:
            card("Kalori Olahraga", f"{round(total_kalori_terbakar)} kcal", "Kalori keluar")
        with s3:
            card("Kalori Bersih", f"{round(kalori_bersih)} kcal", "Makanan - olahraga")

        s4, s5 = st.columns(2)
        with s4:
            card("Target Harian", f"{round(st.session_state.target_kal)} kcal", st.session_state.target_label)
        with s5:
            card("Sisa Kalori", f"{round(sisa_kalori)} kcal", "Sisa dari target")

        progress = kalori_bersih / st.session_state.target_kal if st.session_state.target_kal > 0 else 0
        st.markdown("### Progress Target Kalori")
        st.progress(min(max(progress, 0.0), 1.0))
        st.write(f"{round(progress * 100)}% dari target harian")

        if kalori_bersih > st.session_state.target_kal:
            st.error("Kalori berlebih ⚠️")
        elif abs(kalori_bersih - st.session_state.target_kal) <= 50:
            st.success("Kalori ideal ✅")
        else:
            st.warning("Kalori kurang ⚡")

        evaluasi = evaluate_calories(kalori_bersih, st.session_state.target_kal)
        st.info(evaluasi)

        st.markdown("### Detail Makanan Dipilih")
        if selected_foods:
            food_cols = st.columns(len(selected_foods))
            for idx, item in enumerate(selected_foods):
                with food_cols[idx]:
                    st.markdown(
                        f"""
                        <div class="mini-card">
                            <div class="mini-title">{format_food_name(item)}</div>
                            <div class="mini-value">{foods[item]['kalori']} kcal</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.warning("Belum ada makanan yang dipilih.")

        st.markdown("### Detail Olahraga")
        if st.session_state.olahraga_dilakukan:
            ex_cols = st.columns(len(st.session_state.olahraga_dilakukan))
            for idx, item in enumerate(st.session_state.olahraga_dilakukan):
                with ex_cols[idx]:
                    st.markdown(
                        f"""
                        <div class="mini-card">
                            <div class="mini-title">{format_exercise_name(item)}</div>
                            <div class="mini-value">{exercise_burn[item]} kcal</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.warning("Belum ada olahraga yang dipilih.")

    elif st.session_state.page == "AI / KBS Insight":
        st.markdown("## AI / KBS Insight")

        selected_foods = [
            item
            for item in [
                st.session_state.karbo,
                st.session_state.protein,
                st.session_state.sayur,
                st.session_state.buah,
            ]
            if item != "-"
        ]

        total_kalori_makanan = hitung_total_kalori(selected_foods, foods) if selected_foods else 0
        kalori_olahraga_otomatis = sum(exercise_burn[item] for item in st.session_state.olahraga_dilakukan)
        total_kalori_terbakar = kalori_olahraga_otomatis + st.session_state.kalori_olahraga_manual
        kalori_bersih = total_kalori_makanan - total_kalori_terbakar

        active_rules = get_active_rules(
            st.session_state.target,
            kalori_bersih,
            st.session_state.target_kal,
        )

        i1, i2 = st.columns(2)

        with i1:
            st.markdown(
                '<div class="panel panel-green"><div class="panel-title">🧠 Aturan Aktif</div>',
                unsafe_allow_html=True,
            )
            for rule in active_rules:
                st.markdown(f"- {rule}")
            st.markdown("</div>", unsafe_allow_html=True)

        with i2:
            st.markdown(
                '<div class="panel panel-yellow"><div class="panel-title">📌 Fakta Aktif</div>',
                unsafe_allow_html=True,
            )
            st.markdown(f"- nama = {st.session_state.nama if st.session_state.nama else 'User'}")
            st.markdown(f"- target = {st.session_state.target}")
            st.markdown(f"- jenis_kelamin = {st.session_state.jenis_kelamin}")
            st.markdown(f"- umur = {st.session_state.umur}")
            st.markdown(f"- berat = {st.session_state.berat} kg")
            st.markdown(f"- tinggi = {st.session_state.tinggi} cm")
            st.markdown(f"- total_kalori_makanan = {round(total_kalori_makanan)} kcal")
            st.markdown(f"- total_kalori_olahraga = {round(total_kalori_terbakar)} kcal")
            st.markdown(f"- kalori_bersih = {round(kalori_bersih)} kcal")
            st.markdown(f"- target_kalori = {round(st.session_state.target_kal)} kcal")
            st.markdown("</div>", unsafe_allow_html=True)