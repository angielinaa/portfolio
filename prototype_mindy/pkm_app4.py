# ==============================================================================
# Nama File: mentalcare_ai_app.py
# Deskripsi: Aplikasi MentalCare AI untuk skrining kesehatan mental (DASS) 
#            dan tes kepribadian Big Five
# Versi: 2.1 Final
# Tim PKM: Informatika & Psikologi UMM
# ==============================================================================


# Import library yang diperlukan
import os
import sys
from typing import Dict, List, Tuple


# ==============================================================================
# FUNGSI-FUNGSI HELPER
# ==============================================================================

def clear_screen():
    """Membersihkan layar terminal (works di Windows & Mac/Linux)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_header(judul: str):
    """Menampilkan header dengan format yang rapi"""
    clear_screen()
    print("=" * 80)
    print(f"  {judul.center(76)}")
    print("=" * 80)
    print()

def input_pilihan(prompt: str, pilihan_valid: list) -> str:
    """
    Meminta input dari user dengan validasi
    
    Args:
        prompt: Teks yang ditampilkan untuk meminta input
        pilihan_valid: List pilihan yang valid (contoh: ['0', '1', '2'])
        
    Returns:
        Pilihan yang dipilih user
    """
    while True:
        jawaban = input(prompt).strip()
        if jawaban in pilihan_valid:
            return jawaban
        print(f"❌ Input tidak valid. Pilihan valid: {', '.join(pilihan_valid)}")


# ==============================================================================
# DATA PERTANYAAN SKRINING DASS (100 PERTANYAAN)
# ==============================================================================

def get_dass_questions() -> List[Dict[str, str]]:
    """
    Mengembalikan list 100 pertanyaan DASS dengan kategori masing-masing
    
    Returns:
        List dictionary dengan key:
