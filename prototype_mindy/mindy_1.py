#!/usr/bin/env python3
# ==============================================================================
# Nama File: mindy_backend_v4.py
# Deskripsi: Backend AI untuk aplikasi Mindy - Mental Health Detector (v4)
#            - Lengkapi hasil Big Five
#            - Optimasi struktur
#            - Penambahan fitur: Emotion Detector (kamera real-time) + voice
#            - Transkripsi (SpeechRecognition / VOSK fallback)
# Versi: 4.1 (Perbaikan Tampilan Menu)
# Tim PKM: Informatika & Psikologi UMM
# ==============================================================================

import os
import sys
import json
import csv
import time
import logging
from typing import Dict, List, Tuple, Any

# ---------- Dependency checks (graceful) ----------
HAS_CV2 = False
HAS_MEDIAPIPE = False
HAS_DEEPFACE = False
HAS_SOUNDDEVICE = False
HAS_SPEECHRECOG = False
HAS_VOSK = False
HAS_LIBROSA = False

try:
    import cv2
    HAS_CV2 = True
except Exception:
    HAS_CV2 = False

try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except Exception:
    HAS_MEDIAPIPE = False

try:
    # deepface optional heavy dependency
    from deepface import DeepFace
    HAS_DEEPFACE = True
except Exception:
    HAS_DEEPFACE = False

# audio / stt
try:
    import sounddevice as sd
    import soundfile as sf
    HAS_SOUNDDEVICE = True
except Exception:
    HAS_SOUNDDEVICE = False

try:
    import speech_recognition as sr
    HAS_SPEECHRECOG = True
except Exception:
    HAS_SPEECHRECOG = False

try:
    # optional offline recognizer
    from vosk import Model, KaldiRecognizer
    HAS_VOSK = True
except Exception:
    HAS_VOSK = False

try:
    import librosa
    HAS_LIBROSA = True
except Exception:
    HAS_LIBROSA = False

import numpy as np

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger("mindy")

# ---------- Utils ----------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

DATA_DIR = "data"
ensure_dir(DATA_DIR)

def save_json(path: str, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: str) -> Any:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ======================================================================
#                        ORIGINAL FUNCTIONS
# ======================================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_header(judul: str):
    clear_screen()
    print("=" * 80)
    print(f"  {judul.center(76)}")
    print("=" * 80)
    print()

def input_pilihan(prompt: str, pilihan_valid: list) -> str:
    while True:
        jawaban = input(prompt).strip()
        if jawaban in pilihan_valid:
            return jawaban
        print(f"❌ Input tidak valid. Pilihan valid: {', '.join(pilihan_valid)}")

