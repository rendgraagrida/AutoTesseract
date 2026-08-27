import pyautogui
import pytesseract
import time

# Jika tesseract tidak ada di PATH secara default, kita harus menentukan lokasinya
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def auto_answer_bot():
    print("Bot dimulai! Berpindah ke layar target dalam 3 detik...")
    time.sleep(3)
    
    # 1. Ambil screenshot (tangkapan layar penuh)
    print("Mengambil screenshot layar...")
    screenshot = pyautogui.screenshot()
    
    # Opsional: Jika soal hanya ada di area tertentu, Anda bisa memotong screenshot:
    # screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # 2. Baca teks dari gambar menggunakan Tesseract OCR
    print("Membaca teks dari layar...")
    extracted_text = pytesseract.image_to_string(screenshot)
    print("Teks yang ditemukan:\n", extracted_text)
    
    # 3. Logika Menjawab Soal (Contoh Sederhana)
    # Anda perlu menyesuaikan logika ini berdasarkan teks spesifik soal Anda
    if "Berapa 2 + 2" in extracted_text:
        print("Soal ditemukan: Berapa 2 + 2?")
        
        # 4. Melakukan aksi klik (Misal: klik jawaban "4")
        # Anda perlu mengganti (500, 500) dengan koordinat (x, y) tombol jawaban di layar Anda
        x_target, y_target = 500, 500 
        print(f"Mengklik jawaban di koordinat X:{x_target}, Y:{y_target}")
        
        pyautogui.moveTo(x_target, y_target, duration=0.5)
        pyautogui.click()
        print("Klik berhasil!")
        
    else:
        print("Soal tidak dikenali di layar saat ini.")

if __name__ == "__main__":
    # Menjalankan bot satu kali
    auto_answer_bot()
    
    # Jika ingin berjalan terus-menerus, gunakan loop:
    # while True:
    #     auto_answer_bot()
    #     time.sleep(5) # Jeda 5 detik sebelum mengecek layar lagi