'p': Pertanyaan
'k': Kategori ('D'=Depresi, 'A'=Anxiety, 'S'=Stress)
    """
    return [
        # DEPRESI (33 pertanyaan)
        {"p": "Saya merasa sulit untuk bersemangat tentang apa pun.", "k": "D"},
        {"p": "Saya merasa hidup ini tidak berarti.", "k": "D"},
        {"p": "Saya merasa sedih dan tertekan.", "k": "D"},
        {"p": "Saya kehilangan minat pada hal-hal yang biasanya saya nikmati.", "k": "D"},
        {"p": "Saya merasa tidak berharga sebagai seorang pribadi.", "k": "D"},
        {"p": "Saya merasa putus asa tentang masa depan.", "k": "D"},
        {"p": "Saya merasa lesu dan tidak bertenaga.", "k": "D"},
        {"p": "Saya merasa sulit untuk memulai sesuatu.", "k": "D"},
        {"p": "Saya menyalahkan diri sendiri atas banyak hal.", "k": "D"},
        {"p": "Saya memiliki pikiran untuk mengakhiri hidup saya.", "k": "D"},
        {"p": "Saya menangis tanpa alasan yang jelas.", "k": "D"},
        {"p": "Saya merasa kosong di dalam.", "k": "D"},
        {"p": "Saya merasa terisolasi dari orang lain, bahkan ketika bersama mereka.", "k": "D"},
        {"p": "Saya kehilangan kepercayaan diri saya.", "k": "D"},
        {"p": "Saya merasa segala sesuatu adalah usaha yang berat.", "k": "D"},
        {"p": "Saya tidak bisa melihat sisi positif dari suatu keadaan.", "k": "D"},
        {"p": "Saya merasa lelah sepanjang waktu, bahkan setelah tidur.", "k": "D"},
        {"p": "Saya merasa masa depan tampak suram.", "k": "D"},
        {"p": "Saya merasa sulit untuk membuat keputusan, bahkan yang sederhana sekalipun.", "k": "D"},
        {"p": "Saya merasa tidak ada yang bisa saya harapkan.", "k": "D"},
        {"p": "Saya merasa seperti orang gagal.", "k": "D"},
        {"p": "Saya tidak lagi menikmati makanan seperti dulu.", "k": "D"},
        {"p": "Saya merasa sulit berkonsentrasi pada apa pun.", "k": "D"},
        {"p": "Saya merasa tua dan letih.", "k": "D"},
        {"p": "Saya merasa tidak ada yang peduli pada saya.", "k": "D"},
        {"p": "Saya merasa sulit untuk merasakan emosi positif seperti kebahagiaan.", "k": "D"},
        {"p": "Saya lebih suka tinggal di rumah daripada pergi keluar dan melakukan hal-hal baru.", "k": "D"},
        {"p": "Saya merasa cemas tentang hal-hal sepele.", "k": "D"},
        {"p": "Saya merasa penampilan saya tidak menarik.", "k": "D"},
        {"p": "Saya merasa sulit untuk tidur di malam hari.", "k": "D"},
        {"p": "Saya merasa bersalah atas hal-hal yang bukan salah saya.", "k": "D"},
        {"p": "Saya merasa sulit untuk bangkit dari tempat tidur di pagi hari.", "k": "D"},
        {"p": "Saya merasa hidup ini adalah sebuah hukuman.", "k": "D"},
        
        # KECEMASAN / ANXIETY (33 pertanyaan)
        {"p": "Saya menyadari mulut saya terasa kering.", "k": "A"},
        {"p": "Saya mengalami kesulitan bernapas (misalnya, napas cepat, terengah-engah).", "k": "A"},
        {"p": "Saya merasakan getaran pada tangan saya.", "k": "A"},
        {"p": "Saya khawatir tentang situasi di mana saya mungkin panik dan mempermalukan diri sendiri.", "k": "A"},
        {"p": "Saya merasa dekat dengan kepanikan.", "k": "A"},
        {"p": "Saya merasa jantung saya berdebar kencang tanpa alasan.", "k": "A"},
        {"p": "Saya merasa takut tanpa alasan yang bagus.", "k": "A"},
        {"p": "Saya berkeringat secara berlebihan.", "k": "A"},
        {"p": "Saya merasa pusing atau seperti akan pingsan.", "k": "A"},
        {"p": "Saya khawatir tentang kinerja saya.", "k": "A"},
        {"p": "Saya merasa gugup dan cemas.", "k": "A"},
        {"p": "Saya merasa sulit untuk tetap tenang.", "k": "A"},
        {"p": "Saya merasa kewalahan oleh tanggung jawab.", "k": "A"},
        {"p": "Saya memiliki pikiran yang tidak bisa saya hentikan.", "k": "A"},
        {"p": "Saya merasa tegang atau gelisah.", "k": "A"},
        {"p": "Saya takut akan hal-hal yang paling buruk terjadi.", "k": "A"},
        {"p": "Otot-otot saya terasa tegang.", "k": "A"},
        {"p": "Saya menghindari situasi sosial karena takut.", "k": "A"},
        {"p": "Saya merasa seperti saya berada di ujung tanduk.", "k": "A"},
        {"p": "Perut saya terasa mual atau tidak nyaman.", "k": "A"},
        {"p": "Saya khawatir akan kehilangan kendali.", "k": "A"},
        {"p": "Saya merasa mudah terkejut atau kaget.", "k": "A"},
        {"p": "Saya terus-menerus memikirkan hal-hal yang membuat saya cemas.", "k": "A"},
        {"p": "Saya merasa sulit untuk fokus karena kekhawatiran.", "k": "A"},
        {"p": "Saya merasa seperti ada bahaya yang mengintai.", "k": "A"},
        {"p": "Saya merasa gelisah dan tidak bisa diam.", "k": "A"},
        {"p": "Saya khawatir membuat kesalahan.", "k": "A"},
        {"p": "Saya merasa perlu untuk memeriksa ulang pekerjaan saya berulang kali.", "k": "A"},
        {"p": "Saya merasa seperti ada benjolan di tenggorokan saya.", "k": "A"},
        {"p": "Saya sering memikirkan kembali percakapan dan mengkhawatirkan apa yang saya katakan.", "k": "A"},
        {"p": "Saya merasa kewalahan oleh kebisingan atau cahaya terang.", "k": "A"},
        {"p": "Saya takut akan masa depan.", "k": "A"},
        {"p": "Saya khawatir tentang kesehatan saya secara berlebihan.", "k": "A"},
        
        # STRES (34 pertanyaan)
        {"p": "Saya merasa sulit untuk bersantai.", "k": "S"},
        {"p": "Saya cenderung bereaksi berlebihan terhadap situasi.", "k": "S"},
        {"p": "Saya merasa saya menggunakan banyak energi saraf.", "k": "S"},
        {"p": "Saya mudah marah atau kesal.", "k": "S"},
        {"p": "Saya merasa tidak sabaran.", "k": "S"},
        {"p": "Saya merasa tegang dan gelisah.", "k": "S"},
        {"p": "Saya merasa sulit untuk beristirahat.", "k": "S"},
        {"p": "Saya mudah tersinggung.", "k": "S"},
        {"p": "Saya merasa sulit untuk menenangkan diri setelah sesuatu membuat saya kesal.", "k": "S"},
        {"p": "Saya merasa sulit untuk mentolerir gangguan terhadap apa yang saya lakukan.", "k": "S"},
        {"p": "Saya merasa gelisah.", "k": "S"},
        {"p": "Saya merasa sulit untuk berkonsentrasi.", "k": "S"},
        {"p": "Saya merasa mudah marah karena hal-hal sepele.", "k": "S"},
        {"p": "Saya merasa bahwa saya terlalu sensitif.", "k": "S"},
        {"p": "Saya merasa lelah secara mental.", "k": "S"},
        {"p": "Saya merasa terburu-buru.", "k": "S"},
        {"p": "Saya merasa jadwal saya terlalu padat.", "k": "S"},
        {"p": "Saya merasa sulit untuk membuat pikiran saya rileks.", "k": "S"},
        {"p": "Saya sering menggertakkan gigi.", "k": "S"},
        {"p": "Saya merasa frustrasi dengan mudah.", "k": "S"},
        {"p": "Saya merasa sulit untuk tidur karena pikiran saya terus berpacu.", "k": "S"},
        {"p": "Saya merasa tekanan darah saya tinggi.", "k": "S"},
        {"p": "Saya merasa orang lain terlalu menuntut saya.", "k": "S"},
        {"p": "Saya merasa kewalahan oleh daftar tugas saya.", "k": "S"},
        {"p": "Saya merasa mudah jengkel pada orang lain.", "k": "S"},
        {"p": "Saya merasa tidak punya cukup waktu dalam sehari.", "k": "S"},
        {"p": "Saya merasa sulit untuk duduk diam.", "k": "S"},
        {"p": "Saya sering sakit kepala karena tegang.", "k": "S"},
        {"p": "Saya merasa seperti saya akan meledak.", "k": "S"},
        {"p": "Saya merasa sulit untuk mematikan mode 'kerja' saya.", "k": "S"},
        {"p": "Saya merasa bahwa perubahan kecil dalam rutinitas saya sangat mengganggu.", "k": "S"},
        {"p": "Saya merasa perlu melakukan segala sesuatu dengan sempurna.", "k": "S"},
        {"p": "Saya merasa tidak ada yang berjalan sesuai rencana.", "k": "S"},
        {"p": "Saya merasa mudah lupa karena terlalu banyak pikiran.", "k": "S"},
    ]


# ==============================================================================
# DATA PERTANYAAN BIG FIVE (60 PERTANYAAN)
# ==============================================================================

def get_bigfive_questions() -> List[Dict]:
    """
    Mengembalikan list 60 pertanyaan Big Five Inventory-2 (BFI-2)
    
    Returns:
        List dictionary dengan key:
