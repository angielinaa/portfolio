import tkinter as tk
from tkinter import messagebox
import random

# --- KONFIGURASI WARNA (PALET MODERN) ---
BG_COLOR = "#1e1e2e"        # Latar belakang utama
DISPLAY_BG = "#282c34"      # Latar belakang layar input
TEXT_COLOR = "#ffffff"      # Warna teks putih
BTN_NUM_BG = "#3e3e5e"      # Warna tombol angka
BTN_NUM_HOVER = "#505075"   
BTN_OP_BG = "#ff79c6"       # Warna tombol operator (Neon Pink)
BTN_OP_HOVER = "#ff92d0"
BTN_EQ_BG = "#bd93f9"       # Warna tombol sama dengan (Neon Purple)
BTN_EQ_HOVER = "#d1b4fc"
BTN_CLEAR_BG = "#ff5555"    # Warna tombol C (Red)

# --- BAGIAN 1: LOGIKA ---

def tambah_angka(angka):
    # Mengambil posisi kursor saat ini
    index = layar.index(tk.INSERT)
    # Memasukkan angka di posisi kursor
    layar.insert(index, str(angka))

def bersihkan():
    layar.delete(0, tk.END)

def hitung(event=None): # Parameter event=None agar bisa dipanggil tombol Enter
    try:
        ekspresi = layar.get()
        # Mengganti simbol visual menjadi simbol matematika Python
        # User mungkin ngetik 'x' atau ':' manual, kita handle juga
        ekspresi_bersih = ekspresi.replace('÷', '/').replace('×', '*').replace(':', '/')
        
        hasil = eval(ekspresi_bersih)
        
        # Format hasil: jika bulat, hilangkan .0 di belakang
        if hasil == int(hasil):
            hasil = int(hasil)
            
        layar.delete(0, tk.END)
        layar.insert(0, str(hasil))
        
        # Pindahkan kursor ke akhir agar bisa lanjut hitung
        layar.icursor(tk.END)
        
    except Exception:
        # Jangan tampilkan popup error biar ga ganggu flow ngetik, 
        # cukup tulisan "Error" di layar
        layar.delete(0, tk.END)
        layar.insert(0, "Error")

# --- BAGIAN 2: UI KALKULATOR ---

def build_calculator_ui(root_window):
    # Membersihkan splash screen
    for widget in root_window.winfo_children():
        widget.destroy()

    root_window.title("StarCalc Modern")
    root_window.geometry("320x450")
    root_window.configure(bg=BG_COLOR)

    # LAYAR INPUT
    # Kita biarkan entry state normal agar bisa diketik keyboard
    global layar
    layar = tk.Entry(root_window, width=14, font=('Segoe UI Semibold', 28), 
                     bg=DISPLAY_BG, fg=TEXT_COLOR, 
                     borderwidth=0, relief="flat", justify="right")
    layar.grid(row=0, column=0, columnspan=4, padx=15, pady=(25, 20), ipady=10)
    
    # === FITUR BARU: AUTO FOCUS & KEYBOARD BINDING ===
    layar.focus_set() # Langsung fokus ke layar saat terbuka
    
    # Bind tombol ENTER keyboard untuk memanggil fungsi hitung
    root_window.bind('<Return>', hitung)
    # Bind tombol ESCAPE keyboard untuk memanggil fungsi bersihkan
    root_window.bind('<Escape>', lambda event: bersihkan())
    # =================================================

    # DAFTAR TOMBOL VISUAL
    tombol_list = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ]

    for (text, row, col) in tombol_list:
        bg_color = BTN_NUM_BG
        hover_color = BTN_NUM_HOVER
        cmd = lambda t=text: tambah_angka(t)

        if text in ['÷', '×', '-', '+']:
            bg_color = BTN_OP_BG
            hover_color = BTN_OP_HOVER
            fg_color = BG_COLOR 
        elif text == '=':
            bg_color = BTN_EQ_BG
            hover_color = BTN_EQ_HOVER
            fg_color = BG_COLOR
            cmd = hitung
        elif text == 'C':
            bg_color = BTN_CLEAR_BG
            hover_color = "#ff7777"
            fg_color = TEXT_COLOR
            cmd = bersihkan
        else:
            fg_color = TEXT_COLOR

        btn = tk.Button(root_window, text=text, width=5, height=2, font=('Segoe UI Bold', 16),
                        bg=bg_color, fg=fg_color, activebackground=hover_color,
                        relief="flat", borderwidth=0, cursor="hand2",
                        command=cmd)
        
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    for i in range(4):
        root_window.grid_columnconfigure(i, weight=1)
    for i in range(1, 5):
        root_window.grid_rowconfigure(i, weight=1)

# --- BAGIAN 3: SPLASH SCREEN (TETAP SAMA) ---

def show_splash_screen(root_window):
    root_window.title("Loading...")
    root_window.geometry("320x450")
    
    canvas = tk.Canvas(root_window, width=320, height=450, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    colors = ["#ffffff", "#bd93f9", "#ff79c6", "#8be9fd"] 
    for _ in range(100): 
        x = random.randint(0, 320)
        y = random.randint(0, 450)
        size = random.randint(1, 3)
        color = random.choice(colors)
        canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")

    canvas.create_text(160, 200, text="✨ StarCalc ✨", font=("Segoe UI Bold", 24), fill=BTN_EQ_BG)
    canvas.create_text(160, 240, text="Memuat keajaiban...", font=("Segoe UI", 12), fill=TEXT_COLOR)

    root_window.after(3000, lambda: build_calculator_ui(root_window))

# --- EKSEKUSI UTAMA ---
if __name__ == "__main__":
    main_root = tk.Tk()
    main_root.resizable(False, False)
    show_splash_screen(main_root)
    main_root.mainloop()