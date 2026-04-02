import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ================================
# 1. PAGE CONFIG
# ================================
st.set_page_config(page_title="Dropout Prediction", layout="wide")

# ================================
# 2. LOAD ASSETS
# ================================
@st.cache_resource
def load_assets():
    try:
        model = joblib.load("model.pkl")
        scaler = joblib.load("scaler.pkl")
        features = joblib.load("features.pkl")
        return model, scaler, features
    except Exception as e:
        st.error(f"Gagal memuat file model: {e}")
        return None, None, None

model, scaler, features = load_assets()

# ================================
# 3. CUSTOM CSS (FIXED ALIGNMENT)
# ================================
st.markdown("""
<style>
/* Background Global */
.stApp {
    background-color: #f5f7fa;
}

header {
    visibility: hidden;
}

/* Pengaturan Kontainer Utama agar Pas di Tengah */
.block-container {
    max-width: 800px !important; 
    padding-top: 5rem !important; 
    padding-bottom: 5rem !important;
    margin: auto;
}

/* Judul Utama */
.custom-title {
    font-size: 36px !important; 
    font-weight: 800 !important;
    color: #1e293b !important;
    text-align: center !important;
    display: block !important;
    line-height: 1.2 !important;
}

.custom-subtitle {
    font-size: 16px !important;
    color: #64748b !important;
    text-align: center !important;
    display: block !important;
    margin-bottom: 40px !important;
}

/* Form Input Card */
[data-testid="stForm"] {
    background: white !important;
    padding: 40px !important;
    border-radius: 20px !important;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.05) !important;
    border: none !important;
}

/* KOTAK HASIL (SLIM & NAIK KE ATAS) */
div[data-testid="stVerticalBlock"] > div:has(div > .result-card-trigger) {
    background: white !important;
    padding: 40px;     /* ⬅️ lebih tipis */
    border-radius: 16px !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04) !important;
    margin-top: 8px !important;        /* ⬅️ MEPEEET KE ATAS */
}

/* JUDUL (TIDAK ADA KOTAK DALAM) */
.result-card-trigger {
    background: transparent;           /* ⬅️ hapus kotak */
    padding: 0;
    border: none;
    text-align: left;                  /* biar natural */
    font-size: 20px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 10px;
}

/* Judul Per Bagian */
.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #334155;
    margin-top: 25px;
    margin-bottom: 15px;
    border-bottom: 2px solid #f1f5f9;
    padding-bottom: 5px;
}

/* Tombol Analisis */
div.stButton > button {
    width: 100%; 
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 15px !important;
    font-size: 18px !important;
    font-weight: bold !important;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #45a049 !important;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ================================
# 4. HEADER
# ================================
st.markdown("""
    <div style="text-align: center;">
        <span class="custom-title">🎓 Dropout Prediction System</span>
        <span class="custom-subtitle">Prediksi Risiko Dropout Mahasiswa menggunakan Model XGBoost</span>
    </div>
""", unsafe_allow_html=True)

# ================================
# 5. FORM INPUT
# ================================

# COURSE MAPPING
course_dict = {
    33: "Biofuel Production Technologies",
    171: "Animation and Multimedia Design",
    8014: "Social Service (evening)",
    9003: "Agronomy",
    9070: "Communication Design",
    9085: "Veterinary Nursing",
    9119: "Informatics Engineering",
    9130: "Equinculture",
    9147: "Management",
    9238: "Social Service",
    9254: "Tourism",
    9500: "Nursing",
    9556: "Oral Hygiene",
    9670: "Advertising and Marketing Management",
    9773: "Journalism and Communication",
    9853: "Basic Education",
    9991: "Management (evening)"
}

with st.form("form"):
    st.markdown('<p class="section-title">📘 Data Mahasiswa</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age (17 - 70)", 17, 70, 20)
        prev_grade = st.number_input("Previous Grade (0 - 200)", 0, 200, 130)

    with col2:
        admission = st.number_input("Admission Grade (0 - 200)", 0, 200, 120)
        course = st.selectbox(
            "Course",
            options=list(course_dict.keys()),
            format_func=lambda x: f"{x} - {course_dict[x]}"
        )

    # ========================
    # SEMESTER 1
    # ========================
    st.markdown('<p class="section-title">📊 Semester 1</p>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        s1_grade = st.number_input("Sem 1 Grade (0 - 20)", 0.0, 20.0, 12.0)
        s1_approved = st.number_input("Sem 1 Approved (0 - 12)", 0, 12, 5)

    with col4:
        s1_enrolled = st.number_input("Sem 1 Enrolled (1 - 12)", 1, 12, 6)
        s1_eval = st.number_input("Sem 1 Evaluations (0 - 20)", 0, 20, 6)

    # ========================
    # SEMESTER 2
    # ========================
    st.markdown('<p class="section-title">📊 Semester 2</p>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    with col5:
        s2_grade = st.number_input("Sem 2 Grade (0 - 20)", 0.0, 20.0, 11.0)
        s2_approved = st.number_input("Sem 2 Approved (0 - 12)", 0, 12, 4)

    with col6:
        s2_enrolled = st.number_input("Sem 2 Enrolled (1 - 12)", 1, 12, 6)
        s2_eval = st.number_input("Sem 2 Evaluations (0 - 20)", 0, 20, 5)

    st.markdown('<p class="section-title">💰 Finansial</p>', unsafe_allow_html=True)
    col7, col8 = st.columns(2)

    with col7:
        tuition = st.selectbox("Tuition Paid", [1, 0], format_func=lambda x: "Yes" if x==1 else "No")

    submit = st.form_submit_button("🔍 Analisis Risiko Sekarang")

# ================================
# 6. PROSES PREDIKSI
# ================================
if submit:
    if model and scaler and features:

        # VALIDASI
        if s1_approved > s1_enrolled:
            st.error("Sem 1 Approved tidak boleh lebih besar dari Enrolled")
            st.stop()

        if s2_approved > s2_enrolled:
            st.error("Sem 2 Approved tidak boleh lebih besar dari Enrolled")
            st.stop()

        ratio_1 = s1_approved / s1_enrolled
        ratio_2 = s2_approved / s2_enrolled

        data_dict = {
            'ratio_1': ratio_1,
            'ratio_2': ratio_2,
            'Curricular_units_1st_sem_approved': s1_approved,
            'Curricular_units_2nd_sem_approved': s2_approved,
            'Curricular_units_1st_sem_grade': s1_grade,
            'Curricular_units_2nd_sem_grade': s2_grade,
            'Admission_grade': admission,
            'Age_at_enrollment': age,
            'Tuition_fees_up_to_date': tuition,
            'Course': course,
            'Previous_qualification_grade': prev_grade,
            'Curricular_units_1st_sem_evaluations': s1_eval,
            'Curricular_units_2nd_sem_evaluations': s2_eval,
            'Curricular_units_1st_sem_enrolled': s1_enrolled
        }

        df_input = pd.DataFrame([data_dict])

        # HANDLE FEATURE HILANG (AMAN)
        for col in features:
            if col not in df_input.columns:
                df_input[col] = 0

        df_input = df_input[features]

        df_scaled = scaler.transform(df_input)
        prob = model.predict_proba(df_scaled)[0][1]
        percent = prob * 100

        # CONTAINER HASIL (PAS DI TENAH KOTAK PUTIH)
        with st.container():
            # Marker Trigger untuk CSS
            st.markdown('<div class="result-card-trigger">📊 Hasil Analisis Risiko</div>', unsafe_allow_html=True)

            # Gauge Chart dengan margin pas
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=percent,
                number={'suffix': "%", 'font': {'size': 60, 'color': '#1e293b'}},
                title={'text': "Risiko Dropout", 'font': {'size': 18, 'color': '#64748b'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': "#1e293b"},
                    'steps': [
                        {'range': [0, 40], 'color': "#b7e4c7"},
                        {'range': [40, 70], 'color': "#ffe066"},
                        {'range': [70, 100], 'color': "#ff6b6b"},
                    ],
                    'borderwidth': 0,
                }
            ))
            fig.update_layout(
                height=350, 
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                autosize=True
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Status Alert
            if prob < 0.4:
                st.success(f"✅ **RISIKO RENDAH** | Prediksi: **Graduate**")
            elif prob < 0.7:
                st.warning(f"⚠️ **RISIKO SEDANG** | Kategori: **Waspada**")
            else:
                st.error(f"🚨 **RISIKO TINGGI** | Prediksi: **Dropout**")

            # ============================
            # ANALISIS FAKTOR RISIKO
            # ============================
            st.markdown("<div style='margin-top: 25px;'><strong>🔎 Analisis Faktor Risiko Individual</strong></div>", unsafe_allow_html=True)

            risk_factors = []
            positive_factors = []

            # Akademik Semester 1
            if ratio_1 < 0.5:
                risk_factors.append("Performa Semester 1 rendah (rasio kelulusan rendah)")
            else:
                positive_factors.append("Performa Semester 1 baik")

            # Akademik Semester 2
            if ratio_2 < 0.5:
                risk_factors.append("Performa Semester 2 rendah")
            else:
                positive_factors.append("Performa Semester 2 stabil")

            # Nilai
            if s1_grade < 10:
                risk_factors.append("Nilai Semester 1 di bawah standar")
            if s2_grade < 10:
                risk_factors.append("Nilai Semester 2 di bawah standar")

            # Finansial
            if tuition == 0:
                risk_factors.append("Terdapat masalah finansial (tunggakan biaya)")

            # Admission
            if admission < 100:
                risk_factors.append("Nilai admission relatif rendah")

            # Previous grade
            if prev_grade < 100:
                risk_factors.append("Riwayat akademik sebelumnya kurang kuat")

            # ============================
            # OUTPUT ANALISIS
            # ============================
            if prob < 0.4:
                # LOW RISK
                if risk_factors:
                    st.warning("⚠️ Risiko rendah, namun ada beberapa catatan:")
                    for r in risk_factors:
                        st.write(f"• {r}")
                else:
                    st.success("✅ Tidak ditemukan faktor risiko signifikan. Profil mahasiswa kuat.")

            elif prob < 0.7:
                # MEDIUM RISK (INI YANG KAMU BUTUH)
                st.warning("⚠️ Terdapat indikasi risiko sedang berdasarkan pola data.")

                # kalau kosong → tetap paksa tampilkan faktor umum
                if not risk_factors:
                    st.write("• Performa akademik perlu dipantau lebih lanjut")
                    st.write("• Terdapat indikasi ketidakstabilan performa")
                else:
                    for r in risk_factors:
                        st.write(f"• {r}")

            else:
                # HIGH RISK
                st.error("🚨 Risiko tinggi terdeteksi, membutuhkan perhatian serius.")

                for r in risk_factors:
                    st.write(f"• {r}")

            # ============================
            # REKOMENDASI
            # ============================
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<strong>📋 Rekomendasi Tindakan</strong>", unsafe_allow_html=True)

            if prob < 0.4:
                st.success("✅ Tidak Diperlukan Intervensi Khusus")

                st.write("• 🌟 Pertahankan performa akademik")
                st.write("• 🎯 Ikuti kegiatan pengembangan diri")

            elif prob < 0.7:
                # MEDIUM RISK
                st.warning("⚠️ Perlu Monitoring dan Pendampingan")

                st.write("• 📘 Lakukan monitoring performa akademik secara berkala")
                st.write("• 🧠 Berikan bimbingan akademik ringan")
                st.write("• 📊 Evaluasi perkembangan setiap semester")

            else:
                # HIGH RISK
                st.error("🚨 Intervensi Intensif Diperlukan")

                st.write("• 🧠 Program remedial intensif")
                st.write("• 💰 Bantuan finansial (jika diperlukan)")
                st.write("• 🎓 Pendampingan akademik khusus")