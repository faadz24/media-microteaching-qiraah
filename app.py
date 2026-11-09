import streamlit as st

# 1. Konfigurasi Halaman (Harus di baris pertama setelah import)
st.set_page_config(
    page_title="Smart Qira'ah Reader: Ad-Dirasah fil Jamiah",
    page_icon="🎓",
    layout="wide"
)

# 2. Injeksi CSS untuk Teks Arab, Pop-up Tooltip + Gambar, & Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    
    .main-title {
        color: #1e3a8a;
        text-align: center;
        font-family: sans-serif;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #475569;
        text-align: center;
        font-family: sans-serif;
        margin-bottom: 25px;
    }
    .arabic-title {
        font-family: 'Amiri', serif;
        font-size: 30px;
        color: #1e3a8a;
        direction: rtl;
        text-align: right;
        font-weight: bold;
        margin-top: 20px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 5px;
    }
    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 28px;
        line-height: 2.4;
        direction: rtl;
        text-align: right;
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-right: 6px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* STYLE POP-UP / TOOLTIP INTERAKTIF + GAMBAR */
    .vocab {
        color: #2563eb;
        font-weight: bold;
        border-bottom: 2px dashed #2563eb;
        cursor: pointer;
        position: relative;
        display: inline-block;
        padding: 0 4px;
    }
    .vocab:hover {
        background-color: #fef08a;
        border-radius: 4px;
    }
    .vocab .tooltip-box {
        visibility: hidden;
        width: 310px;
        background-color: #0f172a;
        color: #ffffff;
        text-align: right;
        border-radius: 12px;
        padding: 16px;
        position: absolute;
        z-index: 9999;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s ease, visibility 0.3s ease;
        font-size: 15px;
        line-height: 1.6;
        font-family: sans-serif;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        direction: rtl;
        border: 1px solid #3b82f6;
    }
    .vocab .tooltip-box::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -7px;
        border-width: 7px;
        border-style: solid;
        border-color: #0f172a transparent transparent transparent;
    }
    .vocab:hover .tooltip-box {
        visibility: visible;
        opacity: 1;
    }
    
    .svg-container {
        text-align: center;
        background-color: #1e293b;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .example-box {
        background-color: #1e293b;
        border-right: 3px solid #f59e0b;
        padding: 8px 10px;
        border-radius: 6px;
        margin-top: 8px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Database 17 Mufrodat Lengkap (SVG, Terjemahan, Contoh Kalimat, & CTL)
vocab_db = {
    "المَدْرَسَةُ": {
        "indo": "Sekolah / Madrasah",
        "ctl": "💡 CTL: Jenjang pendidikan awal (MA) sebelum ke Perguruan Tinggi.",
        "ar_ex": "يَتَعَلَّمُ الطُّلَّابُ فِي المَدْرَسَةِ الإِسْلَامِيَّةِ.",
        "id_ex": "Para siswa belajar di madrasah aliyah.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'
    },
    "الطُّلَّابُ": {
        "indo": "Siswa / Mahasiswa",
        "ctl": "💡 CTL: Transisi peran dari siswa MA menjadi mahasiswa mandiri.",
        "ar_ex": "الطُّلَّابُ يَسْتَعِدُّونَ لِلاِمْتِحَانِ النِّهَائِيِّ.",
        "id_ex": "Para siswa sedang bersiap menghadapi ujian akhir.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
    },
    "الجَامِعَةُ": {
        "indo": "Universitas / Perguruan Tinggi",
        "ctl": "💡 CTL: Lembaga tinggi tujuan lulusan MA (PTN, PTKIN).",
        "ar_ex": "يَرْغَبُ أَحْمَدُ فِي الدِّرَاسَةِ بِالجَامِعَةِ الحُكُومِيَّةِ.",
        "id_ex": "Ahmad ingin berkuliah di perguruan tinggi negeri.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M12 3l9 7H3l9-7z"/></svg>'
    },
    "المُسْتَقْبَلُ": {
        "indo": "Masa Depan",
        "ctl": "💡 CTL: Cita-cita karier yang dirancang siswa kelas 12.",
        "ar_ex": "التَّخْطِيطُ الجَيِّدُ مُهِمٌّ لِلْمُسْتَقْبَلِ.",
        "id_ex": "Perencanaan yang baik sangat penting untuk masa depan.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
    },
    "التَّسْجِيلُ": {
        "indo": "Pendaftaran / Registrasi",
        "ctl": "💡 CTL: Proses berkas pendaftaran (SNBP, SNBT, SPAN-PTKIN).",
        "ar_ex": "بَدَأَ التَّسْجِيلُ فِي الجَامِعَةِ هَذَا الشَّهْرَ.",
        "id_ex": "Pendaftaran di universitas telah dimulai bulan ini.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
    },
    "القِسْمُ": {
        "indo": "Jurusan / Program Studi",
        "ctl": "💡 CTL: Spesialisasi ilmu sesuai bakat dan minat.",
        "ar_ex": "اخْتَارَ زَيْدٌ قِسْمَ اللُّغَةِ العَرَبِيَّةِ.",
        "id_ex": "Zaid memilih jurusan Bahasa Arab.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>'
    },
    "الكُلِّيَّةُ": {
        "indo": "Fakultas",
        "ctl": "💡 CTL: Wadah jurusan sejenis (Tarbiyah, Kedokteran, Teknik).",
        "ar_ex": "تَقَعُ كُلِّيَّةُ الطِّبِّ فِي وَسَطِ الجَامِعَةِ.",
        "id_ex": "Fakultas Kedokteran terletak di pusat kampus.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="9" y1="6" x2="15" y2="6"/><line x1="9" y1="10" x2="15" y2="10"/><line x1="9" y1="14" x2="15" y2="14"/></svg>'
    },
    "المَكْتَبَةُ": {
        "indo": "Perpustakaan",
        "ctl": "💡 CTL: Pusat referensi bacaan dan riset tugas mahasiswa.",
        "ar_ex": "يَقْرَأُ الطَّالِبُ الكُتُبَ فِي المَكْتَبَةِ.",
        "id_ex": "Mahasiswa membaca buku-buku di perpustakaan.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'
    },
    "الأُسْتَاذُ": {
        "indo": "Dosen / Pengajar",
        "ctl": "💡 CTL: Tenaga pengajar dan pembimbing riset kampus.",
        "ar_ex": "يَشْرَحُ الأُسْتَاذُ الدَّرْسَ بِوُضُوحٍ.",
        "id_ex": "Dosen menjelaskan pelajaran dengan jelas.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
    },
    "المُجْتَمَعُ": {
        "indo": "Masyarakat / Komunitas",
        "ctl": "💡 CTL: Muara pengabdian ilmu lulusan kampus.",
        "ar_ex": "نَحْنُ نَعْمَلُ لِخِدْمَةِ المُجْتَمَعِ.",
        "id_ex": "Kita bekerja untuk mengabdi kepada masyarakat.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
    },
    "وَاصَلَ - يُوَاصِلُ": {
        "indo": "Melanjutkan",
        "ctl": "💡 CTL: Semangat siswa MA meneruskan studi tinggi.",
        "ar_ex": "يُوَاصِلُ العَالِمُ بَحْثَهُ العِلْمِيَّ.",
        "id_ex": "Peneliti itu melanjutkan penelitian ilmiahnya.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>'
    },
    "اِخْتَارَ - يَخْتَارُ": {
        "indo": "Memilih",
        "ctl": "💡 CTL: Kemandirian mengambil keputusan jurusan.",
        "ar_ex": "يَخْتَارُ الطَّالِبُ التَّخَصُّصَ المُنَاسِبَ.",
        "id_ex": "Mahasiswa memilih spesialisasi yang sesuai.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>'
    },
    "تَنَاسَبَ - يَتَنَاسَبُ": {
        "indo": "Sesuai / Cocok",
        "ctl": "💡 CTL: Menyelaraskan minat diri dengan prodi.",
        "ar_ex": "هَذَا التَّخَصُّصُ يَتَنَاسَبُ مَعَ مَهَارَاتِي.",
        "id_ex": "Jurusan ini cocok dengan keterampilan saya.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
    },
    "اِلْتَحَقَ - يَلْتَحِقُ": {
        "indo": "Bergabung / Masuk PT",
        "ctl": "💡 CTL: Resmi terdaftar menjadi mahasiswa baru.",
        "ar_ex": "اِلْتَحَقَتْ عَائِشَةُ بِكُلِّيَّةِ التَّرْبِيَةِ.",
        "id_ex": "Aisyah masuk ke Fakultas Tarbiyah.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>'
    },
    "اِعْتَمَدَ - يَعْتَمِدُ": {
        "indo": "Berdikari / Mandiri",
        "ctl": "💡 CTL: Kemandirian pola belajar di Perguruan Tinggi.",
        "ar_ex": "يَعْتَمِدُ الطَّالِبُ عَلَى نَفْسِهِ فِي الدِّرَاسَةِ.",
        "id_ex": "Mahasiswa mengandalkan dirinya sendiri dalam belajar.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
    },
    "اِسْتَعَدَّ - يَسْتَعِدُّ": {
        "indo": "Bersiap-siap",
        "ctl": "💡 CTL: Persiapan berkas & mental kelas 12.",
        "ar_ex": "يَسْتَعِدُّ الفَرِيقُ لِلْمُسَابَقَةِ.",
        "id_ex": "Tim bersiap-siap untuk perlombaan.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
    },
    "أَفَادَ - يُفِيدُ": {
        "indo": "Memberi Manfaat",
        "ctl": "💡 CTL: Pengabdian ilmu untuk kemaslahatan masyarakat.",
        "ar_ex": "العِلْمُ النَّافِعُ يُفِيدُ النَّاسَ.",
        "id_ex": "Ilmu yang bermanfaat memberikan kegunaan bagi manusia.",
        "svg": '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
    }
}

# Fungsi Helper untuk Membuat Kosa Kata Ber-Pop-up Lengkap
def v(arabic_word, db_key):
    info = vocab_db[db_key]
    return f'''<span class="vocab">{arabic_word}<span class="tooltip-box"><div class="svg-container">{info['svg']}</div><b style="font-size:18px; color:#38bdf8;">{db_key}</b><br><span style="color:#fde047; font-weight:bold;">{info['indo']}</span><br><div class="example-box"><b>📌 Contoh Kalimat:</b><br><span style="font-family:'Amiri'; font-size:16px;">{info['ar_ex']}</span><br><i style="color:#cbd5e1; font-size:12px;">"{info['id_ex']}"</i></div><div style="font-size:12px; margin-top:6px; color:#94a3b8;">{info['ctl']}</div></span></span>'''

# 4. Header Aplikasi
st.markdown('<h1 class="main-title">🎓 Smart Qira\'ah Reader</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Media Pembelajaran Maharah Qira\'ah Kelas 12 MA — Tema: Ad-Dirasah fil Jamiah</p>', unsafe_allow_html=True)
st.caption("👉 **Petunjuk Guru:** Sorot/Arahkan kursor pada kosa kata biru bergaris bawah untuk melihat Gambar Visual, Contoh Kalimat, & Makna CTL!")

# 5. Sidebar Bank Mufrodat (Navigasi Instan)
st.sidebar.header("📌 Bank 17 Kosa Kata Wajib")
selected_word = st.sidebar.selectbox("Bedah Mufrodat via Sidebar:", list(vocab_db.keys()))

if selected_word:
    info = vocab_db[selected_word]
    st.sidebar.markdown(f'<div style="text-align:center; background:#1e293b; padding:10px; border-radius:8px;">{info["svg"]}</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f"### {selected_word}")
    st.sidebar.markdown(f"**Arti:** {info['indo']}")
    st.sidebar.markdown(f"**📌 Contoh Kalimat:**\n- {info['ar_ex']}\n  *( “{info['id_ex']}” )*")
    st.sidebar.info(info['ctl'])

# 6. Layout Utama (2 Kolom)
col1, col2 = st.columns([2.2, 1])

with col1:
    st.subheader("📖 Teks Bacaan (المَادَّةُ)")
    
    # Paragraf 1
    st.markdown('<div class="arabic-title">الفقرة الأولى: الدِّرَاسَةُ فِي الجَامِعَةِ</div>', unsafe_allow_html=True)
    p1_html = f"""
    بَعْدَ التَّخَرُّجِ مِنَ {v("المَدْرَسَةِ", "المَدْرَسَةُ")} الإِسْلَامِيَّةِ، يُرِيدُ كَثِيرٌ مِنَ {v("الطُّلَّابِ", "الطُّلَّابُ")} أَنْ {v("يُوَاصِلُوا", "وَاصَلَ - يُوَاصِلُ")} دِرَاسَتَهُمْ وَيَدْرُسُوا فِي {v("الجَامِعَةِ", "الجَامِعَةُ")}. يَذْهَبُ الطُّلَّابُ إِلَى الجَامِعَةِ {v("لِلتَّسْجِيلِ", "التَّسْجِيلُ")} وَتَقْدِيمِ الأَوْرَاقِ. فِي الجَامِعَةِ، يَتَعَلَّمُ الطُّلَّابُ أَشْيَاءَ جَدِيدَةً وَ{v("يَسْتَعِدُّونَ", "اِسْتَعَدَّ - يَسْتَعِدُّ")} {v("لِلْمُسْتَقْبَلِ", "المُسْتَقْبَلُ")}. كَمَا يَتَعَلَّمُونَ أَنْ {v("يَعْتَمِدُوا", "اِعْتَمَدَ - يَعْتَمِدُ")} عَلَى أَنْفُسِهِمْ.
    """
    st.markdown(f'<div class="arabic-text">{p1_html}</div>', unsafe_allow_html=True)

    # Paragraf 2
    st.markdown('<div class="arabic-title">الفقرة الثانية: اخْتِيَارُ القِسْمِ وَالكُلِّيَّةِ</div>', unsafe_allow_html=True)
    p2_html = f"""
    {v("يَخْتَارُ", "اِخْتَارَ - يَخْتَارُ")} كُلُّ طَالِبٍ {v("القِسْمَ", "القِسْمُ")} الَّذِي يُحِبُّهُ وَ{v("يُنَاسِبُهُ", "تَنَاسَبَ - يَتَنَاسَبُ")}. مَنْ يُحِبُّ الطِّبَّ {v("يَلْتَحِقُ", "اِلْتَحَقَ - يَلْتَحِقُ")} وَيَدْرُسُ فِي {v("كُلِّيَّةِ", "الكُلِّيَّةُ")} الطِّبِّ، وَمَنْ يُحِبُّ الهَنْدَسَةَ يَدْرُسُ فِي كُلِّيَّةِ الهَنْدَسَةِ. وَهُنَاكَ أَيْضًا كُلِّيَّةُ التَّرْبِيَةِ وَكُلِّيَّةُ الشَّرِيعَةِ. يَخْتَارُ الطُّلَّابُ هَذِهِ الكُلِّيَّاتِ لِأَنَّهُمْ يُرِيدُونَ أَنْ يَتَعَلَّمُوا وَ{v("يُفِيدُوا", "أَفَادَ - يُفِيدُ")} {v("المُجْتَمَعَ", "المُجْتَمَعُ")}.
    """
    st.markdown(f'<div class="arabic-text">{p2_html}</div>', unsafe_allow_html=True)

    # Paragraf 3
    st.markdown('<div class="arabic-title">الفقرة الثالثة: الحَيَاةُ الجَامِعِيَّةُ وَالدِّرَاسَةُ</div>', unsafe_allow_html=True)
    p3_html = f"""
    فِي الجَامِعَةِ، يَحْضُرُ الطُّلَّابُ الدُّرُوسَ فِي الفَصْلِ مَعَ {v("الأُسْتَاذِ", "الأُسْتَاذُ")}. وَيَذْهَبُونَ إِلَى {v("المَكْتَبَةِ", "المَكْتَبَةُ")} لِلْقِرَاءَةِ وَالبَحْثِ عَنِ المَعْلُومَاتِ. كَمَا يَتَعَلَّمُونَ مِنْ خِلَالِ المُنَاقَشَةِ مَعَ الأَسَاتِذَةِ وَالأَصْدِقَاءِ. وَيَسْتَخْدِمُونَ طُرُقًا حَدِيثَةً فِي التَّعَلُّمِ لِكَيْ يَكُونُوا مُسْتَعِدِّينَ لِلْعَمَلِ فِي المُسْتَقْبَلِ.
    """
    st.markdown(f'<div class="arabic-text">{p3_html}</div>', unsafe_allow_html=True)

with col2:
    st.subheader("💡 Diskusi Kontekstual (CTL)")
    st.write("Panduan pertanyaan guru saat membimbing bacaan:")
    
    with st.expander("❓ Diskusi Paragraf 1"):
        st.write("• Mengapa lulusan MA harus mulai belajar mandiri (*يَعْتَمِدُوا عَلَى أَنْفُسِهِمْ*) saat di kampus?")
        st.write("• Jalur pendaftaran (*التَّسْجِيلُ*) apa saja yang kalian ketahui untuk masuk PTN/PTKIN?")

    with st.expander("❓ Diskusi Paragraf 2"):
        st.write("• Bagaimana cara kalian memilih jurusan (*القِسْمُ*) yang sesuai (*يُنَاسِبُهُ*) dengan bakat?")
        st.write("• Apa perbedaan peran Fakultas Kedokteran, Teknik, Tarbiyah, dan Syariah?")

    with st.expander("❓ Diskusi Paragraf 3"):
        st.write("• Apa perbedaan cara belajar di kelas MA dengan di perpustakaan (*المَكْتَبَةُ*) kampus?")
        st.write("• Mengapa diskusi bersama dosen (*الأُسْتَاذُ*) sangat penting di perguruan tinggi?")
