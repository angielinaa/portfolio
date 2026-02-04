# Nama File: pkm_app.py
# Deskripsi: Prototipe aplikasi untuk skrining kesehatan mental dan tes kepribadian MBTI.
# Versi: 2.0 (Integrasi pertanyaan gaya Sakinorva)

# ==============================================================================
# BAGIAN FUNGSI-FUNGSI UTAMA
# ==============================================================================

def mulai_skrining():
    """Menjalankan alur pertanyaan skrining kesehatan mental."""
    # ... (Fungsi ini tetap sama seperti sebelumnya, tidak perlu diubah) ...
    pertanyaan = [
        "Dalam seminggu terakhir, seberapa sering Anda merasa cemas atau khawatir berlebihan?",
        "Dalam seminggu terakhir, seberapa sering Anda merasa sedih atau putus asa?",
        "Dalam seminggu terakhir, seberapa sering Anda kehilangan minat atau kesenangan dalam melakukan sesuatu?",
        "Dalam seminggu terakhir, seberapa sering Anda merasa lelah atau tidak bertenaga?",
        "Dalam seminggu terakhir, seberapa sering Anda kesulitan untuk tidur atau tidur terlalu banyak?"
    ]
    opsi_jawaban = { "1": "Tidak pernah (0 hari)", "2": "Beberapa hari (1-2 hari)", "3": "Sebagian besar hari (3-4 hari)", "4": "Hampir setiap hari (5-7 hari)" }
    skor_jawaban = { "1": 0, "2": 1, "3": 2, "4": 3 }
    total_skor = 0
    
    print("\n--- Mulai Skrining Kesehatan Diri ---")
    print("Jawablah pertanyaan berikut berdasarkan apa yang Anda rasakan selama SEMINGGU TERAKHIR.")
    
    for i, p in enumerate(pertanyaan):
        print(f"\nPertanyaan #{i+1}: {p}")
        for nomor, teks in opsi_jawaban.items():
            print(f"  {nomor}. {teks}")
        while True:
            jawaban_user = input("Pilih jawaban (1/2/3/4): ")
            if jawaban_user in opsi_jawaban:
                total_skor += skor_jawaban[jawaban_user]
                break
            else:
                print("Input tidak valid. Mohon masukkan angka 1, 2, 3, atau 4.")
    interpretasi_hasil_skrining(total_skor)

def interpretasi_hasil_skrining(skor):
    """Memberikan interpretasi berdasarkan total skor skrining."""
    # ... (Fungsi ini tetap sama seperti sebelumnya, tidak perlu diubah) ...
    print("\n--- Hasil Skrining Anda ---")
    print(f"Total skor Anda adalah: {skor}")
    if skor <= 4:
        print("Interpretasi: Gejala yang Anda rasakan berada pada tingkat minimal. Tetap jaga kesehatan mental Anda!")
    elif skor <= 9:
        print("Interpretasi: Anda mengalami gejala ringan. Dianjurkan untuk lebih memperhatikan kondisi diri dan mencari cara relaksasi.")
    elif skor <= 14:
        print("Interpretasi: Anda mengalami gejala tingkat sedang. Pertimbangkan untuk berbicara dengan teman terpercaya atau keluarga.")
    else:
        print("Interpretasi: Anda mengalami gejala yang cukup signifikan. Sangat disarankan untuk berkonsultasi dengan profesional.")
    print("\nINGAT: Hasil ini bukan diagnosis medis. Ini adalah alat bantu untuk refleksi diri.")

def tentukan_tipe_mbti(skor):
    """Menentukan 4 huruf tipe kepribadian berdasarkan skor tertinggi."""
    tipe = ""
    tipe += "E" if skor['E'] > skor['I'] else "I"
    tipe += "N" if skor['N'] > skor['S'] else "S"
    tipe += "F" if skor['F'] > skor['T'] else "T"
    tipe += "P" if skor['P'] > skor['J'] else "J"
    return tipe

