import streamlit as st

# 1. Konfigurasi Halaman (Harus berada di paling atas setelah import)
st.set_page_config(
    page_title="Smart Qira'ah Reader: Ad-Dirasah fil Jamiah",
    page_icon="🎓",
    layout="wide"
)

# 2. Injeksi CSS untuk Teks Arab RTL & Tampilan Menarik
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
        font-size: 26px;
        line-height: 2.3;
        direction: rtl;
        text-align: right;
        background-color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        border-right: 6px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Database 17 Mufrodat Lengkap
vocab_db = {
    "المَدْرَسَةُ": {"indo": "Sekolah / Madrasah", "ctl": "💡 Konteks CTL: Jenjang pendidikan awal (MA) sebelum melangkah ke jenjang Perguruan Tinggi."},
    "الطُّلَّابُ": {"indo": "Siswa / Mahasiswa", "ctl": "💡 Konteks CTL: Para pelajar yang bersiap mentransisikan peran diri menjadi mahasiswa mandiri."},
    "الجَامِعَةُ": {"indo": "Universitas / Perguruan Tinggi", "ctl": "💡 Konteks CTL: Lembaga tinggi tempat siswa MA melanjutkan studi (PTN, PTKIN, luar negeri)."},
    "المُسْتَقْبَلُ": {"indo": "Masa Depan", "ctl": "💡 Konteks CTL: Cita-cita karier dan tujuan hidup yang dirancang siswa kelas 12."},
    "التَّسْجِيلُ": {"indo": "Pendaftaran / Registrasi", "ctl": "💡 Konteks CTL: Proses administratif melengkapi berkas jalur pendaftaran (SNBP, SNBT, SPAN-PTKIN)."},
    "القِسْمُ": {"indo": "Jurusan / Program Studi", "ctl": "💡 Konteks CTL: Spesialisasi ilmu yang dipilih siswa sesuai bakat dan minat akademik."},
    "الكُلِّيَّةُ": {"indo": "Fakultas", "ctl": "💡 Konteks CTL: Unit gabungan beberapa jurusan sejenis (misal: Fakultas Tarbiyah, Kedokteran, Teknik)."},
    "المَكْتَبَةُ": {"indo": "Perpustakaan", "ctl": "💡 Konteks CTL: Pusat referensi bacaan, jurnal akademik, dan tempat mahasiswa meriset tugas."},
    "الأُسْتَاذُ": {"indo": "Dosen / Pengajar", "ctl": "💡 Konteks CTL: Tenaga pengajar dan pembimbing riset ilmiah di lingkungan perguruan tinggi."},
    "المُجْتَمَعُ": {"indo": "Masyarakat / Komunitas", "ctl": "💡 Konteks CTL: Muara pengabdian ilmu yang didapatkan mahasiswa setelah menyelesaikan kuliah."},
    "وَاصَلَ - يُوَاصِلُ": {"indo": "Melanjutkan", "ctl": "💡 Konteks CTL: Semangat siswa MA untuk meneruskan pendidikan ke tingkatan yang lebih tinggi."},
    "اِخْتَارَ - يَخْتَارُ": {"indo": "Memilih", "ctl": "💡 Konteks CTL: Proses kemandirian mengambil keputusan menentukan jurusan kampus."},
    "تَنَاسَبَ - يَتَنَاسَبُ": {"indo": "Sesuai / Cocok", "ctl": "💡 Konteks CTL: Menyesuaikan jurusan yang dipilih dengan potensi dan minat diri."},
    "اِلْتَحَقَ - يَلْتَحِقُ": {"indo": "Bergabung / Masuk PT", "ctl": "💡 Konteks CTL: Resmi terdaftar dan menjadi mahasiswa di fakultas pilihan."},
    "اِعْتَمَدَ - يَعْتَمِدُ": {"indo": "Berdikari / Mandiri", "ctl": "💡 Konteks CTL: Kemandirian pola belajar mahasiswa di kampus tanpa bergantung penuh pada guru."},
    "اِسْتَعَدَّ - يَسْتَعِدُّ": {"indo": "Bersiap-siap", "ctl": "💡 Konteks CTL: Persiapan berkas, nilai, dan mental siswa kelas 12 menjelang kelulusan."},
    "أَفَادَ - يُفِيدُ": {"indo": "Memberi Manfaat", "ctl": "💡 Konteks CTL: Tujuan utama menuntut ilmu tinggi agar membawa dampak positif bagi masyarakat."}
}

