import pygame
import time
import random

# --- 1. INISIALISASI ---
pygame.init()

# --- 2. PALET WARNA (PASTEL CUTE) ---
WARNA_BG_1 = (255, 245, 250)    # Lavender Blush
WARNA_BG_2 = (255, 228, 225)    # Misty Rose
WARNA_ULAR = (147, 112, 219)    # Medium Purple
WARNA_KEPALA = (75, 0, 130)     # Indigo
WARNA_MAKANAN = (255, 105, 180) # Hot Pink
WARNA_TEKS = (72, 61, 139)      # Dark Slate Blue
PUTIH = (255, 255, 255)
OVERLAY_PAUSE = (255, 255, 255, 180) # Putih transparan

# --- 3. PENGATURAN LAYAR ---
LEBAR_LAYAR = 600
TINGGI_LAYAR = 400
UKURAN_BLOK = 20 

dis = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
pygame.display.set_caption('CUTE SNAKE: Final Version 🎀')

clock = pygame.time.Clock()

# Font
font_judul = pygame.font.SysFont("comicsansms", 35)
font_biasa = pygame.font.SysFont("comicsansms", 20)
font_kecil = pygame.font.SysFont("comicsansms", 15)

# --- 4. FUNGSI GAMBAR ---

def gambar_background_grid():
    for baris in range(0, TINGGI_LAYAR, UKURAN_BLOK):
        for kolom in range(0, LEBAR_LAYAR, UKURAN_BLOK):
            rect = [kolom, baris, UKURAN_BLOK, UKURAN_BLOK]
            if (baris // UKURAN_BLOK + kolom // UKURAN_BLOK) % 2 == 0:
                pygame.draw.rect(dis, WARNA_BG_1, rect)
            else:
                pygame.draw.rect(dis, WARNA_BG_2, rect)

def skor_akhir(score):
    value = font_biasa.render("Poin: " + str(score), True, WARNA_TEKS)
    s = pygame.Surface((100, 30))
    s.set_alpha(128)
    s.fill(PUTIH)
    dis.blit(s, (5,5))
    dis.blit(value, [10, 5])

def gambar_ular(block_size, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1: # Kepala
            pygame.draw.circle(dis, WARNA_KEPALA, (int(x[0] + block_size/2), int(x[1] + block_size/2)), block_size//2)
            # Mata
            pygame.draw.circle(dis, PUTIH, (int(x[0] + block_size/2 - 4), int(x[1] + block_size/2 - 4)), 3)
            pygame.draw.circle(dis, PUTIH, (int(x[0] + block_size/2 + 4), int(x[1] + block_size/2 - 4)), 3)
        else: # Badan
            pygame.draw.circle(dis, WARNA_ULAR, (int(x[0] + block_size/2), int(x[1] + block_size/2)), block_size//2)

def pesan_tengah(msg, color, y_offset=0, font_type="biasa"):
    if font_type == "judul":
        mesg = font_judul.render(msg, True, color)
    elif font_type == "kecil":
        mesg = font_kecil.render(msg, True, color)
    else:
        mesg = font_biasa.render(msg, True, color)
    text_rect = mesg.get_rect(center=(LEBAR_LAYAR/2, TINGGI_LAYAR/2 + y_offset))
    dis.blit(mesg, text_rect)

# --- 5. MENU PILIH KECEPATAN (DIPERLAMBAT LAGI) ---
def menu_awal():
    intro = True
    kecepatan_pilihan = 10 
    
    while intro:
        dis.fill(WARNA_BG_1)
        
        # Hiasan menu
        pygame.draw.rect(dis, PUTIH, [LEBAR_LAYAR/2 - 220, TINGGI_LAYAR/2 - 120, 440, 240], border_radius=20)
        pygame.draw.rect(dis, WARNA_ULAR, [LEBAR_LAYAR/2 - 220, TINGGI_LAYAR/2 - 120, 440, 240], 4, border_radius=20)
        
        pesan_tengah("PILIH KECEPATAN", WARNA_KEPALA, -70, "judul")
        pesan_tengah("1: Lambat Banget (5 FPS) 🐌", WARNA_TEKS, -20, "biasa")
        pesan_tengah("2: Sedang (10 FPS) 🐇", WARNA_TEKS, 20, "biasa")
        pesan_tengah("3: Lumayan Cepat (15 FPS) 🐆", WARNA_TEKS, 60, "biasa")
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    kecepatan_pilihan = 5  # SANGAT LAMBAT
                    intro = False
                elif event.key == pygame.K_2:
                    kecepatan_pilihan = 10 # SEDANG
                    intro = False
                elif event.key == pygame.K_3:
                    kecepatan_pilihan = 15 # AGAK CEPAT
                    intro = False
    
    return kecepatan_pilihan

# --- 6. FUNGSI PAUSE (FITUR BARU) ---
def pause_game():
    paused = True
    while paused:
        # Layar semi transparan
        s = pygame.Surface((LEBAR_LAYAR, TINGGI_LAYAR), pygame.SRCALPHA)
        s.fill(OVERLAY_PAUSE)
        dis.blit(s, (0,0))
        
        pesan_tengah("PAUSE ⏸️", WARNA_KEPALA, -30, "judul")
        pesan_tengah("Tekan SPASI untuk Lanjut", WARNA_TEKS, 10, "biasa")
        pesan_tengah("Tekan Q untuk Keluar Game", WARNA_MAKANAN, 50, "kecil")
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False # Lanjut main
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# --- 7. GAME LOOP UTAMA ---
def gameLoop(kecepatan_fps):
    game_over = False
    game_close = False

    x1 = LEBAR_LAYAR / 2
    y1 = TINGGI_LAYAR / 2

    x1_change = 0
    y1_change = 0
    arah_terakhir = "DIAM" 

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, LEBAR_LAYAR - UKURAN_BLOK) / UKURAN_BLOK) * UKURAN_BLOK
    foody = round(random.randrange(0, TINGGI_LAYAR - UKURAN_BLOK) / UKURAN_BLOK) * UKURAN_BLOK

    while not game_over:

        while game_close == True:
            dis.fill(WARNA_BG_1)
            # Kotak Game Over
            s = pygame.Surface((LEBAR_LAYAR, TINGGI_LAYAR))
            s.set_alpha(200)
            s.fill(WARNA_BG_1)
            dis.blit(s, (0,0))
            
            pesan_tengah("YAH KALAH! 😭", WARNA_MAKANAN, -30, "judul")
            pesan_tengah(f"Skor Akhir: {Length_of_snake - 1}", WARNA_TEKS, 10, "biasa")
            pesan_tengah("Tekan C (Main Lagi) atau Q (Keluar)", WARNA_KEPALA, 50, "kecil")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        pilihan_baru = menu_awal()
                        gameLoop(pilihan_baru)

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # KONTROL ARAH
                if event.key == pygame.K_LEFT and arah_terakhir != "KANAN":
                    x1_change = -UKURAN_BLOK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and arah_terakhir != "KIRI":
                    x1_change = UKURAN_BLOK
                    y1_change = 0
                elif event.key == pygame.K_UP and arah_terakhir != "BAWAH":
                    y1_change = -UKURAN_BLOK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and arah_terakhir != "ATAS":
                    y1_change = UKURAN_BLOK
                    x1_change = 0
                
                # FITUR PAUSE (SPASI)
                elif event.key == pygame.K_SPACE:
                    pause_game() # Panggil fungsi pause

        x1 += x1_change
        y1 += y1_change

        # Tembus Tembok
        x1 = x1 % LEBAR_LAYAR
        y1 = y1 % TINGGI_LAYAR
        
        # Update Arah Terakhir (Anti Bug Balik Arah)
        if x1_change < 0: arah_terakhir = "KIRI"
        elif x1_change > 0: arah_terakhir = "KANAN"
        elif y1_change < 0: arah_terakhir = "ATAS"
        elif y1_change > 0: arah_terakhir = "BAWAH"

        gambar_background_grid()
        
        # Makanan
        pygame.draw.circle(dis, WARNA_MAKANAN, (int(foodx + UKURAN_BLOK/2), int(foody + UKURAN_BLOK/2)), UKURAN_BLOK//2)
        pygame.draw.line(dis, (50, 205, 50), (foodx + 10, foody), (foodx + 15, foody - 5), 2)

        # Ular
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        gambar_ular(UKURAN_BLOK, snake_List)
        skor_akhir(Length_of_snake - 1)
        
        # Petunjuk Pause Kecil di Pojok
        txt_pause = font_kecil.render("SPASI = Pause", True, WARNA_TEKS)
        dis.blit(txt_pause, (LEBAR_LAYAR - 120, 5))

        pygame.display.update()

        if abs(x1 - foodx) < 5 and abs(y1 - foody) < 5:
            foodx = round(random.randrange(0, LEBAR_LAYAR - UKURAN_BLOK) / UKURAN_BLOK) * UKURAN_BLOK
            foody = round(random.randrange(0, TINGGI_LAYAR - UKURAN_BLOK) / UKURAN_BLOK) * UKURAN_BLOK
            Length_of_snake += 1

        clock.tick(kecepatan_fps)

    pygame.quit()
    quit()

# Eksekusi
fps_terpilih = menu_awal()
gameLoop(fps_terpilih)