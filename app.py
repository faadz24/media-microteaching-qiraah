import streamlit as st

# 1. Konfigurasi Halaman (Harus di baris pertama setelah import)
st.set_page_config(
    page_title="Smart Qira'ah Reader: Ad-Dirasah fil Jamiah",
    page_icon="🎓",
    layout="wide"
)

# 2. Injeksi CSS untuk Teks Arab, Pop-up Tooltip + Gambar untuk SEMUA KATA
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
    
    /* GAYA KATA TARGET (17 MUFRODAT UTAMA) */
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
    
    /* GAYA KATA PENDUKUNG (SEMUA KATA LAIN DALAM TEKS) */
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

# 3. Database Seluruh Kata dalam Teks Bacaan (Setiap kata ber-gambar spesifik!)
words_db = {
    # --- 17 TARGET MUFRODAT UTAMA (FOTO + CONTOH KALIMAT + CTL) ---
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

    # --- SELURUH KATA PENDUKUNG DI LUAR 17 MUFRODAT (LENGKAP GAMBAR SPESIFIK) ---
    "بَعْدَ": {"type": "regular", "indo": "Setelah", "gram": "Zaraf Zaman (Keterangan Waktu)", "img_url": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"},
    "التَّخَرُّجِ": {"type": "regular", "indo": "Kelulusan / Wisuda", "gram": "Isim Masdar", "img_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400"},
    "مِنَ": {"type": "regular", "indo": "Dari", "gram": "Harf Jar", "img_url": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=400"},
    "الثَّانَوِيَّةِ": {"type": "regular", "indo": "Tingkat Menengah / Aliyah", "gram": "Kata Sifat (Na'at)", "img_url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=400"},
    "الإِسْلَامِيَّةِ": {"type": "regular", "indo": "Islam / Keislaman", "gram": "Kata Sifat (Na'at)", "img_url": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?w=400"},
    "يُرِيدُ": {"type": "regular", "indo": "Ingin / Menghendaki", "gram": "Fi'il Mudhari'", "img_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400"},
    "كَثِيرٌ": {"type": "regular", "indo": "Banyak", "gram": "Isim Sifat", "img_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400"},
    "أَنْ": {"type": "regular", "indo": "Bahwa / Untuk", "gram": "Harf Nashab", "img_url": "https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=400"},
    "يَدْرُسُوا": {"type": "regular", "indo": "Belajar / Berkuliah", "gram": "Fi'il Mudhari' Jamak", "img_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400"},
    "فِي": {"type": "regular", "indo": "Di / Di dalam", "gram": "Harf Jar", "img_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400"},
    "يَذْهَبُ": {"type": "regular", "indo": "Pergi / Berangkat", "gram": "Fi'il Mudhari'", "img_url": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400"},
    "إِلَى": {"type": "regular", "indo": "Ke / Kepada", "gram": "Harf Jar", "img_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"},
    "وَتَقْدِيمِ": {"type": "regular", "indo": "Dan menyerahkan / mengajukan", "gram": "Harf Athaf + Masdar", "img_url": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=400"},
    "الأَوْرَاقِ": {"type": "regular", "indo": "Berkas-berkas / Dokumen", "gram": "Isim Jamak Taksir", "img_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"},
    "يَتَعَلَّمُ": {"type": "regular", "indo": "Belajar / Mempelajari", "gram": "Fi'il Mudhari'", "img_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"},
    "أَشْيَاءَ": {"type": "regular", "indo": "Hal-hal / Sesuatu", "gram": "Isim Jamak", "img_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400"},
    "جَدِيدَةً": {"type": "regular", "indo": "Baru", "gram": "Na'at / Kata Sifat", "img_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400"},
    "كَمَا": {"type": "regular", "indo": "Sebagaimana / Juga", "gram": "Harf Sambung", "img_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400"},
    "يَتَعَلَّمُونَ": {"type": "regular", "indo": "Mereka belajar", "gram": "Fi'il Mudhari' Jamak", "img_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400"},
    "عَلَى": {"type": "regular", "indo": "Atas / Pada", "gram": "Harf Jar", "img_url": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=400"},
    "أَنْفُسِهِمْ": {"type": "regular", "indo": "Diri mereka sendiri", "gram": "Isim + Dhamir (Kemandirian)", "img_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400"},
    "كُلُّ": {"type": "regular", "indo": "Setiap / Masing-masing", "gram": "Isim Mudhaf", "img_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400"},
    "طَالِبٍ": {"type": "regular", "indo": "Siswa / Pelajar", "gram": "Isim Mufrad (Tunggal)", "img_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"},
    "الَّذِي": {"type": "regular", "indo": "Yang", "gram": "Isim Maushul (Kata Hubung)", "img_url": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=400"},
    "يُحِبُّهُ": {"type": "regular", "indo": "Ia menyukainya", "gram": "Fi'il Mudhari' + Dhamir", "img_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=400"},
    "يُنَاسِبُهُ": {"type": "regular", "indo": "Sesuai / Cocok baginya", "gram": "Fi'il Mudhari' + Dhamir", "img_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400"},
    "مَنْ": {"type": "regular", "indo": "Barangsiapa / Siapa yang", "gram": "Isim Syarat / Maushul", "img_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"},
    "يُحِبُّ": {"type": "regular", "indo": "Menyukai", "gram": "Fi'il Mudhari'", "img_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=400"},
    "الطِّبَّ": {"type": "regular", "indo": "Kedokteran / Ilmu Medis", "gram": "Isim Jurusan", "img_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400"},
    "يَدْرُسُ": {"type": "regular", "indo": "Belajar / Berkuliah", "gram": "Fi'il Mudhari'", "img_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"},
    "الطِّبِّ": {"type": "regular", "indo": "Kedokteran", "gram": "Isim Mudhaf Ilaih", "img_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400"},
    "الهَنْدَسَةَ": {"type": "regular", "indo": "Teknik / Rekayasa", "gram": "Isim Jurusan", "img_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400"},
    "الهَنْدَسَةِ": {"type": "regular", "indo": "Teknik", "gram": "Isim Jurusan", "img_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400"},
    "وَهُنَاكَ": {"type": "regular", "indo": "Dan di sana / Terdapat juga", "gram": "Isim Isyarah", "img_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400"},
    "أَيْضًا": {"type": "regular", "indo": "Juga / Pula", "gram": "Maf'ul Mutlaq", "img_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400"},
    "التَّرْبِيَةِ": {"type": "regular", "indo": "Pendidikan / Tarbiyah", "gram": "Isim Fakultas", "img_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=400"},
    "الشَّرِيعَةِ": {"type": "regular", "indo": "Syariah / Hukum Islam", "gram": "Isim Fakultas", "img_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400"},
    "هَذِهِ": {"type": "regular", "indo": "Ini (Kata Tunjuk)", "gram": "Isim Isyarah", "img_url": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=400"},
    "الكُلِّيَّاتِ": {"type": "regular", "indo": "Fakultas-fakultas", "gram": "Isim Jamak Muannats", "img_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400"},
    "لِأَنَّهُمْ": {"type": "regular", "indo": "Karena mereka", "gram": "Harf Sababiyah + Dhamir", "img_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400"},
    "يُرِيدُونَ": {"type": "regular", "indo": "Mereka ingin / bertekad", "gram": "Fi'il Mudhari' Jamak", "img_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400"},
    "يَتَعَلَّمُوا": {"type": "regular", "indo": "Agar mereka belajar", "gram": "Fi'il Mudhari' Manshub", "img_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400"},
    "يَحْضُرُ": {"type": "regular", "indo": "Menghadiri / Mengikuti", "gram": "Fi'il Mudhari'", "img_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=400"},
    "الدُّرُوسَ": {"type": "regular", "indo": "Pelajaran-pelajaran / Perkuliahan", "gram": "Isim Jamak Taksir", "img_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"},
    "الفَصْلِ": {"type": "regular", "indo": "Ruang Kelas", "gram": "Isim Tempat", "img_url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"},
    "مَعَ": {"type": "regular", "indo": "Bersama / Dengan", "gram": "Zaraf Makan", "img_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400"},
    "وَيَذْهَبُونَ": {"type": "regular", "indo": "Dan mereka pergi", "gram": "Fi'il Mudhari' Jamak", "img_url": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400"},
    "لِلْقِرَاءَةِ": {"type": "regular", "indo": "Untuk membaca", "gram": "Harf Jar + Masdar", "img_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400"},
    "وَالبَحْثِ": {"type": "regular", "indo": "Dan meriset / mencari data", "gram": "Isim Masdar", "img_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"},
    "عَنِ": {"type": "regular", "indo": "Tentang / Dari", "gram": "Harf Jar", "img_url": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=400"},
    "المَعْلُومَاتِ": {"type": "regular", "indo": "Informasi / Data", "gram": "Isim Jamak Muannats", "img_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400"},
    "مِنْ": {"type": "regular", "indo": "Dari / Melalui", "gram": "Harf Jar", "img_url": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=400"},
    "خِلَالِ": {"type": "regular", "indo": "Melalui / Sela-sela", "gram": "Zaraf", "img_url": "https://images.unsplash.com/photo-1508873696983-2df515122519?w=400"},
    "المُنَاقَشَةِ": {"type": "regular", "indo": "Diskusi / Tanya Jawab", "gram": "Isim Masdar", "img_url": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=400"},
    "الأَسَاتِذَةِ": {"type": "regular", "indo": "Para Dosen / Pengajar", "gram": "Isim Jamak dari Ustadz", "img_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=400"},
    "وَالأَصْدِقَاءِ": {"type": "regular", "indo": "Dan teman-teman", "gram": "Isim Jamak Taksir", "img_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400"},
    "وَيَسْتَخْدِمُونَ": {"type": "regular", "indo": "Dan mereka menggunakan", "gram": "Fi'il Mudhari' Jamak", "img_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400"},
    "طُرُقًا": {"type": "regular", "indo": "Metode-metode / Cara", "gram": "Isim Jamak", "img_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"},
    "حَدِيثَةً": {"type": "regular", "indo": "Modern / Terbaru", "gram": "Na'at / Kata Sifat", "img_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400"},
    "التَّعَلُّمِ": {"type": "regular", "indo": "Pembelajaran / Studi", "gram": "Isim Masdar", "img_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"},
    "لِكَيْ": {"type": "regular", "indo": "Supaya / Agar", "gram": "Harf Nashab", "img_url": "https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=400"},
    "يَكُونُوا": {"type": "regular", "indo": "Agar mereka menjadi", "gram": "Fi'il Mudhari' Naqis", "img_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400"},
    "مُسْتَعِدِّينَ": {"type": "regular", "indo": "Siap sedia", "gram": "Khabar Kana (Jamak)", "img_url": "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=400"},
    "لِلْعَمَلِ": {"type": "regular", "indo": "Untuk bekerja", "gram": "Harf Jar + Masdar", "img_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400"}
}

# Fungsi Builder Pop-Up Interaktif Ber-Gambar untuk Setiap Kata
def w(arabic_word, db_key=None):
    key = db_key if db_key else arabic_word
    info = words_db.get(key, {
        "type": "regular", 
        "indo": "Kata dalam teks", 
        "gram": "Kosa kata", 
        "img_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400"
    })
    
    img_url = info["img_url"]

    if info["type"] == "target":
        # Pop-Up Lengkap 17 Mufrodat Utama (Biru Putus-putus)
        return f'''<span class="vocab-target">{arabic_word}<span class="tooltip-box"><img src="{img_url}" class="popup-img"><b style="font-size:17px; color:#38bdf8;">{key}</b><br><span style="color:#fde047; font-weight:bold;">{info['indo']}</span><br><div class="example-box"><b>📌 Contoh Kalimat:</b><br><span style="font-family:'Amiri'; font-size:16px;">{info['ar_ex']}</span><br><i style="color:#cbd5e1; font-size:11px;">"{info['id_ex']}"</i></div><div style="font-size:11px; margin-top:5px; color:#94a3b8;">{info['ctl']}</div></span></span>'''
    else:
        # Pop-Up Kata Pendukung (Garis Halus Grey, Tetap Punya Gambar Spesifik!)
        gram_info = f'<br><small style="color:#94a3b8;">({info.get("gram", "")})</small>' if "gram" in info else ""
        return f'''<span class="vocab-regular">{arabic_word}<span class="tooltip-box"><img src="{img_url}" class="popup-img"><b style="font-size:16px; color:#38bdf8;">{arabic_word}</b><br><span style="color:#fde047; font-weight:bold;">{info['indo']}</span>{gram_info}</span></span>'''

# 4. Header Aplikasi
st.markdown('<h1 class="main-title">🎓 Smart Qira\'ah Reader</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Media Pembelajaran Maharah Qira\'ah Kelas 12 MA — Tema: Ad-Dirasah fil Jamiah</p>', unsafe_allow_html=True)
st.caption("👉 **Petunjuk Guru:** *Seluruh kata tanpa terkecuali* dalam teks ini kini interaktif! Arahkan/Klik kata mana saja di layar untuk melihat gambar foto visual, arti bahasa Indonesia, serta penjelasannya.")

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

# 6. Area Utama Teks Bacaan (100% Seluruh Kata Memiliki Gambar Penuh)
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
