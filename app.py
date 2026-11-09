import streamlit as st

# 1. Konfigurasi Halaman (Harus berada di paling atas setelah import)
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
    
    /* STYLE POP-UP / TOOLTIP INTERAKTIF + GAMBAR KONTEKSTUAL */
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
        width: 320px;
        background-color: #0f172a;
        color: #ffffff;
        text-align: right;
        border-radius: 12px;
        padding: 14px;
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
    
    .popup-img {
        width: 100%;
        height: 140px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #334155;
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

# 3. Database 17 Mufrodat Lengkap dengan Gambar Foto Kontekstual Asli (Unsplash)
vocab_db = {
    "المَدْرَسَةُ": {
        "indo": "Sekolah / Madrasah",
        "ctl": "💡 CTL: Jenjang pendidikan awal (MA) sebelum ke Perguruan Tinggi.",
        "ar_ex": "يَتَعَلَّمُ الطُّلَّابُ فِي المَدْرَسَةِ الإِسْلَامِيَّةِ.",
        "id_ex": "Para siswa belajar di madrasah aliyah.",
        "img_url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"
    },
    "الطُّلَّابُ": {
        "indo": "Siswa / Mahasiswa",
        "ctl": "💡 CTL: Transisi peran dari siswa MA menjadi mahasiswa mandiri.",
        "ar_ex": "الطُّلَّابُ يَسْتَعِدُّونَ لِلاِمْتِحَانِ النِّهَائِيِّ.",
        "id_ex": "Para siswa sedang bersiap menghadapi ujian akhir.",
        "img_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"
    },
    "الجَامِعَةُ": {
        "indo": "Universitas / Perguruan Tinggi",
        "ctl": "💡 CTL: Lembaga tinggi tujuan lulusan MA (PTN, PTKIN).",
        "ar_ex": "يَرْغَبُ أَحْمَدُ فِي الدِّرَاسَةِ بِالجَامِعَةِ الحُكُومِيَّةِ.",
        "id_ex": "Ahmad ingin berkuliah di perguruan tinggi negeri.",
        "img_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400"
    },
    "المُسْتَقْبَلُ": {
        "indo": "Masa Depan",
        "ctl": "💡 CTL: Cita-cita karier yang dirancang siswa kelas 12.",
        "ar_ex": "التَّخْطِيطُ الجَيِّدُ مُهِمٌّ لِلْمُسْتَقْبَلِ.",
        "id_ex": "Perencanaan yang baik sangat penting untuk masa depan.",
        "img_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"
    },
    "التَّسْجِيلُ": {
        "indo": "Pendaftaran / Registrasi",
        "ctl": "💡 CTL: Proses berkas pendaftaran (SNBP, SNBT, SPAN-PTKIN).",
        "ar_ex": "بَدَأَ التَّسْجِيلُ فِي الجَامِعَةِ هَذَا الشَّهْرَ.",
        "id_ex": "Pendaftaran di universitas telah dimulai bulan ini.",
        "img_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"
    },
    "القِسْمُ": {
        "indo": "Jurusan / Program Studi",
        "ctl": "💡 CTL: Spesialisasi ilmu sesuai bakat dan minat.",
        "ar_ex": "اخْتَارَ زَيْدٌ قِسْمَ اللُّغَةِ العَرَبِيَّةِ.",
        "id_ex": "Zaid memilih jurusan Bahasa Arab.",
        "img_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400"
    },
    "الكُلِّيَّةُ": {
        "indo": "Fakultas",
        "ctl": "💡 CTL: Wadah jurusan sejenis (Tarbiyah, Kedokteran, Teknik).",
        "ar_ex": "تَقَعُ كُلِّيَّةُ الطِّبِّ فِي وَسَطِ الجَامِعَةِ.",
        "id_ex": "Fakultas Kedokteran terletak di pusat kampus.",
        "img_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400"
    },
    "المَكْتَبَةُ": {
        "indo": "Perpustakaan",
        "ctl": "💡 CTL: Pusat referensi bacaan dan riset tugas mahasiswa.",
        "ar_ex": "يَقْرَأُ الطَّالِبُ الكُتُبَ فِي المَكْتَبَةِ.",
        "id_ex": "Mahasiswa membaca buku-buku di perpustakaan.",
        "img_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400"
    },
    "الأُسْتَاذُ": {
        "indo": "Dosen / Pengajar",
        "ctl": "💡 CTL: Tenaga pengajar dan pembimbing riset kampus.",
        "ar_ex": "يَشْرَحُ الأُسْتَاذُ الدَّرْسَ بِوُضُوحٍ.",
        "id_ex": "Dosen menjelaskan pelajaran dengan jelas.",
        "img_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=400"
    },
    "المُجْتَمَعُ": {
        "indo": "Masyarakat / Komunitas",
        "ctl": "💡 CTL: Muara pengabdian ilmu lulusan kampus.",
        "ar_ex": "نَحْنُ نَعْمَلُ لِخِدْمَةِ المُجْتَمَعِ.",
        "id_ex": "Kita bekerja untuk mengabdi kepada masyarakat.",
        "img_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400"
    },
    "وَاصَلَ - يُوَاصِلُ": {
        "indo": "Melanjutkan",
        "ctl": "💡 CTL: Semangat siswa MA meneruskan studi tinggi.",
        "ar_ex": "يُوَاصِلُ العَالِمُ بَحْثَهُ العِلْمِيَّ.",
        "id_ex": "Peneliti itu melanjutkan penelitian ilmiahnya.",
        "img_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"
    },
    "اِخْتَارَ - يَخْتَارُ": {
        "indo": "Memilih",
        "ctl": "💡 CTL: Kemandirian mengambil keputusan jurusan.",
        "ar_ex": "يَخْتَارُ الطَّالِبُ التَّخَصُّصَ المُنَاسِبَ.",
        "id_ex": "Mahasiswa memilih spesialisasi yang sesuai.",
        "img_url": "https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=400"
    },
    "تَنَاسَبَ - يَتَنَاسَبُ": {
        "indo": "Sesuai / Cocok",
        "ctl": "💡 CTL: Menyelaraskan minat diri dengan prodi.",
        "ar_ex": "هَذَا التَّخَصُّصُ يَتَنَاسَبُ مَعَ مَهَارَاتِي.",
        "id_ex": "Jurusan ini cocok dengan keterampilan saya.",
        "img_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400"
    },
    "اِلْتَحَقَ - يَلْتَحِقُ": {
        "indo": "Bergabung / Masuk PT",
        "ctl": "💡 CTL: Resmi terdaftar menjadi mahasiswa baru.",
        "ar_ex": "اِلْتَحَقَتْ عَائِشَةُ بِكُلِّيَّةِ التَّرْبِيَةِ.",
        "id_ex": "Aisyah masuk ke Fakultas Tarbiyah.",
        "img_url": "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=400"
    },
    "اِعْتَمَدَ - يَعْتَمِدُ": {
        "indo": "Berdikari / Mandiri",
        "ctl": "💡 CTL: Kemandirian pola belajar di Perguruan Tinggi.",
        "ar_ex": "يَعْتَمِدُ الطَّالِبُ عَلَى نَفْسِهِ فِي الدِّرَاسَةِ.",
        "id_ex": "Mahasiswa mengandalkan dirinya sendiri dalam belajar.",
        "img_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400"
    },
    "اِسْتَعَدَّ - يَسْتَعِدُّ": {
        "indo": "Bersiap-siap",
        "ctl": "💡 CTL: Persiapan berkas & mental kelas 12.",
        "ar_ex": "يَسْتَعِدُّ الفَرِيقُ لِلْمُسَابَقَةِ.",
        "id_ex": "Tim bersiap-siap untuk perlombaan.",
        "img_url": "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=400"
    },
    "أَفَادَ - يُفِيدُ": {
        "indo": "Memberi Manfaat",
        "ctl": "💡 CTL: Pengabdian ilmu untuk kemaslahatan masyarakat.",
        "ar_ex": "العِلْمُ النَّافِعُ يُفِيدُ النَّاسَ.",
        "id_ex": "Ilmu yang bermanfaat memberikan kegunaan bagi manusia.",
        "img_url": "https://images.unsplash.com/photo-1531206715517-5c0ba140b2b8?w=400"
    }
}

# Fungsi Helper untuk Membuat Kosa Kata Ber-Pop-up Lengkap + Gambar Foto
def v(arabic_word, db_key):
    info = vocab_db[db_key]
    return f'''<span class="vocab">{arabic_word}<span class="tooltip-box"><img src="{info['img_url']}" class="popup-img"><b style="font-size:18px; color:#38bdf8;">{db_key}</b><br><span style="color:#fde047; font-weight:bold;">{info['indo']}</span><br><div class="example-box"><b>📌 Contoh Kalimat:</b><br><span style="font-family:'Amiri'; font-size:16px;">{info['ar_ex']}</span><br><i style="color:#cbd5e1; font-size:12px;">"{info['id_ex']}"</i></div><div style="font-size:12px; margin-top:6px; color:#94a3b8;">{info['ctl']}</div></span></span>'''

# 4. Header Aplikasi
st.markdown('<h1 class="main-title">🎓 Smart Qira\'ah Reader</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Media Pembelajaran Maharah Qira\'ah Kelas 12 MA — Tema: Ad-Dirasah fil Jamiah</p>', unsafe_allow_html=True)
st.caption("👉 **Petunjuk Guru:** Sorot/Arahkan kursor pada kosa kata biru bergaris bawah untuk melihat Gambar Foto Asli, Contoh Kalimat, & Makna CTL!")

# 5. Sidebar Bank Mufrodat (Navigasi Instan)
st.sidebar.header("📌 Bank 17 Kosa Kata Wajib")
selected_word = st.sidebar.selectbox("Bedah Mufrodat via Sidebar:", list(vocab_db.keys()))

if selected_word:
    info = vocab_db[selected_word]
    st.sidebar.image(info["img_url"], use_container_width=True)
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