'p': Pertanyaan
'r': Boolean (True jika reversed item)
'trait': Trait yang diukur (E/A/C/N/O)
    """
    return [
        {"p": "ramah dan mudah bergaul.", "r": False, "trait": "E"},
        {"p": "penuh kasih, berhati lembut.", "r": False, "trait": "A"},
        {"p": "cenderung tidak teratur.", "r": True, "trait": "C"},
        {"p": "banyak merasa cemas.", "r": True, "trait": "N"},
        {"p": "memiliki sedikit minat pada seni.", "r": True, "trait": "O"},
        {"p": "memiliki kepribadian yang asertif (tegas).", "r": False, "trait": "E"},
        {"p": "bersikap hormat, memperlakukan orang lain dengan hormat.", "r": False, "trait": "A"},
        {"p": "cenderung malas.", "r": True, "trait": "C"},
        {"p": "tetap optimis setelah mengalami kegagalan.", "r": False, "trait": "N"},
        {"p": "ingin tahu tentang banyak hal yang berbeda.", "r": False, "trait": "O"},
        {"p": "jarang merasa bersemangat atau antusias.", "r": True, "trait": "E"},
        {"p": "cenderung mencari-cari kesalahan orang lain.", "r": True, "trait": "A"},
        {"p": "dapat diandalkan, stabil.", "r": False, "trait": "C"},
        {"p": "moody (suasana hatinya mudah berubah-ubah).", "r": True, "trait": "N"},
        {"p": "penuh ide, menemukan cara-cara cerdas untuk melakukan sesuatu.", "r": False, "trait": "O"},
        {"p": "cenderung pendiam.", "r": True, "trait": "E"},
        {"p": "memiliki sedikit simpati untuk orang lain.", "r": True, "trait": "A"},
        {"p": "sistematis, suka menjaga kerapian.", "r": False, "trait": "C"},
        {"p": "tenang dalam situasi tegang.", "r": False, "trait": "N"},
        {"p": "lebih menyukai pekerjaan yang konvensional (biasa saja).", "r": True, "trait": "O"},
        {"p": "dominan, bertindak sebagai pemimpin.", "r": False, "trait": "E"},
        {"p": "memulai pertengkaran dengan orang lain.", "r": True, "trait": "A"},
        {"p": "sulit untuk memulai mengerjakan tugas.", "r": True, "trait": "C"},
        {"p": "merasa aman, nyaman dengan diri sendiri.", "r": False, "trait": "N"},
        {"p": "menghindari diskusi filosofis.", "r": True, "trait": "O"},
        {"p": "tidak terlalu aktif dibandingkan orang lain.", "r": True, "trait": "E"},
        {"p": "memiliki sifat pemaaf.", "r": False, "trait": "A"},
        {"p": "bisa agak ceroboh.", "r": True, "trait": "C"},
        {"p": "stabil secara emosional, tidak mudah marah.", "r": False, "trait": "N"},
        {"p": "memiliki sedikit kreativitas.", "r": True, "trait": "O"},
        {"p": "terkadang pemalu, tertutup.", "r": True, "trait": "E"},
        {"p": "suka menolong dan tidak egois terhadap orang lain.", "r": False, "trait": "A"},
        {"p": "menjaga barang-barang tetap rapi dan bersih.", "r": False, "trait": "C"},
        {"p": "banyak merasa khawatir.", "r": True, "trait": "N"},
        {"p": "menghargai seni dan keindahan.", "r": False, "trait": "O"},
        {"p": "merasa sulit untuk memengaruhi orang lain.", "r": True, "trait": "E"},
        {"p": "terkadang kasar kepada orang lain.", "r": True, "trait": "A"},
        {"p": "efisien, menyelesaikan berbagai hal.", "r": False, "trait": "C"},
        {"p": "sering merasa sedih.", "r": True, "trait": "N"},
        {"p": "adalah seorang pemikir yang kompleks dan mendalam.", "r": False, "trait": "O"},
        {"p": "penuh energi.", "r": False, "trait": "E"},
        {"p": "curiga terhadap niat orang lain.", "r": True, "trait": "A"},
        {"p": "dapat diandalkan, selalu bisa diandalkan.", "r": False, "trait": "C"},
        {"p": "mampu mengendalikan emosinya.", "r": False, "trait": "N"},
        {"p": "mengalami kesulitan membayangkan sesuatu.", "r": True, "trait": "O"},
        {"p": "banyak bicara.", "r": False, "trait": "E"},
        {"p": "bisa bersikap dingin dan tidak peduli.", "r": True, "trait": "A"},
        {"p": "meninggalkan barang berantakan, tidak membersihkan.", "r": True, "trait": "C"},
        {"p": "jarang merasa cemas atau takut.", "r": False, "trait": "N"},
        {"p": "berpikir puisi dan sastra itu membosankan.", "r": True, "trait": "O"},
        {"p": "lebih suka membiarkan orang lain mengambil alih (memimpin).", "r": True, "trait": "E"},
        {"p": "sopan, santun kepada orang lain.", "r": False, "trait": "A"},
        {"p": "gigih, bekerja sampai tugas selesai.", "r": False, "trait": "C"},
        {"p": "cenderung merasa tertekan (depresi).", "r": True, "trait": "N"},
        {"p": "memiliki imajinasi yang biasa-biasa saja.", "r": True, "trait": "O"},
        {"p": "menunjukkan banyak antusiasme.", "r": False, "trait": "E"},
        {"p": "berprasangka baik tentang orang lain.", "r": False, "trait": "A"},
        {"p": "terkadang berperilaku tidak bertanggung jawab.", "r": True, "trait": "C"},
        {"p": "temperamental, mudah emosi.", "r": True, "trait": "N"},
        {"p": "cerdas dalam berpendapat.", "r": False, "trait": "O"},
    ]


# ==============================================================================
# FUNGSI SKRINING DASS
# ==============================================================================

def mulai_skrining_dass():
    """Menjalankan skrining DASS dengan 100 pertanyaan (skala 0-4)"""
    
    tampilkan_header("SKRINING KESEHATAN MENTAL (DASS)")
    
    # Tampilkan instruksi
    print("📋 INSTRUKSI:")
    print("   Untuk setiap pernyataan, jawablah berdasarkan pengalaman Anda")
    print("   selama SEMINGGU TERAKHIR.\n")
    print("   Skala Jawaban:")
    print("   0 = Tidak pernah")
    print("   1 = Jarang")
    print("   2 = Netral")
    print("   3 = Kadang")
    print("   4 = Sering\n")
    
    input("Tekan ENTER untuk memulai...")
    
    # Ambil pertanyaan
    pertanyaan = get_dass_questions()
    
    # Dictionary untuk menyimpan skor per kategori
    skor = {'D': 0, 'A': 0, 'S': 0}
    
    # Loop untuk setiap pertanyaan
    for i, item in enumerate(pertanyaan, 1):
        tampilkan_header(f"SKRINING DASS - Pertanyaan {i}/{len(pertanyaan)}")
        
        print(f"Pernyataan: {item['p']}\n")
        print("Pilihan:")
        print("  0. Tidak pernah")
        print("  1. Jarang")
        print("  2. Netral")
        print("  3. Kadang")
        print("  4. Sering\n")
        
        # Input jawaban dengan validasi
        jawaban = input_pilihan("Pilih jawaban (0-4): ", ['0', '1', '2', '3', '4'])
        
        # Tambahkan skor ke kategori yang sesuai
        kategori = item['k']
        skor[kategori] += int(jawaban)
    
    # Kalikan skor dengan 2 (sesuai standar DASS-21)
    # CATATAN: Kuesioner Anda 100 item, BUKAN DASS-21 (21 item) atau DASS-42 (42 item).
    # Skoring ini (kali 2) dan threshold di bawah ini MUNGKIN TIDAK VALID
    # untuk 100 item Anda. Ini harus dikonsultasikan dengan tim Psikologi Anda.
    # Namun, secara program, ini mengikuti logika kode Anda sebelumnya.
    skor['D'] *= 2
    skor['A'] *= 2
    skor['S'] *= 2
    
    # Tampilkan hasil
    tampilkan_hasil_dass(skor)

def tampilkan_hasil_dass(skor: Dict[str, int]):
    """Menampilkan hasil skrining DASS dengan interpretasi lengkap"""
    
    def get_level(score: int, thresholds: Tuple[int, int, int, int]) -> Tuple[str, bool]:
        """Menentukan tingkat berdasarkan skor"""
        if score <= thresholds[0]:
            return ("Normal", False)
        elif score <= thresholds[1]:
            return ("Ringan", False)
        elif score <= thresholds[2]:
            return ("Sedang", True)
        elif score <= thresholds[3]:
            return ("Parah", True)
        else:
            return ("Sangat Parah", True)
    
    # Threshold untuk setiap kategori (berdasarkan DASS-21)
    thresholds_depresi = (9, 13, 20, 27)
    thresholds_kecemasan = (7, 9, 14, 19)
    thresholds_stres = (14, 18, 25, 33)
    
    # Hitung tingkat untuk setiap kategori
    level_d, perlu_bantuan_d = get_level(skor['D'], thresholds_depresi)
    level_a, perlu_bantuan_a = get_level(skor['A'], thresholds_kecemasan)
    level_s, perlu_bantuan_s = get_level(skor['S'], thresholds_stres)
    
    # Tampilkan hasil
    tampilkan_header("HASIL SKRINING DASS")
    
    print("⚠️  CATATAN PENTING:")
    print("   Hasil ini BUKAN diagnosis medis, tapi indikator untuk refleksi diri.\n")
    
    # Hasil Depresi
    print("=" * 80)
    print("DEPRESI")
    print("=" * 80)
    print(f"Skor Anda: {skor['D']}")
    print(f"Tingkat: {level_d}")
    print("\nRange Skor:")
    print("  • Normal: 0-9 | Ringan: 10-13")
    print("  • Sedang: 14-20 | Parah: 21-27")
    print("  • Sangat Parah: 28+\n")
    
    # Hasil Kecemasan
    print("=" * 80)
    print("KECEMASAN (ANXIETY)")
    print("=" * 80)
    print(f"Skor Anda: {skor['A']}")
    print(f"Tingkat: {level_a}")
    print("\nRange Skor:")
    print("  • Normal: 0-7 | Ringan: 8-9")
    print("  • Sedang: 10-14 | Parah: 15-19")
    print("  • Sangat Parah: 20+\n")
    
    # Hasil Stres
    print("=" * 80)
    print("STRES")
    print("=" * 80)
    print(f"Skor Anda: {skor['S']}")
    print(f"Tingkat: {level_s}")
    print("\nRange Skor:")
    print("  • Normal: 0-14 | Ringan: 15-18")
    print("  • Sedang: 19-25 | Parah: 26-33")
    print("  • Sangat Parah: 34+\n")
    
    # Rekomendasi
    print("=" * 80)
    print("REKOMENDASI")
    print("=" * 80)
    
    perlu_bantuan = perlu_bantuan_d or perlu_bantuan_a or perlu_bantuan_s
    
    if perlu_bantuan:
        print("⚠️  Jika salah satu atau lebih hasil Anda berada di tingkat 'Sedang'")
        print("   atau lebih tinggi, sangat disarankan untuk berbicara dengan")
        print("   konselor, psikolog, atau profesional kesehatan mental.\n")
        
        # Tampilkan layanan bantuan
        print("=" * 80)
        print("LAYANAN BANTUAN PSIKOLOG")
        print("=" * 80)
        print("\n📞 SEJIWA")
        print("   Telepon: 119 (ekstensi 8)")
        print("\n📞 HALO KEMENKES")
        print("   Telepon: 1500 567")
        print("   WhatsApp: +62 812 6050 0567")
        print("   SMS: +62 812 8156 2620")
        print("\n💡 Jangan ragu untuk menghubungi layanan di atas.")
        print("   Kesehatan mental Anda penting!")
    else:
        print("✅ Hasil Anda menunjukkan tingkat yang baik.")
        print("   Tetap jaga kesehatan mental Anda dengan:")
        print("   • Istirahat cukup")
        print("   • Olahraga teratur")
        print("   • Menjaga hubungan sosial yang sehat")
    
    print("\n" + "=" * 80)
    print("⚠️  CATATAN PENTING:")
    print("   Aplikasi ini adalah prototipe untuk tujuan edukasi dan penelitian")
    print("   Program Kreativitas Mahasiswa (PKM) dalam bidang Penerapan IPTEK.")
    print("   Tidak menggantikan konsultasi dengan profesional kesehatan mental.")
    print("=" * 80 + "\n")
    
    input("Tekan ENTER untuk kembali ke menu utama...")


# ==============================================================================
# FUNGSI TES BIG FIVE
# ==============================================================================

def mulai_tes_bigfive():
    """Menjalankan tes Big Five dengan 60 pertanyaan (skala 1-5)"""
    
    tampilkan_header("TES BIG FIVE PERSONALITY (BFI-2)")
    
    # Tampilkan instruksi
    print("📋 INSTRUKSI:")
    print("   Di bawah ini adalah sejumlah karakteristik yang mungkin menggambarkan")
    print("   diri Anda atau mungkin juga tidak. Silakan tunjukkan seberapa setuju")
    print("   Anda bahwa karakteristik berikut menggambarkan diri Anda.\n")
    print("   Skala Jawaban:")
    print("   1 = Sangat tidak setuju")
    print("   2 = Sedikit tidak setuju")
    print("   3 = Netral")
    print("   4 = Sedikit setuju")
    print("   5 = Sangat setuju\n")
    print("   Setiap pertanyaan diawali dengan: 'Saya adalah seseorang yang...'\n")
    
    input("Tekan ENTER untuk memulai...")
    
    # Ambil pertanyaan
    pertanyaan = get_bigfive_questions()
    
    # Dictionary untuk menyimpan skor per trait
    skor = {'E': 0, 'A': 0, 'C': 0, 'N': 0, 'O': 0}
    
    # Loop untuk setiap pertanyaan
    for i, item in enumerate(pertanyaan, 1):
        tampilkan_header(f"TES BIG FIVE - Pertanyaan {i}/{len(pertanyaan)}")
        
        print(f"Saya adalah seseorang yang {item['p']}\n")
        print("Pilihan:")
        print("  1. Sangat tidak setuju")
        print("  2. Sedikit tidak setuju")
        print("  3. Netral")
        print("  4. Sedikit setuju")
        print("  5. Sangat setuju\n")
        
        # Input jawaban dengan validasi
        jawaban = input_pilihan("Pilih jawaban (1-5): ", ['1', '2', '3', '4', '5'])
        
        # Hitung skor
        trait = item['trait']
        nilai = int(jawaban)
        
        # Jika reversed item, balik skornya (1→5, 2→4, 3→3, 4→2, 5→1)
        if item['r']:
            nilai = 6 - nilai
        
        skor[trait] += nilai
    
    # Tampilkan hasil
    tampilkan_hasil_bigfive(skor)

def tampilkan_hasil_bigfive(skor: Dict[str, int]):
    """Menampilkan hasil tes Big Five dengan interpretasi lengkap"""
    
    # Hitung rata-rata skor (setiap trait punya 12 item)
    avg_skor = {trait: skor[trait] / 12 for trait in skor}
    
    def get_trait_level(score: float) -> str:
        """Menentukan tingkat trait"""
        if score < 2.5:
            return "Rendah"
        elif score < 3.5:
            return "Sedang"
        else:
            return "Tinggi"
    
    def get_trait_descriptions(trait: str, score: float) -> Tuple[str, str, str]:
        """Memberikan nama, penjelasan, dan interpretasi trait"""
        descriptions = {
            'E': {
                'name': 'EXTRAVERSION (Ekstraversi)',
                'meaning': 'Mengukur seberapa aktif dan antusias Anda dalam berinteraksi sosial serta mencari stimulasi dari lingkungan luar.',
                'high': 'Anda ramah, aktif, dan suka bersosialisasi. Anda merasa berenergi saat bersama orang lain dan cenderung ekspresif dalam menyampaikan pemikiran.',
                'low': 'Anda lebih pendiam dan menikmati waktu sendiri. Anda lebih suka lingkungan yang tenang dan memilih interaksi sosial yang bermakna.'
            },
            'A': {
                'name': 'AGREEABLENESS (Keramahan)',
                'meaning': 'Mengukur kecenderungan Anda untuk bersikap kooperatif, empatik, dan menghargai hubungan harmonis dengan orang lain.',
                'high': 'Anda penuh kasih, kooperatif, dan mudah percaya. Anda peduli terhadap kesejahteraan orang lain dan cenderung mengutamakan harmoni dalam hubungan.',
                'low': 'Anda lebih skeptis dan kompetitif. Anda mengutamakan kebenaran daripada harmoni sosial dan tidak ragu untuk mengungkapkan pendapat yang berbeda.'
            },
            'C': {
                'name': 'CONSCIENTIOUSNESS (Kehati-hatian)',
                'meaning': 'Mengukur tingkat organisasi, tanggung jawab, dan disiplin diri Anda dalam mencapai tujuan.',
                'high': 'Anda terorganisir, dapat diandalkan, dan gigih. Anda menyelesaikan tugas dengan baik, terencana, dan memiliki disiplin diri yang kuat.',
                'low': 'Anda lebih spontan dan fleksibel. Anda tidak terlalu khawatir tentang kerapian dan jadwal, lebih suka mengikuti alur dan beradaptasi dengan situasi.'
            },
            'N': {
                'name': 'NEUROTICISM (Stabilitas Emosional)',
                'meaning': 'Mengukur kecenderungan Anda mengalami emosi negatif seperti kecemasan, kesedihan, atau ketidakstabilan emosional. Skor rendah menunjukkan stabilitas emosional yang baik.',
                'high': 'Anda cenderung mengalami emosi negatif seperti cemas dan stress. Anda sensitif terhadap tekanan dan mungkin lebih mudah merasa khawatir tentang berbagai hal.',
                'low': 'Anda stabil secara emosional dan tenang. Anda jarang merasa cemas atau tertekan dan cenderung tetap tenang dalam menghadapi tantangan.'
            },
            'O': {
                'name': 'OPENNESS (Keterbukaan)',
                'meaning': 'Mengukur seberapa terbuka Anda terhadap pengalaman baru, ide-ide kreatif, dan keragaman perspektif.',
                'high': 'Anda kreatif, ingin tahu, dan terbuka pada pengalaman baru. Anda menikmati ide-ide abstrak, seni, dan eksplorasi intelektual.',
                'low': 'Anda lebih praktis dan konvensional. Anda lebih suka hal-hal yang sudah dikenal dan terbukti, serta cenderung fokus pada hal-hal konkret dan aplikatif.'
            }
        }
        
        desc = descriptions[trait]
        
        # Interpretasi: Skor < 2.5 = Rendah, Skor >= 3.5 = Tinggi, dazn 2.5 s/d 3.49 = Sedang
        if score >= 3.5:
            interpretation = desc['high']
        elif score < 2.5:
            interpretation = desc['low']
        else: # Antara 2.5 dan 3.49
            interpretation = "Anda berada di tingkat sedang, menunjukkan keseimbangan antara kedua sisi."
            if trait == 'N': # Penjelasan khusus untuk Neuroticism Sedang
                interpretation = "Anda berada di tingkat sedang, umumnya stabil secara emosional namun terkadang bisa sensitif terhadap stres."

        return desc['name'], desc['meaning'], interpretation
    
    # Tampilkan hasil
    tampilkan_header("HASIL TES BIG FIVE PERSONALITY")
    
    print("📊 TENTANG BIG FIVE:")
    print("   Model kepribadian Big Five adalah model yang paling teruji secara ilmiah")
    print("   dan digunakan secara luas dalam psikologi. Hasil ini menggambarkan lima")
    print("   dimensi utama kepribadian Anda.\n")
    
    # Tampilkan hasil untuk setiap trait
    for trait in ['E', 'A', 'C', 'N', 'O']:
        score = avg_skor[trait]
        level = get_trait_level(score)
        name, meaning, interpretation = get_trait_descriptions(trait, score)
        
        print("=" * 80)
        print(name)
        print("=" * 80)
        print(f"Skor Rata-rata: {score:.2f} / 5.00")
        print(f"Tingkat: {level}")
        print()
        
        # Progress bar visual
        bar_length = int(score * 10)  # Max 50 karakter (skala 0-5 -> 0-50)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        print(f"[{bar}] {(score/5)*100:.1f}%")
        print()
        
        print(f"Penjelasan: {meaning}")
        print()
        print(f"Interpretasi: {interpretation}")
        print()
    
    # Interpretasi umum
    print("=" * 80)
    print("INTERPRETASI UMUM")
    print("=" * 80)
    print("Setiap orang memiliki kombinasi unik dari kelima dimensi ini.")
    print("Tidak ada skor yang 'lebih baik' atau 'lebih buruk' - setiap kepribadian")
    print("memiliki kekuatan dan tantangannya sendiri.")
    print()
    print("Hasil tes ini dapat membantu Anda memahami diri sendiri lebih baik,")
    print("namun ingatlah bahwa kepribadian adalah hal yang kompleks dan dapat")
    print("berkembang seiring waktu.")
    
    print("\n" + "=" * 80)
    print("⚠️  CATATAN PENTING:")
    print("   Aplikasi ini adalah prototipe untuk tujuan edukasi dan penelitian")
    print("   Program Kreativitas Mahasiswa (PKM) dalam bidang Penerapan IPTEK.")
    print("   Hasil tes ini tidak menggantikan konsultasi dengan profesional")
    print("   kesehatan mental atau psikolog berlisensi.")
    print("=" * 80 + "\n")
    
    input("Tekan ENTER untuk kembali ke menu utama...")


# ==============================================================================
# MENU UTAMA
# ==============================================================================

def tampilkan_menu_utama():
    """Menampilkan menu utama aplikasi"""
    tampilkan_header("MENTALCARE AI - Aplikasi Kesehatan Mental")
    
    print("🧠 Selamat Datang di MentalCare AI")
    print("   Aplikasi untuk skrining kesehatan mental dan tes kepribadian\n")
    print("   Dikembangkan oleh:")
    print("   • Prodi Informatika UMM")
    print("   • Prodi Psikologi UMM")
    print("   Program Kreativitas Mahasiswa (PKM) - Penerapan IPTEK\n")
    
    print("=" * 80)
    print("MENU UTAMA")
    print("=" * 80)
    print("1. Skrining Kesehatan Mental (DASS) - 100 pertanyaan")
    print("2. Tes Big Five Personality (BFI-2) - 60 pertanyaan")
    print("3. Tentang Aplikasi")
    print("4. Keluar\n")

def tampilkan_tentang():
    """Menampilkan informasi tentang aplikasi"""
    tampilkan_header("TENTANG MENTALCARE AI")
    
    print("📱 MENTALCARE AI v2.1")
    print("   Aplikasi Skrining Kesehatan Mental Berbasis AI\n")
    
    print("=" * 80)
    print("FITUR UTAMA")
    print("=" * 80)
    print("1. Skrining Kesehatan Mental (DASS)")
    print("   • Menggunakan 100 pertanyaan komprehensif (bukan DASS-21/42 standar)")
    print("   • Mengukur Depresi, Anxiety (Kecemasan), dan Stress")
    print("   • Hasil dengan interpretasi dan rekomendasi berdasarkan skoring DASS-21")
    print()
    print("2. Tes Big Five Personality (BFI-2)")
    print("   • Tes dengan validitas dan reliabilitas ilmiah yang paling tinggi")
    print("   • 60 pertanyaan dari Big Five Inventory-2")
    print("   • Mengukur 5 dimensi kepribadian:")
    print("     - Extraversion (Ekstraversi)")
    print("     - Agreeableness (Keramahan)")
    print("     - Conscientiousness (Kehati-hatian)")
    print("     - Neuroticism (Stabilitas Emosional)")
    print("     - Openness (Keterbukaan)")
    print()
    
    print("=" * 80)
    print("TIM PENGEMBANG")
    print("=" * 80)
    print("Mahasiswa Prodi Informatika UMM:")
    print("  • [Nama Mahasiswa Informatika]")
    print()
    print("Mahasiswa Prodi Psikologi UMM:")
    print("  • [Nama Mahasiswa Psikologi 1]")
    print("  • [Nama Mahasiswa Psikologi 2]")
    print()
    
    print("=" * 80)
    print("LAYANAN BANTUAN DARURAT")
    print("=" * 80)
    print("Jika Anda atau seseorang yang Anda kenal membutuhkan bantuan segera:")
    print()
    print("📞 SEJIWA: 119 (ekstensi 8)")
    print("📞 HALO KEMENKES:")
    print("   • Telepon: 1500 567")
    print("   • WhatsApp: +62 812 6050 0567")
    print("   • SMS: +62 812 8156 2620")
    print()
    
    print("=" * 80)
    print("DISCLAIMER")
    print("=" * 80)
    print("⚠️  PENTING:")
    print("   • Aplikasi ini adalah PROTOTIPE untuk tujuan edukasi dan penelitian PKM")
    print("   • Hasil skrining BUKAN diagnosis medis")
    print("   • Tidak menggantikan konsultasi dengan profesional kesehatan mental")
    print("   • Jika Anda mengalami gejala yang mengkhawatirkan, segera konsultasikan")
    print("     dengan psikolog atau profesional kesehatan mental")
    print("=" * 80 + "\n")
    
    input("Tekan ENTER untuk kembali ke menu utama...")


# ==============================================================================
# MAIN PROGRAM
# ==============================================================================

def main():
    """Fungsi utama yang menjalankan aplikasi"""
    
    while True:
        tampilkan_menu_utama()
        
        # Input pilihan menu
        pilihan = input_pilihan("Pilih menu (1-4): ", ['1', '2', '3', '4'])
        
        if pilihan == '1':
            # Skrining DASS
            mulai_skrining_dass()
            
        elif pilihan == '2':
            # Tes Big Five
            mulai_tes_bigfive()
            
        elif pilihan == '3':
            # Tentang aplikasi
            tampilkan_tentang()
            
        elif pilihan == '4':
            # Keluar dari aplikasi
            tampilkan_header("TERIMA KASIH")
            print("✅ Terima kasih telah menggunakan MentalCare AI!")
            print("   Jaga kesehatan mental Anda selalu. 💚\n")
            print("   Dikembangkan oleh Tim PKM Informatika & Psikologi UMM")
            print("=" * 80)
            sys.exit(0)


# ==============================================================================
# ENTRY POINT - Di sinilah program dimulai (BAGIAN YANG DIPERBAIKI)
# ==============================================================================

if __name__ == "__main__":  # <-- KESALAHAN UTAMA ADA DI SINI
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C
        print("\n\n⚠️  Program dihentikan oleh user.")
        print("Terima kasih telah menggunakan MentalCare AI!")
        sys.exit(0)
    except Exception as e:
        # Handle error lainnya
        print(f"\n❌ Terjadi error: {str(e)}")
        print("Mohon hubungi pengembang jika masalah berlanjut.")
        sys.exit(1)