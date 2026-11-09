# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Smart Qira'ah Reader",
    page_icon="🎓",
    layout="wide"
)

# 2. Injeksi CSS untuk Teks Arab & RTL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    
    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 28px;
        line-height: 2.2;
        direction: rtl;
        text-align: right;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #1e3a8a;
        margin-bottom: 20px;
    }
    .arabic-title {
        font-family: 'Amiri', serif;
        font-size: 32px;
        color: #1e3a8a;
        direction: rtl;
        text-align: right;
        font-weight: bold;
    }
    .ctl-box {
        background-color: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 15px;
        border-radius: 8px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Database 17 Mufrodat
vocab_db = {
    "المَدْرَسَةُ": {"indo": "Sekolah / Madrasah", "ctl": "💡 CTL: Jenjang MA sebelum menuju ke Perguruan Tinggi."},
    "الطُّلَّابُ": {"indo": "Siswa / Mahasiswa", "ctl": "💡 CTL: Transisi peran dari siswa MA menjadi mahasiswa mandiri."},
    "الجَامِعَةُ": {"indo": "Universitas / PT", "ctl": "💡 CTL: Perguruan tinggi tujuan lulusan MA (PTN/PTKIN)."},
    "المُسْتَقْبَلُ": {"indo": "Masa Depan", "ctl": "💡 CTL: Perencanaan karier & cita-cita siswa kelas 12."},
    "التَّسْجِيلُ": {"indo": "Pendaftaran", "ctl": "💡 CTL: Alur administrasi masuk kampus (SNBP, SNBT, SPAN-PTKIN)."},
    "القِسْمُ": {"indo": "Jurusan / Prodi", "ctl": "💡 CTL: Program studi yang sesuai minat dan bakat."},
    "الكُلِّيَّةُ": {"indo": "Fakultas", "ctl": "💡 CTL: Wadah spesialisasi ilmu (Tarbiyah, Kedokteran, Teknik)."},
    "المَكْتَبَةُ": {"indo": "Perpustakaan", "ctl": "💡 CTL: Pusat riset bacaan dan referensi kuliah."},
    "الأُسْتَاذُ": {"indo": "Dosen / Pengajar", "ctl": "💡 CTL: Pendamping dan pembimbing akademis mahasiswa."},
    "المُجْتَمَعُ": {"indo": "Masyarakat", "ctl": "💡 CTL: Muara kebermanfaatan ilmu lulusan kampus."},
    "وَاصَلَ - يُوَاصِلُ": {"indo": "Melanjutkan", "ctl": "💡 CTL: Semangat meneruskan studi ke jenjang tinggi."},
    "اِخْتَارَ - يَخْتَارُ": {"indo": "Memilih", "ctl": "💡 CTL: Kemandirian memilih jalan studi lanjut."},
    "تَنَاسَبَ - يَتَنَاسَبُ": {"indo": "Sesuai / Cocok", "ctl": "💡 CTL: Menyelaraskan minat diri dengan prodi."},
    "اِلْتَحَقَ - يَلْتَحِقُ": {"indo": "Bergabung / Masuk", "ctl": "💡 CTL: Resmi terdaftar sebagai mahasiswa baru."},
    "اِعْتَمَدَ - يَعْتَمِدُ": {"indo": "Berdikari / Mandiri", "ctl": "💡 CTL: Kemandirian pola belajar di Perguruan Tinggi."},
    "اِسْتَعَدَّ - يَسْتَعِدُّ": {"indo": "Bersiap-siap", "ctl": "💡 CTL: Persiapan berkas & mental kelas 12."},
    "أَفَادَ - يُفِيدُ": {"indo": "Memberi Manfaat", "ctl": "💡 CTL: Pengabdian ilmu untuk kemaslahatan masyarakat."}
}

# 4. Header Aplikasi
st.title("🎓 Smart Qira'ah Reader: Ad-Dirasah fil Jamiah")
st.caption("Media Pembelajaran Maharah Qira'ah Kelas 12 MA (Pendekatan CTL)")

# 5. Sidebar Navigasi Mufrodat
st.sidebar.header("📌 Bank 17 Mufrodat Interaktif")
selected_word = st.sidebar.selectbox("Pilih Kosa Kata untuk Bedah Makna:", list(vocab_db.keys()))

# Tampilan detail mufrodat di sidebar
if selected_word:
    info = vocab_db[selected_word]
    st.sidebar.subheader(selected_word)
    st.sidebar.write(f"**Arti:** {info['indo']}")
    st.sidebar.info(info['ctl'])

# 6. Area Utama Teks Bacaan
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📖 Teks Bacaan (المَادَّةُ)")
    
    # Paragraf 1
    st.markdown('<div class="arabic-title">الفقرة الأولى: الدِّرَاسَةُ فِي الجَامِعَةِ</div>', unsafe_allow_html=True)
    p1_text = """
    بَعْدَ التَّخَرُّجِ مِنَ المَدْرَسَةِ الإِسْلَامِيَّةِ، يُرِيدُ كَثِيرٌ مِنَ الطُّلَّابِ أَنْ يُوَاصِلُوا دِرَاسَتَهُمْ وَيَدْرُسُوا فِي الجَامِعَةِ. يَذْهَبُ الطُّلَّابُ إِلَى الجَامِعَةِ لِلتَّسْجِيلِ وَتَقْدِيمِ الأَوْرَاقِ. فِي الجَامِعَةِ، يَتَعَلَّمُ الطُّلَّابُ أَشْيَاءَ جَدِيدَةً وَيَسْتَعِدُّونَ لِلْمُسْتَقْبَلِ. كَمَا يَتَعَلَّمُونَ أَنْ يَعْتَمِدُوا عَلَى أَنْفُسِهِمْ.
    """
    st.markdown(f'<div class="arabic-text">{p1_text}</div>', unsafe_allow_html=True)

    # Paragraf 2
    st.markdown('<div class="arabic-title">الفقرة الثانية: اخْتِيَارُ القِسْمِ وَالكُلِّيَّةِ</div>', unsafe_allow_html=True)
    p2_text = """
    يَخْتَارُ كُلُّ طَالِبٍ القِسْمَ الَّذِي يُحِبُّهُ وَيُنَاسِبُهُ. مَنْ يُحِبُّ الطِّبَّ يَلْتَحِقُ وَيَدْرُسُ فِي كُلِّيَّةِ الطِّبِّ، وَمَنْ يُحِبُّ الهَنْدَسَةَ يَدْرُسُ فِي كُلِّيَّةِ الهَنْدَسَةِ. وَهُنَاكَ أَيْضًا كُلِّيَّةُ التَّرْبِيَةِ وَكُلِّيَّةُ الشَّرِيعَةِ. يَخْتَارُ الطُّلَّابُ هَذِهِ الكُلِّيَّاتِ لِأَنَّهُمْ يُرِيدُونَ أَنْ يَتَعَلَّمُوا وَيُفِيدُوا المُجْتَمَعَ.
    """
    st.markdown(f'<div class="arabic-text">{p2_text}</div>', unsafe_allow_html=True)

    # Paragraf 3
    st.markdown('<div class="arabic-title">الفقرة الثالثة: الحَيَاةُ الجَامِعِيَّةُ وَالدِّرَاسَةُ</div>', unsafe_allow_html=True)
    p3_text = """
    فِي الجَامِعَةِ، يَحْضُرُ الطُّلَّابُ الدُّرُوسَ فِي الفَصْلِ مَعَ الأُسْتَاذِ. وَيَذْهَبُونَ إِلَى المَكْتَبَةِ لِلْقِرَاءَةِ وَالبَحْثِ عَنِ المَعْلُومَاتِ. كَمَا يَتَعَلَّمُونَ مِنْ خِلَالِ المُنَاقَشَةِ مَعَ الأَسَاتِذَةِ وَالأَصْدِقَاءِ. وَيَسْتَخْدِمُونَ طُرُقًا حَدِيثَةً فِي التَّعَلُّمِ لِكَيْ يَكُونُوا مُسْتَعِدِّينَ لِلْعَمَلِ فِي المُسْتَقْبَلِ.
    """
    st.markdown(f'<div class="arabic-text">{p3_text}</div>', unsafe_allow_html=True)

with col2:
    st.subheader("💡 Fokus Diskusi CTL")
    st.write("Gunakan bagian ini untuk memandu pertanyaan interaktif ke siswa:")
    st.expander("Pertanyaan Paragraf 1").write("Apa alasan utama lulusan MA ingin melanjutkan ke Perguruan Tinggi?")
    st.expander("Pertanyaan Paragraf 2").write("Bagaimana cara memilih fakultas/jurusan yang sesuai dengan potensi diri?")
    st.expander("Pertanyaan Paragraf 3").write("Apa perbedaan suasana belajar di sekolah (MA) dengan di kampus?")
