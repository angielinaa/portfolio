# --- PROTOTIPE APLIKASI SKRINING KESEHATAN MENTAL SEDERHANA ---
# Peringatan: Ini BUKAN alat diagnosis medis. Ini hanya simulasi logika.

def mulai_skrining():
    """Fungsi untuk menjalankan alur pertanyaan skrining."""
    
    # Daftar pertanyaan (contoh sederhana, tim psikologi harus membuat yang lebih valid)
    pertanyaan = [
        "Dalam seminggu terakhir, seberapa sering Anda merasa cemas atau khawatir berlebihan?",
        "Dalam seminggu terakhir, seberapa sering Anda merasa sedih atau putus asa?",
        "Dalam seminggu terakhir, seberapa sering Anda kehilangan minat atau kesenangan dalam melakukan sesuatu?",
        "Dalam seminggu terakhir, seberapa sering Anda merasa lelah atau tidak bertenaga?",
        "Dalam seminggu terakhir, seberapa sering Anda kesulitan untuk tidur atau tidur terlalu banyak?"
    ]
    
    # Opsi jawaban dan skornya
    opsi_jawaban = {
        "1": "Tidak pernah (0 hari)",
        "2": "Beberapa hari (1-2 hari)",
        "3": "Sebagian besar hari (3-4 hari)",
        "4.": "Hampir setiap hari (5-7 hari)"
    }
    
    skor_jawaban = {
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3
    }

    total_skor = 0
    
    print("\n--- Mulai Skrining Kesehatan Diri ---")
    print("Jawablah pertanyaan berikut berdasarkan apa yang Anda rasakan selama SEMINGGU TERAKHIR.")
    
    # Looping untuk menampilkan setiap pertanyaan
    for i, p in enumerate(pertanyaan):
        print(f"\nPertanyaan #{i+1}: {p}")
        
        # Menampilkan pilihan jawaban
        for nomor, teks in opsi_jawaban.items():
            print(f"  {nomor}. {teks}")
            
        # Meminta input dari pengguna
        while True:
            jawaban_user = input("Pilih jawaban (1/2/3/4): ")
            if jawaban_user in opsi_jawaban:
                total_skor += skor_jawaban[jawaban_user]
                break
            else:
                print("Input tidak valid. Mohon masukkan angka 1, 2, 3, atau 4.")

    return total_skor

def interpretasi_hasil(skor):
    """Fungsi untuk memberikan interpretasi berdasarkan total skor."""
    
    print("\n--- Hasil Skrining Anda ---")
    print(f"Total skor Anda adalah: {skor}")
    
    if skor <= 4:
        print("Interpretasi: Gejala yang Anda rasakan berada pada tingkat minimal. Tetap jaga kesehatan mental Anda!")
    elif skor <= 9:
        print("Interpretasi: Anda mengalami gejala ringan. Dianjurkan untuk lebih memperhatikan kondisi diri dan mencari cara relaksasi.")
    elif skor <= 14:
        print("Interpretasi: Anda mengalami gejala tingkat sedang. Pertimbangkan untuk berbicara dengan teman terpercaya atau keluarga.")
    else:
        print("Interpretasi: Anda mengalami gejala yang cukup signifikan. Sangat disarankan untuk berkonsultasi dengan profesional seperti psikolog atau konselor untuk mendapatkan panduan lebih lanjut.")
        
    print("\nINGAT: Hasil ini bukan diagnosis medis. Ini adalah alat bantu untuk refleksi diri.")


# --- PROGRAM UTAMA ---
def main():
    """Fungsi utama untuk menjalankan seluruh aplikasi."""
    print("==============================================")
    print("  Selamat Datang di Aplikasi Well-Being Check ")
    print("==============================================")
    print("Aplikasi ini bertujuan untuk membantu Anda merefleksikan kondisi diri.")
    
    while True:
        print("\nMenu Utama:")
        print("1. Mulai Skrining Diri")
        print("2. Keluar")
        
        pilihan = input("Pilih menu (1/2): ")
        
        if pilihan == '1':
            skor_akhir = mulai_skrining()
            interpretasi_hasil(skor_akhir)
        elif pilihan == '2':
            print("Terima kasih telah menggunakan aplikasi ini. Jaga diri Anda!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

# Menjalankan program utama saat file dieksekusi
if __name__ == "__main__":
    main()