def mulai_tes_mbti():
    """Menjalankan alur tes kepribadian MBTI dengan pertanyaan adaptasi Sakinorva."""
    
    # Daftar pertanyaan yang diadaptasi dari gaya Sakinorva.
    # Tim psikologi bisa meninjau dan menyesuaikan daftar ini.
    pertanyaan_mbti = [
        # Introversion (I) vs. Extraversion (E)
        {"p": "Anda lebih suka menghabiskan waktu...", "o1": ("Dalam kelompok besar dan aktif", "E"), "o2": ("Sendirian atau dengan beberapa teman dekat", "I")},
        {"p": "Saat di pesta, Anda cenderung...", "o1": ("Berbicara dengan banyak orang berbeda", "E"), "o2": ("Berbicara mendalam dengan satu atau dua orang", "I")},
        {"p": "Anda merasa mendapatkan energi dari...", "o1": ("Berinteraksi dengan dunia luar", "E"), "o2": ("Waktu refleksi dan kesendirian", "I")},
        {"p": "Dalam diskusi, Anda biasanya...", "o1": ("Cepat merespons dan menyuarakan pikiran", "E"), "o2": ("Memikirkan dulu baik-baik sebelum berbicara", "I")},
        {"p": "Lingkaran pertemanan Anda...", "o1": ("Luas dan mencakup banyak kenalan", "E"), "o2": ("Kecil tapi dalam dan erat", "I")},

        # Sensing (S) vs. Intuition (N)
        {"p": "Anda lebih mempercayai...", "o1": ("Pengalaman langsung dan fakta konkret", "S"), "o2": ("Inspirasi, firasat, dan pola tersembunyi", "N")},
        {"p": "Saat belajar hal baru, Anda lebih suka...", "o1": ("Mengikuti instruksi langkah demi langkah", "S"), "o2": ("Melihat gambaran besar dan konsepnya", "N")},
        {"p": "Anda cenderung lebih fokus pada...", "o1": ("Realitas saat ini dan apa yang nyata", "S"), "o2": ("Kemungkinan masa depan dan apa yang bisa terjadi", "N")},
        {"p": "Anda mendeskripsikan sesuatu secara...", "o1": ("Literal dan detail", "S"), "o2": ("Metaforis dan imajinatif", "N")},
        {"p": "Anda lebih tertarik pada...", "o1": ("Penerapan praktis dari sebuah ide", "S"), "o2": ("Teori dan ide itu sendiri", "N")},

        # Thinking (T) vs. Feeling (F)
        {"p": "Saat membuat keputusan, Anda lebih dipandu oleh...", "o1": ("Logika, objektivitas, dan prinsip keadilan", "T"), "o2": ("Nilai-nilai pribadi, empati, dan dampaknya pada orang lain", "F")},
        {"p": "Saat memberikan kritik, Anda lebih mengutamakan...", "o1": ("Kejujuran dan kebenaran, meskipun pahit", "T"), "o2": ("Menjaga perasaan dan keharmonisan", "F")},
        {"p": "Anda lebih mudah terpengaruh oleh...", "o1": ("Argumen yang kuat dan logis", "T"), "o2": ("Cerita yang menyentuh dan penuh perasaan", "F")},
        {"p": "Anda melihat diri Anda sebagai orang yang...", "o1": ("Tegas dan berkepala dingin", "T"), "o2": ("Hangat dan berhati lembut", "F")},
        {"p": "Tujuan utama Anda adalah...", "o1": ("Menjadi orang yang kompeten dan efisien", "T"), "o2": ("Menjadi orang yang baik dan otentik", "F")},

        # Judging (J) vs. Perceiving (P)
        {"p": "Gaya hidup Anda lebih...", "o1": ("Teratur, terencana, dan terjadwal", "J"), "o2": ("Spontan, fleksibel, dan mudah beradaptasi", "P")},
        {"p": "Saat mengerjakan tugas, Anda lebih suka...", "o1": ("Menyelesaikannya jauh sebelum tenggat waktu", "J"), "o2": ("Bekerja di bawah tekanan mendekati tenggat waktu", "P")},
        {"p": "Anda lebih merasa nyaman ketika...", "o1": ("Keputusan sudah dibuat dan segala sesuatu sudah pasti", "J"), "o2": ("Pilihan tetap terbuka dan ada ruang untuk perubahan", "P")},
        {"p": "Daftar tugas (to-do list) bagi Anda adalah...", "o1": ("Sesuatu yang harus diikuti dan diselesaikan", "J"), "o2": ("Sekadar panduan yang bisa berubah sewaktu-waktu", "P")},
        {"p": "Anda lebih suka lingkungan kerja yang...", "o1": ("Memiliki struktur dan tujuan yang jelas", "J"), "o2": ("Memberikan kebebasan dan sedikit aturan", "P")},
    ]
    
    skor = {'I': 0, 'E': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    
    print("\n--- Mulai Tes Kepribadian MBTI ---")
    print("Pilih jawaban yang paling sesuai dengan diri Anda. Tes ini terdiri dari 20 pertanyaan.")
    
    for i, q in enumerate(pertanyaan_mbti):
        print(f"\nPertanyaan #{i+1}: {q['p']}")
        print(f"  1. {q['o1'][0]}")
        print(f"  2. {q['o2'][0]}")
        
        while True:
            jawaban_user = input("Pilih jawaban (1/2): ")
            if jawaban_user == '1':
                dimensi = q['o1'][1]
                skor[dimensi] += 1
                break
            elif jawaban_user == '2':
                dimensi = q['o2'][1]
                skor[dimensi] += 1
                break
            else:
                print("Input tidak valid. Mohon masukkan angka 1 atau 2.")
                
    hasil_tipe = tentukan_tipe_mbti(skor)
    
    print("\n--- Hasil Tes Kepribadian Anda ---")
    print(f"Tipe kepribadian Anda kemungkinan adalah: {hasil_tipe}")
    print(f"Detail Skor: E({skor['E']}) I({skor['I']}), N({skor['N']}) S({skor['S']}), F({skor['F']}) T({skor['T']}), P({skor['P']}) J({skor['J']})")
    print("\nCATATAN: Tes ini hanya untuk hiburan dan refleksi diri, bukan alat psikometrik yang tervalidasi secara klinis.")

# ==============================================================================
# PROGRAM UTAMA (MAIN LOOP)
# ==============================================================================

def main():
    """Fungsi utama untuk menjalankan seluruh aplikasi."""
    print("==============================================")
    print("  Selamat Datang di Aplikasi Well-Being Check ")
    print("==============================================")
    print("Aplikasi ini bertujuan untuk membantu Anda merefleksikan kondisi diri.")
    
    while True:
        print("\nMenu Utama:")
        print("1. Skrining Awal Kesehatan Mental")
        print("2. Tes Kepribadian MBTI (Gaya Sakinorva)")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1/2/3): ")
        
        if pilihan == '1':
            mulai_skrining()
        elif pilihan == '2':
            mulai_tes_mbti()
        elif pilihan == '3':
            print("\nTerima kasih telah menggunakan aplikasi ini. Jaga diri Anda!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

# Menjalankan program utama saat file dieksekusi
if __name__ == "__main__":
    main()