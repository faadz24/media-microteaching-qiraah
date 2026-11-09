import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Smart Qira'ah Reader: Ad-Dirasah fil Jamiah",
    page_icon="🎓",
    layout="wide"
)

# 2. Injeksi CSS untuk Teks Arab, Pop-up Tooltip, & Styling
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
        line-height: 2.5;
        direction: rtl;
        text-align: right;
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-right: 6px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* INTERAKSI KATA */
    .vocab-target {
        color: #2563eb;
        font-weight: bold;
        border-bottom: 2px dashed #2563eb;
        cursor: pointer;
        position: relative;
        display: inline-block;
        padding: 0 4px;
    }
    .vocab-target:hover {
        background-color: #fef08a;
        border-radius: 4px;
    }
    
    .vocab-regular {
        color: #0f172a;
        cursor: pointer;
        position: relative;
        display: inline-block;
        padding: 0 2px;
        border-bottom: 1px dotted #cbd5e1;
    }
    .vocab-regular:hover {
        background-color: #e2e8f0;
        border-radius: 4px;
        color: #1e3a8a;
    }

    /* TOOLTIP / POP-UP */
    .tooltip-box {
        visibility: hidden;
        width: 300px;
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
        font-size: 14px;
        line-height: 1.5;
        font-family: sans-serif;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        direction: rtl;
        border: 1px solid #3b82f6;
    }
    .tooltip-box::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -7px;
        border-width: 7px;
        border-style: solid;
        border-color: #0f172a transparent transparent transparent;
    }
    .vocab-target:hover .tooltip-box, .vocab-regular:hover .tooltip-box {
        visibility: visible;
        opacity: 1;
    }
    
    .popup-img {
        width: 100%;
        height: 130px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid #334155;
    }
    .example-box {
        background-color: #1e293b;
        border-right: 3px solid #f59e0b;
        padding: 6px 8px;
        border-radius: 6px;
        margin-top: 6px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Database Complete (17 Target Mufrodat + Kata-Kata Lain dalam Teks)
words_db = {
    # --- 17 TARGET MUFRODAT UTAMA (LENGKAP PHOTO + CTL) ---
    "المَدْرَسَةُ": {"type": "target", "indo": "Sekolah / Madrasah", "ctl": "💡 CTL: Jenjang MA sebelum ke Perguruan Tinggi.", "ar_ex": "يَتَعَلَّمُ الطُّلَّابُ فِي المَدْرَسَةِ الإِسْلَامِيَّةِ.", "id_ex": "Para siswa belajar di madrasah aliyah.", "img_url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"},
    "الطُّلَّابُ": {"type": "target", "indo": "Siswa / Mahasiswa", "ctl": "💡 CTL: Transisi dari siswa MA menjadi mahasiswa.", "ar_ex": "الطُّلَّابُ يَسْتَعِدُّونَ لِلاِمْتِحَانِ.", "id_ex": "Para siswa bersiap untuk ujian.", "img_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"},
    "الجَامِعَةُ": {"type": "target", "indo": "Universitas / Perguruan Tinggi", "ctl": "💡 CTL: Perguruan tinggi tujuan (PTN/PTKIN).", "ar_ex": "يَدْرُسُ فِي الجَامِعَةِ الحُكُومِيَّةِ.", "id_ex": "Berkuliah di perguruan tinggi negeri.", "img_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400"},
    "المُسْتَقْبَلُ": {"type": "target", "indo": "Masa Depan", "ctl": "💡 CTL: Perencanaan karier & cita-cita siswa.", "ar_ex": "التَّخْطِيطُ الجَيِّدُ مُهِمٌّ لِلْمُسْتَقْبَلِ.", "id_ex": "Perencanaan yang baik penting untuk masa depan.", "img_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"},
    "التَّسْجِيلُ": {"type": "target", "indo": "Pendaftaran / Registrasi", "ctl": "💡 CTL: Alur administrasi masuk (SNBP/SPAN-PTKIN).", "ar_ex": "بَدَأَ التَّسْجِيلُ فِي الجَامِعَةِ.", "id_ex": "Pendaftaran universitas telah dibuka.", "img_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"},
    "القِسْمُ": {"type": "target", "indo": "Jurusan / Prodi", "ctl": "💡 CTL: Spesialisasi studi sesuai minat & bakat.", "ar_ex": "اخْتَارَ قِسْمَ اللُّغَةِ العَرَبِيَّةِ.", "id_ex": "Memilih jurusan Bahasa Arab.", "img_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400"},
    "الكُلِّيَّةُ": {"type": "target", "indo": "Fakultas", "ctl": "💡 CTL: Wadah jurusan sejenis (Tarbiyah, Kedokteran, dll).", "ar_ex": "كُلِّيَّةُ الطِّبِّ فِي الجَامِعَةِ.", "id_ex": "Fakultas kedokteran di universitas.", "img_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400"},
    "المَكْتَبَةُ": {"type": "target", "indo": "Perpustakaan", "ctl": "💡 CTL: Pusat rujukan riset & bacaan mahasiswa.", "ar_ex": "يَقْرَأُ الكُتُبَ فِي المَكْتَبَةِ.", "id_ex": "Membaca buku-buku di perpustakaan.", "img_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400"},
    "الأُسْتَاذُ": {"type": "target", "indo": "Dosen / Pengajar", "ctl": "💡 CTL: Pendidik & pembimbing riset di kampus.", "ar_ex": "يَشْرَحُ الأُسْتَاذُ الدَّرْسَ.", "id_ex": "Dosen menjelaskan pelajaran.", "img_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=400"},
    "المُجْتَمَعُ": {"type": "target", "indo": "Masyarakat / Komunitas", "ctl": "💡 CTL: Muara pengabdian ilmu sarjana.", "ar_ex": "نَعْمَلُ لِخِدْمَةِ المُجْتَمَعِ.", "id_ex": "Bekerja mengabdi pada masyarakat.", "img_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400"},
    "وَاصَلَ - يُوَاصِلُ": {"type": "target", "indo": "Melanjutkan", "ctl": "💡 CTL: Semangat meneruskan pendidikan ke PT.", "ar_ex": "يُوَاصِلُ دِرَاسَتَهُ العَالِيَةَ.", "id_ex": "Melanjutkan studi tingginya.", "img_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"},
    "اِخْتَارَ - يَخْتَارُ": {"type": "target", "indo": "Memilih", "ctl": "💡 CTL: Kemandirian mengambil keputusan prodi.", "ar_ex": "يَخْتَارُ التَّخَصُّصَ المُنَاسِبَ.", "id_ex": "Memilih jurusan yang cocok.", "img_url": "https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=400"},
    "تَنَاسَبَ - يَتَنَاسَبُ": {"type": "target", "indo": "Sesuai / Cocok", "ctl": "💡 CTL: Menyelaraskan potensi diri dengan prodi.", "ar_ex": "يَتَنَاسَبُ مَعَ مَهَارَاتِي.", "id_ex": "Sesuai dengan keterampilanku.", "img_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400"},
    "اِلْتَحَقَ - يَلْتَحِقُ": {"type": "target", "indo": "Bergabung / Masuk PT", "ctl": "💡 CTL: Resmi terdaftar menjadi mahasiswa baru.", "ar_ex": "اِلْتَحَقَ بِالجَامِعَةِ.", "id_ex": "Masuk ke universitas.", "img_url": "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=400"},
    "اِعْتَمَدَ - يَعْتَمِدُ": {"type": "target", "indo": "Berdikari / Mandiri", "ctl": "💡 CTL: Kemandirian pola belajar di Perguruan Tinggi.", "ar_ex": "يَعْتَمِدُ عَلَى نَفْسِهِ.", "id_ex": "Mengandalkan dirinya sendiri.", "img_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400"},
    "اِسْتَعَدَّ - يَسْتَعِدُّ": {"type": "target", "indo": "Bersiap-siap", "ctl": "💡 CTL: Persiapan berkas & mental kelas 12.", "ar_ex": "يَسْتَعِدُّ لِلاِمْتِحَانِ.", "id_ex": "Bersiap-siap menghadapi ujian.", "img_url": "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=400"},
    "أَفَادَ - يُفِيدُ": {"type": "target", "indo": "Memberi Manfaat", "ctl": "💡 CTL: Pengabdian ilmu untuk kemaslahatan.", "ar_ex": "العِلْمُ يُفِيدُ النَّاسَ.", "id_ex": "Ilmu memberikan manfaat bagi manusia.", "img_url": "https://images.unsplash.com/photo-1531206715517-5c0ba140b2b8?w=400"},

    # --- KATA-KATA PENDUKUNG DALAM TEKS (POPU-UP SIMPEL) ---
    "بَعْدَ": {"type": "regular", "indo": "Setelah (Zaraf Zaman)", "gram": "Harf / Kata Keterangan Waktu"},
    "التَّخَرُّجِ": {"type": "regular", "indo": "Kelulusan / Wisuda", "gram": "Isim Masdar (Dari verb: tajarraja)"},
    "مِنَ": {"type": "regular", "indo": "Dari", "gram": "Harf Jar"},
    "الإِسْلَامِيَّةِ": {"type": "regular", "indo": "Islam / Keislaman", "gram": "Na'at (Kata Sifat)"},
    "يُرِيدُ": {"type": "regular", "indo": "Ingin / Menghendaki", "gram": "Fi'il Mudhari' (Verba Present)"},
    "كَثِيرٌ": {"type": "regular", "indo": "Banyak", "gram": "Isim Sifat"},
    "أَنْ": {"type": "regular", "indo": "Bahwa / Untuk", "gram": "Harf Nashab"},
    "دِرَاسَتَهُمْ": {"type": "regular", "indo": "Studi / Pembelajaran Mereka", "gram": "Isim + Dhamir (Kata Ganti)"},
    "وَيَدْرُسُوا": {"type": "regular", "indo": "Dan mereka belajar / berkuliah", "gram": "Fi'il Mudhari' Manshub"},
    "فِي": {"type": "regular", "indo": "Di / Di dalam", "gram": "Harf Jar"},
    "يَذْهَبُ": {"type": "regular", "indo": "Pergi / Berangkat", "gram": "Fi'il Mudhari'"},
    "إِلَى": {"type": "regular", "indo": "Ke / Kepada", "gram": "Harf Jar"},
    "وَتَقْدِيمِ": {"type": "regular", "indo": "Dan menyerahkan / mengajukan", "gram": "Isim Masdar + Harf Athaf"},
    "الأَوْرَاقِ": {"type": "regular", "indo": "Berkas-berkas / Dokumen", "gram": "Isim Jamak Taksir"},
    "يَتَعَلَّمُ": {"type": "regular", "indo": "Belajar / Mempelajari", "gram": "Fi'il Mudhari'"},
    "أَشْيَاءَ": {"type": "regular", "indo": "Hal-hal / Sesuatu", "gram": "Isim Jamak"},
    "جَدِيدَةً": {"type": "regular", "indo": "Baru", "gram": "Na'at / Kata Sifat"},
    "لِلْمُسْتَقْبَلِ": {"type": "regular", "indo": "Untuk masa depan", "gram": "Harf Jar + Isim"},
    "كَمَا": {"type": "regular", "indo": "Sebagaimana / Juga", "gram": "Harf Sambung"},
    "يَتَعَلَّمُونَ": {"type": "regular", "indo": "Mereka belajar", "gram": "Fi'il Mudhari' Jamak"},
    "عَلَى": {"type": "regular", "indo": "Atas / Kepada", "gram": "Harf Jar"},
    "أَنْفُسِهِمْ": {"type": "regular", "indo": "Diri mereka sendiri", "gram": "Isim + Dhamir (Kemandirian)"},
    "كُلُّ": {"type": "regular", "indo": "Setiap / Masing-masing", "gram": "Isim Mudhaf"},
    "طَالِبٍ": {"type": "regular", "indo": "Siswa / Pelajar", "gram": "Isim Mufrad (Tunggal)"},
    "الَّذِي": {"type": "regular", "indo": "Yang (Isim Maushul)", "gram": "Kata Hubung Yang"},
    "يُحِبُّهُ": {"type": "regular", "indo": "Ia menyukainya", "gram": "Fi'il Mudhari' + Dhamir"},
    "مَنْ": {"type": "regular", "indo": "Barangsiapa / Siapa yang", "gram": "Isim Syarat / Maushul"},
    "الطِّبَّ": {"type": "regular", "indo": "Kedokteran / Ilmu Medis", "gram": "Isim"},
    "يَدْرُسُ": {"type": "regular", "indo": "Belajar / Berkuliah", "gram": "Fi'il Mudhari'"},
    "الطِّبِّ": {"type": "regular", "indo": "Kedokteran", "gram": "Isim Mudhaf Ilaih"},
    "الهَنْدَسَةَ": {"type": "regular", "indo": "Teknik / Rekayasa", "gram": "Isim Jurusan"},
    "وَهُنَاكَ": {"type": "regular", "indo": "Dan di sana / Terdapat juga", "gram": "Isim Isyarah"},
    "أَيْضًا": {"type": "regular", "indo": "Juga / Pula", "gram": "Maf'ul Mutlaq / Maf'ul Fih"},
    "التَّرْبِيَةِ": {"type": "regular", "indo": "Pendidikan / Tarbiyah", "gram": "Isim Fakultas"},
    "الشَّرِيعَةِ": {"type": "regular", "indo": "Syariah / Hukum Islam", "gram": "Isim Fakultas"},
    "هَذِهِ": {"type": "regular", "indo": "Ini (Kata Tunjuk)", "gram": "Isim Isyarah Muannats"},
    "الكُلِّيَّاتِ": {"type": "regular", "indo": "Fakultas-fakultas", "gram": "Isim Jamak Muannats Salim"},
    "لِأَنَّهُمْ": {"type": "regular", "indo": "Karena mereka", "gram": "Harf Sababiyah + Dhamir"},
    "يُرِيدُونَ": {"type": "regular", "indo": "Mereka ingin / menghendaki", "gram": "Fi'il Mudhari' Jamak"},
    "يَحْضُرُ": {"type": "regular", "indo": "Menghadiri / Mengikuti", "gram": "Fi'il Mudhari'"},
    "الدُّرُوسَ": {"type": "regular", "indo": "Pelajaran-pelajaran / Kuliah", "gram": "Isim Jamak Taksir"},
    "الفَصْلِ": {"type": "regular", "indo": "Ruang Kelas", "gram": "Isim Tempat"},
    "مَعَ": {"type": "regular", "indo": "Bersama / Dengan", "gram": "Zaraf Makan"},
    "وَيَذْهَبُونَ": {"type": "regular", "indo": "Dan mereka pergi", "gram": "Fi'il Mudhari' Jamak"},
    "لِلْقِرَاءَةِ": {"type": "regular", "indo": "Untuk membaca", "gram": "Harf Jar + Isim Masdar"},
    "وَالبَحْثِ": {"type": "regular", "indo": "Dan meriset / mencari", "gram": "Isim Masdar"},
    "عَنِ": {"type": "regular", "indo": "Tentang / Dari", "gram": "Harf Jar"},
    "المَعْلُومَاتِ": {"type": "regular", "indo": "Informasi / Data", "gram": "Isim Jamak Muannats Salim"},
    "مِنْ": {"type": "regular", "indo": "Dari / Melalui", "gram": "Harf Jar"},
    "خِلَالِ": {"type": "regular", "indo": "Melalui / Sela-sela", "gram": "Zaraf"},
    "المُنَاقَشَةِ": {"type": "regular", "indo": "Diskusi / Tanya Jawab", "gram": "Isim Masdar"},
    "الأَسَاتِذَةِ": {"type": "regular", "indo": "Para Dosen / Pengajar", "gram": "Isim Jamak dari Ustadz"},
    "وَالأَصْدِقَاءِ": {"type": "regular", "indo": "Dan teman-teman", "gram": "Isim Jamak Taksir"},
    "وَيَسْتَخْدِمُونَ": {"type": "regular", "indo": "Dan mereka menggunakan", "gram": "Fi'il Mudhari' Jamak"},
    "طُرُقًا": {"type": "regular", "indo": "Metode-metode / Cara", "gram": "Isim Jamak Taksir"},
    "حَدِيثَةً": {"type": "regular", "indo": "Modern / Terbaru", "gram": "Na'at / Kata Sifat"},
    "لِكَيْ": {"type": "regular", "indo": "Supaya / Agar", "gram": "Harf Nashab"},
    "يَكُونُوا": {"type": "regular", "indo": "Agar mereka menjadi", "gram": "Fi'il Mudhari' Naqis"},
    "مُسْتَعِدِّينَ": {"type": "regular", "indo": "Siap / Siap sedia", "gram": "Khabar Kana (Jamak)"},
    "لِلْعَمَلِ": {"type": "regular", "indo": "Untuk bekerja", "gram": "Harf Jar + Isim Masdar"}
}

# Fungsi Builder untuk Membuat Setiap Kata Interaktif
def w(arabic_word, db_key=None):
    key = db_key if db_key else arabic_word
    info = words_db.get(key, {"type": "regular", "indo": "Kata dalam teks", "gram": "Kata"})
    
    if info["type"] == "target":
        # Pop-Up Lengkap untuk 17 Mufrodat Utama
        return f'''<span class="vocab-target">{arabic_word}<span class="tooltip-box"><img src="{info['img_url']}" class="popup-img"><b style="font-size:17px; color:#38bdf8;">{key}</b><br><span style="color:#fde047; font-weight:bold;">{info['indo']}</span><br><div class="example-box"><b>📌 Contoh Kalimat:</b><br><span style="font-family:'Amiri'; font-size:16px;">{info['ar_ex']}</span><br><i style="color:#cbd5e1; font-size:11px;">"{info['id_ex']}"</i></div><div style="font-size:11px; margin-top:5px; color:#94a3b8;">{info['ctl']}</div></span></span>'''
    else:
        # Pop-Up Simpel untuk Kata Pendukung Lainnya
        gram_info = f'<br><small style="color:#94a3b8;">({info.get("gram", "")})</small>' if "gram" in info else ""
        return f'''<span class="vocab-regular">{arabic_word}<span class="tooltip-box" style="width:200px; text-align:center;"><b style="font-size:16px; color:#38bdf8;">{arabic_word}</b><br><span style="color:#fde047;">{info['indo']}</span>{gram_info}</span></span>'''

# 4. Header Aplikasi
st.markdown('<h1 class="main-title">🎓 Smart Qira\'ah Reader</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Media Pembelajaran Maharah Qira\'ah Kelas 12 MA — Tema: Ad-Dirasah fil Jamiah</p>', unsafe_allow_html=True)
st.caption("👉 **Petunjuk Guru:** *Setiap kata* dalam teks ini kini dapat diklik/disorot! Kata bergaris bawah biru adalah **17 Mufrodat Utama** (Pop-up Gambar + CTL), sedangkan kata lainnya menampilkan **Pop-up Arti & Tata Bahasa**.")

# 5. Sidebar Bank Mufrodat Target
target_keys = [k for k, v in words_db.items() if v.get("type") == "target"]
st.sidebar.header("📌 Bank 17 Kosa Kata Wajib")
selected_word = st.sidebar.selectbox("Bedah Mufrodat Utama via Sidebar:", target_keys)

if selected_word:
    info = words_db[selected_word]
    st.sidebar.image(info["img_url"], use_container_width=True)
    st.sidebar.markdown(f"### {selected_word}")
    st.sidebar.markdown(f"**Arti:** {info['indo']}")
    st.sidebar.markdown(f"**📌 Contoh Kalimat:**\n- {info['ar_ex']}\n  *( “{info['id_ex']}” )*")
    st.sidebar.info(info['ctl'])

# 6. Layout Utama Teks Bacaan (Semua Kata Ber-Pop-up)
col1, col2 = st.columns([2.2, 1])

with col1:
    st.subheader("📖 Teks Bacaan (المَادَّةُ)")
    
    # Paragraf 1
    st.markdown('<div class="arabic-title">الفقرة الأولى: الدِّرَاسَةُ فِي الجَامِعَةِ</div>', unsafe_allow_html=True)
    p1_html = f"""
    {w("بَعْدَ")} {w("التَّخَرُّجِ")} {w("مِنَ")} {w("المَدْرَسَةِ", "المَدْرَسَةُ")} {w("الإِسْلَامِيَّةِ")}، {w("يُرِيدُ")} {w("كَثِيرٌ")} {w("مِنَ")} {w("الطُّلَّابِ", "الطُّلَّابُ")} {w("أَنْ")} {w("يَدْرُسُوا")} {w("فِي")} {w("الجَامِعَةِ", "الجَامِعَةُ")}. {w("يَذْهَبُ")} {w("الطُّلَّابُ", "الطُّلَّابُ")} {w("إِلَى")} {w("الجَامِعَةِ", "الجَامِعَةُ")} {w("لِلتَّسْجِيلِ", "التَّسْجِيلُ")} {w("وَتَقْدِيمِ")} {w("الأَوْرَاقِ")}. {w("فِي")} {w("الجَامِعَةِ", "الجَامِعَةُ")}، {w("يَتَعَلَّمُ")} {w("الطُّلَّابُ", "الطُّلَّابُ")} {w("أَشْيَاءَ")} {w("جَدِيدَةً")} {w("وَيَسْتَعِدُّونَ", "اِسْتَعَدَّ - يَسْتَعِدُّ")} {w("لِلْمُسْتَقْبَلِ", "المُسْتَقْبَلُ")}. {w("كَمَا")} {w("يَتَعَلَّمُونَ")} {w("أَنْ")} {w("يَعْتَمِدُوا", "اِعْتَمَدَ - يَعْتَمِدُ")} {w("عَلَى")} {w("أَنْفُسِهِمْ")}.
    """
    st.markdown(f'<div class="arabic-text">{p1_html}</div>', unsafe_allow_html=True)

    # Paragraf 2
    st.markdown('<div class="arabic-title">الفقرة الثانية: اخْتِيَارُ القِسْمِ وَالكُلِّيَّةِ</div>', unsafe_allow_html=True)
    p2_html = f"""
    {w("يَخْتَارُ", "اِخْتَارَ - يَخْتَارُ")} {w("كُلُّ")} {w("طَالِبٍ")} {w("القِسْمَ", "القِسْمُ")} {w("الَّذِي")} {w("يُحِبُّهُ")} {w("وَيُنَاسِبُهُ", "تَنَاسَبَ - يَتَنَاسَبُ")}. {w("مَنْ")} {w("يُحِبُّ")} {w("الطِّبَّ")} {w("يَدْرُسُ")} {w("فِي")} {w("كُلِّيَّةِ", "الكُلِّيَّةُ")} {w("الطِّبِّ")}، {w("وَمَنْ")} {w("يُحِبُّ")} {w("الهَنْدَسَةَ")} {w("يَدْرُسُ")} {w("فِي")} {w("كُلِّيَّةِ", "الكُلِّيَّةُ")} {w("الهَنْدَسَةِ")}. {w("وَهُنَاكَ")} {w("أَيْضًا")} {w("كُلِّيَّةُ", "الكُلِّيَّةُ")} {w("التَّرْبِيَةِ")} {w("وَكُلِّيَّةُ", "الكُلِّيَّةُ")} {w("الشَّرِيعَةِ")}. {w("يَخْتَارُ", "اِخْتَارَ - يَخْتَارُ")} {w("الطُّلَّابُ", "الطُّلَّابُ")} {w("هَذِهِ")} {w("الكُلِّيَّاتِ", "الكُلِّيَّةُ")} {w("لِأَنَّهُمْ")} {w("يُرِيدُونَ")} {w("أَنْ")} {w("يَتَعَلَّمُوا")} {w("وَيُفِيدُوا", "أَفَادَ - يُفِيدُ")} {w("المُجْتَمَعَ", "المُجْتَمَعُ")}.
    """
    st.markdown(f'<div class="arabic-text">{p2_html}</div>', unsafe_allow_html=True)

    # Paragraf 3
    st.markdown('<div class="arabic-title">الفقرة الثالثة: الحَيَاةُ الجَامِعِيَّةُ وَالدِّرَاسَةُ</div>', unsafe_allow_html=True)
    p3_html = f"""
    {w("فِي")} {w("الجَامِعَةِ", "الجَامِعَةُ")}، {w("يَحْضُرُ")} {w("الطُّلَّابُ", "الطُّلَّابُ")} {w("الدُّرُوسَ")} {w("فِي")} {w("الفَصْلِ")} {w("مَعَ")} {w("الأُسْتَاذِ", "الأُسْتَاذُ")}. {w("وَيَذْهَبُونَ")} {w("إِلَى")} {w("المَكْتَبَةِ", "المَكْتَبَةُ")} {w("لِلْقِرَاءَةِ")} {w("وَالبَحْثِ")} {w("عَنِ")} {w("المَعْلُومَاتِ")}. {w("كَمَا")} {w("يَتَعَلَّمُونَ")} {w("مِنْ")} {w("خِلَالِ")} {w("المُنَاقَشَةِ")} {w("مَعَ")} {w("الأَسَاتِذَةِ", "الأُسْتَاذُ")} {w("وَالأَصْدِقَاءِ")}. {w("وَيَسْتَخْدِمُونَ")} {w("طُرُقًا")} {w("حَدِيثَةً")} {w("فِي")} {w("التَّعَلُّمِ")} {w("لِكَيْ")} {w("يَكُونُوا")} {w("مُسْتَعِدِّينَ", "اِسْتَعَدَّ - يَسْتَعِدُّ")} {w("لِلْعَمَلِ")} {w("فِي")} {w("المُسْتَقْبَلِ", "المُسْتَقْبَلُ")}.
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