# 4. Header Aplikasi
st.markdown('<h1 class="main-title">🎓 Smart Qira\'ah Reader</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Media Pembelajaran Maharah Qira\'ah Kelas 12 MA — Tema: Ad-Dirasah fil Jamiah</p>', unsafe_allow_html=True)

# 5. Sidebar Navigasi Mufrodat
st.sidebar.header("📌 Bank 17 Kosa Kata Wajib")
selected_word = st.sidebar.selectbox("Pilih kata untuk dibedah maknanya:", list(vocab_db.keys()))

if selected_word:
    info = vocab_db[selected_word]
    st.sidebar.markdown(f"### {selected_word}")
    st.sidebar.markdown(f"**Arti:** {info['indo']}")
    st.sidebar.info(info['ctl'])

# 6. Layout Utama (2 Kolom)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📖 Teks Bacaan (المَادَّةُ)")
    
    # Paragraf 1
    st.markdown('<div class="arabic-title">الفقرة الأولى: الدِّرَاسَةُ فِي الجَامِعَةِ</div>', unsafe_allow_html=True)
    p1_text = """
    بَعْدَ التَّخَرُّجِ مِنَ المَدْرَسَةِ الإِسْلَامِيَّةِ، يُرِيدُ كَثِيرٌ مِنَ الطُّلَّابِ أَنْ يَدْرُسُوا فِي الجَامِعَةِ. يَذْهَبُ الطُّلَّابُ إِلَى الجَامِعَةِ لِلتَّسْجِيلِ وَتَقْدِيمِ الأَوْرَاقِ. فِي الجَامِعَةِ، يَتَعَلَّمُ الطُّلَّابُ أَشْيَاءَ جَدِيدَةً وَيَسْتَعِدُّونَ لِلْمُسْتَقْبَلِ. كَمَا يَتَعَلَّمُونَ أَنْ يَعْتَمِدُوا عَلَى أَنْفُسِهِمْ.
    """
    st.markdown(f'<div class="arabic-text">{p1_text}</div>', unsafe_allow_html=True)

    # Paragraf 2
    st.markdown('<div class="arabic-title">الفقرة الثانية: اخْتِيَارُ القِسْمِ وَالكُلِّيَّةِ</div>', unsafe_allow_html=True)
    p2_text = """
    يَخْتَارُ كُلُّ طَالِبٍ القِسْمَ الَّذِي يُحِبُّهُ وَيُنَاسِبُهُ. مَنْ يُحِبُّ الطِّبَّ يَدْرُسُ فِي كُلِّيَّةِ الطِّبِّ، وَمَنْ يُحِبُّ الهَنْدَسَةَ يَدْرُسُ فِي كُلِّيَّةِ الهَنْدَسَةِ. وَهُنَاكَ أَيْضًا كُلِّيَّةُ التَّرْبِيَةِ وَكُلِّيَّةُ الشَّرِيعَةِ. يَخْتَارُ الطُّلَّابُ هَذِهِ الكُلِّيَّاتِ لِأَنَّهُمْ يُرِيدُونَ أَنْ يَتَعَلَّمُوا وَيُفِيدُوا المُجْتَمَعَ.
    """
    st.markdown(f'<div class="arabic-text">{p2_text}</div>', unsafe_allow_html=True)

    # Paragraf 3
    st.markdown('<div class="arabic-title">الفقرة الثالثة: الحَيَاةُ الجَامِعِيَّةُ وَالدِّرَاسَةُ</div>', unsafe_allow_html=True)
    p3_text = """
    فِي الجَامِعَةِ، يَحْضُرُ الطُّلَّابُ الدُّرُوسَ فِي الفَصْلِ مَعَ الأُسْتَاذِ. وَيَذْهَبُونَ إِلَى المَكْتَبَةِ لِلْقِرَاءَةِ وَالبَحْثِ عَنِ المَعْلُومَاتِ. كَمَا يَتَعَلَّمُونَ مِنْ خِلَالِ المُنَاقَشَةِ مَعَ الأَسَاتِذَةِ وَالأَصْدِقَاءِ. وَيَسْتَخْدِمُونَ طُرُقًا حَدِيثَةً فِي التَّعَلُّمِ لِكَيْ يَكُونُوا مُسْتَعِدِّينَ لِلْعَمَلِ فِي المُسْتَقْبَلِ.
    """
    st.markdown(f'<div class="arabic-text">{p3_text}</div>', unsafe_allow_html=True)

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