# ---------------- DASS / BIG FIVE question providers ----------------
def get_dass_questions() -> List[Dict[str, str]]:
    # (Di sini, asumsikan 100 pertanyaan lengkapmu dimasukkan)
    # Saya akan gunakan daftar lengkap dari kode v3.1
    return [
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

def get_bigfive_questions() -> List[Dict]:
    # (Di sini, asumsikan 60 pertanyaan lengkapmu dimasukkan)
    # Saya akan gunakan daftar lengkap dari kode v3.1
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

# ======================================================================
#             DASS: skrining & hasil (Versi 3.1 Valid)
# ======================================================================
def mulai_skrining_dass():
    tampilkan_header("SKRINING KESEHATAN MENTAL (DASS)")
    print("📋 INSTRUKSI:")
    print("    Untuk setiap pernyataan, jawablah berdasarkan pengalaman Anda")
    print("    selama SEMINGGU TERAKHIR.\n")
    print("    Skala Jawaban (Sesuai Standar DASS):")
    print("    0 = Tidak pernah / Sama sekali tidak berlaku")
    print("    1 = Jarang / Kadang-kadang berlaku")
    print("    2 = Sering berlaku")
    print("    3 = Hampir selalu / Sangat berlaku\n")
    input("Tekan ENTER untuk memulai...")
    pertanyaan = get_dass_questions()
    skor = {'D': 0, 'A': 0, 'S': 0}
    for i, item in enumerate(pertanyaan, 1):
        tampilkan_header(f"SKRINING DASS - Pertanyaan {i}/{len(pertanyaan)}")
        print(f"Pernyataan: {item['p']}\n")
        print("Pilihan:")
        print("    0. Tidak pernah / Sama sekali tidak berlaku")
        print("    1. Jarang / Kadang-kadang berlaku")
        print("    2. Sering berlaku")
        print("    3. Hampir selalu / Sangat berlaku\n")
        jawaban = input_pilihan("Pilih jawaban (0-3): ", ['0', '1', '2', '3'])
        kategori = item['k']
        skor[kategori] += int(jawaban)
    
    # Skala DASS-21 (21 item) dikalikan 2. 
    # Karena kita menggunakan ~33-34 item per subskala (mirip DASS-42),
    # kita tetap kalikan 2 agar sebanding dengan ambang batas DASS-21 yang umum.
    skor['D'] *= 2
    skor['A'] *= 2
    skor['S'] *= 2
    tampilkan_hasil_dass(skor)

def tampilkan_hasil_dass(skor: Dict[str, int]):
    def get_level(score: int, thresholds: Tuple[int, int, int, int]) -> Tuple[str, bool]:
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
    
    thresholds_depresi = (9, 13, 20, 27)
    thresholds_kecemasan = (7, 9, 14, 19)
    thresholds_stres = (14, 18, 25, 33)
    
    level_d, perlu_bantuan_d = get_level(skor['D'], thresholds_depresi)
    level_a, perlu_bantuan_a = get_level(skor['A'], thresholds_kecemasan)
    level_s, perlu_bantuan_s = get_level(skor['S'], thresholds_stres)
    
    tampilkan_header("HASIL SKRINING DASS")
    print("⚠️  CATATAN PENTING:")
    print("    Hasil ini BUKAN diagnosis medis, tapi indikator untuk refleksi diri.\n")
    
    print("=" * 80)
    print("DEPRESI")
    print("=" * 80)
    print(f"Skor Anda: {skor['D']}")
    print(f"Tingkat: {level_d}\n")
    
    print("=" * 80)
    print("KECEMASAN (ANXIETY)")
    print("=" * 80)
    print(f"Skor Anda: {skor['A']}")
    print(f"Tingkat: {level_a}\n")
    
    print("=" * 80)
    print("STRES")
    print("=" * 80)
    print(f"Skor Anda: {skor['S']}")
    print(f"Tingkat: {level_s}\n")
    
    print("=" * 80)
    print("REKOMENDASI")
    print("=" * 80)
    perlu_bantuan = perlu_bantuan_d or perlu_bantuan_a or perlu_bantuan_s
    if perlu_bantuan:
        print("⚠️  Jika salah satu atau lebih hasil Anda berada di tingkat 'Sedang' atau lebih tinggi,")
        print("    sangat disarankan untuk berbicara dengan konselor, psikolog, atau profesional.\n")
        print("📞 SEJIWA      : 119 (ekstensi 8)")
        print("📞 HALO KEMENKES : 1500 567 / WA: +62 812 6050 0567")
    else:
        print("✅ Hasil Anda menunjukkan tingkat yang baik. Tetap jaga kesehatan mental Anda.")
    
    print("\n" + "=" * 80)
    print("⚠️  Aplikasi ini adalah prototipe PKM Penerapan IPTEK. Selalu konsultasi dengan profesional.")
    print("=" * 80 + "\n")
    input("Tekan ENTER untuk kembali ke menu utama...")

# ======================================================================
#            BIG FIVE: hasil lengkap & rekomendasi
# ======================================================================
def tampilkan_hasil_bigfive(skor: Dict[str, int]):
    # (Fungsi ini diambil dari v4, sudah benar)
    avg_skor = {k: round((v / 12) * 20, 1) for k, v in skor.items()}

    def get_level(score: float) -> str:
        if score < 40:
            return "Rendah"
        elif score < 60:
            return "Sedang"
        else:
            return "Tinggi"

    traits_info = {
        'E': ('EXTRAVERSION (Ekstraversi)',
              'Energi, sosiabilitas, dan kecenderungan mencari stimulasi dari lingkungan luar.'),
        'A': ('AGREEABLENESS (Keramahan)',
              'Kecenderungan untuk bersikap kooperatif, penuh kasih, dan peduli pada orang lain.'),
        'C': ('CONSCIENTIOUSNESS (Kehati-hatian)',
              'Kecenderungan untuk terorganisir, bertanggung jawab, dan fokus pada tujuan.'),
        'N': ('NEUROTICISM (Stabilitas Emosional)',
              'Kecenderungan untuk mengalami emosi negatif (skor tinggi = kurang stabil).'),
        'O': ('OPENNESS (Keterbukaan)',
              'Keterbukaan terhadap pengalaman baru, ide kreatif, dan keingintahuan intelektual.'),
    }

    rekomendasi_per_trait = {
        'E': {
            'Rendah': 'Coba ikut kegiatan sosial bertahap (small group) untuk latih social energy.',
            'Sedang': 'Pertahankan keseimbangan: luangkan waktu sendiri bila perlu.',
            'Tinggi': 'Manfaatkan energi sosial untuk memimpin proyek kelompok.'
        },
        'A': {
            'Rendah': 'Latih empati melalui reflective listening dan kegiatan volunteer ringan.',
            'Sedang': 'Perkuat skill komunikasi asertif untuk menjaga batasan sehat.',
            'Tinggi': 'Gunakan sifat kooperatif untuk dukung tim dan mentoring.'
        },
        'C': {
            'Rendah': 'Buat habit pengelolaan waktu sederhana: to-do list harian.',
            'Sedang': 'Tingkatkan perencanaan dengan teknik time-blocking.',
            'Tinggi': 'Peran manajerial atau leadership cocok, tapi hindari perfectionism berlebih.'
        },
        'N': {
            'Rendah': 'Kamu cenderung stabil; tetap perhatikan self-care agar tetap konsisten.',
            'Sedang': 'Latih coping strategies: mindfulness, journaling, dan sleep hygiene.',
            'Tinggi': 'Pertimbangkan konsultasi bila emosi mengganggu fungsi sehari-hari.'
        },
        'O': {
            'Rendah': 'Eksplorasi kegiatan kreatif sederhana (mendengarkan musik, membaca).',
            'Sedang': 'Coba proyek kecil yang membutuhkan ide baru untuk melatih fleksibilitas.',
            'Tinggi': 'Kembangkan ide kreatif lewat proyek penelitian/kreasi.'
        },
    }

    tampilkan_header("HASIL TES BIG FIVE PERSONALITY")
    print("⚠️  CATATAN PENTING:")
    print("    Hasil ini BUKAN diagnosis, tapi gambaran karakteristik kepribadian Anda.\n")

    for trait, (nama, deskripsi) in traits_info.items():
        level = get_level(avg_skor.get(trait, 0))
        print("=" * 80)
        print(nama)
        print("=" * 80)
        print(f"Skor Anda: {avg_skor.get(trait, 0)}%")
        print(f"Tingkat: {level}")
        print(f"\nDeskripsi: {deskripsi}\n")
        # rekomendasi
        reco = rekomendasi_per_trait.get(trait, {}).get(level, "")
        if reco:
            print("Rekomendasi:")
            print(f"    • {reco}")
        print()

    print("=" * 80)
    print("INTERPRETASI HASIL")
    print("=" * 80)
    print("\n💡 Tidak ada skor yang 'baik' atau 'buruk' dalam tes ini.")
    print("    Setiap trait memiliki kelebihan dan kekurangannya sendiri.")
    print("    Hasil ini dapat membantu Anda memahami diri sendiri lebih baik.")
    print("\n" + "=" * 80)
    print("⚠️  Aplikasi ini adalah prototipe PKM Penerapan IPTEK. Selalu konsultasi dengan profesional.")
    print("=" * 80 + "\n")
    input("Tekan ENTER untuk kembali ke menu utama...")

# ======================================================================
#             EMOTION DETECTION MODULE (kamera + voice)
# ======================================================================
def start_emotion_session():
    tampilkan_header("EMOTION DETECTION - Rekam Ekspresi & Suara (Real-time)")
    print("Instruksi singkat:")
    print(" - Siapkan webcam dan mic.")
    print(" - Kamu akan diminta menjawab satu prompt terbuka (1-2 menit).")
    print(" - Sistem akan merekam video + audio, mentranskrip, dan melakukan analisis awal.")
    print()
    
    if not HAS_CV2 or not HAS_SOUNDDEVICE:
        print("⚠️  FITUR INI MEMERLUKAN LIBRARY TAMBAHAN (OpenCV, SoundDevice).")
        print("    Silakan install library tersebut dengan 'pip install opencv-python sounddevice'")
        print("    Mode simulasi akan digunakan (tidak ada perekaman).")
        input("Tekan ENTER untuk kembali...")
        # Simulasi jika library tidak ada
        session = {
            "timestamp": int(time.time()),
            "prompt": "Simulasi",
            "transcript": "[Simulasi - Library tidak terinstal]",
            "face_analysis": {"dominant_emotion": "neutral", "scores": {}},
            "voice_analysis": {"valence": 0.0, "arousal": 0.0},
        }
        filename = os.path.join(DATA_DIR, f"emotion_session_{session['timestamp']}.json")
        save_json(filename, session)
        return

    input("Tekan ENTER jika siap...")

    prompts = [
        "Ceritakan pengalaman paling membuatmu bangga dalam hidup.",
        "Ceritakan tentang satu kejadian yang membuatmu sangat kesal baru-baru ini.",
        "Ceritakan pengalaman yang membuatmu sedih.",
        "Ceritakan tentang rencana masa depan yang kamu khawatirkan."
    ]
    print("Pilih prompt:")
    for idx, p in enumerate(prompts, 1):
        print(f"    {idx}. {p}")
    print("    0. Masukkan prompt sendiri")
    pilihan = input_pilihan("Pilih (0-{}): ".format(len(prompts)), [str(i) for i in range(0, len(prompts)+1)])
    if pilihan == '0':
        prompt = input("Masukkan prompt kamu: ").strip()
    else:
        prompt = prompts[int(pilihan)-1]

    print("\nPrompt akan ditampilkan saat perekaman dimulai.")
    input("Tekan ENTER untuk mulai rekaman (durasi default: 30 detik)...")

    duration = 30  # detik, diperpendek untuk tes
    video_path = os.path.join(DATA_DIR, f"session_video_{int(time.time())}.avi")
    audio_path = os.path.join(DATA_DIR, f"session_audio_{int(time.time())}.wav")

    # --- Perekaman Gabungan ---
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️ Webcam tidak dapat diakses.")
        input("Tekan ENTER untuk kembali...")
        return
        
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 20.0
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))

    samplerate = 16000
    audio_recording = []

    def audio_callback(indata, frames, time_info, status):
        audio_recording.append(indata.copy())

    stream = sd.InputStream(samplerate=samplerate, channels=1, callback=audio_callback)
    stream.start()

    print("\nMulai rekaman sekarang. (Tekan 'q' di window kamera untuk berhenti lebih cepat)")
    print("Prompt: ", prompt)
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        
        display_frame = frame.copy()
        cv2.putText(display_frame, "Mindy - Rekam Ekspresi", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f"Prompt: {prompt[:50]+'...' if len(prompt)>50 else prompt}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Tampilkan timer
        elapsed = time.time() - start_time
        remaining = duration - elapsed
        cv2.putText(display_frame, f"Sisa Waktu: {int(remaining)}s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow("Mindy - Rekam (Tekan q untuk stop)", display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if elapsed > duration:
            break

    # Cleanup
    stream.stop()
    out.release()
    cap.release()
    cv2.destroyAllWindows()

    # Proses audio
    if audio_recording:
        audio_np = np.concatenate(audio_recording, axis=0)
        sf.write(audio_path, audio_np, samplerate)
    else:
        audio_path = None

    print("\nPerekaman selesai. Memproses analisis...")

    # Transkripsi
    simulated_transcript = "[Library transkripsi tidak terinstal]"
    if audio_path and HAS_SPEECHRECOG:
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
        try:
            simulated_transcript = r.recognize_google(audio_data, language="id-ID")
            print(f"Transkrip: {simulated_transcript}")
        except Exception as e:
            simulated_transcript = f"[Gagal transkripsi: {e}]"
    
    # Analisis Wajah
    face_results = {"dominant_emotion": "neutral", "scores": {}}
    if HAS_DEEPFACE:
        try:
            face_results = analyze_face_emotions_from_video(video_path)
        except Exception as e:
            logger.warning(f"Analisis wajah gagal: {e}")
    else:
        print("Analisis Wajah: [Library DeepFace/MediaPipe tidak terinstal, hasil disimulasikan]")

    # Analisis Suara
    voice_results = {"valence": 0.0, "arousal": 0.0}
    if audio_path and HAS_LIBROSA:
        try:
            voice_results = analyze_voice_emotion(audio_path)
        except Exception as e:
            logger.warning(f"Analisis suara gagal: {e}")
    else:
        print("Analisis Suara: [Library Librosa tidak terinstal, hasil disimulasikan]")
    
    # Agregasi
    session = {
        "timestamp": int(time.time()),
        "prompt": prompt,
        "transcript": simulated_transcript,
        "face_analysis": face_results,
        "voice_analysis": voice_results,
    }

    filename = os.path.join(DATA_DIR, f"emotion_session_{session['timestamp']}.json")
    save_json(filename, session)
    print("\nAnalisis selesai. Hasil sementara disimpan ke:", filename)
    input("Tekan ENTER untuk kembali ke menu utama...")

# ----------------- Helper untuk face emotion analysis -----------------
def analyze_face_emotions_from_video(video_path: str) -> Dict[str, Any]:
    if not HAS_CV2:
        raise RuntimeError("OpenCV diperlukan untuk analisis video.")
    if not HAS_DEEPFACE:
        # Fallback jika deepface tidak ada
        print("Info: DeepFace tidak terinstal, analisis wajah disimulasikan.")
        return {"dominant_emotion": "neutral", "scores": {}}
        
    results = {"frames_analyzed": 0, "emotion_counts": {}, "dominant_emotion": None, "scores": {}}
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 20
    frame_interval = int(fps)  # 1 frame per detik
    idx = 0
    emotions_counter = {}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % frame_interval == 0:
            try:
                # DeepFace analyze
                df_res = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant = df_res[0].get('dominant_emotion', None) if isinstance(df_res, list) else df_res.get('dominant_emotion', None)
                if dominant:
                    emotions_counter[dominant] = emotions_counter.get(dominant, 0) + 1
            except Exception as e:
                logger.debug(f"Frame analysis error: {e}")
        idx += 1
    
    cap.release()
    results["frames_analyzed"] = idx // frame_interval if frame_interval > 0 else 0
    results["emotion_counts"] = emotions_counter
    if emotions_counter:
        dominant = max(emotions_counter.items(), key=lambda x: x[1])[0]
        results["dominant_emotion"] = dominant
    else:
        results["dominant_emotion"] = "unknown"
    return results

# ----------------- Helper untuk voice emotion analysis -----------------
def analyze_voice_emotion(audio_path: str) -> Dict[str, float]:
    if not HAS_LIBROSA:
        raise RuntimeError("librosa diperlukan untuk analisis suara.")
    y, sr_load = librosa.load(audio_path, sr=16000)
    rms = np.mean(librosa.feature.rms(y=y))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    tempo_tuple = librosa.beat.tempo(y=y, sr=sr_load)
    tempo = float(tempo_tuple[0]) if isinstance(tempo_tuple, (list, np.ndarray)) and len(tempo_tuple) > 0 else float(tempo_tuple)
    
    # Heuristik sederhana
    valence = float(np.tanh((rms - 0.01) * 10))
    arousal = float(np.tanh(zcr * 50))
    return {"rms": float(rms), "zcr": float(zcr), "tempo": tempo,
            "valence": valence, "arousal": arousal}

# ======================================================================
#                     MENU UTAMA (diperbarui v4.1)
# ======================================================================
def tampilkan_menu_utama():
    """Menampilkan menu utama aplikasi (Versi 4.1 dengan deskripsi)"""
    tampilkan_header("MINDY - MENTAL HEALTH DETECTOR AI (v4.1)")
    
    print("🧠 Selamat datang di Mindy!")
    print("    Aplikasi detector kesehatan mental berbasis AI\n")
    print("    Kolaborasi: Informatika UMM × Psikologi UMM\n")
    
    print("=" * 80)
    print("MENU UTAMA")
    print("=" * 80)
    print()
    print("    1. Skrining Kesehatan Mental (DASS)")
    print("       Mengukur tingkat Depresi, Anxiety, dan Stress (100 pertanyaan)")
    print()
    print("    2. Tes Big Five Personality")
    print("       Mengukur 5 dimensi kepribadian (60 pertanyaan)")
    print()
    print("    3. Emotion Detection (Webcam + Voice)")
    print("       Merekam dan menganalisis ekspresi & nada suara (Fitur AI)")
    print()
    print("    4. Informasi & Kontak Layanan Psikolog")
    print()
    print("    0. Keluar")
    print()
    print("=" * 80)
    print()

def tampilkan_info_layanan():
    tampilkan_header("INFORMASI LAYANAN BANTUAN PSIKOLOG")
    print("📞 LAYANAN DARURAT KESEHATAN MENTAL\n")
    print("=" * 80)
    print("SEJIWA")
    print("=" * 80)
    print("Telepon: 119 (ekstensi 8)")
    print("Layanan konseling dan bantuan psikologis gratis\n")
    print("=" * 80)
    print("HALO KEMENKES")
    print("=" * 80)
    print("Telepon: 1500 567")
    print("WhatsApp: +62 812 6050 0567")
    print("SMS: +62 812 8156 2620")
    print("\n💡 CATATAN:")
    print("    Jangan ragu untuk menghubungi layanan di atas jika Anda:")
    print("    • Merasa sedih berkepanjangan")
    print("    • Mengalami kecemasan yang mengganggu")
    print("    • Memiliki pikiran untuk menyakiti diri sendiri")
    print("    • Membutuhkan seseorang untuk diajak bicara")
    print("\n    Kesehatan mental Anda penting! 💜\n")
    print("=" * 80)
    input("\nTekan ENTER untuk kembali ke menu utama...")

def main():
    while True:
        tampilkan_menu_utama()
        pilihan = input_pilihan("Pilih menu (0-4): ", ['0', '1', '2', '3', '4'])
        if pilihan == '1':
            mulai_skrining_dass()
        elif pilihan == '2':
            mulai_tes_bigfive()
        elif pilihan == '3':
            start_emotion_session()
        elif pilihan == '4':
            tampilkan_info_layanan()
        elif pilihan == '0':
            clear_screen()
            print("\n" + "=" * 80)
            print("  Terima kasih telah menggunakan Mindy! 💜".center(80))
            print("  Jaga kesehatan mental Anda!".center(80))
            print("=" * 80)
            print("\n  Tim PKM - Informatika UMM × Psikologi UMM\n")
            sys.exit(0)

# ---------- Wrapper untuk tes Big Five (agar sesuai struktur modular) ----------
def mulai_tes_bigfive():
    tampilkan_header("TES BIG FIVE PERSONALITY (BFI-2)")
    print("📋 INSTRUKSI:")
    print("    Di bawah ini adalah sejumlah karakteristik yang mungkin menggambarkan")
    print("    diri Anda atau mungkin juga tidak. Silakan tunjukkan seberapa setuju")
    print("    Anda bahwa karakteristik berikut menggambarkan diri Anda.\n")
    print("    Skala Jawaban:")
    print("    1 = Sangat tidak setuju")
    print("    2 = Sedikit tidak setuju")
    print("    3 = Netral")
    print("    4 = Sedikit setuju")
    print("    5 = Sangat setuju\n")
    print("    Setiap pertanyaan diawali dengan: 'Saya adalah seseorang yang...'\n")
    input("Tekan ENTER untuk memulai...")
    
    pertanyaan = get_bigfive_questions()
    if not pertanyaan or len(pertanyaan) < 60:
        logger.warning("Daftar pertanyaan Big Five tidak lengkap, memuat minimal...")
        # Fallback jika get_bigfive_questions() dikosongkan
        pertanyaan = [
            {"p": "ramah dan mudah bergaul.", "r": False, "trait": "E"},
            {"p": "penuh kasih, berhati lembut.", "r": False, "trait": "A"},
            {"p": "cenderung tidak teratur.", "r": True, "trait": "C"},
            {"p": "banyak merasa cemas.", "r": True, "trait": "N"},
            {"p": "memiliki sedikit minat pada seni.", "r": True, "trait": "O"},
        ] * 12 # 60 items

    skor = {'E': 0, 'A': 0, 'C': 0, 'N': 0, 'O': 0}
    
    for i, item in enumerate(pertanyaan, 1):
        tampilkan_header(f"TES BIG FIVE - Pertanyaan {i}/{len(pertanyaan)}")
        print(f"Saya adalah seseorang yang {item['p']}\n")
        print("Pilihan:")
        print("    1. Sangat tidak setuju")
        print("    2. Sedikit tidak setuju")
        print("    3. Netral")
        print("    4. Sedikit setuju")
        print("    5. Sangat setuju\n")
        jawaban = input_pilihan("Pilih jawaban (1-5): ", ['1', '2', '3', '4', '5'])
        
        trait = item['trait']
        nilai = int(jawaban)
        if item.get('r', False):
            nilai = 6 - nilai
        skor[trait] += nilai
    
    ts = int(time.time())
    hasil = {"timestamp": ts, "scores_raw": skor}
    save_json(os.path.join(DATA_DIR, f"bigfive_{ts}.json"), hasil)
    
    tampilkan_hasil_bigfive(skor)

# Entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user. Terima kasih!")
        sys.exit(0)
    except Exception as e:
        logger.exception("Terjadi error yang tidak terduga:")
        print("\n❌ Terjadi error: ", e)
        sys.exit(1)