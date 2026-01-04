🤖 Smart Vision Detector (OpenCV + Voice Control)

📌 Deskripsi

Smart Vision Detector adalah aplikasi berbasis OpenCV dan AI yang mampu membedakan manusia dan benda secara real-time menggunakan kamera, serta dilengkapi kontrol suara (voice command) untuk menjalankan perintah seperti mulai deteksi, berhenti, masuk, dan keluar aplikasi.

Aplikasi ini juga menggunakan GUI berbasis Tkinter untuk menampilkan hasil deteksi secara interaktif.

🚀 Fitur Utama

✔ Deteksi manusia secara real-time
✔ Deteksi dan klasifikasi benda
✔ Pembedaan objek manusia dan non-manusia
✔ Kontrol suara (Voice Command)
✔ Kamera live detection
✔ Tampilan GUI menggunakan Tkinter
✔ Sistem masuk & keluar dengan perintah suara

🎤 Voice Command yang Didukung

"Start" / "Mulai" → Menjalankan deteksi kamera

"Stop" → Menghentikan deteksi

"Masuk" → Membuka kamera

"Keluar" / "Exit" → Menutup aplikasi

⚙️ Langkah-langkah Setup
1️⃣ Persiapan Lingkungan

Pastikan Python sudah terinstal.

python --version


Disarankan menggunakan Python 3.8 – 3.11

2️⃣ Install Dependency

Install semua library yang dibutuhkan:

pip install opencv-python numpy pillow SpeechRecognition pyaudio


📌 Jika pyaudio error di Windows, gunakan file .whl sesuai versi Python.

3️⃣ Import Library

Gunakan import berikut pada file Python:

import cv2
import numpy as np
import threading
import time
import os
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import speech_recognition as sr


Fungsi Library:

cv2 → Deteksi objek & kamera

numpy → Pengolahan data gambar

threading → Menjalankan voice & kamera bersamaan

time → Delay & kontrol waktu

os → Manajemen sistem

tkinter → GUI aplikasi

PIL → Menampilkan frame kamera di GUI

speech_recognition → Pengenalan suara

4️⃣ Cara Kerja Sistem

Kamera menangkap video secara real-time

OpenCV mendeteksi manusia dan objek

Sistem mengklasifikasikan objek (manusia / benda)

Voice command diproses secara paralel

GUI menampilkan hasil deteksi

Perintah suara mengontrol masuk dan keluar aplikasi

📷 Contoh Penggunaan

Sistem keamanan & monitoring

Deteksi manusia di area tertentu

Smart camera berbasis AI

Proyek Computer Vision


💡 Catatan Penting

Gunakan kamera dengan pencahayaan cukup

Mikrofon harus aktif untuk voice command

Jalankan aplikasi sebagai administrator jika diperlukan
