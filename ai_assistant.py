import keyboard
import pyautogui
import pytesseract
from pytesseract import Output
from google import genai
import os
import time
from dotenv import load_dotenv

# 1. Konfigurasi Environment & API
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Sesuaikan dengan lokasi instalasi Tesseract di komputer Anda
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def proses_layar():
    print("\n[+] Memproses layar...")
    
    try:
        # 2. Mengambil Screenshot
        screenshot = pyautogui.screenshot()
        
        # 3. Ekstraksi Teks menggunakan OCR
        # Kita menggunakan image_to_data untuk mendapatkan teks sekaligus koordinatnya
        ocr_data = pytesseract.image_to_data(screenshot, output_type=Output.DICT)
        
        # Menggabungkan teks untuk dikirim ke AI
        teks_soal = " ".join([word for word in ocr_data['text'] if word.strip()])
        
        if not teks_soal:
            print("[-] Tidak ada teks yang terbaca di layar.")
            return

        print(f"[+] Meminta jawaban dari AI untuk divalidasi...")

        # 4. Memanggil REST API AI
        # Instruksikan AI untuk mengembalikan SATU KATA KUNCI UNIK dari jawaban yang benar
        # agar kita bisa mencarinya di layar.
        prompt = f"""
Tugas Anda adalah memvalidasi soal berikut.
Pilih jawaban yang benar, lalu balas HANYA dengan 1-2 kata yang paling unik dari pilihan jawaban yang benar tersebut.
Jangan berikan penjelasan. Jangan gunakan tanda baca tambahan. Teks ini harus persis sama dengan yang ada di soal.

Soal dan pilihan:
{teks_soal}
"""
        
        response = client.models.generate_content(
            model='gemini-3.7-flash',
            contents=prompt
        )
        
        kata_kunci_jawaban = response.text.strip()
        print("="*40)
        print(f"JAWABAN DARI AI: '{kata_kunci_jawaban}'")
        print("="*40)
        
        # 5. Mencari koordinat kata kunci di layar
        # Kita pisahkan kata kunci jika AI mengembalikan lebih dari 1 kata, dan cari kata pertamanya
        target_word = kata_kunci_jawaban.split()[0] 
        
        found = False
        n_boxes = len(ocr_data['text'])
        for i in range(n_boxes):
            word_on_screen = ocr_data['text'][i]
            # Cari kata yang mirip/sama (case-insensitive)
            if target_word.lower() in word_on_screen.lower() and len(word_on_screen.strip()) > 1:
                # Dapatkan koordinat dari kata tersebut
                x = ocr_data['left'][i]
                y = ocr_data['top'][i]
                w = ocr_data['width'][i]
                h = ocr_data['height'][i]
                
                # Hitung titik tengah dari kotak teks tersebut
                center_x = x + (w / 2)
                center_y = y + (h / 2)
                
                print(f"[+] Menemukan kata '{word_on_screen}' di koordinat (X: {center_x}, Y: {center_y})")
                
                # 6. Menggerakkan Mouse dan Klik
                pyautogui.moveTo(center_x, center_y, duration=0.5)
                pyautogui.click()
                print("[+] Berhasil mengklik target!")
                
                found = True
                break # Berhenti setelah menemukan dan mengklik target pertama
                
        if not found:
            print("[-] Gagal menemukan kata kunci jawaban di layar.")
        
    except Exception as e:
        print(f"[-] Terjadi kesalahan: {e}")

# Mendaftarkan Hotkey (Contoh: F9)
hotkey = 'f9'
keyboard.add_hotkey(hotkey, proses_layar)

print(f"Tool background untuk validasi soal telah aktif! Tekan '{hotkey}' untuk membaca layar dan mengklik.")
print("Tekan 'ESC' untuk mematikan program.")

# Menahan program agar terus berjalan di background
keyboard.wait('esc')
print("Program dihentikan.")
