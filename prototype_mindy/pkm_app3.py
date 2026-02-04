# Nama File: pkm_app.py
# Deskripsi: Prototipe aplikasi untuk skrining kesehatan mental dan tes kepribadian MBTI.
# Versi: 6.1 (Revisi Alur Kembali ke Menu)

# ==============================================================================
# BAGIAN FUNGSI-FUNGSI UTAMA
# ==============================================================================

def mulai_skrining_dass():
    """Menjalankan alur skrining kesehatan mental berbasis DASS dengan 100 pertanyaan."""
    
    # BANK SOAL SKRINING - 100 PERTANYAAN
    # Kategori: 'D' = Depresi, 'A' = Kecemasan (Anxiety), 'S' = Stres
    pernyataan_skrining = [
        # Depresi
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
        # Kecemasan (Anxiety)
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
        # Stres
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
    
    skor = {'D': 0, 'A': 0, 'S': 0}
    
    skala_jawaban = {
        "0": "Tidak pernah atau sama sekali tidak berlaku untuk saya",
        "1": "Kadang-kadang berlaku untuk saya",
        "2": "Sering berlaku untuk saya",
        "3": "Hampir selalu atau sangat berlaku untuk saya"
    }

    print(f"\n--- Skrining Awal Kesehatan Mental ({len(pernyataan_skrining)} Pertanyaan) ---")
    print("Untuk setiap pernyataan, jawablah berdasarkan pengalaman Anda selama SEMINGGU TERAKHIR.")
    
    for i, item in enumerate(pernyataan_skrining):
        print(f"\nPernyataan #{i+1}: {item['p']}")
        for nomor, teks in skala_jawaban.items():
            print(f"  {nomor}. {teks}")
        
        while True:
            jawaban_user = input("Pilih jawaban (0-3): ")
            if jawaban_user in skala_jawaban:
                kategori = item['k']
                skor[kategori] += int(jawaban_user)
                break
            else:
                print("Input tidak valid. Mohon masukkan angka dari 0 hingga 3.")
    
    skor['D'] *= 2
    skor['A'] *= 2
    skor['S'] *= 2
    
    interpretasi_hasil_dass(skor)

def interpretasi_hasil_dass(skor):
    """Memberikan interpretasi berdasarkan skor DASS."""
    
    def get_level(score, thresholds):
        if score <= thresholds[0]: return "Normal"
        if score <= thresholds[1]: return "Ringan"
        if score <= thresholds[2]: return "Sedang"
        if score <= thresholds[3]: return "Parah"
        return "Sangat Parah"

    thresholds_depresi = (9, 13, 20, 27)
    thresholds_kecemasan = (7, 9, 14, 19)
    thresholds_stres = (14, 18, 25, 33)

    level_d = get_level(skor['D'], thresholds_depresi)
    level_a = get_level(skor['A'], thresholds_kecemasan)
    level_s = get_level(skor['S'], thresholds_stres)

    print("\n--- Hasil Skrining Anda ---")
    print("Hasil ini BUKAN diagnosis medis, tapi indikator untuk refleksi diri.")
    
    print("\nDEPRESI")
    print(f"  - Skor Anda: {skor['D']}")
    print(f"  - Tingkat: {level_d}")
    
    print("\nKECEMASAN (ANXIETY)")
    print(f"  - Skor Anda: {skor['A']}")
    print(f"  - Tingkat: {level_a}")

    print("\nSTRES")
    print(f"  - Skor Anda: {skor['S']}")
    print(f"  - Tingkat: {level_s}")

    print("\nREKOMENDASI: Jika salah satu atau lebih hasil Anda berada di tingkat 'Sedang' atau lebih tinggi, sangat disarankan untuk berbicara dengan konselor, psikolog, atau profesional kesehatan mental.")

def tentukan_tipe_mbti(skor):
    """Menentukan 4 huruf tipe kepribadian berdasarkan skor."""
    tipe = ""
    tipe += "E" if skor['E'] > skor['I'] else "I"
    tipe += "N" if skor['N'] > skor['S'] else "S"
    tipe += "F" if skor['F'] > skor['T'] else "T"
    tipe += "P" if skor['P'] > skor['J'] else "J"
    return tipe

def mulai_tes_mbti_skala():
    """Menjalankan alur tes MBTI dengan sistem skoring skala dan bank soal ultimate."""
    pernyataan_mbti = [
        # --- Extraversion (E) vs Introversion (I) ---
        {"p": "Saya mudah memulai percakapan dengan orang yang baru saya temui.", "d": ("E", "I")},
        {"p": "Saya sering tenggelam dalam pikiran dan imajinasi saya sendiri.", "d": ("I", "E")},
        {"p": "Saya merasa paling berenergi setelah menghabiskan waktu sendirian.", "d": ("I", "E")},
        {"p": "Saya lebih suka lingkungan yang ramai dan penuh aktivitas.", "d": ("E", "I")},
        {"p": "Saya tidak keberatan menjadi pusat perhatian.", "d": ("E", "I")},
        {"p": "Saya cenderung memikirkan sesuatu baik-baik sebelum mengatakannya.", "d": ("I", "E")},
        {"p": "Saya lebih suka mengekspresikan diri secara tertulis daripada lisan.", "d": ("I", "E")},
        {"p": "Saya cepat bosan jika sendirian terlalu lama.", "d": ("E", "I")},
        {"p": "Berbicara dengan banyak orang di sebuah pesta membuat saya bersemangat.", "d": ("E", "I")},
        {"p": "Saya menganggap diri saya sebagai orang yang privat dan tertutup.", "d": ("I", "E")},
        {"p": "Saya seringkali 'berpikir sambil berbicara'.", "d": ("E", "I")},
        {"p": "Aktivitas sosial yang intens membuat energi saya terkuras.", "d": ("I", "E")},
        {"p": "Saya lebih suka mendengarkan daripada berbicara.", "d": ("I", "E")},
        {"p": "Saya memiliki lingkaran pertemanan yang luas.", "d": ("E", "I")},
        {"p": "Saya butuh waktu untuk 'memulihkan diri' setelah bersosialisasi.", "d": ("I", "E")},
        {"p": "Saya lebih suka perayaan ulang tahun yang besar daripada yang kecil dan intim.", "d": ("E", "I")},
        {"p": "Saya sering merasa sulit untuk keluar dan bertemu orang baru.", "d": ("I", "E")},
        {"p": "Saya adalah orang yang mudah didekati dan terbuka.", "d": ("E", "I")},
        {"p": "Saya memproses informasi dengan membicarakannya dengan orang lain.", "d": ("E", "I")},
        {"p": "Saya merasa nyaman berada dalam keheningan bersama orang lain.", "d": ("I", "E")},
        {"p": "Saya lebih memilih pekerjaan yang memungkinkan banyak interaksi sosial.", "d": ("E", "I")},
        {"p": "Saya seringkali melewatkan panggilan telepon dari nomor tak dikenal.", "d": ("I", "E")},
        {"p": "Saya merasa lebih hidup saat berada di tengah keramaian.", "d": ("E", "I")},
        {"p": "Saya sering merasa kewalahan di lingkungan yang terlalu merangsang.", "d": ("I", "E")},
        {"p": "Saya biasanya yang mengambil inisiatif untuk memperkenalkan diri.", "d": ("E", "I")},
        {"p": "Saya lebih memilih hubungan yang dalam dengan segelintir orang.", "d": ("I", "E")},
        {"p": "Saya merasa ide-ide saya menjadi lebih jelas saat saya menjelaskannya kepada orang lain.", "d": ("E", "I")},
        {"p": "Saya sering menganalisis percakapan di kepala saya setelah percakapan itu berakhir.", "d": ("I", "E")},
        {"p": "Saya menikmati kerja kelompok dan kolaborasi.", "d": ("E", "I")},
        {"p": "Pikiran terdalam saya hanya untuk diri saya sendiri atau orang yang sangat saya percayai.", "d": ("I", "E")},
        {"p": "Saya cenderung bertindak lebih dulu, baru berpikir kemudian.", "d": ("E", "I")},
        {"p": "Saya merenungkan banyak hal sebelum membuat keputusan.", "d": ("I", "E")},
        {"p": "Saya mudah mengungkapkan antusiasme saya secara verbal.", "d": ("E", "I")},
        {"p": "Saya lebih suka mengamati dari pinggir daripada terjun langsung ke tengah-tengah aksi.", "d": ("I", "E")},
        {"p": "Saya senang bertemu orang-orang baru di acara sosial.", "d": ("E", "I")},
        {"p": "Saya merasa percakapan ringan (small talk) itu melelahkan.", "d": ("I", "E")},
        {"p": "Saya merasa percaya diri saat berbicara di depan umum.", "d": ("E", "I")},
        # --- Sensing (S) vs Intuition (N) ---
        {"p": "Saya lebih tertarik pada ide-ide teoretis dan konsep-konsep abstrak.", "d": ("N", "S")},
        {"p": "Saya lebih praktis dan membumi dalam pendekatan saya terhadap kehidupan.", "d": ("S", "N")},
        {"p": "Saya lebih percaya pada fakta yang bisa dibuktikan daripada firasat.", "d": ("S", "N")},
        {"p": "Saya sering memikirkan makna tersembunyi atau pola di balik sesuatu.", "d": ("N", "S")},
        {"p": "Saya lebih fokus pada realitas saat ini daripada kemungkinan di masa depan.", "d": ("S", "N")},
        {"p": "Saya suka membayangkan berbagai skenario masa depan.", "d": ("N", "S")},
        {"p": "Saat mempelajari sesuatu, saya ingin tahu penerapan praktisnya.", "d": ("S", "N")},
        {"p": "Saya menikmati diskusi filosofis.", "d": ("N", "S")},
        {"p": "Saya cenderung memperhatikan detail-detail kecil yang orang lain lewatkan.", "d": ("S", "N")},
        {"p": "Saya lebih sering mengandalkan inspirasi saat bekerja.", "d": ("N", "S")},
        {"p": "Saya lebih suka instruksi yang jelas dan langkah-demi-langkah.", "d": ("S", "N")},
        {"p": "Saya sering melamun tentang hal-hal yang tidak berhubungan dengan situasi saat ini.", "d": ("N", "S")},
        {"p": "Saya adalah orang yang realistis.", "d": ("S", "N")},
        {"p": "Saya sering membaca yang tersirat.", "d": ("N", "S")},
        {"p": "Saya lebih suka menggunakan metode yang sudah teruji dan berhasil.", "d": ("S", "N")},
        {"p": "Saya sering merasa bahwa kenyataan itu membosankan.", "d": ("N", "S")},
        {"p": "Saya menghargai tradisi dan cara-cara konvensional.", "d": ("S", "N")},
        {"p": "Saya lebih tertarik pada 'apa yang bisa terjadi' daripada 'apa yang sudah ada'.", "d": ("N", "S")},
        {"p": "Saya mengingat peristiwa sebagai rangkaian fakta yang spesifik.", "d": ("S", "N")},
        {"p": "Saya mengingat peristiwa sebagai kesan atau perasaan keseluruhan.", "d": ("N", "S")},
        {"p": "Saya lebih suka bekerja dengan data dan angka daripada dengan simbol dan metafora.", "d": ("S", "N")},
        {"p": "Saya mudah melihat hubungan antara hal-hal yang tampaknya tidak berhubungan.", "d": ("N", "S")},
        {"p": "Saya lebih suka berbicara tentang hal-hal yang konkret.", "d": ("S", "N")},
        {"p": "Saya suka memikirkan asal-usul alam semesta dan makna kehidupan.", "d": ("N", "S")},
        {"p": "Saya merasa lebih nyaman dengan apa yang sudah diketahui daripada apa yang tidak diketahui.", "d": ("S", "N")},
        {"p": "Saya tertarik pada hal-hal baru dan belum teruji.", "d": ("N", "S")},
        {"p": "Saya percaya bahwa pengalaman adalah guru terbaik.", "d": ("S", "N")},
        {"p": "Saya percaya bahwa imajinasi adalah aset yang paling berharga.", "d": ("N", "S")},
        {"p": "Saya cenderung mengambil pernyataan orang lain secara harfiah.", "d": ("S", "N")},
        {"p": "Saya sering mencari makna yang lebih dalam dalam segala hal.", "d": ("N", "S")},
        {"p": "Saya lebih mengagumi keterampilan praktis daripada ide-ide orisinal.", "d": ("S", "N")},
        {"p": "Saya lebih mengagumi ide-ide orisinal daripada keterampilan praktis.", "d": ("N", "S")},
        {"p": "Saya memecahkan masalah dengan memeriksa detailnya dengan cermat.", "d": ("S", "N")},
        {"p": "Saya memecahkan masalah dengan melakukan brainstorming untuk kemungkinan-kemungkinan baru.", "d": ("N", "S")},
        {"p": "Saya lebih suka mendeskripsikan sesuatu dengan cara yang spesifik dan terukur.", "d": ("S", "N")},
        {"p": "Saya sering menggunakan analogi dan perumpamaan saat berbicara.", "d": ("N", "S")},
        {"p": "Saya lebih suka masa kini daripada masa depan.", "d": ("S", "N")},
        {"p": "Saya lebih suka masa depan daripada masa kini.", "d": ("N", "S")},
        # --- Thinking (T) vs Feeling (F) ---
        {"p": "Saya mengutamakan logika dan objektivitas saat membuat pilihan.", "d": ("T", "F")},
        {"p": "Keputusan saya sangat dipengaruhi oleh perasaan dan dampaknya pada orang lain.", "d": ("F", "T")},
        {"p": "Saya tidak ragu untuk menyampaikan kritik yang jujur jika itu diperlukan.", "d": ("T", "F")},
        {"p": "Menjaga keharmonisan dalam kelompok lebih penting daripada membuktikan siapa yang benar.", "d": ("F", "T")},
        {"p": "Saya merasa lebih penting untuk menjadi adil daripada disukai.", "d": ("T", "F")},
        {"p": "Saya sering menempatkan diri pada posisi orang lain.", "d": ("F", "T")},
        {"p": "Saya bisa tetap tenang dan tidak emosional dalam situasi sulit.", "d": ("T", "F")},
        {"p": "Saya mudah tersentuh oleh cerita atau film yang emosional.", "d": ("F", "T")},
        {"p": "Saya bangga dengan kemampuan saya untuk membuat keputusan yang tidak personal.", "d": ("T", "F")},
        {"p": "Saya selalu mempertimbangkan nilai-nilai pribadi saya saat mengambil keputusan.", "d": ("F", "T")},
        {"p": "Saya lebih termotivasi oleh pencapaian daripada oleh pujian.", "d": ("T", "F")},
        {"p": "Saya merasa sulit untuk mengatakan 'tidak' karena takut mengecewakan orang lain.", "d": ("F", "T")},
        {"p": "Analisis pro dan kontra adalah langkah pertama saya dalam memutuskan sesuatu.", "d": ("T", "F")},
        {"p": "Saya sering membuat keputusan berdasarkan intuisi atau perasaan saya.", "d": ("F", "T")},
        {"p": "Saya lebih suka efisiensi daripada kerja sama.", "d": ("T", "F")},
        {"p": "Saya mencari keaslian dan hubungan yang tulus dengan orang lain.", "d": ("F", "T")},
        {"p": "Saya bisa dengan mudah menunjukkan kelemahan dalam argumen orang lain.", "d": ("T", "F")},
        {"p": "Saya percaya bahwa kebaikan dan belas kasih adalah kunci dari segalanya.", "d": ("F", "T")},
        {"p": "Saya lebih suka kebenaran yang pahit daripada kebohongan yang manis.", "d": ("T", "F")},
        {"p": "Saya sering menghindari konfrontasi untuk menjaga perasaan orang lain.", "d": ("F", "T")},
        {"p": "Saya menilai situasi berdasarkan kriteria yang objektif.", "d": ("T", "F")},
        {"p": "Saya menilai situasi berdasarkan bagaimana hal itu akan mempengaruhi orang-orang yang terlibat.", "d": ("F", "T")},
        {"p": "Saya merasa sulit untuk memahami orang yang sangat emosional.", "d": ("T", "F")},
        {"p": "Saya merasa mudah terhubung dengan perasaan orang lain.", "d": ("F", "T")},
        {"p": "Saya lebih suka memberikan solusi yang logis daripada dukungan emosional.", "d": ("T", "F")},
        {"p": "Saya lebih suka memberikan dukungan emosional daripada solusi yang logis.", "d": ("F", "T")},
        {"p": "Saya menganggap penting untuk bersikap konsisten dan berprinsip.", "d": ("T", "F")},
        {"p": "Saya menganggap penting untuk bersikap fleksibel dan memahami keadaan.", "d": ("F", "T")},
        {"p": "Saya merasa puas ketika saya dapat menyelesaikan masalah yang kompleks.", "d": ("T", "F")},
        {"p": "Saya merasa puas ketika saya dapat membantu orang lain.", "d": ("F", "T")},
        {"p": "Saya cenderung menyembunyikan perasaan saya.", "d": ("T", "F")},
        {"p": "Saya cenderung memakai hati saya di lengan baju saya (mudah menunjukkan perasaan).", "d": ("F", "T")},
        {"p": "Kritik tidak terlalu mempengaruhi saya secara pribadi.", "d": ("T", "F")},
        {"p": "Kritik bisa sangat menyakitkan bagi saya.", "d": ("F", "T")},
        {"p": "Saya tertarik pada sains dan teknologi.", "d": ("T", "F")},
        {"p": "Saya tertarik pada seni dan humaniora.", "d": ("F", "T")},
        {"p": "Dalam konflik, fokus saya adalah pada masalah itu sendiri.", "d": ("T", "F")},
        {"p": "Dalam konflik, fokus saya adalah pada perasaan orang-orang yang terlibat.", "d": ("F", "T")},
        # --- Judging (J) vs Perceiving (P) ---
        {"p": "Saya suka membuat daftar tugas dan mengikuti rencana yang telah ditetapkan.", "d": ("J", "P")},
        {"p": "Saya lebih suka membiarkan pilihan saya tetap terbuka dan tidak terburu-buru mengambil keputusan.", "d": ("P", "J")},
        {"p": "Saya merasa tidak nyaman jika segala sesuatunya tidak terorganisir.", "d": ("J", "P")},
        {"p": "Saya menikmati spontanitas dan kejutan dalam hidup.", "d": ("P", "J")},
        {"p": "Saya lebih suka menyelesaikan pekerjaan terlebih dahulu sebelum bersantai.", "d": ("J", "P")},
        {"p": "Saya seringkali menunda-nunda pekerjaan hingga menit terakhir.", "d": ("P", "J")},
        {"p": "Saya merasa puas setelah sebuah keputusan dibuat.", "d": ("J", "P")},
        {"p": "Saya melihat tenggat waktu (deadline) sebagai sesuatu yang fleksibel.", "d": ("P", "J")},
        {"p": "Saya lebih menyukai kehidupan yang terstruktur dan dapat diprediksi.", "d": ("J", "P")},
        {"p": "Saya mudah beradaptasi dengan perubahan rencana yang tiba-tiba.", "d": ("P", "J")},
        {"p": "Saya tidak suka membiarkan pekerjaan menggantung tanpa kepastian.", "d": ("J", "P")},
        {"p": "Saya sering mencampuradukkan antara waktu kerja dan waktu bermain.", "d": ("P", "J")},
        {"p": "Saya selalu merencanakan perjalanan saya secara detail.", "d": ("J", "P")},
        {"p": "Saya suka menjelajahi tempat baru tanpa rencana yang pasti.", "d": ("P", "J")},
        {"p": "Memiliki rutinitas harian membuat saya merasa nyaman.", "d": ("J", "P")},
        {"p": "Saya merasa terkekang oleh terlalu banyak aturan dan struktur.", "d": ("P", "J")},
        {"p": "Saya lebih suka mengetahui apa yang diharapkan dari saya.", "d": ("J", "P")},
        {"p": "Saya suka menjaga pilihan saya tetap terbuka selama mungkin.", "d": ("P", "J")},
        {"p": "Saya merasa stres jika rencana saya terganggu.", "d": ("J", "P")},
        {"p": "Saya melihat aturan sebagai saran, bukan perintah.", "d": ("P", "J")},
        {"p": "Saya biasanya tepat waktu.", "d": ("J", "P")},
        {"p": "Saya sering terlambat.", "d": ("P", "J")},
        {"p": "Saya suka menyelesaikan satu tugas sebelum memulai yang lain.", "d": ("J", "P")},
        {"p": "Saya suka mengerjakan beberapa tugas secara bersamaan.", "d": ("P", "J")},
        {"p": "Saya lebih suka kepastian daripada ketidakpastian.", "d": ("J", "P")},
        {"p": "Saya lebih suka ketidakpastian daripada kepastian.", "d": ("P", "J")},
        {"p": "Saya membuat keputusan dengan cepat.", "d": ("J", "P")},
        {"p": "Saya butuh banyak waktu untuk membuat keputusan.", "d": ("P", "J")},
        {"p": "Saya menikmati lingkungan kerja yang terorganisir.", "d": ("J", "P")},
        {"p": "Saya menikmati lingkungan kerja yang fleksibel.", "d": ("P", "J")},
        {"p": "Saya lebih suka mengikuti jadwal.", "d": ("J", "P")},
        {"p": "Saya lebih suka mengikuti kata hati.", "d": ("P", "J")},
    ]

    skor = {'I': 0, 'E': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    skala_jawaban = {"1": "Sangat Tidak Setuju", "2": "Tidak Setuju", "3": "Netral", "4": "Setuju", "5": "Sangat Setuju"}

    print(f"\n--- Mulai Tes Kepribadian MBTI (Versi Skala - {len(pernyataan_mbti)} Pertanyaan) ---")
    print("Untuk setiap pernyataan, tunjukkan tingkat persetujuan Anda.")
    print("Tes ini akan memakan waktu. Mohon jawab dengan jujur sesuai diri Anda.")
    
    for i, item in enumerate(pernyataan_mbti):
        print(f"\nPernyataan #{i+1}: {item['p']}")
        for nomor, teks in skala_jawaban.items():
            print(f"  {nomor}. {teks}")
        
        while True:
            jawaban_user = input("Pilih jawaban (1-5): ")
            if jawaban_user in skala_jawaban:
                dim_setuju, dim_tidak_setuju = item['d']
                if jawaban_user == '5': skor[dim_setuju] += 2
                elif jawaban_user == '4': skor[dim_setuju] += 1
                elif jawaban_user == '2': skor[dim_tidak_setuju] += 1
                elif jawaban_user == '1': skor[dim_tidak_setuju] += 2
                break
            else:
                print("Input tidak valid. Mohon masukkan angka dari 1 hingga 5.")
                
    hasil_tipe = tentukan_tipe_mbti(skor)
    
    print("\n--- Hasil Tes Kepribadian Anda ---")
    print(f"Berdasarkan jawaban Anda, tipe kepribadian Anda kemungkinan adalah: {hasil_tipe}")
    print("\nDetail Skor Akhir:")
    print(f"  - Extraversion (E): {skor['E']} vs. Introversion (I): {skor['I']}")
    print(f"  - Intuition (N): {skor['N']} vs. Sensing (S): {skor['S']}")
    print(f"  - Feeling (F): {skor['F']} vs. Thinking (T): {skor['T']}")
    print(f"  - Perceiving (P): {skor['P']} vs. Judging (J): {skor['J']}")
    print("\nCATATAN: Tes ini adalah prototipe untuk refleksi diri.")


# ==============================================================================
# PROGRAM UTAMA (MAIN LOOP)
# ==============================================================================

def main():
    """Fungsi utama untuk menjalankan seluruh aplikasi."""
    print("==============================================")
    print("  Selamat Datang di Aplikasi Well-Being Check ")
    print("==============================================")
    
    while True:
        print("\nMenu Utama:")
        print("1. Skrining Kesehatan Mental (100 Pertanyaan DASS)")
        print("2. Tes Kepribadian MBTI (150 Pertanyaan)")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1/2/3): ")
        
        if pilihan == '1':
            mulai_skrining_dass()
        elif pilihan == '2':
            mulai_tes_mbti_skala()
        elif pilihan == '3':
            print("\nTerima kasih telah menggunakan aplikasi ini. Jaga diri Anda!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

        if pilihan in ['1', '2']:
            input("\nTekan Enter untuk kembali ke Menu Utama...")

if __name__ == "__main__":
    main()