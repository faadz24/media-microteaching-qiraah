import streamlit as st
from gtts import gTTS
import io

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Smart Qira'ah Reader: Ad-Dirasah fil Jamiah",
    page_icon="🎓",
    layout="wide"
)

# 2. Manajemen Navigasi Halaman & State Evaluasi
if "page" not in st.session_state:
    st.session_state.page = "opening"
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# 3. Injeksi CSS Utama
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
        margin-bottom: 20px;
    }
    
    /* STYLE HERO / BANNER OPENING */
    .opening-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
        color: #ffffff;
        padding: 35px 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.25);
        margin-bottom: 30px;
        border: 2px solid #3b82f6;
        text-align: center;
    }
    .opening-arabic {
        font-family: 'Amiri', serif;
        font-size: 38px;
        font-weight: bold;
        direction: rtl;
        color: #fde047;
        margin-bottom: 15px;
        line-height: 1.5;
    }
    .opening-indo {
        font-size: 18px;
        line-height: 1.7;
        color: #f1f5f9;
        max-width: 850px;
        margin: 0 auto;
    }
    
    .feature-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    /* STYLE BACAAN TEKS ARAB */
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
        line-height: 2.6;
        direction: rtl;
        text-align: right;
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-right: 6px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* GAYA KATA TARGET & PENDUKUNG */
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
        padding: 0 3px;
        border-bottom: 1px dotted #94a3b8;
    }
    .vocab-regular:hover {
        background-color: #e2e8f0;
        border-radius: 4px;
        color: #1e3a8a;
    }

    /* TOOLTIP / POP-UP FLOATING BOX */
    .tooltip-box {
        visibility: hidden;
        width: 310px;
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

    /* EVALUASI SOAL STYLING & PENYESUAIAN FONT PILIHAN */
    .question-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px 25px;
        margin-top: 15px;
        margin-bottom: 12px;
        border-left: 6px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
    }
    .question-arabic {
        font-family: 'Amiri', serif;
        font-size: 26px;
        direction: rtl;
        text-align: right;
        color: #0f172a;
        font-weight: bold;
        margin-bottom: 10px;
        line-height: 1.8;
    }

    /* MEMBESARKAN FONT PILIHAN JAWABAN RADIO BUTTON STREAMLIT */
    div[role="radiogroup"] label p {
        font-family: 'Amiri', serif, sans-serif !important;
        font-size: 21px !important;
        line-height: 1.8 !important;
        color: #0f172a !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

DEFAULT_IMG = "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400"

# 4. Database Seluruh Kata
words_db = {
    # --- 17 TARGET MUFRODAT UTAMA (PAKAI GAMBAR + CTL) ---
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

    # --- KATA PENDUKUNG LAINNYA (TANPA GAMBAR) ---
    "بَعْدَ": {"type": "regular", "indo": "Setelah", "gram": "Zaraf Zaman (Keterangan Waktu)", "ar_ex": "نَلْتَقِي بَعْدَ الصَّلَاةِ.", "id_ex": "Kita bertemu setelah shalat."},
    "التَّخَرُّجِ": {"type": "regular", "indo": "Kelulusan / Wisuda", "gram": "Isim Masdar", "ar_ex": "اِحْتَفَلَ الطُّلَّابُ بِالتَّخَرُّجِ.", "id_ex": "Para siswa merayakan kelulusan."},
    "مِنَ": {"type": "regular", "indo": "Dari", "gram": "Harf Jar", "ar_ex": "خَرَجَ الطَّالِبُ مِنَ الفَصْلِ.", "id_ex": "Siswa itu keluar dari kelas."},
    "الثَّانَوِيَّةِ": {"type": "regular", "indo": "Tingkat Menengah / Aliyah", "gram": "Kata Sifat (Na'at)", "ar_ex": "دَرَسْتُ فِي المَدْرَسَةِ الثَّانَوِيَّةِ.", "id_ex": "Saya belajar di madrasah aliyah."},
    "الإِسْلَامِيَّةِ": {"type": "regular", "indo": "Islam / Keislaman", "gram": "Kata Sifat (Na'at)", "ar_ex": "تِلْكَ المَدْرَسَةُ إِسْلَامِيَّةٌ.", "id_ex": "Sekolah itu bernuansa islami."},
    "يُرِيدُ": {"type": "regular", "indo": "Ingin / Menghendaki", "gram": "Fi'il Mudhari'", "ar_ex": "يُرِيدُ الطَّالِبُ أَنْ يَنْجَحَ.", "id_ex": "Siswa itu ingin sukses."},
    "كَثِيرٌ": {"type": "regular", "indo": "Banyak", "gram": "Isim Sifat", "ar_ex": "فِي المَكْتَبَةِ كُتُبٌ كَثِيرَةٌ.", "id_ex": "Di perpustakaan ada banyak buku."},
    "أَنْ": {"type": "regular", "indo": "Bahwa / Untuk", "gram": "Harf Nashab", "ar_ex": "أُرِيدُ أَنْ أَتَعَلَّمَ العَرَبِيَّةَ.", "id_ex": "Saya ingin belajar bahasa Arab."},
    "يَدْرُسُوا": {"type": "regular", "indo": "Belajar / Berkuliah", "gram": "Fi'il Mudhari' Jamak", "ar_ex": "يُرِيدُ الطُّلَّابُ أَنْ يَدْرُسُوا بِنَشَاطٍ.", "id_ex": "Para siswa ingin belajar dengan giat."},
    "فِي": {"type": "regular", "indo": "Di / Di dalam", "gram": "Harf Jar", "ar_ex": "الأُسْتَاذُ فِي الفَصْلِ.", "id_ex": "Dosen ada di dalam kelas."},
    "يَذْهَبُ": {"type": "regular", "indo": "Pergi / Berangkat", "gram": "Fi'il Mudhari'", "ar_ex": "يَذْهَبُ الطَّالِبُ إِلَى المَدْرَسَةِ.", "id_ex": "Siswa itu pergi ke sekolah."},
    "إِلَى": {"type": "regular", "indo": "Ke / Kepada", "gram": "Harf Jar", "ar_ex": "سَافَرَ الأُسْتَاذُ إِلَى المَدِينَةِ.", "id_ex": "Dosen itu bepergian ke kota."},
    "وَتَقْدِيمِ": {"type": "regular", "indo": "Dan menyerahkan / mengajukan", "gram": "Harf Athaf + Masdar", "ar_ex": "يَجِبُ تَقْدِيمُ الأَوْرَاقِ فَوْرًا.", "id_ex": "Penyerahan berkas harus dilakukan segera."},
    "الأَوْرَاقِ": {"type": "regular", "indo": "Berkas-berkas / Dokumen", "gram": "Isim Jamak Taksir", "ar_ex": "قَدَّمَ الطَّالِبُ الأَوْرَاقَ المَطْلُوبَةَ.", "id_ex": "Siswa menyerahkan berkas-berkas yang diminta."},
    "يَتَعَلَّمُ": {"type": "regular", "indo": "Belajar / Mempelajari", "gram": "Fi'il Mudhari'", "ar_ex": "يَتَعَلَّمُ الطَّالِبُ اللُّغَةَ العَرَبِيَّةَ.", "id_ex": "Siswa itu mempelajari bahasa Arab."},
    "أَشْيَاءَ": {"type": "regular", "indo": "Hal-hal / Sesuatu", "gram": "Isim Jamak", "ar_ex": "تَعَلَّمْتُ أَشْيَاءَ مُفِيدَةً.", "id_ex": "Saya mempelajari hal-hal yang bermanfaat."},
    "جَدِيدَةً": {"type": "regular", "indo": "Baru", "gram": "Na'at / Kata Sifat", "ar_ex": "اشْتَرَيْتُ كُتُبًا جَدِيدَةً.", "id_ex": "Saya membeli buku-buku baru."},
    "كَمَا": {"type": "regular", "indo": "Sebagaimana / Juga", "gram": "Harf Sambung", "ar_ex": "يَقْرَأُ الطَّالِبُ كَمَا يَكْتُبُ.", "id_ex": "Siswa itu membaca sebagaimana ia menulis."},
    "يَتَعَلَّمُونَ": {"type": "regular", "indo": "Mereka belajar", "gram": "Fi'il Mudhari' Jamak", "ar_ex": "الطُّلَّابُ يَتَعَلَّمُونَ بِنَشَاطٍ.", "id_ex": "Para siswa belajar dengan aktif."},
    "عَلَى": {"type": "regular", "indo": "Atas / Pada", "gram": "Harf Jar", "ar_ex": "الكِتَابُ عَلَى المَكْتَبِ.", "id_ex": "Buku itu ada di atas meja."},
    "أَنْفُسِهِمْ": {"type": "regular", "indo": "Diri mereka sendiri", "gram": "Isim + Dhamir (Kemandirian)", "ar_ex": "يَعْتَمِدُ الطُّلَّابُ عَلَى أَنْفُسِهِمْ.", "id_ex": "Para siswa mengandalkan diri mereka sendiri."},
    "كُلُّ": {"type": "regular", "indo": "Setiap / Masing-masing", "gram": "Isim Mudhaf", "ar_ex": "كُلُّ طَالِبٍ يَحْضُرُ فِي الفَصْلِ.", "id_ex": "Setiap siswa hadir di kelas."},
    "طَالِبٍ": {"type": "regular", "indo": "Siswa / Pelajar", "gram": "Isim Mufrad (Tunggal)", "ar_ex": "هَذَا طَالِبٌ مُجْتَهِدٌ.", "id_ex": "Ini adalah siswa yang rajin."},
    "الَّذِي": {"type": "regular", "indo": "Yang", "gram": "Isim Maushul (Kata Hubung)", "ar_ex": "هَذَا هُوَ الأُسْتَاذُ الَّذِي يَدْرُسُنَا.", "id_ex": "Ini adalah dosen yang mengajar kami."},
    "يُحِبُّهُ": {"type": "regular", "indo": "Ia menyukainya", "gram": "Fi'il Mudhari' + Dhamir", "ar_ex": "هَذَا قِسْمٌ يُحِبُّهُ الطَّالِبُ.", "id_ex": "Ini adalah jurusan yang disukai siswa."},
    "يُنَاسِبُهُ": {"type": "regular", "indo": "Sesuai / Cocok baginya", "gram": "Fi'il Mudhari' + Dhamir", "ar_ex": "اخْتَارَ التَّخَصُّصَ الَّذِي يُنَاسِبُهُ.", "id_ex": "Ia memilih jurusan yang sesuai baginya."},
    "مَنْ": {"type": "regular", "indo": "Barangsiapa / Siapa yang", "gram": "Isim Syarat / Maushul", "ar_ex": "مَنْ يَجْتَهِدْ يَنْجَحْ.", "id_ex": "Barangsiapa bersungguh-sungguh maka ia sukses."},
    "يُحِبُّ": {"type": "regular", "indo": "Menyukai", "gram": "Fi'il Mudhari'", "ar_ex": "يُحِبُّ الطَّالِبُ القِرَاءَةَ.", "id_ex": "Siswa itu menyukai membaca."},
    "الطِّبَّ": {"type": "regular", "indo": "Kedokteran / Ilmu Medis", "gram": "Isim Jurusan", "ar_ex": "يَدْرُسُ أَحْمَدُ الطِّبَّ.", "id_ex": "Ahmad belajar ilmu kedokteran."},
    "يَدْرُسُ": {"type": "regular", "indo": "Belajar / Berkuliah", "gram": "Fi'il Mudhari'", "ar_ex": "يَدْرُسُ الطَّالِبُ فِي الفَصْلِ.", "id_ex": "Siswa itu belajar di kelas."},
    "الطِّبِّ": {"type": "regular", "indo": "Kedokteran", "gram": "Isim Mudhaf Ilaih", "ar_ex": "تَخَرَّجَ مِنْ كُلِّيَّةِ الطِّبِّ.", "id_ex": "Ia lulus dari Fakultas Kedokteran."},
    "الهَنْدَسَةَ": {"type": "regular", "indo": "Teknik / Rekayasa", "gram": "Isim Jurusan", "ar_ex": "يُحِبُّ زَيْدٌ الهَنْدَسَةَ.", "id_ex": "Zaid menyukai bidang teknik."},
    "الهَنْدَسَةِ": {"type": "regular", "indo": "Teknik", "gram": "Isim Jurusan", "ar_ex": "يَدْرُسُ فِي كُلِّيَّةِ الهَنْدَسَةِ.", "id_ex": "Ia belajar di Fakultas Teknik."},
    "وَهُنَاكَ": {"type": "regular", "indo": "Dan di sana / Terdapat juga", "gram": "Isim Isyarah", "ar_ex": "وَهُنَاكَ كُلِّيَّاتٌ كَثِيرَةٌ.", "id_ex": "Dan di sana terdapat banyak fakultas."},
    "أَيْضًا": {"type": "regular", "indo": "Juga / Pula", "gram": "Maf'ul Mutlaq", "ar_ex": "أَنَا طَالِبٌ أَيْضًا.", "id_ex": "Saya juga seorang siswa."},
    "التَّرْبِيَةِ": {"type": "regular", "indo": "Pendidikan / Tarbiyah", "gram": "Isim Fakultas", "ar_ex": "يَدْرُسُ فِي كُلِّيَّةِ التَّرْبِيَةِ.", "id_ex": "Ia belajar di Fakultas Pendidikan (Tarbiyah)."},
    "الشَّرِيعَةِ": {"type": "regular", "indo": "Syariah / Hukum Islam", "gram": "Isim Fakultas", "ar_ex": "يَدْرُسُ الفِقْهَ فِي كُلِّيَّةِ الشَّرِيعَةِ.", "id_ex": "Ia belajar fikih di Fakultas Syariah."},
    "هَذِهِ": {"type": "regular", "indo": "Ini (Kata Tunjuk)", "gram": "Isim Isyarah", "ar_ex": "هَذِهِ جَامِعَةٌ مَشْهُورَةٌ.", "id_ex": "Ini adalah universitas yang terkenal."},
    "الكُلِّيَّاتِ": {"type": "regular", "indo": "Fakultas-fakultas", "gram": "Isim Jamak Muannats", "ar_ex": "تَضُمُّ الجَامِعَةُ هَذِهِ الكُلِّيَّاتِ.", "id_ex": "Universitas itu mencakup fakultas-fakultas ini."},
    "لِأَنَّهُمْ": {"type": "regular", "indo": "Karena mereka", "gram": "Harf Sababiyah + Dhamir", "ar_ex": "يَجْتَهِدُونَ لِأَنَّهُمْ يُرِيدُونَ النَّجَاحَ.", "id_ex": "Mereka bersungguh-sungguh karena menginginkan kelulusan."},
    "يُرِيدُونَ": {"type": "regular", "indo": "Mereka ingin / bertekad", "gram": "Fi'il Mudhari' Jamak", "ar_ex": "الطُّلَّابُ يُرِيدُونَ التَّفَوُّقَ.", "id_ex": "Para siswa ingin meraih prestasi."},
    "يَتَعَلَّمُوا": {"type": "regular", "indo": "Agar mereka belajar", "gram": "Fi'il Mudhari' Manshub", "ar_ex": "يَذْهَبُونَ لِكَيْ يَتَعَلَّمُوا.", "id_ex": "Mereka pergi supaya mereka belajar."},
    "يَحْضُرُ": {"type": "regular", "indo": "Menghadiri / Mengikuti", "gram": "Fi'il Mudhari'", "ar_ex": "يَحْضُرُ الطَّالِبُ فِي الوَقْتِ المُنَاسِبِ.", "id_ex": "Siswa hadir pada waktu yang tepat."},
    "الدُّرُوسَ": {"type": "regular", "indo": "Pelajaran-pelajaran / Perkuliahan", "gram": "Isim Jamak Taksir", "ar_ex": "يَفْهَمُ الطَّالِبُ الدُّرُوسَ جَيِّدًا.", "id_ex": "Siswa paham pelajaran-pelajaran dengan baik."},
    "الفَصْلِ": {"type": "regular", "indo": "Ruang Kelas", "gram": "Isim Tempat", "ar_ex": "يَجْلِسُ الطُّلَّابُ فِي الفَصْلِ.", "id_ex": "Para siswa duduk di ruang kelas."},
    "مَعَ": {"type": "regular", "indo": "Bersama / Dengan", "gram": "Zaraf Makan", "ar_ex": "يَتَنَاقَشُ الطَّالِبُ مَعَ الأُسْتَاذِ.", "id_ex": "Siswa berdiskusi bersama dosen."},
    "وَيَذْهَبُونَ": {"type": "regular", "indo": "Dan mereka pergi", "gram": "Fi'il Mudhari' Jamak", "ar_ex": "وَيَذْهَبُونَ إِلَى المَكْتَبَةِ كُلَّ يَوْمٍ.", "id_ex": "Dan mereka pergi ke perpustakaan setiap hari."},
    "لِلْقِرَاءَةِ": {"type": "regular", "indo": "Untuk membaca", "gram": "Harf Jar + Masdar", "ar_ex": "يَذْهَبُ إِلَى المَكْتَبَةِ لِلْقِرَاءَةِ.", "id_ex": "Ia pergi ke perpustakaan untuk membaca."},
    "وَالبَحْثِ": {"type": "regular", "indo": "Dan meriset / mencari data", "gram": "Isim Masdar", "ar_ex": "يَقُومُ الطُّلَّابُ بِالقِرَاءَةِ وَالبَحْثِ.", "id_ex": "Para siswa melakukan pembacaan dan penelitian."},
    "عَنِ": {"type": "regular", "indo": "Tentang / Dari", "gram": "Harf Jar", "ar_ex": "يَبْحَثُ الطَّالِبُ عَنِ المَعْلُومَاتِ.", "id_ex": "Siswa mencari informasi."},
    "المَعْلُومَاتِ": {"type": "regular", "indo": "Informasi / Data", "gram": "Isim Jamak Muannats", "ar_ex": "يَجْمَعُ الطَّالِبُ المَعْلُومَاتِ المَفِيدَةَ.", "id_ex": "Siswa mengumpulkan informasi yang berguna."},
    "مِنْ": {"type": "regular", "indo": "Dari / Melalui", "gram": "Harf Jar", "ar_ex": "تَعَلَّمْتُ الكَثِيرَ مِنْ الأُسْتَاذِ.", "id_ex": "Saya belajar banyak hal dari dosen."},
    "خِلَالِ": {"type": "regular", "indo": "Melalui / Sela-sela", "gram": "Zaraf", "ar_ex": "نَتَعَلَّمُ مِنْ خِلَالِ المُنَاقَشَةِ.", "id_ex": "Kita belajar melalui diskusi."},
    "المُنَاقَشَةِ": {"type": "regular", "indo": "Diskusi / Tanya Jawab", "gram": "Isim Masdar", "ar_ex": "جَرَتْ المُنَاقَشَةُ بِبَالِغِ الاِهْتِمَامِ.", "id_ex": "Diskusi berlangsung dengan penuh perhatian."},
    "الأَسَاتِذَةِ": {"type": "regular", "indo": "Para Dosen / Pengajar", "gram": "Isim Jamak dari Ustadz", "ar_ex": "يَحْتَرِمُ الطُّلَّابُ الأَسَاتِذَةَ.", "id_ex": "Para siswa menghormati para dosen."},
    "وَالأَصْدِقَاءِ": {"type": "regular", "indo": "Dan teman-teman", "gram": "Isim Jamak Taksir", "ar_ex": "يَتَكَلَّمُ الطَّالِبُ مَعَ الأَصْدِقَاءِ.", "id_ex": "Siswa berbicara bersama teman-teman."},
    "وَيَسْتَخْدِمُونَ": {"type": "regular", "indo": "Dan mereka menggunakan", "gram": "Fi'il Mudhari' Jamak", "ar_ex": "وَيَسْتَخْدِمُونَ الحَاسُوبَ فِي الدِّرَاسَةِ.", "id_ex": "Dan mereka menggunakan komputer dalam belajar."},
    "طُرُقًا": {"type": "regular", "indo": "Metode-metode / Cara", "gram": "Isim Jamak", "ar_ex": "يَتَّبِعُ الأُسْتَاذُ طُرُقًا حَدِيثَةً.", "id_ex": "Dosen menerapkan metode-metode modern."},
    "حَدِيثَةً": {"type": "regular", "indo": "Modern / Terbaru", "gram": "Na'at / Kata Sifat", "ar_ex": "يَسْتَخْدِمُونَ وَسَائِلَ حَدِيثَةً.", "id_ex": "Mereka menggunakan media modern."},
    "التَّعَلُّمِ": {"type": "regular", "indo": "Pembelajaran / Studi", "gram": "Isim Masdar", "ar_ex": "التَّعَلُّمُ عَمَلِيَّةٌ مُسْتَمِرَّةٌ.", "id_ex": "Pembelajaran adalah proses yang berkelanjutan."},
    "لِكَيْ": {"type": "regular", "indo": "Supaya / Agar", "gram": "Harf Nashab", "ar_ex": "ادْرُسْ جَيِّدًا لِكَيْ تَنْجَحَ.", "id_ex": "Belajarlah dengan baik agar kamu lulus."},
    "يَكُونُوا": {"type": "regular", "indo": "Agar mereka menjadi", "gram": "Fi'il Mudhari' Naqis", "ar_ex": "يَتَعَلَّمُونَ لِكَيْ يَكُونُوا نَاجِحِينَ.", "id_ex": "Mereka belajar agar menjadi orang-orang sukses."},
    "مُسْتَعِدِّينَ": {"type": "regular", "indo": "Siap sedia", "gram": "Khabar Kana (Jamak)", "ar_ex": "الطُّلَّابُ مُسْتَعِدُّونَ لِلْعَمَلِ.", "id_ex": "Para siswa siap untuk bekerja."},
    "لِلْعَمَلِ": {"type": "regular", "indo": "Untuk bekerja", "gram": "Harf Jar + Masdar", "ar_ex": "يَسْتَعِدُّ الخِرِّيجُونَ لِلْعَمَلِ.", "id_ex": "Para lulusan bersiap untuk bekerja."}
}

# 5. Database 20 Soal Pilihan Ganda & Kunci Jawaban
quiz_data = [
    {
        "id": 1,
        "q": "مَا الْفِكْرَةُ الرَّئِيسَةُ الَّتِي تَجْمَعُ الْفَقَرَاتِ الثَّلَاثَ؟",
        "opts": {"A": "أَهَمِّيَّةُ التَّعْلِيمِ فِي الْمَدْرَسَةِ الثَّانَوِيَّةِ", "B": "مَرَاحِلُ الدِّرَاسَةِ وَالْحَيَاةُ فِي الْجَامِعَةِ", "C": "أَنْوَاعُ الْكُلِّيَّاتِ فِي الْجَامِعَةِ", "D": "دَوْرُ الْأُسْتَاذِ فِي تَعْلِيمِ الطُّلَّابِ", "E": "أَهَمِّيَّةُ الْعَمَلِ بَعْدَ التَّخَرُّجِ"},
        "key": "B"
    },
    {
        "id": 2,
        "q": "لِمَاذَا يَذْهَبُ الطُّلَّابُ إِلَى الْجَامِعَةِ بَعْدَ التَّخَرُّجِ مِنَ الْمَدْرَسَةِ؟",
        "opts": {"A": "لِلْعَمَلِ فِي الْمُؤَسَّسَاتِ الْحُكُومِيَّةِ", "B": "لِلْبَحْثِ عَنِ الْأَصْدِقَاءِ الْجُدُدِ", "C": "لِلتَّسْجِيلِ وَتَقْدِيمِ الْأَوْرَاقِ وَمُوَاصَلَةِ التَّعْلِيمِ", "D": "لِاخْتِيَارِ الْمَدْرَسَةِ الثَّانَوِيَّةِ", "E": "لِلْحُصُولِ عَلَى وَظِيفَةٍ فَوْرًا"},
        "key": "C"
    },
    {
        "id": 3,
        "q": "مَا الْمَقْصُودُ بِعِبَارَةِ «يَعْتَمِدُوا عَلَى أَنْفُسِهِمْ» فِي الْفَقَرَةِ الْأُولَى؟",
        "opts": {"A": "أَنْ يَعِيشُوا بَعِيدًا عَنْ أُسَرِهِمْ دَائِمًا", "B": "أَنْ يَتَّخِذُوا قَرَارَاتِهِمْ وَيَتَحَمَّلُوا مَسْؤُولِيَّاتِهِمْ", "C": "أَنْ يَتَوَقَّفُوا عَنِ التَّعَلُّمِ مِنَ الْأَسَاتِذَةِ", "D": "أَنْ يَدْرُسُوا دُونَ الْحَاجَةِ إِلَى الْكُتُبِ", "E": "أَنْ يَعْمَلُوا دُونَ مُسَاعَدَةِ الْمُجْتَمَعِ"},
        "key": "B"
    },
    {
        "id": 4,
        "q": "مَا الْعَلَاقَةُ بَيْنَ اخْتِيَارِ الْقِسْمِ وَالْإِفَادَةِ لِلْمُجْتَمَعِ؟",
        "opts": {"A": "لَا عَلاقَةَ بَيْنَهُمَا", "B": "اخْتِيَارُ الْقِسْمِ يَهْدِفُ إِلَى تَجَنُّبِ الْعَمَلِ", "C": "يَخْتَارُ الطَّالِبُ تَخَصُّصًا يُنَاسِبُ مَيْلَهُ وَيُمَكِّنُهُ مِنْ خِدْمَةِ الْمُجْتَمَعِ", "D": "الْمُجْتَمَعُ هُوَ الَّذِي يَخْتَارُ الْقِسْمَ بَدَلًا مِنَ الطَّالِبِ", "E": "اخْتِيَارُ الْقِسْمِ يَعْتَمِدُ عَلَى رَغْبَةِ الْأُسْتَاذِ فَقَطْ"},
        "key": "C"
    },
    {
        "id": 5,
        "q": "إِذَا كَانَ الطَّالِبُ يُحِبُّ الْعُلُومَ الصِّحِّيَّةَ وَعِلَاجَ الْمَرْضَى، فَأَيُّ اخْتِيَارٍ يُنَاسِبُهُ وَفْقًا لِلنَّصِّ؟",
        "opts": {"A": "كُلِّيَّةُ الْهَنْدَسَةِ", "B": "كُلِّيَّةُ التَّرْبِيَةِ", "C": "كُلِّيَّةُ الشَّرِيعَةِ", "D": "كُلِّيَّةُ الطِّبِّ", "E": "قِسْمُ الْمَعْلُومَاتِ"},
        "key": "D"
    },
    {
        "id": 6,
        "q": "مَاذَا يُمْكِنُ أَنْ نَسْتَنْتِجَ مِنْ تَكْرَارِ فِعْلِ «يَتَعَلَّمُ» وَمُشْتَقَّاتِهِ فِي النَّصِّ؟",
        "opts": {"A": "أَنَّ الْجَامِعَةَ مَكَانٌ لِلتَّعَلُّمِ الْمُسْتَمِرِّ وَتَطْوِيرِ الْمَهَارَاتِ", "B": "أَنَّ الطُّلَّابَ يَدْرُسُونَ لِاجْتِيَازِ الِامْتِحَانِ فَقَطْ", "C": "أَنَّ التَّعَلُّمَ يَنْتَهِي بَعْدَ اخْتِيَارِ الْكُلِّيَّةِ", "D": "أَنَّ الْجَامِعَةَ تُرَكِّزُ عَلَى الْعَمَلِ دُونَ الدِّرَاسَةِ", "E": "أَنَّ الطُّلَّابَ لَا يَحْتَاجُونَ إِلَى الْمَعْرِفَةِ الْجَدِيدَةِ"},
        "key": "A"
    },
    {
        "id": 7,
        "q": "مَا الْفَرْقُ الْأَسَاسِيُّ بَيْنَ الْفَقَرَةِ الْأُولَى وَالثَّانِيَةِ؟",
        "opts": {"A": "الْأُولَى تَتَحَدَّثُ عَنِ الْمَكْتَبَةِ وَالثَّانِيَةُ عَنِ الْفَصْلِ", "B": "الْأُولَى تُبَيِّنُ الدُّخُولَ إِلَى الْجَامِعَةِ وَالثَّانِيَةُ تُرَكِّزُ عَلَى اخْتِيَارِ التَّخَصُّصِ", "C": "الْأُولَى عَنِ الْعَمَلِ وَالثَّانِيَةُ عَنِ السَّفَرِ", "D": "الْأُولَى عَنِ الْأَسَاتِذَةِ وَالثَّانِيَةُ عَنِ الْأَصْدِقَاءِ", "E": "كِلْتَاهُمَا تَتَحَدَّثَانِ عَنِ الِامْتِحَانَاتِ"},
        "key": "B"
    },
    {
        "id": 8,
        "q": "مَا الْمَعْنَى الْأَقْرَبُ لِكَلِمَةِ «يُنَاسِبُهُ» فِي الْفَقَرَةِ الثَّانِيَةِ؟",
        "opts": {"A": "يُعَارِضُهُ", "B": "يُجْبِرُهُ", "C": "يُلَائِمُهُ", "D": "يُبْعِدُهُ", "E": "يُهْمِلُهُ"},
        "key": "C"
    },
    {
        "id": 9,
        "q": "أَيُّ الْعِبَارَاتِ الْآتِيَةِ تُمَثِّلُ اسْتِنْتَاجًا مِنَ النَّصِّ وَلَيْسَتْ مَعْلُومَةً مَذْكُورَةً صَرَاحَةً؟",
        "opts": {"A": "يَذْهَبُ الطُّلَّابُ إِلَى الْجَامِعَةِ لِلتَّسْجِيلِ", "B": "يَتَعَلَّمُ الطُّلَّابُ أَشْيَاءَ جَدِيدَةً", "C": "يَسْتَخْدِمُ الطُّلَّابُ طُرُقًا حَدِيثَةً فِي التَّعَلُّمِ", "D": "يَحْتَاجُ الطَّالِبُ إِلَى تَحَمُّلِ الْمَسْؤُولِيَّةِ فِي حَيَاتِهِ الْجَامِعِيَّةِ", "E": "هُنَاكَ كُلِّيَّةُ الطِّبِّ وَالْهَنْدَسَةِ"},
        "key": "D"
    },
    {
        "id": 10,
        "q": "لِمَاذَا يَذْهَبُ الطُّلَّابُ إِلَى الْمَكْتَبَةِ حَسَبَ الْفَقَرَةِ الثَّالِثَةِ؟",
        "opts": {"A": "لِمُقَابَلَةِ أَصْحَابِ الْجَامِعَةِ فَقَطْ", "B": "لِلْقِرَاءَةِ وَالْبَحْثِ عَنِ الْمَعْلُومَاتِ", "C": "لِتَقْدِيمِ أَوْرَاقِ التَّسْجِيلِ", "D": "لِحُضُورِ الدُّرُوسِ مَعَ الْأُسْتَاذِ", "E": "لِاخْتِيَارِ الْكُلِّيَّةِ"},
        "key": "B"
    },
    {
        "id": 11,
        "q": "مَا الَّذِي يُمَيِّزُ التَّعَلُّمَ فِي الْفَقَرَةِ الثَّالِثَةِ؟",
        "opts": {"A": "الِاعْتِمَادُ عَلَى الْحِفْظِ فَقَطْ", "B": "الِاعْتِمَادُ عَلَى الْمُحَاضَرَاتِ دُونَ الْمُنَاقَشَةِ", "C": "تَنَوُّعُ مَصَادِرِ التَّعَلُّمِ وَطُرُقِهِ", "D": "الِاعْتِمَادُ عَلَى الْمَكْتَبَةِ دُونَ الْأُسْتَاذِ", "E": "تَرْكُ اسْتِخْدَامِ الْمَعْلُومَاتِ الْحَدِيثَةِ"},
        "key": "C"
    },
    {
        "id": 12,
        "q": "مَا وَظِيفَةُ الْعِبَارَةِ «لِكَيْ يَكُونُوا مُسْتَعِدِّينَ لِلْعَمَلِ فِي الْمُسْتَقْبَلِ»؟",
        "opts": {"A": "بَيَانُ سَبَبِ اسْتِخْدَامِ الطُّرُقِ الْحَدِيثَةِ", "B": "ذِكْرُ مَكَانِ الدِّرَاسَةِ", "C": "بَيَانُ نَوْعِ الْكُلِّيَّةِ", "D": "وَصْفُ وَقْتِ التَّسْجِيلِ", "E": "ذِكْرُ شَرْطِ دُخُولِ الْمَكْتَبَةِ"},
        "key": "A"
    },
    {
        "id": 13,
        "q": "إِذَا كَانَ الطَّالِبُ يَحْضُرُ الدُّرُوسَ وَلَكِنَّهُ لَا يَبْحَثُ وَلَا يُنَاقِشُ، فَأَيُّ جَانِبٍ مِنَ التَّعَلُّمِ لَمْ يُطَبِّقْهُ كَامِلًا؟",
        "opts": {"A": "التَّسْجِيلَ وَتَقْدِيمَ الْأَوْرَاقِ", "B": "اخْتِيَارَ الْكُلِّيَّةِ", "C": "الِاعْتِمَادَ عَلَى النَّفْسِ فَقَطْ", "D": "تَنَوُّعَ أَنْشِطَةِ التَّعَلُّمِ وَالْمُشَارَكَةَ فِيهَا", "E": "التَّخَرُّجَ مِنَ الْمَدْرَسَةِ"},
        "key": "D"
    },
    {
        "id": 14,
        "q": "مَا الْمَعْنَى الْأَقْرَبُ لِكَلِمَةِ «الْمُسْتَقْبَلِ» فِي النَّصِّ؟",
        "opts": {"A": "الْمَاضِي", "B": "الْحَاضِر", "C": "الزَّمَنُ الْقَادِمُ", "D": "الْوَقْتُ الْقَصِيرُ", "E": "الْوَقْتُ الْمَجْهُولُ"},
        "key": "C"
    },
    {
        "id": 15,
        "q": "مَا الْعَلَاقَةُ بَيْنَ الْفِقْرَةِ الثَّانِيَةِ وَالْفِقْرَةِ الثَّالِثَةِ؟",
        "opts": {"A": "الثَّانِيَةُ تَعْرِضُ اخْتِيَارَ التَّخَصُّصِ وَالثَّالِثَةُ تَعْرِضُ كَيْفِيَّةَ الدِّرَاسَةِ فِيهِ", "B": "الثَّانِيَةُ تَعْرِضُ التَّسْجِيلَ وَالثَّالِثَةُ تَعْرِضُ التَّخَرُّجَ", "C": "الثَّانِيَةُ تَعْرِضُ الْعَمَلَ وَالثَّالِثَةُ تَعْرِضُ الْبَطَالَةَ", "D": "الثَّانِيَةُ تَعْرِضُ الْمَاضِيَ وَالثَّالِثَةُ تَعْرِضُ الْحَاضِرَ", "E": "لَا تُوجَدُ عَلاقَةٌ مَعْنَوِيَّةٌ بَيْنَهُمَا"},
        "key": "A"
    },
    {
        "id": 16,
        "q": "مَا الَّذِي يُمْكِنُ أَنْ يَحْدُثَ إِذَا لَمْ يَخْتَرِ الطَّالِبُ قِسْمًا يُنَاسِبُ مَيْلَهُ؟",
        "opts": {"A": "سَيَتَعَلَّمُ بِطَرِيقَةٍ أَفْضَلَ حَتْمًا", "B": "قَدْ يَجِدُ صُعُوبَةً فِي الِاسْتِمْرَارِ وَتَحْقِيقِ أَهْدَافِهِ", "C": "سَيَحْصُلُ عَلَى وَظِيفَةٍ دُونَ دِرَاسَةٍ", "D": "سَيُصْبِحُ أُسْتَاذًا فِي الْجَامِعَةِ", "E": "لَنْ يَحْتَاجَ إِلَى اخْتِيَارِ كُلِّيَّةٍ"},
        "key": "B"
    },
    {
        "id": 17,
        "q": "أَيُّ الْعَنَاوِينِ الْآتِيَةِ أَكْثَرُ شُمُولًا لِلْفَقَرَاتِ الثَّلَاثِ؟",
        "opts": {"A": "أَنْوَاعُ الْمَكْتَبَاتِ الْجَامِعِيَّةِ", "B": "دَوْرُ الْأُسْتَاذِ فِي التَّدْرِيسِ", "C": "اخْتِيَارُ كُلِّيَّةِ الطِّبِّ", "D": "رِحْلَةُ الطَّالِبِ فِي التَّعْلِيمِ الْجَامِعِيِّ", "E": "طُرُقُ التَّسْجِيلِ فِي الْجَامِعَةِ"},
        "key": "D"
    },
    {
        "id": 18,
        "q": "أَيُّ الْعِبَارَاتِ الْآتِيَةِ تَتَّفِقُ مَعَ مَضْمُونِ النَّصِّ؟",
        "opts": {"A": "النَّجَاحُ الْجَامِعِيُّ يَعْتَمِدُ عَلَى الْحُضُورِ فِي الْفَصْلِ فَقَطْ", "B": "اخْتِيَارُ الْكُلِّيَّةِ لَا يَحْتَاجُ إِلَى مُرَاعَاةِ مَيْلِ الطَّالِبِ", "C": "الْجَامِعَةُ تُسَاعِدُ الطُّلَّابَ عَلَى اكْتِسَابِ الْمَعْرِفَةِ وَالِاسْتِعْدَادِ لِلْمُسْتَقْبَلِ", "D": "الْمُنَاقَشَةُ مَعَ الْأَصْدِقَاءِ تُعَوِّضُ جَمِيعَ أَنْوَاعِ التَّعَلُّمِ", "E": "الْمَكْتَبَةُ مَكَانٌ لِلتَّسْجِيلِ فَقَطْ"},
        "key": "C"
    },
    {
        "id": 19,
        "q": "مَا الْعَلَاقَةُ بَيْنَ الِاسْتِقْلَالِيَّةِ فِي التَّعَلُّمِ وَالِاسْتِعْدَادِ لِلْمُسْتَقْبَلِ وَفْقًا لِلنَّصِّ؟",
        "opts": {"A": "الِاسْتِقْلَالِيَّةُ تَمْنَعُ الطَّالِبَ مِنَ التَّعَاوُنِ مَعَ الْآخَرِينَ", "B": "الِاسْتِقْلَالِيَّةُ وَاكْتِسَابُ الْمَعْرِفَةِ يُسَاعِدَانِ الطَّالِبَ عَلَى تَطْوِيرِ نَفْسِهِ وَالِاسْتِعْدَادِ لِلْحَيَاةِ الْعَمَلِيَّةِ", "C": "الِاسْتِعْدَادُ لِلْمُسْتَقْبَلِ يَعْتَمِدُ عَلَى اخْتِيَارِ الْكُلِّيَّةِ فَقَطْ", "D": "الِاسْتِقْلَالِيَّةُ تَعْنِي عَدَمَ الْحَاجَةِ إِلَى الْأَسَاتِذَةِ", "E": "التَّعَلُّمُ الْجَامِعِيُّ لَا يُسَاعِدُ عَلَى تَطْوِيرِ الْمَهَارَاتِ"},
        "key": "B"
    },
    {
        "id": 20,
        "q": "مَا الْخُلَاصَةُ الْأَدَقُّ الَّتِي يُمْكِنُ اسْتِنْتَاجُهَا مِنَ النَّصِّ كُلِّهِ؟",
        "opts": {"A": "الْحَيَاةُ الْجَامِعِيَّةُ تَقْتَصِرُ عَلَى اخْتِيَارِ الْكُلِّيَّةِ", "B": "التَّعْلِيمُ الْجَامِعِيُّ يَجْمَعُ بَيْنَ اخْتِيَارِ التَّخَصُّصِ وَاكْتِسَابِ الْمَعْرِفَةِ وَبِنَاءِ الِاسْتِقْلَالِيَّةِ وَالِاسْتِعْدَادِ لِلْمُسْتَقْبَلِ", "C": "الْجَامِعَةُ مَكَانٌ لِلْعَمَلِ دُونَ الدِّرَاسَةِ", "D": "الْمُهِمُّ فِي الْجَامِعَةِ هُوَ اخْتِيَارُ كُلِّيَّةٍ مَشْهُورَةٍ", "E": "يَتَعَلَّمُ الطُّلَّابُ مِنَ الْكُتُبِ فَقَطْ"},
        "key": "B"
    }
]

# Fungsi Builder Pop-Up Interaktif
def w(arabic_word, db_key=None):
    key = db_key if db_key else arabic_word
    info = words_db.get(key, {
        "type": "regular", 
        "indo": "Kata dalam teks", 
        "gram": "Kosa kata", 
        "ar_ex": "هَذِهِ كَلِمَةٌ فِي النَّصِّ.",
        "id_ex": "Ini adalah kata di dalam teks."
    })
    
    ar_ex = info.get("ar_ex", "هَذِهِ كَلِمَةٌ فِي النَّصِّ.")
    id_ex = info.get("id_ex", "Ini adalah kata di dalam teks.")

    if info["type"] == "target":
        img_url = info.get("img_url", DEFAULT_IMG)
        return f'''<span class="vocab-target">{arabic_word}<span class="tooltip-box"><img src="{img_url}" class="popup-img"><b style="font-size:17px; color:#38bdf8;">{key}</b><br><span style="color:#fde047; font-weight:bold;">{info['indo']}</span><br><div class="example-box"><b>📌 Contoh Kalimat:</b><br><span style="font-family:'Amiri'; font-size:16px;">{ar_ex}</span><br><i style="color:#cbd5e1; font-size:11px;">"{id_ex}"</i></div><div style="font-size:11px; margin-top:5px; color:#94a3b8;">{info['ctl']}</div></span></span>'''
    else:
        gram_info = f'<br><small style="color:#94a3b8;">({info.get("gram", "")})</small>' if "gram" in info else ""
        return f'''<span class="vocab-regular">{arabic_word}<span class="tooltip-box"><b style="font-size:16px; color:#38bdf8;">{arabic_word}</b><br><span style="color:#fde047; font-weight:bold;">{info['indo']}</span>{gram_info}<br><div class="example-box"><b>📌 Contoh Kalimat:</b><br><span style="font-family:'Amiri'; font-size:15px;">{ar_ex}</span><br><i style="color:#cbd5e1; font-size:11px;">"{id_ex}"</i></div></span></span>'''


# ==============================================================================
# HALAMAN 1: OPENING / WELCOME SCREEN
# ==============================================================================
if st.session_state.page == "opening":
    st.markdown('<h1 class="main-title">🎓 Smart Qira\'ah Reader</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Media Pembelajaran Maharah Qira\'ah Interaktif Berbasis CTL — Kelas 12 MA</p>', unsafe_allow_html=True)

    # Hero Welcome Banner
    st.markdown("""
    <div class="opening-card">
        <div class="opening-arabic">أَهْلًا وَسَهْلًا وَمَرْحَبًا بِكُمْ فِي تَطْبِيقِ "Smart Qira'ah Reader"! ✨</div>
        <div class="opening-indo">
            Media pembelajaran membaca bahasa Arab modern untuk membantu siswa kelas 12 MA memahami teks <b>"Ad-Dirasah fil Jamiah" (الدِّرَاسَةُ فِي الجَامِعَةِ)</b> secara kontekstual, visual, dan interaktif dalam rangka persiapan menuju Perguruan Tinggi Impian.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ringkasan Fitur Unggulan
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class="feature-card">
            <h4>💡 Pendekatan CTL</h4>
            <p style="font-size:14px; color:#475569;">Menghubungkan teks bacaan perkuliahan dengan realitas pendaftaran PTN/PTKIN & kemandirian siswa.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div class="feature-card">
            <h4>🖼️ Pop-up Visual Interaktif</h4>
            <p style="font-size:14px; color:#475569;">Sorot kata mana saja untuk memunculkan gambar visual, arti, contoh kalimat, dan tata bahasa.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_f3:
        st.markdown("""
        <div class="feature-card">
            <h4>🔊 Audio Pelafalan & Evaluasi</h4>
            <p style="font-size:14px; color:#475569;">Dilengkapi pemutar audio mufrodat di sidebar dan latihan 20 soal pilihan ganda interaktif.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tombol Utama Navigasi Halaman Depan
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 MULAI PEMBELAJARAN (ابدَأ الدِّرَاسَةَ)", use_container_width=True, type="primary"):
            st.session_state.page = "learning"
            st.rerun()


# ==============================================================================
# HALAMAN 2: MATERI PEMBELAJARAN & READER
# ==============================================================================
elif st.session_state.page == "learning":
    
    # Navigation Top Bar (Hanya Tombol Kembali & Mode Fokus)
    top_col1, top_col2 = st.columns([1.5, 2])
    with top_col1:
        if st.button("⬅️ Ke Halaman Utama"):
            st.session_state.page = "opening"
            st.rerun()
    with top_col2:
        focus_mode = st.toggle("📖 Mode Fokus Baca (Sembunyikan Pop-up)", value=False)

    st.markdown("---")

    if focus_mode:
        st.markdown("""
        <style>
            .tooltip-box { display: none !important; }
            .vocab-target, .vocab-regular {
                border-bottom: none !important;
                cursor: default !important;
                color: #0f172a !important;
                font-weight: normal !important;
                background-color: transparent !important;
            }
            .vocab-target:hover, .vocab-regular:hover { background-color: transparent !important; }
        </style>
        """, unsafe_allow_html=True)
        st.info("💡 **Mode Fokus Baca Aktif:** Teks dalam kondisi bersih tanpa garis bawah/pop-up untuk kelancaran siswa membaca di proyektor.")
    else:
        st.caption("👉 **Petunjuk Guru:** Klik/Sorot kata mana saja pada teks untuk melihat Gambar Visual, Arti, Contoh Kalimat, & CTL.")

    # SIDEBAR BANK MUFRODAT TARGET + FITUR AUDIO GTTS
    target_keys = [k for k, v in words_db.items() if v.get("type") == "target"]
    st.sidebar.header("📌 Bank 17 Kosa Kata Wajib")
    selected_word = st.sidebar.selectbox("Bedah Mufrodat Utama via Sidebar:", target_keys)

    if selected_word:
        info = words_db[selected_word]
        st.sidebar.image(info["img_url"], use_container_width=True)
        st.sidebar.markdown(f"### {selected_word}")
        
        # PEMUTAR AUDIO BEBAS BLOKIR VIA gTTS
        st.sidebar.markdown("🔊 **Pelafalan Audio (الاستماع):**")
        try:
            tts = gTTS(text=selected_word, lang='ar')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.sidebar.audio(fp, format='audio/mp3')
        except Exception:
            st.sidebar.warning("⚠️ Suara tidak dapat diputar saat offline.")
        
        st.sidebar.markdown(f"**Arti:** {info['indo']}")
        st.sidebar.markdown(f"**📌 Contoh Kalimat:**\n- {info['ar_ex']}\n  *( “{info['id_ex']}” )*")
        st.sidebar.info(info['ctl'])

    # Area Utama Teks Bacaan & Panel Diskusi
    col1, col2 = st.columns([2.2, 1])

    with col1:
        st.subheader("📖 Teks Bacaan (المَادَّةُ)")
        
        # Paragraf 1
        st.markdown('<div class="arabic-title">الفقرة الأولى: الدِّرَاسَةُ فِي الجَامِعَةِ</div>', unsafe_allow_html=True)
        p1_html = f"""
        {w("بَعْدَ")} {w("التَّخَرُّجِ")} {w("مِنَ")} {w("المَدْرَسَةِ", "المَدْرَسَةُ")} {w("الثَّانَوِيَّةِ")} {w("الإِسْلَامِيَّةِ")}، {w("يُرِيدُ")} {w("كَثِيرٌ")} {w("مِنَ")} {w("الطُّلَّابِ", "الطُّلَّابُ")} {w("أَنْ")} {w("يَدْرُسُوا")} {w("فِي")} {w("الجَامِعَةِ", "الجَامِعَةُ")}. {w("يَذْهَبُ")} {w("الطُّلَّابُ", "الطُّلَّابُ")} {w("إِلَى")} {w("الجَامِعَةِ", "الجَامِعَةُ")} {w("لِلتَّسْجِيلِ", "التَّسْجِيلُ")} {w("وَتَقْدِيمِ")} {w("الأَوْرَاقِ")}. {w("فِي")} {w("الجَامِعَةِ", "الجَامِعَةُ")}، {w("يَتَعَلَّمُ")} {w("الطُّلَّابُ", "الطُّلَّابُ")} {w("أَشْيَاءَ")} {w("جَدِيدَةً")} {w("وَيَسْتَعِدُّونَ", "اِسْتَعَدَّ - يَسْتَعِدُّ")} {w("لِلْمُسْتَقْبَلِ", "المُسْتَقْبَلُ")}. {w("كَمَا")} {w("يَتَعَلَّمُونَ")} {w("أَنْ")} {w("يَعْتَمِدُوا", "اِعْتَمَدَ - يَعْتَمِدُ")} {w("عَلَى")} {w("أَنْفُسِهِمْ")}.
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

    # TOMBOL EVALUASI DIPINDAH KE PALING BAWAH HALAMAN BACAAN
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #1e3a8a;'>Sudah Selesai Membaca & Berdiskusi?</h4>", unsafe_allow_html=True)
    
    col_eval_btn1, col_eval_btn2, col_eval_btn3 = st.columns([1, 2, 1])
    with col_eval_btn2:
        if st.button("📝 LANJUT KE EVALUASI SOAL (الاِخْتِبَارُ)", type="primary", use_container_width=True):
            st.session_state.page = "evaluasi"
            st.rerun()


# ==============================================================================
# HALAMAN 3: EVALUASI KOREKSI LANGSUNG PER NOMOR
# ==============================================================================
elif st.session_state.page == "evaluasi":
    
    # Navigation Top Bar
    top_col1, top_col2 = st.columns([1.2, 3])
    with top_col1:
        if st.button("⬅️ Kembali ke Materi"):
            st.session_state.page = "learning"
            st.rerun()

    st.markdown("---")

    # Header Evaluasi
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="font-family: 'Amiri', serif; color: #1e3a8a; font-size: 36px; margin-bottom: 5px;">اِخْتِبَارُ فَهْمِ الْمَقْرُوءِ</h2>
        <h3 style="color: #334155; margin-top: 0;">Evaluasi Pemahaman Teks Bahasa Arab (Koreksi Langsung)</h3>
        <p style="color: #64748b;"><b>Mata Pelajaran:</b> Bahasa Arab | <b>Kelas:</b> XII MA (Genap) | <b>Bentuk:</b> Pilihan Ganda (20 Soal)</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("📌 **التَّعْلِيمَاتُ (Petunjuk Guru & Siswa):** Pilihlah opsi jawaban per nomor. **Hasil koreksi & apresiasi akan langsung muncul di bawah nomor tersebut** untuk bahan diskusi bersama di kelas!")

    # Ringkasan Skor Real-Time
    answered_count = len(st.session_state.user_answers)
    correct_count = 0
    for q_id, u_ans in st.session_state.user_answers.items():
        q_item = next((item for item in quiz_data if item["id"] == q_id), None)
        if q_item and u_ans == q_item["key"]:
            correct_count += 1

    st.caption(f"📊 **Progres Pengerjaan Kelas:** Terjawab: **{answered_count} / 20** | Jawaban Benar: **{correct_count}**")

    # Loop Render Soal dengan Koreksi Langsung
    for item in quiz_data:
        q_num = item["id"]
        q_text = item["q"]
        opts = item["opts"]
        key_ans = item["key"]
        
        st.markdown(f"""
        <div class="question-card">
            <div style="color: #2563eb; font-weight: bold; font-size: 14px; margin-bottom: 5px;">Soal Nomor {q_num} dari 20</div>
            <div class="question-arabic">{q_num}. {q_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Format Pilihan Jawaban
        formatted_opts = [f"{k}. {v}" for k, v in opts.items()]
        
        # Pilihan Jawaban
        saved_ans = st.session_state.user_answers.get(q_num, None)
        default_idx = None
        if saved_ans:
            default_idx = ["A", "B", "C", "D", "E"].index(saved_ans)

        choice = st.radio(
            label=f"Pilih Jawaban Soal {q_num}:",
            options=formatted_opts,
            index=default_idx,
            key=f"q_radio_{q_num}",
            label_visibility="collapsed"
        )

        # Koreksi Langsung & Apresiasi Emoticon Per Nomor (Indensasi & Syntax Sudah Diperbaiki)
        if choice:
            user_choice_key = choice.split(".")[0]
            st.session_state.user_answers[q_num] = user_choice_key

            if user_choice_key == key_ans:
                st.success(f"🎉 **أَحْسَنْتَ! (Hebat Sekali! Jawabanmu Tepat!)** 🥳👏✨\n\nJawaban **[{user_choice_key}]** adalah jawaban yang benar!")
            else:
                st.error(f"🥺 **عَفْوًا، الإِجَابَةُ غَيْرُ صَحِيحَةٍ (Aduh, Sayang Sekali Kurang Tepat!)** 😢💔\n\n**Jawaban Kamu:** [{user_choice_key}]")

        st.markdown("<hr style='margin: 25px 0; border: 0.5px dashed #cbd5e1;'>", unsafe_allow_html=True)

    # Tombol Reset
    if st.button("🔄 Reset / Ulangi Semua Soal Evaluasi"):
        st.session_state.user_answers = {}
        st.rerun()
