import cv2
import numpy as np
import threading
import time
import os
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import speech_recognition as sr

# Pastikan folder model dan output tersedia
model_dir = "models"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

cfg_path = os.path.join(model_dir, "yolov4-tiny.cfg")
weights_path = os.path.join(model_dir, "yolov4-tiny.weights")
names_path = os.path.join(model_dir, "coco.names")

# Cek file model
if not all(os.path.exists(path) for path in [cfg_path, weights_path, names_path]):
    print("⚠ ERROR: Model tidak ditemukan! Pastikan folder 'models' berisi:")
    exit(1)

# Load model YOLO
net = cv2.dnn.readNet(weights_path, cfg_path)
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
else:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load class COCO
with open(names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
video_writer = cv2.VideoWriter(
    os.path.join(output_dir, "deteksi_output.avi"),
    cv2.VideoWriter_fourcc(*"XVID"),
    20,
    (frame_width, frame_height)
)

layer_names = net.getLayerNames()
out_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

frame = None
running = True
lock = threading.Lock()

def read_camera():
    global frame, running
    while running:
        ret, temp_frame = cap.read()
        if ret:
            with lock:
                frame = temp_frame

thread = threading.Thread(target=read_camera, daemon=True)
thread.start()

def detect_objects(image):
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(out_layers)

    boxes, confidences, class_ids = [], [], []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x, center_y, w, h = (detection[0:4] * [width, height, width, height]).astype(int)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                
                detected_label = classes[class_id]
                
                # Deteksi manusia (person)
                if detected_label == "person":
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                else:
                    # Deteksi benda selain manusia, tampilkan label "Benda"
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.3)
    return boxes, confidences, class_ids, indices

def update_frame():
    global frame
    if frame is not None:
        with lock:
            frame_copy = frame.copy()
        boxes, confidences, class_ids, indices = detect_objects(frame_copy)
        
        if indices is not None and len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                detected_label = classes[class_ids[i]]
                
                # Jika objek adalah manusia
                if detected_label == "person":
                    label = "Manusia"
                    color = (0, 255, 0)  # Hijau
                else:
                    # Label "Benda" untuk selain manusia
                    label = "Benda"
                    color = (0, 0, 255)  # Merah

                # Gambar kotak deteksi dengan ketebalan lebih besar
                cv2.rectangle(frame_copy, (x, y), (x + w, y + h), color, 3)
                cv2.rectangle(frame_copy, (x, y - 25), (x + 150, y), color, -1)  # Background teks
                
                # Tambahkan teks label dengan ukuran lebih besar
                confidence_text = f"{label} ({confidences[i]*100:.1f}%)"
                cv2.putText(frame_copy, confidence_text, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Simpan frame ke video
        video_writer.write(frame_copy)
        
        frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_camera.imgtk = imgtk
        lbl_camera.configure(image=imgtk)

    lbl_camera.after(10, update_frame)

def listen_for_voice_commands():
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    while running:
        with mic as source:
            r.adjust_for_ambient_noise(source)  # Menyesuaikan dengan suara lingkungan
            print("🔊 Mendengarkan perintah suara...")
            audio = r.listen(source)
            
            try:
                command = r.recognize_google(audio).lower()
                print(f"Perintah Deteksi: {command}")
                
                if "mati" in command or "matikan kamera" in command:
                    print("⚠ Kamera dimatikan.")
                    exit_app()
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"⚠ Error dalam mendengarkan perintah suara: {e}")

def exit_app():
    global running
    running = False
    cap.release()
    video_writer.release()
    root.quit()

# Menjalankan thread untuk mendengarkan perintah suara
voice_thread = threading.Thread(target=listen_for_voice_commands, daemon=True)
voice_thread.start()

root = tk.Tk()
root.title("Deteksi Manusia & Benda")
root.geometry("700x600")

lbl_camera = Label(root)
lbl_camera.pack(pady=10)

btn_exit = Button(root, text="Keluar", command=exit_app, font=("Arial", 14), width=20, height=2)
btn_exit.pack(pady=10)

update_frame()
root.mainloop()
